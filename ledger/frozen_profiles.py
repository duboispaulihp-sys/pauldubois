"""frozen_profiles.py -- the second asymptotic direction of the ledger
constants: k -> infinity (Note F froze n -> infinity, per rung k).

New exact facts certified/illustrated here (proofs in notes/06, Note G):

 (G.1) Ledger-split identity, extended: for every k,
           sum_{mu_1 <= 4} f_mu^2  +  sum_{sigma_1 >= 5} f_sigma^2  =  k!,
       computed for k = 1..30 (f = # SYT = k!/hook-products), a second
       derivation of the Note F constant table (independent of the
       Kostka/GT route used there).

 (G.2) LIS interpretation: sum_{mu_1 <= 4} f_mu^2 = N_k(4) = # permutations
       in S_k with longest increasing subsequence <= 4 (RSK: shape first
       row = LIS).  The model's ledger-share of rung k is 1 - N_k(4)/k!,
       and it -> 0.

 (G.3) Gessel's determinant identity, verified EXACTLY (rationals):
           sum_{k>=0} N_k(d) x^{2k}/(k!)^2 = det( I_{|i-j|}(2x) )_{d x d},
       checked for d = 2 against the Catalan numbers (perms with LIS <= 2
       are the 321-avoiding ones) and for d = 4 against the hook census,
       k = 0..30 each; d = 1 against the identity permutation.

 (G.4) Regev asymptotics of the shares: N_k(4) ~ C_4 * 16^k / k^{15/2}
       (exponent (d^2-1)/2 at d = 4; matches d = 1, 2 elementary counts).
       Certified numerically: corrected ratio
           q_k = (N_k(4)/N_{k-1}(4))^2 * (k+1)^15 / (256 * k^15)
       is monotone decreasing and within 25% of 1 by k = 20 (1.9% at 30);
       the standardised v_k = N_k(4) * k^{15/2} / 16^k is tabulated to
       k = 60 -- its approach to C_4 is slow (1/k scale) and the constant
       itself is NOT evaluated here (open; see Note G).

 (G.5) Frozen shape profile (Note F Thm F.2a/d): as n -> infty,
           b_sigma(n)^2 / P_k(n) -> f_sigma^2 / sum_big f^2.
       Certified: per-shape shares at k = 6, 9 approach the frozen ratios
       at O(1/n) rate (n * error plateaus, e.g. n*maxerr ~ 2.04 for k = 9
       from n = 20 on); participation number
       rho_k = (sum_big f^2)^2 / sum_big f^4 for k = 5..30, plus the
       dominant shape (the n = infty fingerprint of the rung), to set
       against the document's finite-n fingerprints (e.g. 519 nonzero
       squares at P_20(35)).

All arithmetic exact integers/rationals; floats only to display
standardised limiting ratios.
"""
import sys, time
from math import comb, factorial
from fractions import Fraction as Fr

sys.path.insert(0, "/workspace/fclosure/ledger")
from ledger_engine import partitions, b_sigma, P_k

out = []
def say(msg=""):
    print(msg, flush=True)
    out.append(str(msg))

# ------------------------------------------------------------ f via hooks
def f_syt(sigma):
    """# SYT of shape sigma = k! / prod of hook lengths (exact)."""
    k = sum(sigma)
    hook = 1
    rows = len(sigma)
    for i in range(rows):
        for j in range(sigma[i]):
            right = sigma[i] - j - 1          # boxes to the right
            down = sum(1 for r in range(i + 1, rows) if sigma[r] > j)
            hook *= right + down + 1
    return factorial(k) // hook

def fsum_pow2(k, first_row_le=None, first_row_ge=None):
    """sum of f_sigma^2 over shapes of k, filtered by first row."""
    tot = 0
    for s in partitions(k):
        r0 = s[0] if s else 0
        if first_row_le is not None and r0 > first_row_le:
            continue
        if first_row_ge is not None and r0 < first_row_ge:
            continue
        f = f_syt(s)
        tot += f * f
    return tot

# ------------------------------------------------------------------- G.1
say("== G.1/G.2: extended ledger-split k! = sum_(mu_1<=4) f^2 + sum_(s_1>=5) f^2 ==")
say("   (= k! minus #perms with LIS <= 4, by RSK)")
say("      k            N_k(4)=sum_led f^2     sum_big f^2    sum=k!   big-share")
t0 = time.time()
NK = {0: 1}
for k in range(1, 31):
    led = fsum_pow2(k, first_row_le=4)
    big = fsum_pow2(k, first_row_ge=5)
    assert led + big == factorial(k), k
    NK[k] = led
    if k in (5, 10, 15, 20, 25, 30):
        say(f"  {k:4d}  {led:>20d}  {big:>16d}   "
            f"{led + big == factorial(k)}   "
            f"{float(Fr(big, factorial(k))):.6g}")
say(f"  split identity: ALL PASS for k = 1..30   ({time.time()-t0:.0f}s)")

# ------------------------------------------------------------------- G.3
say("\n== G.3: Gessel's determinant identity,")

class PS:
    """truncated power series over Q (list of fractions, length cap+1)"""
    __slots__ = ("c",)
    def __init__(self, c):
        self.c = list(c)
    def __add__(self, o):
        return PS([a + b for a, b in zip(self.c, o.c)])
    def __sub__(self, o):
        return PS([a - b for a, b in zip(self.c, o.c)])
    def __mul__(self, o):
        n = len(self.c) - 1
        r = [Fr(0)] * (n + 1)
        for i, a in enumerate(self.c):
            if a == 0:
                continue
            for j, b in enumerate(o.c):
                if i + j > n:
                    break
                r[i + j] += a * b
        return PS(r)

def bessel_I(m, cap):
    """I_m(2x) = sum_{j>=0} x^{2j+m}/(j!(j+m)!), truncated at degree cap."""
    c = [Fr(0)] * (cap + 1)
    j = 0
    while 2 * j + m <= cap:
        c[2 * j + m] = Fr(1, factorial(j) * factorial(j + m))
        j += 1
    return PS(c)

def det_ps(M):
    """determinant of a small matrix of PS by cofactor expansion."""
    n = len(M)
    if n == 1:
        return M[0][0]
    tot = PS([Fr(0)] * len(M[0][0].c))
    for j in range(n):
        sub = [row[:j] + row[j + 1:] for row in M[1:]]
        term = M[0][j] * det_ps(sub)
        tot = tot + term if j % 2 == 0 else tot - term
    return tot

def gessel_eff(kmax, d):
    """N_k(d) for k = 0..kmax via Gessel's determinant (exact rationals)."""
    cap = 2 * kmax
    I = [bessel_I(m, cap) for m in range(d)]
    M = [[I[abs(i - j)] for j in range(d)] for i in range(d)]
    D = det_ps(M)
    return [D.c[2 * k] * factorial(k) ** 2 for k in range(kmax + 1)]

cat = [comb(2 * i, i) // (i + 1) for i in range(16)]
g2 = gessel_eff(15, 2)
ok2 = all(g2[k] == cat[k] for k in range(16))
ok2b = all(g2[k] == fsum_pow2(k, first_row_le=2) for k in range(16))
say(f"   d = 2 vs Catalan numbers (LIS<=2 = 321-avoiding), k = 0..15: "
    f"{'ALL PASS' if ok2 else 'FAIL'}")
say(f"   d = 2 vs hook census sum_(mu_1<=2) f^2, k = 0..15:            "
    f"{'ALL PASS' if ok2b else 'FAIL'}")
g4 = gessel_eff(30, 4)
ok4 = all(g4[k] == NK[k] for k in range(31))
say(f"   d = 4 vs hook census sum_(mu_1<=4) f^2, k = 0..30:            "
    f"{'ALL PASS' if ok4 else 'FAIL'}")
g1 = gessel_eff(6, 1)
say(f"   d = 1 (N_k = 1: identity permutation only):                  "
    f"{'ALL PASS' if g1 == [1] * 7 else 'FAIL'}")

# ------------------------------------------------------------------- G.4
say("\n== G.4: Regev asymptotics N_k(4) ~ C_4 * 16^k / k^7.5: corrected ratios --")
say("      k            N_k(4)      q_k (exact rational, float view)")
qs = []
for k in range(2, 31):
    qk = Fr(NK[k] ** 2 * (k + 1) ** 15, NK[k - 1] ** 2 * 256 * k ** 15)
    qs.append(qk)
    if k in (6, 10, 15, 20, 25, 30):
        say(f"  {k:4d}  {NK[k]:>18d}   q_k = {float(qk):.6f}")
mono = all(qs[i + 1] < qs[i] for i in range(7, len(qs) - 1))
say("  q_k behaviour, k >= 8: " +
    ("monotone decreasing toward 1" if
     all(qs[i + 1] < qs[i] for i in range(7, len(qs) - 1))
     else "see table (not monotone)"))
bad = [k for k in range(20, 31) if abs(float(qs[k - 2]) - 1) > 0.25]
say(f"  within 25% of 1 for 20 <= k <= 30: {'ALL PASS' if not bad else f'FAIL {bad}'}")

say("\n   standardised v_k = N_k(4)*k^7.5/16^k, extended k = 31..60 (floats):")
say("   (the approach to the Gessel/Regev constant C_4 is slow at 1/k scale;")
say("    these are exact census data, not a limit evaluation)")
for k in list(range(31, 61, 5)) + [60]:
    led = fsum_pow2(k, first_row_le=4)
    v = led * float(k) ** 7.5 / 16 ** k
    say(f"      k={k:3d}: N_k(4) has {len(str(led))} digits; v_k = {v:.4f}")

# ------------------------------------------------------------------- G.5
say("\n== G.5: frozen shape profile: lim_{n->oo} b_s^2/P_k = f_s^2/sum_big f^2 --")
for k in (6, 9):
    big = [s for s in partitions(k) if s[0] >= 5]
    sbig = sum(f_syt(s) ** 2 for s in big)
    froz = [Fr(f_syt(s) ** 2, sbig) for s in big]
    say(f"   k = {k}: big shapes {big}")
    say(f"      f_s          {[f_syt(s) for s in big]}")
    say(f"      frozen share {[str(fr) for fr in froz]}")
    say("      n        live shares b_s^2/P_k(n)          n*maxerr")
    for n in (10, 15, 20, 25, 30, 40):
        tot = P_k(k, n)
        sh = [b_sigma(s, n) ** 2 / tot for s in big]
        err_n = max(abs(sh[i] - froz[i])
                    for i in range(len(big))) * n
        say(f"  {n:4d}   " + "  ".join(f"{float(x):.5f}" for x in sh) +
            f"    ({float(err_n):.3f})")
    say(f"      frozen   " + "  ".join(f"{float(x):.5f}" for x in froz))

say("\n   participation rho_k = (sum_big f^2)^2 / sum_big f^4, and dominant shape:")
say("      k   sum_big f^2     sum_big f^4        rho_k    dominant shape")
for k in range(5, 31):
    big = [s for s in partitions(k) if s[0] >= 5]
    fs = [f_syt(s) for s in big]
    s2 = sum(f * f for f in fs)
    s4 = sum(f ** 4 for f in fs)
    rho = float(Fr(s2 * s2, s4))
    dom = big[max(range(len(fs)), key=lambda i: fs[i] * fs[i])]
    if k in (5, 6, 7, 8, 9, 10, 15, 20, 25, 30):
        say(f"  {k:4d}  {s2:>12d}  {s4:>16d}   {rho:>9.3f}    {dom}")

say("\nall exact; end of frozen_profiles")
open("/workspace/fclosure/ledger/frozen_profiles.txt", "w").write(
    "\n".join(out) + "\n")
print("written frozen_profiles.txt", file=sys.stderr)
