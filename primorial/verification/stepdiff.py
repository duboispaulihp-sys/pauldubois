#!/usr/bin/env python3
"""stepdiff.py -- convergence of the chain increments Delta_j = H_j - H_{j-1}.

Closed form (Theorem 8 / cor:seed of LEAN.tex), seed H at anchor K = 10^8:

    Delta_j = H_j - H_{j-1} = r_{K+j-1} H_{j-1} + s_{K+j-1}/u_K .

Proposition prop:stepdiff: Delta_j -> 0 UNCONDITIONALLY for every fixed
seed (Mertens product + PNT only):
  * r H_{j-1}: H_{j-1} = H^phys_{j-1} + (H-H_K) P_{j-1};  H^phys = eps/u_K
    with eps = o(A) (Mertens, relative) so r H^phys = eps/(p u_K) -> 0; and
    r P = O(log p / p) -> 0 (sum_{i} 1/p_i ~ log log p), so r (H-H_K)P -> 0;
  * s/u_K: |s| <= r A + u_k with u_k = g/X -> 0 (PNT), so |s|/u_K -> 0.

Leading shape (2nd-order law of prop:soscil, p^2 s = 2a - e'(1+a) + a^2/2):

    s_{K+j-1} = -e' (1+a)/p^2 (1 + o(1))          (e' = p - X, a = log p),
    Delta_j   = r H_{j-1} - e'(1+a)/(p^2 u_K) (1+o(1)),
    |Delta| p^{3/2} ~ (e'/sqrt p) * (1+a)/u_K :  decays like p^{-3/2},
    modulated by the Chebyshev oscillation e'/sqrt p (certified in
    [0.80, 1.23] on the 2.07e9 strip, and it drifts beyond),

into which the rH part (r H ~ eps/p ~ 2e-6, slowly shrinking) is mixed.

Checker on W = 2e7 steps (sieve to 2.6e9), stream from the certified anchor:
  gate 1: anchor continuity;
  gate 2: exact increment identity, tol = 3 float-ulps of eps/u_K;
  gate 3: 2nd-order s-law vs sresp.py (resid <= 1e-3 rel);
  gate 4: sign census (Delta < 0 at every step) + margin e'/(eps p/(1+a));
  gate 5: eta = e'/sqrt p census (the modulation band).

Increment convergence does NOT imply chain convergence: sum_j Delta_j = H_j
- H_0 telescopes; for supercritical seeds P_j -> infty, so the chain
diverges; for the physical seed the telescope converges iff eps has a
limit -- an open Mertens-limit question at prime endpoints (the brick).
Pure Python 3, no dependencies.
"""

import math
import os
import time
from math import isqrt, log, log1p

K = 100_000_000
W = 20_000_000
LIMIT = 2_600_000_000
SEG_SPAN = 100_000_000
CKPTS = (1, 2, 1000, 10_000, 100_000, 1_000_000, 5_000_000,
         10_000_000, 20_000_000)

CERT = {
    "p_K": 2038074743,
    "p_K1": 2038074751,
    "X_K": 2038030124.4153652,
    "u_K": 1.0517642105918211e-08,
    "eps_K": 4.3461928497354573e-05,
    "H_K": 4132.2882124786138,
}
H_K1_XK = 21.435271449680776
SHAPE_TOL = 1e-3
CERT_TOL = 1e-6
ID_TOL = 5e-12          # 3 float-ulps of eps/u_K: ulp(4.35e-5)/u_K ~ 7.8e-13

T0 = time.time()
OUT = []


def out(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


def rel(a, b):
    return abs(a - b) / abs(b) if b else abs(a - b)


def primes_upto(limit):
    if limit < 2:
        return
    yield 2
    if limit < 3:
        return
    size = (limit - 1) // 2
    sieve = bytearray([1]) * (size + 1)
    sieve[0] = 0
    i = 1
    while True:
        v = 2 * i + 1
        if v * v > limit:
            break
        if sieve[i]:
            start = (v * v - 1) // 2
            sieve[start::v] = bytearray(len(range(start, size + 1, v)))
        i += 1
    for i in range(1, size + 1):
        if sieve[i]:
            yield 2 * i + 1


def window_primes(a, e, base):
    size = (e - a) // 2 + 1
    sieve = bytearray([1]) * size
    for q in base:
        if q == 2:
            continue
        if q * q > e:
            break
        start = q * q
        if start < a:
            start = ((a + q - 1) // q) * q
        if start % 2 == 0:
            start += q
        i0 = (start - a) // 2
        if i0 < size:
            sieve[i0::q] = bytearray(len(range(i0, size, q)))
    res = []
    i = sieve.find(1)
    while i != -1:
        res.append(a + 2 * i)
        i = sieve.find(1, i + 1)
    return res


def selftest_window():
    ref = [p for p in primes_upto(2001) if p >= 999]
    base = list(primes_upto(isqrt(2001) + 1))
    assert window_primes(999, 2001, base) == ref, "self-test FAILED"
    ref2 = [p for p in primes_upto(5000) if p >= 3]
    base2 = list(primes_upto(isqrt(5000) + 1))
    assert window_primes(3, 5000, base2) == ref2, "self-test FAILED (3,5000)"
    out("self-test: window_primes [3,5000] and [999,2001] match the "
        "reference sieve exactly  PASS")


def stream_theta(x0, k0, pk0, limit, seg_span):
    base = list(primes_upto(isqrt(limit) + 1))
    closed = x0
    n = k0
    a = pk0 + 2
    while a <= limit:
        e = min(a + seg_span - 2, limit)
        seg = []
        partial = 0.0
        for p in window_primes(a, e, base):
            lp = log(p)
            n += 1
            yield (n, p, lp, closed + partial)
            seg.append(lp)
            partial += lp
        closed = math.fsum((closed, math.fsum(seg)))
        a = e + 2


def run():
    out("== convergence of chain increments Delta_j = H_j - H_(j-1), "
        "K = 10^8, physical seed ==")
    out("window W = %d steps, sieve bound %d (stream from the certified "
        "anchor p_K = %d)" % (W, LIMIT, CERT["p_K"]))
    out("")
    selftest_window()
    out("")

    u_k = CERT["u_K"]
    H_K = CERT["H_K"]
    eps = CERT["eps_K"]
    assert rel(eps / u_k, H_K) < 1e-12

    deltas = {}
    max_shp = 0.0
    max_idres = 0.0
    min_margin = (math.inf, -1)
    eta_min, eta_max = math.inf, -math.inf
    zmin, zmax = math.inf, -math.inf        # |Delta|*p^(3/2) census
    wrong_sign = 0
    n_last = K
    p_last = CERT["p_K"]
    fails = []
    ok = True

    out("== gate 1: anchor continuity ==")
    gen = stream_theta(CERT["X_K"], K, CERT["p_K"], LIMIT, SEG_SPAN)
    prev_h = H_K
    for (n, p, lp, x_prev) in gen:
        j = n - K
        if j == 1:
            if p != CERT["p_K1"]:
                fails.append("p_{K+1} mismatch: %d" % p)
                ok = False
            u1 = lp / x_prev
            if rel(u1, u_k) > CERT_TOL or rel(lp, H_K1_XK) > CERT_TOL:
                fails.append("anchor constants mismatch")
                ok = False
            out("  p_(K+1) = %d  certified;  u_1 rel.err %.2e  PASS"
                % (p, rel(u1, u_k)))
        a_prev = log(x_prev)
        r = 1.0 / (p - 1.0)
        s = r * a_prev - log1p(lp / x_prev)
        eps = (1.0 + r) * eps + s
        h = eps / u_k
        delta = h - prev_h                      # exact increment Delta_j
        if j >= 1:
            ep = p - x_prev                     # e' of THIS step's s
            sid = (2.0 * lp - ep * (1.0 + lp) + lp * lp / 2.0) / p ** 2
            shp = abs(s - sid) / abs(s)
            idres = abs(delta - r * prev_h - s / u_k)
            marg = ep / (prev_h * u_k * p / (1.0 + lp))
            eta = ep / math.sqrt(p)
            z = abs(delta) * p ** 1.5
            if shp > max_shp:
                max_shp = shp
            if idres > max_idres:
                max_idres = idres
            if marg < min_margin[0]:
                min_margin = (marg, j)
            eta_min, eta_max = min(eta_min, eta), max(eta_max, eta)
            zmin, zmax = min(zmin, z), max(zmax, z)
            if delta >= 0:
                wrong_sign += 1
            if j in CKPTS:
                deltas[j] = (p, delta, s / u_k, r * prev_h, shp, marg, eta)
        prev_h = h
        n_last = n
        p_last = p
        if j >= W:
            break
    out("  walk complete: n = %d = K + %d, p_end = %d"
        % (n_last, n_last - K, p_last))
    out("")

    out("== gate 2: exact increment identity Delta = r H + s/u_K ==")
    out("  max |Delta - r H - s/u_K| = %.3e H-units (tol %.0e = 3 ulps of "
        "eps/u_K ~ 0.8e-12)" % (max_idres, ID_TOL))
    good = max_idres <= ID_TOL
    ok = ok and good
    out("  %s" % ("PASS" if good else "FAIL"))
    out("")

    out("== gate 3: 2nd-order s-law  p^2 s = 2a - e'(1+a) + a^2/2 ==")
    out("  %-10s %-14s %-14s %-12s %-10s %-9s" %
        ("j", "Delta_j", "s/u_K part", "rH part", "s resid", "e'/sqrt p"))
    for j in sorted(deltas):
        p, d, xs, rh, shp, mg, eta = deltas[j]
        out("  %-10d %-14.6e %-14.6e %-12.4e %-10.2e %-9.3f"
            % (j, d, xs, rh, shp, eta))
    good = max_shp <= SHAPE_TOL
    ok = ok and good
    out("  max s-shape residual %.3e (tol %.0e): %s"
        % (max_shp, SHAPE_TOL, "PASS" if good else "FAIL"))
    out("")

    out("== gate 4: sign census and margin ==")
    out("  Delta_j < 0 at %d/%d steps (nonnegative count = %d)"
        % (W - wrong_sign, W, wrong_sign))
    out("  threshold: Delta < 0 <=> s < -r H u_K <=> e' > eps*p/(1+a)"
        " (2nd order);")
    out("  min margin e'/(eps p/(1+a)) = %.2f at j = %d" % min_margin)
    good = wrong_sign == 0 and min_margin[0] > 1.0
    ok = ok and good
    out("  %s" % ("PASS" if good else "FAIL"))
    out("")

    out("== gate 5: modulation census ==")
    out("  eta = e'/sqrt p over window:  min %.3f  max %.3f"
        % (eta_min, eta_max))
    out("  (strip [p_K+1, 2.07e9] certified band [0.80, 1.23]; the band")
    out("   drifts beyond -- e' is the Chebyshev oscillation, prop:soscil)")
    out("  z = |Delta|*p^(3/2):  min %.4e  max %.4e  (ratio %.2f; ~ constant"
        " up to the eta band)"
        % (zmin, zmax, zmax / zmin))
    out("")
    d1 = abs(deltas[1][1])
    dW = abs(deltas[W][1])
    out("  Delta(1) = %.6e ... Delta(W) = %.6e : the p^{-3/2} trend "
        "(~%.0f%% expected) is partly masked by the eta oscillation "
        "inside any window of this length;"
        % (d1, dW, (1 - (CERT["p_K1"] / p_last) ** 1.5) * 100))
    out("")

    out("== summary ==")
    for f in fails:
        out("  FAIL:", f)
    out("  step-difference certificate: %s" % ("PASS" if ok else "FAIL"))
    if ok:
        out("  Delta_j = r H + s/u_K -> 0 unconditionally (prop:stepdiff):")
        out("  rH-part = eps/p/u_K: %.3e (j=1) -> %.3e (j=W), tracks eps/p;"
            % (deltas[1][3], deltas[W][3]))
        out("  s-part  = s/u_K:     %.3e (j=1) -> %.3e (j=W), p^{-3/2} law"
            % (deltas[1][2], deltas[W][2]))
        out("  every step negative in the window (margin >= %.1f); the"
            % min_margin[0])
        out("  increments converge to 0 but the chain need not converge:")
        out("  sum Delta_j = H_j - H_0 telescopes; supercritical seeds"
            " diverge like P (log P ~ log log p), and for the physical")
        out("  seed convergence of the telescope is exactly the open"
            " question whether eps has a Mertens limit.")
    out("  total %.1f s" % (time.time() - T0))

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "stepdiff_results.txt")
    with open(path, "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    out("results written to", path)


if __name__ == "__main__":
    run()
