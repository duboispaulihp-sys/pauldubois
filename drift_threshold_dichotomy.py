#!/usr/bin/env python3
"""Threshold dichotomy verifier for formal/ThresholdNo.lean.

Reproduces, with exact integer arithmetic, every certificate emitted as a Lean
literal: for each anchor, the no-side instance (floor decaying no faster than
X0/D per window) forcing the prefix sums above the budget head, and the pairing
against the V1 yes-side (DriftReductionV1.driftBound1/2/3). The Lean chains are
carried at the reduced certificate scale (den^K); this script checks the same
integers, the closed form of the total, and the band statements. Stdlib only.
"""
from fractions import Fraction

D = 30000000
Q = 30000
LAUNCH = 1000000      # = D/30, the launch cap in dhat units
FLOOR0 = 39000        # = 13/10000 * D, the error-floor cap in chat units

# (anchor, head M = floor(D_max * D), full-scale X0, reduced link den >= num, K)
ANCHORS = [
    ("anchor 1", 1541354, 27840000, 125, 116, 110),
    ("anchor 2", 1744063, 28440000, 250, 237, 100),
    ("anchor 3", 1928014, 28740000, 500, 479, 180),
]
YES_X = {"anchor 1": 27832580, "anchor 2": 28423857, "anchor 3": 28736617}


def main():
    print(f"D = {D}, Q = {Q}, launch cap = {LAUNCH}, floor cap = {FLOOR0}\n")
    ok = True
    for name, head, X0, sden, snum, K in ANCHORS:
        S = sden ** K
        R = [snum ** m * sden ** (K - m) * FLOOR0 for m in range(K + 1)]
        CUM = []
        acc = 0
        for r in R:
            acc += r
            CUM.append(acc)
        need = head - LAUNCH + 1
        ratio = Fraction(CUM[K], S)
        dhat_bound = LAUNCH + CUM[K] // S
        closed = Fraction(FLOOR0 * sden, sden - snum)   # limit of the floor sum
        Xc = D - FLOOR0 * D // need                     # transfer-only critical X0
        muc = Fraction(Xc, D)
        yes = Fraction(YES_X[name], D)
        no = Fraction(snum, sden)
        checks = {
            f"link reduction: {X0}/D = {snum}/{sden}": Fraction(X0, D) == no,
            f"chat prefix {float(ratio):.4f} >= {need}": CUM[K] >= need * S,
            f"dhat prefix {dhat_bound} >= head+1 = {head + 1}": dhat_bound >= head + 1,
            f"closed form matches: CUM = FLOOR0*(sden^(K+1)-snum^(K+1))/(sden-snum)":
                CUM[K] == FLOOR0 * (sden ** (K + 1) - snum ** (K + 1)) // (sden - snum),
            "transfer-only critical inside band": yes < muc < no,
        }
        print(f"{name}: head M = {head}")
        print(f"  yes (V1): floor contracts at mu <= {yes} = {float(yes):.7f} => all prefix sums <= {head}")
        print(f"  no (ThresholdNo.lean): floor persists at mu >= {no} = {float(no):.7f}")
        print(f"  K = {K} windows (chain depth {K + 1}), certificate scale {sden}^{K} "
              f"({len(str(S))} digits), floor-sum limit = {float(closed):.2f}")
        print(f"  forced chat prefix >= {float(ratio):.4f}; dhat prefix >= {dhat_bound}; "
              f"band width = {float(no - yes):.3e}")
        for label, passed in checks.items():
            print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
            ok &= passed
        print()
    print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
