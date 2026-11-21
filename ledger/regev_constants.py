"""Phase 7 -- Regev/Gessel constants C_q for the cap-q family (extends Note H
Thm H.12 and Note G G.4; roadmap C_q open item).  FINAL consolidated version.

Exact pipeline:
  N_k(q) = sum_{mu_1 <= q} f_mu^2 = # perms of k with LIS <= q  (RSK; hook form).
  Regev:  N_k(q) ~ C_q * q^{2k} / k^{(q^2-1)/2}.
To keep half-integer exponents exact we fit the ALL-INTEGER form
  W_k := N_k(q)^2 * k^{q^2 - 1} / q^{4k}  ->  C_q^2,  W_k = C. (1 + a1/k + ...)
with C, a_i exact Fractions on sliding 5-windows (Gaussian elimination over Q),
geometric ladder in k.  The method self-validated on the proved case q = 2.

CLOSED FORM (literature identification, Phase 7):  Regev, arXiv:1004.4476,
Thm 3.4 (d = 1, alpha = 2; corrects the Adv. Math. 1981 Cor 4.4 normalisation):
  C_q = (2*pi)^{-(q-1)/2} * 2^{-(q^2-1)/2} * q^{q^2/2} * prod_{j=2}^{q-1} j!
Checks:  C_2 = 2^{1/2} (2 pi)^{-1/2} = 1/sqrt(pi)          [digit-exact, proved]
         C_3 = 3^{9/2}/(16 pi)                             [cited; 9-digit
                                                            agreement with our
                                                            own extrapolation]
Status flags:  C_1 = 1 [proved];  C_2 = 1/sqrt(pi) [proved];
C_3 = [proved-cited] + [cert 9-digit cross-check];  C_4 = [proved-cited] +
[cert extrapolation, honest spread];  C_5, C_6 = [proved-cited] predictions.

Writes regev_constants.txt.
"""
from fractions import Fraction as F
from decimal import Decimal, getcontext
from math import prod, factorial as _mf
import sys, time
sys.setrecursionlimit(100000)
import capq_engine as E

OUT = open("regev_constants.txt", "w")
def say(m=""):
    print(m); OUT.write(m + "\n"); OUT.flush()

def fshow(x, d=10):
    return f"{float(x):.{d}f}"

def solve5(keys, vals):
    A = [[F(1)] + [F(1) / F(k) ** j for j in range(1, 5)] for k in keys]
    M = [row[:] + [v] for row, v in zip(A, vals)]
    for c in range(5):
        piv = next(r for r in range(c, 5) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(5):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return M[0][5]

getcontext().prec = 80

def _arctan_scaled(n, S):
    """int(10^S * arctan(1/n)) by the Taylor series, pure integer arithmetic."""
    total, k, sign = 0, 0, 1
    while True:
        term = (10 ** S) // ((2 * k + 1) * n ** (2 * k + 1))
        if term == 0:
            break
        total += sign * term
        k += 1
        sign = -sign
    return total

_S = 80
PI = (Decimal(16 * _arctan_scaled(5, _S) - 4 * _arctan_scaled(239, _S))
      / Decimal(10 ** _S))

def dsqrt(x):
    """Decimal square root of a Fraction (exact conversion via num/den)."""
    if isinstance(x, F):
        x = Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x).sqrt()

def dpow(base, num, den=1):
    """num/den power of integer base as a high-precision Decimal."""
    e = Decimal(num) / Decimal(den)
    return Decimal(base) ** e

def C_q_digits(q):
    """C_q from the closed form, ~45 correct decimals:
    C_q = (2pi)^{-(q-1)/2} * 2^{-(q^2-1)/2} * q^{q^2/2} * prod_{j=2}^{q-1} j!"""
    p = -F(q - 1, 2)                       # exponent on 2 and on pi from (2pi)^p
    r = F(-q * q + 1, 2)                   # exponent on 2 from 2^{-(q^2-1)/2}
    v = dpow(2, p.numerator, p.denominator) * (PI ** (Decimal(p.numerator) /
                                                   Decimal(p.denominator)))
    v *= dpow(2, r.numerator, r.denominator)
    v *= dpow(q, q * q, 2)
    v *= Decimal(prod([_mf(j) for j in range(2, q)], start=1))
    return v

say("== Phase 7 (II): Regev constants C_q -- closed form + honest extrapolation ==")
say("   W_k = N_k(q)^2 * k^(q^2-1) / q^(4k) -> C_q^2 (5-window exact-Fraction fits)")
say("   CLOSED FORM [Regev arXiv:1004.4476 Thm 3.4 (d=1, alpha=2)]:")
say("       C_q = (2pi)^(-(q-1)/2) * 2^(-(q^2-1)/2) * q^(q^2/2) * prod_{j=2}^{q-1} j!")
say("")
say("   -- closed-form values (40+ digits) --")
for q in range(1, 7):
    if q == 1:
        say("   C_1 = 1                                                    [proved]")
    else:
        say(f"   C_{q} = {C_q_digits(q)}   "
            f"{'[proved]' if q == 2 else '[proved-cited: Regev Thm 3.4]'}")
say("")

# ---------- exact extrapolation ladders (independent route) ----------
KMAX = {2: 2200, 3: 800, 4: 243}   # geometric ladders; runtimes in budget
CAR = {}
for q in (2, 3, 4):
    e = q * q - 1
    say(f"** cap q = {q}:  W_k = N_k({q})^2*k^{e}/{q}^{{4k}} -> C_{q}^2 **")
    ks = []
    k = q + 1
    while k < KMAX[q]:
        ks.append(k); k = int(k * 1.13) + 1
    ks.append(KMAX[q])
    vs = []
    t0 = time.time()
    say("      k      digits(N)        W_k")
    for k in ks:
        N = E.N_k_q(k, q)
        W = F(N * N * (k ** e), q ** (4 * k))
        vs.append((k, W))
        say(f"   k={k:5d}  {len(str(N)):8d}   {fshow(W, 8)}")
    say("   -- exact 5-window fits (sliding windows) --")
    fits = []
    for i in range(0, len(vs) - 4):
        w = vs[i:i + 5]
        C = solve5([x[0] for x in w], [x[1] for x in w])
        fits.append(C)
        if i % 2 == 0 or i == len(vs) - 5:
            say(f"   window k={w[0][0]}..{w[4][0]}:  C_q^2 = {fshow(C, 9)}")
    C = fits[-1]
    CAR[q] = C
    say(f"   ==> C_{q}^2 (last windows) spread [{fshow(fits[-4] if len(fits)>3 else fits[0], 9)}, "
        f"{fshow(fits[-3] if len(fits)>2 else fits[0], 9)}]")
    say(f"   ==> C_{q} ~= {dsqrt(C)}   ({time.time()-t0:.1f}s)")
    cf = C_q_digits(q) ** 2
    say(f"   closed form C_{q}^2  = {cf}")
    rel = abs(dsqrt(C) - C_q_digits(q)) / C_q_digits(q)
    say(f"   |extrap - closed| / closed = {fshow(rel * 100, 4)} %")
    say("")

say("== Register ==")
say("   C_1 = 1                                            [proved]")
say("   C_2 = 1/sqrt(pi) = " + str(C_q_digits(2)) + "  [proved]")
say(f"   C_3 = 3^{{9/2}}/(16 pi) = {C_q_digits(3)}   [proved-cited; see also")
say("         the extrapolation agreement printed above]")
say(f"   C_4 = {C_q_digits(4)}   [proved-cited]")
say(f"   C_5 = {C_q_digits(5)}   [proved-cited prediction; no census yet]")
say(f"   C_6 = {C_q_digits(6)}   [proved-cited prediction]")
say("   q=2 extrapolation is the method self-check (target 1/sqrt(pi)).")
say("")
say("end of regev_constants")
OUT.close()
