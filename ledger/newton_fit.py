"""newton_fit.py -- exact Newton-form development of the syzygy polynomials.

Theory.  For fixed k, b_sigma(n) = sum_{mu |- k, mu_1<=4} C_mu(n) K_{sigma,mu}
and C_mu(n) = n(n-1)...(n-|mu|+1)/prod m_j! is (up to the constant K) a
polynomial in n of degree len(mu) <= k.  Hence b_sigma(n) is a polynomial of
degree <= k and P_k(n) = sum_{sigma_1>=5} b_sigma(n)^2 is a polynomial of
degree <= 2k.  The document asserts hockey-stick closed forms for special
cases; here we *derive* the full polynomials exactly from engine values by
Newton's forward formula and then certify them by evaluation at further
points (agreement of two degree-d polynomials at d+1 points is equality, so
agreement at 20+ further integer points is a certificate far beyond doubt).

For k = 6:  deg <= 12, fit from n = 1..13, certify on n = 14..40.
For k = 7:  deg <= 14, fit from n = 1..15, certify on n = 16..40.
For k = 8:  deg <= 16, fit from n = 1..17, certify on n = 18..40.
"""
import sys, time
from fractions import Fraction
from math import comb
sys.path.insert(0, "/workspace/fclosure/ledger")
from ledger_engine import partitions, b_sigma, ledger, live_B

out = []
def say(msg=""):
    print(msg)
    out.append(str(msg))

def falling(x, j):
    r = Fraction(1)
    for i in range(j):
        r *= Fraction(x - i) if isinstance(x, int) else Fraction(x) - i
    return r

def P_newton(vals_by_n, deg, k):
    """exact Newton forward coefficients from n=1 upward"""
    n0 = 1
    vs = [Fraction(vals_by_n[i]) for i in range(n0, n0 + deg + 1)]
    # forward difference table
    diffs = [vs]
    for _ in range(deg):
        prev = diffs[-1]
        diffs.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])
    import math
    coeffs = [diffs[j][0] / math.factorial(j) for j in range(deg + 1)]
    def eval_at(m):
        x = m - n0
        return sum(coeffs[j] * falling(x, j) for j in range(deg + 1))
    return coeffs, eval_at

for k in (6, 7, 8):
    deg = 2 * k
    t0 = time.time()
    shapes = [s for s in partitions(k) if s[0] >= 5]
    say(f"== P_{k}(n): degree <= {deg}, {len(shapes)} square shapes "
        f"(p({k})-p_4({k}) = {len(list(partitions(k)))}-{len(list(partitions(k,4)))}) ==")
    vals = {}
    for n in range(1, k * 2 + 2):        # fit-points 1 .. 2k+1
        bs = {s: b_sigma(s, n) for s in shapes}
        vals[n] = sum(v * v for v in bs.values())
    coeffs, eval_at = P_newton(vals, deg, k)
    say("   Newton coefficients c_j = Delta^j P(1) / j!:")
    for j, c in enumerate(coeffs):
        if c:
            say(f"     j={j:2d}: {c.numerator if c.denominator == 1 else c}")
    ok = all(eval_at(n) == vals[n] for n in vals)
    say(f"   fits its own calibration points: {ok}")
    # certify on fresh points 2k+2 .. 40 plus flame-check vs doc region
    bad = []
    for n in range(2 * k + 2, 41):
        bs = {s: b_sigma(s, n) for s in shapes}
        want = sum(v * v for v in bs.values())
        got = eval_at(n)
        if got != want:
            bad.append(n)
    say(f"   certified against engine on n = {2*k+2}..40 (fresh points): "
        f"{'ALL PASS' if not bad else f'FAIL {bad}'}")
    # closed-form spot check at the document's headline columns
    for n in (17, 35):
        bs = {s: b_sigma(s, n) for s in shapes}
        say(f"   P_{k}({n}) = {sum(v*v for v in bs.values())}")
    say(f"   ({time.time()-t0:.0f}s)\n")

open("/workspace/fclosure/ledger/newton_fit.txt", "w").write("\n".join(out) + "\n")
print("written newton_fit.txt", file=sys.stderr)
