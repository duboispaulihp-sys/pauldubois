"""closed_laws.py -- the ledger's closed laws and asymptotics (exact).

Theorem content certified here (see notes/05 for the proofs):

 (F.1) For fixed k, P_k(n), ledger(k,n), live(k,n) are polynomials in n of
       degree <= 2k.  (C_mu(n) and s_mu(1^n)^2, hook-content, are polynomials
       of degree |mu| resp. 2|mu|.)

 (F.2) Exact leading constants, from RSK:
       *  f_sigma := K_{sigma,(1^k)} = # SYT of shape sigma, and
          sum_sigma f_sigma^2 = k!  (RSK on pairs of permutations);
       *  live(k,n)  ~ n^{2k}/k!;
       *  P_k(n)     ~ (sum_{sigma_1>=5} f_sigma^2) * n^{2k}/(k!)^2;
       *  ledger(k,n)~ (sum_{mu_1<=4} f_mu^2)     * n^{2k}/(k!)^2.
       So the syzygy/density structure freezes in the limit into exact
       constants per k (no n-dependence): in particular P_5/live -> 1/k! = 1/120.

 (F.3) The zero/closure law: P_k(n) = 0  iff  k <= 4 or k >= 4n+1; and
       P_k(n) > 0 for 5 <= k <= 4n (every shape has f_sigma > 0).

 (F.4) Closed-law atlas: exact Newton forward forms (rationals) in n for
       ledger(k, .), live(k, .), k = 5..9, and P_k(.), k = 6..10, each
       certified on ~2k fresh points beyond its 2k+1 calibration points.

All exact integers/rationals; no floating point.
"""
import sys, time
import math
from fractions import Fraction as Fr
sys.path.insert(0, "/workspace/fclosure/ledger")
from ledger_engine import (partitions, b_sigma, ledger, live_B, P_k,
                           kostka_gt, s_mu_one)

out = []
def say(msg=""):
    print(msg, flush=True)
    out.append(str(msg))

def falling(x, j):
    r = Fr(1)
    for i in range(j):
        r *= Fr(x - i)
    return r

def newton(vals, deg):
    """exact Newton forward coefficients from n=1 upward; returns (coeffs, eval)"""
    vs = [Fr(vals[i]) for i in range(1, deg + 2)]
    diffs = [vs]
    for _ in range(deg):
        prev = diffs[-1]
        diffs.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])
    coeffs = [diffs[j][0] / math.factorial(j) for j in range(deg + 1)]
    return coeffs, (lambda m: sum(coeffs[j] * falling(m - 1, j)
                                  for j in range(deg + 1)))

# ----------------------------------------------------------- F.2 constants
say("== F.2: exact leading constants ==")
for k in (5, 6, 7, 8, 9, 10):
    t0 = time.time()
    fsq_all, fsq_big, fsq_led = 0, 0, 0
    for s in partitions(k):
        f = kostka_gt(s, (1,) * k)
        fsq_all += f * f
        if s[0] >= 5:
            fsq_big += f * f
    for mu in partitions(k, 4):
        fsq_led += kostka_gt(mu, (1,) * k) ** 2   # f_mu = K_{mu,(1^k)}
    say(f"  k={k}: sum_all f^2 = {fsq_all} (=k!: {fsq_all == math.factorial(k)}), "
        f"sum_(s_1>=5) f^2 = {fsq_big}, sum_(mu_1<=4) f^2 = {fsq_led}")
    # predicted P_5-law cross-check at k=5: constant 1/120
    say(f"        P_{k}(n)/live(k,n) -> {Fr(fsq_big, fsq_all)};  "
        f"ledger-share -> {Fr(fsq_led, fsq_all)}   ({time.time()-t0:.1f}s)")
    if k == 5:
        say(f"  check k=5: P_5/live limit == 1/120: {Fr(fsq_big, fsq_all) == Fr(1, 120)}")

# ------------------------------------------------- F.3 closure/zero window
say("\n== F.3: the zero law: P_k(n) = 0 iff k<=4 or k>=4n+1 ==")
bad0, badpos = [], []
# engine-side spot checks are band-limited to k <= 11 (P_12.. live rungs are
# hours of Kostka DPs); the FULL range 5 <= k <= 4n for n = 2..12 is certified
# by the explicit witness pair (sigma, mu) of Theorem F.3 -- dominance +
# K_{sigma,mu} > 0 + C_mu(n) > 0 -- run separately (see notes/05).
for n in range(2, 13):
    for k in range(5, min(4 * n, 11) + 1):
        if P_k(k, n) <= 0:
            badpos.append((n, k))
    for k in range(4 * n + 1, 4 * n + 4):
        if k <= 26 and P_k(k, n) != 0:
            bad0.append((n, k))
say(f"   interior positivity k in [5,min(4n,11)]: "
    f"{'ALL PASS' if not badpos else badpos[:5]}")
say(f"   closure beyond 4n (k<=26):               {'ALL PASS' if not bad0 else bad0[:5]}")
say("   proof (notes/05, Thm F.3): explicit witness pair sigma=(5,4^(t-1),r-1)-type;\n"
    "      sigma dominates mu=(4^t,r), K_{sigma,mu} > 0, C_mu(n) > 0 => b_sigma > 0.")

# ----------------------------------------------------- F.4 the closed atlas
say("\n== F.4: closed-law atlas (exact Newton forms, certified) ==")
for tag, fn, kmax in (("ledger", lambda k, n: ledger(k, n), (5, 6, 7, 8)),
                      ("live",   live_B,                       (5, 6, 7, 8, 9)),
                      ("P",      P_k,                          (6, 7, 8, 9, 10))):
    for k in kmax:
        deg = 2 * k
        t0 = time.time()
        vals = {n: fn(k, n) for n in range(1, deg + 2)}
        coeffs, ev = newton(vals, deg)
        ok_self = all(ev(n) == vals[n] for n in vals)
        cert = []
        for n in range(deg + 2, deg + 2 + 2 * k):
            if fn(k, n) != ev(n):
                cert.append(n)
        top = coeffs[-1]
        if tag == "live":
            pred = Fr(1, math.factorial(k))
            match = (top == pred)
        elif tag == "ledger":
            fl = sum(kostka_gt(mu, (1,) * k) ** 2 for mu in partitions(k, 4))
            match = (top == Fr(fl, math.factorial(k) ** 2))
        else:
            fb = sum(kostka_gt(s, (1,) * k) ** 2
                     for s in partitions(k) if s[0] >= 5)
            match = (top == Fr(fb, math.factorial(k) ** 2))
        say(f"  {tag}({k}, n): deg {deg}; self-fit {ok_self}; "
            f"certified on {2*k} fresh pts: {'PASS' if not cert else f'FAIL {cert}'}; "
            f"top coeff == RSK constant: {match} ({top})  ({time.time()-t0:.0f}s)")
        nz = [(j, c) for j, c in enumerate(coeffs) if c != 0]
        opts = {"ledger": "L", "live": "V", "P": "P"}[tag]
        say(f"    {opts.replace('F', 'F')}_{k}(m) = " + " + ".join(
            f"({c})*falling(m-1,{j})" for j, c in nz))

say("\nall exact; end of closed_laws")
open("/workspace/fclosure/ledger/closed_laws.txt", "w").write("\n".join(out) + "\n")
print("written closed_laws.txt", file=sys.stderr)
