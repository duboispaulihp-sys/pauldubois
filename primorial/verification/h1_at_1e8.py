#!/usr/bin/env python3
"""
h1_at_1e8.py -- exact anchor evaluation at K = 10^8: the first chain step H_1.

Goal
----
Seed H_0 = H at the anchor K = 10^8 (u fixed at u_K) and evaluate the first
step of the anchored chain (Theorem 8):

    H_1 = (1 + r_K) H + s_K / u_K
        = eps_{K+1} / u_K + (1 + r_K) (H - H_K^{phys})   [exact decomposition]

Here everything is computed EXACTLY (to float64) from a segmented sieve up to
~2.05e9:

    X_K = theta(p_K) with p_K = 2,038,074,743 (the 10^8-th prime; the sieve
          independently verifies pi(p_K) = 10^8),
    Pi_K = prod_{p <= p_K} (1 - 1/p)          (running accumulator, log1p form),
    f_K  = e^gamma * X_K * Pi_K               (Nicolas's f at the anchor),
    eps_K = A_K (1/f_K - 1) = -A_K expm1(log f_K)/f_K   (sign-consistent form),
    H_K^{phys} = eps_K / u_K,
    g_K = log p_{K+1}, u_K = g_K/X_K, r_K = 1/(p_{K+1}-1), Q_K = 1+r_K,
    s_K = r_K A_K - log1p(u_K),
    fixed point  H_c = -s_K/(r_K u_K)  so that  H_1 - H = r_K (H - H_c).

All primes up to p_{K+1} are visited once; every prime <= p_K contributes
log p to X and log1p(-1/p) to log Pi_  (Neumaier-safe: per-segment fsum of
exactly-rounded partials, final fsum over partials).

Pure Python 3, no dependencies.  Runtime: ~minutes (sieve to 2.05e9).
"""
import math
import sys
import time

BOUND = 2_038_074_743          # claimed p_{1e8}; verified below via pi == 10^8
TOP = 2_050_000_000
E_GAMMA = 1.78107241799019798785
TARGET_COUNT = 100_000_000

t0 = time.time()


def base_primes(n):
    m = bytearray([1]) * (n + 1)
    m[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n) + 1):
        if m[p]:
            step_count = len(range(p * p, n + 1, p))
            m[p * p:: p] = b"\x00" * step_count
    return [i for i in range(2, n + 1) if m[i]]


BASE = base_primes(math.isqrt(TOP))
print(f"[{time.time()-t0:7.1f}s] base primes to {math.isqrt(TOP)}: {len(BASE)}",
      flush=True)

SEG = 1 << 22
X_parts = []      # per-segment exact partial sums of log p  (theta)
M_parts = []      # per-segment exact partial sums of log1p(-1/p) (log Pi)
cnt = 0
P2 = None
lo = 2
nseg = (TOP - lo + SEG - 1) // SEG
iseg = 0
# scalar accumulators used only inside the (single) segment that contains BOUND
X_tail = 0.0
M_tail = 0.0
cnt_at_bound = None

while lo < TOP and P2 is None:
    hi = min(lo + SEG, TOP)
    n = hi - lo
    seg = bytearray([1]) * n
    for p in BASE:
        start = p * p
        if start >= hi:
            continue
        if start < lo:
            start = ((lo + p - 1) // p) * p
        m = len(range(start, hi, p))
        seg[start - lo:: p] = b"\x00" * m
    fnd = seg.find
    pr = []
    i = fnd(1)
    while i != -1:
        pr.append(lo + i)
        i = fnd(1, i + 1)
    iseg += 1
    if iseg % 25 == 0:
        print(f"[{time.time()-t0:7.1f}s] segment {iseg}/{nseg} (lo={lo:>11}, "
              f"cnt={cnt+len(pr)})", flush=True)
    if hi - 1 <= BOUND:
        X_parts.append(math.fsum(map(math.log, pr)))
        M_parts.append(math.fsum([math.log1p(-1.0 / p) for p in pr]))
        cnt += len(pr)
        lo = hi
        continue
    # segment containing BOUND (or beyond): split, stop at first prime > BOUND
    head = []
    for p in pr:
        if p <= BOUND:
            head.append(p)
            cnt += 1
        else:
            P2 = p
            break
    cnt_at_bound = cnt
    X_tail = math.fsum(map(math.log, head))
    M_tail = math.fsum([math.log1p(-1.0 / p) for p in head])
    lo = hi

assert cnt_at_bound == TARGET_COUNT, (
    f"pi(BOUND) = {cnt_at_bound}, expected {TARGET_COUNT}: "
    "BOUND is not p_(1e8) under this sieve")
assert P2 is not None, "no prime after BOUND below TOP?!"

X_K = math.fsum(X_parts) + X_tail          # theta(p_K)
logPi_K = math.fsum(M_parts) + M_tail      # log prod (1 - 1/p)
Pi_K = math.exp(logPi_K)

PK, PK1 = BOUND, P2
D = X_K - PK
A = math.log(X_K)
g = math.log(PK1)
u = g / X_K
r = 1.0 / (PK1 - 1.0)
Q = 1.0 + r
s = r * A - math.log1p(u)

GAMMA = 0.577215664901533
log_f = GAMMA + math.log(A) + logPi_K   # log f(p_K) = gamma + log log theta + log Pi; expm1-safe
fK = math.exp(log_f)
epsK = A * (-math.expm1(log_f)) / fK
Hphys = epsK / u
Hc = -s / (r * u)
sq_pg = math.sqrt(PK) / g
band_lo, band_hi = 1.954 * sq_pg, 2.046 * sq_pg   # Theorem-C RH band, lower edge

# next prime: no new sieving needed (theta(p_{K+1}) = theta(p_K) + log p_{K+1})
XK1 = X_K + g
A1 = math.log(XK1)
logPi1 = logPi_K + math.log1p(-1.0 / PK1)
log_f2 = GAMMA + math.log(A1) + logPi1
f2 = math.exp(log_f2)
epsK1 = A1 * (-math.expm1(log_f2)) / f2
rho1 = log_f2 * math.sqrt(PK1) * g
rhoK = log_f * math.sqrt(PK) * A


def H1(H):
    return Q * H + s / u


print(f"[{time.time()-t0:7.1f}s] sieve complete; pi(p_K) = {cnt_at_bound}",
      flush=True)
print()
print(f"p_K      = {PK}   (pi(p_K) = {cnt_at_bound} verified)")
print(f"p_(K+1)  = {PK1}   (g - next gap = {PK1 - PK})")
print(f"X_K = theta(p_K)     = {X_K:.9f}")
print(f"D_K = X_K - p_K      = {D:.6f}   (sign(D) = {D > 0})")
print(f"A_K = log X_K        = {A:.12f}")
print(f"g_K = log p_(K+1)    = {g:.12f}")
print(f"u_K = g/X            = {u:.12e}")
print(f"r_K = 1/(p1 - 1)     = {r:.12e}")
print(f"Q_K = 1 + r_K        = {Q:.18f}")
print(f"log Pi_K             = {logPi_K:.12f}")
print(f"log f(p_K)           = {log_f:.12e}   (f<1 <=> eps>0)")
print(f"eps_K = A(1/f - 1)   = {epsK:.9e}   (positive iff f<1)")
print(f"H_K^(phys) = eps/u   = {Hphys:.6f}   (trend estimate was 4.21e3)")
print(f"Theorem-C RH band    = [{band_lo:.1f}, {band_hi:.1f}]  "
      f"(H_K inside: {band_lo <= Hphys <= band_hi})")
print(f"s_K = r A - log1p(u) = {s:.9e}   (sign(s) = {s > 0}; "
      f"sign(D) = {D > 0})")
print(f"H_c = -s/(r u)       = {Hc:.6f}   (fixed point: H_1 = H iff H = H_c)")
print(f" Nicolas corridor: (log f)sqrt(p)log p at p_K, p_(K+1): "
      f"{rhoK:.6f}, {rho1:.6f}   (liminf -2.046, limsup -1.954)")
print(f"f(p_(K+1))           = {f2:.9f}   (<1 iff eps_(K+1)>0: "
      f"{f2 < 1})")
print(f"A_(K+1)             = {A1:.9f};  eps_(K+1) = {epsK1:.9e}")
print("next-prime check:  u_K * H_1(Hphys)  vs  eps_(K+1)  (should agree):")
print(f"  H_1(Hphys)*u_K = {H1(Hphys) * u:.9e}   eps_(K+1) = {epsK1:.9e}   "
      f"rel diff = {abs(H1(Hphys) * u - epsK1) / abs(epsK1):.2e}")
print()
print("H_1 = Q_K H + s_K/u_K for the requested seeds:")
for H in (0.0, Hphys, 1.0e3, 1.0e4, 1.0e6):
    print(f"  H = {H:>15.6f}  ->  H_1 = {H1(H):>18.6f}   "
          f"(H_1 - H = {H1(H) - H:+.6e})")
print()
print("decomposition check: H_1(Hphys) - eps_{K+1}/u_K  (should be ~0):")
epsK1_over_u = Q * epsK / u + s / u
print(f"  Q*eps/u + s/u = {epsK1_over_u:.9e};  Q*Hphys + s/u = "
      f"{H1(Hphys):.9e}")
resid = H1(Hphys) - epsK1_over_u
print(f"  residual = {resid:.3e}")
print()
print("constraint by H (monotone corridor): H_1 - H = r_K (H - H_c), "
      "slope Q_K > 1; i.e. H_1 > H iff H > H_c, and for all "
      "H in [0, 1e6] (H << H_c) H_1 < H but H_1/H -> 1 + r_K.")

with open("h1_at_1e8_results.txt", "w") as fh:
    fh.write("H1 anchor evaluation at K = 1e8 (exact sieve to 2.05e9)\n")
    fh.write(f"p_K = {PK}  pi(p_K) = {cnt_at_bound}  p_(K+1) = {PK1}\n")
    fh.write(f"X_K = theta(p_K) = {X_K!r}\n")
    fh.write(f"D_K = {D!r}  A_K = {A!r}  g_K = {g!r}\n")
    fh.write(f"u_K = {u!r}  r_K = {r!r}  Q_K = {Q!r}  s_K = {s!r}\n")
    fh.write(f"log_pi_K = {logPi_K!r}  log_f = {log_f!r}  f_K = {fK!r}\n")
    fh.write(f"eps_K = {epsK!r}  H_phys = {Hphys!r}  H_c = {Hc!r}\n")
    fh.write(f"X_K+1 = {XK1!r}  A_K+1 = {A1!r}  log_f_(K+1) = {log_f2!r}  "
             f"f_K+1 = {f2!r}  eps_K+1 = {epsK1!r}\n")
    fh.write(f"rho_K = {rhoK!r}  rho_(K+1) = {rho1!r}\n")
    for H in (0.0, Hphys, 1.0e3, 1.0e4, 1.0e6):
        fh.write(f"H = {H!r}  H1 = {H1(H)!r}\n")
print("results written to h1_at_1e8_results.txt")
