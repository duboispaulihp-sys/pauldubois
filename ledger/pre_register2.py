"""pre_register2.py -- pre-registered ledger predictions, rungs k = 9, 10, 11,
columns n = 36..40.

Extends pre_register.py (which covered k = 5..8 with full decompositions) to
the next three syzygy rungs, plus the one-row "maturation" law b_(k)(n) for
k = 5..9 at these columns.  Everything is computed with the exact engine
(Route B Kostka b-law + hook-square ledger, cross-arbitrated in calibrate.py)
and every line is internally asserted:

  * P_k(n) = sum_{sigma_1 >= 5} b_sigma(n)^2  for k = 9, 10, 11  (square-count
    law; shape counts 12 / 19 / 29),
  * P_k(n) = live_B(k, n) - ledger(k, n)                      (defining law),
  * b_(k)(n) = sum_j (-1)^j C(n,j) C(n+k-5j-1, k-5j)  for k = 5..9
    (one-row maturation law; the document verified n = 4..26 -- the doc's
    one-row checks -- and this extends to n = 36..40),
  * for each rung k we also record the largest square (shape (k)) and the
    smallest two (the "newborn" shapes), as fingerprints for future audits.

All numbers are exact integers; no floating point anywhere.
"""
import sys, time
from math import comb
sys.path.insert(0, "/workspace/fclosure/ledger")
from ledger_engine import partitions, b_sigma, live_B, ledger, P_k, b_one_row

out = []
def say(msg=""):
    print(msg)
    out.append(str(msg))

say("PRE-REGISTERED LEDGER PREDICTIONS, RUNGS k = 9, 10, 11, COLUMNS n = 36..40")
say("(engine: Kostka b-law Route B; ledger by hook-square; P by live - ledger)")
say("=" * 78)

# ---------------------------------------------- 1. one-row maturation b_(k)
say("\n-- 1. One-row maturation law b_(k)(n) = "
    "sum_j (-1)^j C(n,j) C(n+k-5j-1, k-5j), k = 5..9 --")
say("     n      b_(5)         b_(6)           b_(7)            b_(8)"
    "             b_(9)")
for n in range(36, 41):
    vals = [b_sigma((k,), n) for k in (5, 6, 7, 8, 9)]
    for k, v in zip((5, 6, 7, 8, 9), vals):
        assert v == b_one_row(k, n), (n, k, v, b_one_row(k, n))
    say("  {:4d}".format(n) + "".join(f"  {v:>13d}" for v in vals))
say("  (doc's verified range was n = 4..26; here extended to n = 36..40)")

# ------------------------------------- 2. P_9 / P_10 / P_11 decompositions
for k in (9, 10, 11):
    big = [s for s in partitions(k) if s[0] >= 5]
    say(f"\n-- 2.k Rung P_{k}: square-count p({k}) - p_4({k}) = {len(big)}"
        f" shapes sigma_1 >= 5 --")
    say(f"     n     P_{k}(n)" + "".join(
        f"   b^2_{s}" for s in big))
    for n in range(36, 41):
        bs = {s: b_sigma(s, n) for s in big}
        tot = sum(v * v for v in bs.values())
        assert tot == P_k(k, n) == live_B(k, n) - ledger(k, n), (k, n, tot)
        row = f"  {n:4d}  {tot}"
        for s in big:
            row += f"   {bs[s] * bs[s]}"
        say(row)
    sq = sorted(((b_sigma(s, 40) * b_sigma(s, 40), s) for s in big))
    say(f"  fingerprints at n=40: largest b^2 = {sq[-1][1]} ({sq[-1][0]}), "
        f"smallest b^2 = {sq[0][1]} ({sq[0][0]}), next {sq[1][1]} ({sq[1][0]})")
    say(f"  (all shapes present: {[b_sigma(s, 36) > 0 for s in big].count(True)}"
        f"/{len(big)} nonzero b_sigma at n=36; P_{k}(40) digits = "
        f"{len(str(P_k(k, 40)))})")

say("\nall assertions passed; end of pre_register2")
open("/workspace/fclosure/ledger/pre_register2.txt", "w").write(
    "\n".join(out) + "\n")
print("written pre_register2.txt", file=sys.stderr)
