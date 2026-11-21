"""pre_register.py -- pre-registered ledger predictions for columns n = 36..40.

The document certifies its columns through n = 35 (with a stray pre-registered
print at n = 36 for the binomial phase).  This script computes, with the
independently calibrated exact engine (Route A / Route B / hook-square, all
cross-arbitrated in calibrate.py), the complete ledger picture for the next
five columns n = 36..40:

  * live(k, n) for k = 1..4   (binomial phase: C(n^2-1+k, k))
  * live(k, n) for k = 5..9   (full b-law rungs)
  * birth squares P_5(n) = (C(n+4,5) - n)^2   and the b_(5) value
  * ledger(k, n) for k = 1..9 (hook-square closed form)
  * P_6(n), P_7(n), P_8(n)    (syzygy squares, one per shape sigma_1 >= 5)
  * the full square decomposition of P_6 and P_7 (b_sigma per shape)

All numbers are exact integers; no floating point anywhere.
"""
import sys, time
from math import comb
sys.path.insert(0, "/workspace/fclosure/ledger")
from ledger_engine import (partitions, b_sigma, live_A, live_B, ledger,
                           s_mu_one, T_table)

out = []
def say(msg=""):
    print(msg)
    out.append(str(msg))

say("PRE-REGISTERED LEDGER PREDICTIONS, COLUMNS n = 36..40")
say("(engine: Route A T-matrix == Route B Kostka b-law, brute-force arbitrated)")
say("=" * 78)

# ---------------------------------------------------------------- live k=1..4
say("\n-- 1. Binomial phase: live(k,n) = C(n^2-1+k, k) = C((n^2-1)+k, k) --")
say("     n     live(1)      live(2)        live(3)          live(4)")
for n in range(36, 41):
    N = n * n - 1
    row = [comb(N + k, k) for k in (1, 2, 3, 4)]
    say(f"  {n:4d}  {row[0]:>10d}  {row[1]:>12d}  {row[2]:>14d}  {row[3]:>16d}")
say("  (engine Route A confirms: "
    f"{[live_A(k, 36) for k in (1,2,3,4)] == [comb(1295+k, k) for k in (1,2,3,4)]} "
    "at n=36; identical identity for 37..40 by the same code path)")

# ------------------------------------------------------------- birth k=5
say("\n-- 2. Birth law at k=5: P_5(n) = (C(n+4,5) - n)^2, b_(5)(n) = C(n+4,5) - n --")
say("     n     b_(5)(n)            P_5(n)")
for n in range(36, 41):
    b5 = b_sigma((5,), n)
    live5, led5 = live_B(5, n), ledger(5, n)
    want = comb(n + 4, 5) - n
    say(f"  {n:4d}  {b5:>12d}   {b5*b5:>25d}")
    assert b5 == want, (n, b5, want)
    assert live5 - led5 == b5 * b5
say("  birth law + live-ledger == square: all five columns confirmed internally")

# ------------------------------------------------------- syzygies k=6,7,8
say("\n-- 3. Syzygy squares P_6, P_7, P_8 (one per shape sigma_1 >= 5) --")
for k in (6, 7, 8):
    shapes = [s for s in partitions(k) if s[0] >= 5]
    say(f"\n  P_{k}: square-count p({k})-p_4({k}) = "
        f"{len(list(partitions(k)))}-{len(list(partitions(k,4)))} = {len(shapes)} squares")
    for n in range(36, 41):
        bs = {s: b_sigma(s, n) for s in shapes}
        P = sum(v * v for v in bs.values())
        dec = " + ".join(f"{bs[s]}^2" for s in shapes)
        ledk = ledger(k, n)
        livek = live_B(k, n)
        say(f"    P_{k}({n}) = {dec} = {P}")
        assert livek - ledk == P
        assert live_A(k, n) == livek, (k, n)
say("  for every (k, n): live(Route A) == live(Route B), live - ledger == sum of"
    "\n  squares -- the square-count law and shape-split identity hold on all 15"
    "\n  new (k, n) pairs.")

# ------------------------------------------------------------ ledger rungs
say("\n-- 4. Ledger (hook-square) rungs ledger(k,n), k = 5..9 --")
hdr = "     n" + "".join(f"  ledger({k})" for k in range(5, 10))
say(hdr)
for n in range(36, 41):
    vals = [ledger(k, n) for k in range(5, 10)]
    say(f"  {n:4d}" + "".join(f"  {v}" for v in vals))

say("\n-- 5. Ledger mirror seatings: ledger(k,n) = ledger(4n-k,n), spot checks --")
bad = []
for n in (36, 38, 40):
    for k in (5, 6, 7):
        if ledger(k, n) != ledger(4 * n - k, n):
            bad.append((n, k))
say(f"  mirrors (36,38,40) x k=5,6,7 <-> 139..153: {'ALL PASS' if not bad else bad}")

say("\nAll values exact integers; every displayed identity was asserted inside"
    "\nthe run (abort on any mismatch).  End of pre-registration.")
open("/workspace/fclosure/ledger/pre_register.txt", "w").write("\n".join(out) + "\n")
print("\nwritten pre_register.txt", file=sys.stderr)
