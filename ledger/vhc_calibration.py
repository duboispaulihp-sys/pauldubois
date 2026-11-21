"""vhc_calibration.py -- the combinatorial model as a VHC testbed.

The document's certified ledger for h(A)^boxtimes n is, in effect, an
inductive machine whose per-column identity

    live(k,n) = ledger(k,n) + P_k(n),   P_k(n) = sum_{sigma_1>=5} b_sigma(n)^2,

splits each cohomological degree into
  * the "ledger" part  -- classes whose algebraicity is forced by the
    dictionary construction (the divisor-fed core), and
  * the "syzygy" part  -- classes born beyond it, exactly the input that a
    variational mechanism (semiregularity / motivated classes) has to supply.

This script computes, exactly, the VHC calibration tables of that model:

  (1) the zero window: P_k(n) = 0 for k <= 4 (the model solves its own
      variational problem there -- the binomial phase), first binding at k=5;
  (2) per-column P_k(n) for n = 2..16, k = 1..9;
  (3) the syzygy square counts p(k) - p_4(k), the number of independent
      "Weil-type slots" the variational mechanism must certify per degree;
  (4) the ledger density ledger/live per degree (exact rationals).

All integers exact; no floating point.
"""
import sys, time
sys.path.insert(0, "/workspace/fclosure/ledger")
from ledger_engine import partitions, ledger, live_B, P_k

out = []
def say(msg=""):
    print(msg)
    out.append(str(msg))

say("VHC CALIBRATION OF THE LEDGER MODEL (h(A)^boxtimes n)")
say("live = ledger + sum_{sigma_1>=5} b_sigma^2 ; exact integers")
say("=" * 76)

# ------------------------------------------------------------ 1. zero window
say("\n-- 1. The zero window: P_k(n) for k = 1..4 --")
bad = []
for n in range(2, 17):
    for k in range(1, 5):
        if P_k(k, n) != 0:
            bad.append((n, k))
say(f"   P_k(n) = 0 for all n = 2..16, k = 1..4: {not bad}  "
    f"(binomial phase; the caps bind only from k = 5)")
say("   -> the model's variational content starts at degree k = 5 in every"
    "\n      column: the birth of the first syzygy square b_(5)(n)^2.")

# --------------------------------------------------------------- 2. table
say("\n-- 2. Syzygy census P_k(n), n = 2..16, k = 1..9 --")
ks = list(range(1, 10))
say("     n: " + "  ".join(f"k={k}" for k in ks))
table = {}
for n in range(2, 17):
    t0 = time.time()
    row = []
    for k in ks:
        row.append(0 if k <= 4 else P_k(k, n))
    table[n] = row
    say(f"  {n:3d}: " + "  ".join(f"{v}" for v in row) + f"   ({time.time()-t0:.1f}s)")

# ------------------------------------------------- 3. square-count column
say("\n-- 3. Syzygy square counts p(k) - p_4(k): independent Weil-type slots --")
say("     k:  " + "  ".join(f"{k:5d}" for k in range(5, 10)))
cnt = [len(list(partitions(k))) - len(list(partitions(k, 4))) for k in range(5, 10)]
say("        " + "  ".join(f"{v:5d}" for v in cnt))

# ----------------------------------------------------- 4. ledger densities
say("\n-- 4. Ledger share ledger(k,n)/live(k,n) at the frontier columns --")
from fractions import Fraction as Fr
for n in (8, 12, 16):
    say(f"   n = {n}:")
    for k in range(5, 10):
        lv, lg = live_B(k, n), ledger(k, n)
        say(f"     k = {k}: 1 - ledger/live = {Fr(lv-lg, lv)}")
    say("")

say("-- 5. Read --")
say("   The zero window k<=4 = the model's proven 'divisor VHC'; every")
say("   nonvanishing P_k(n) entry is one Weil-type slot per shape sigma_1>=5,")
say("   and the certificates of the uploaded document (birth law, square")
say("   decomposition, mirror law, Newton forms -- all audited digit-exactly")
say("   in notes/03) are exactly the model's inductive VHC-proof pattern:")
say("   propagate algebraicity column by column by closed laws.")
open("/workspace/fclosure/ledger/vhc_tables.md", "w").write("\n".join(out) + "\n")
print("written vhc_tables.md", file=sys.stderr)
