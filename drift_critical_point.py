#!/usr/bin/env python3
"""Exact-arithmetic verifier for Part XI: the 1000/999 accounting identity and the
exact critical ratio mu* of the threshold dichotomy, per anchor. Companion to
formal/DriftCritical.lean (the never-exceeds boundary theorems). Stdlib only;
all arithmetic in exact rationals / integers."""

from fractions import Fraction as F

D = 30000000
Q = 30000
D0MAX = 10 ** 6
C0MAX = 39000
ANCHORS = [
    (1541354, F(27832580, 30000000), F(116, 125)),
    (1744063, F(28423857, 30000000), F(237, 250)),
    (1928014, F(28736617, 30000000), F(479, 500)),
]
ok = True


def check(name, cond):
    global ok
    print(("  [PASS] " if cond else "  [FAIL] ") + name)
    ok = ok and bool(cond)


print("Part XI verifier: exact critical points of the threshold dichotomy\n")

for M, nu, rho in ANCHORS:
    print(f"anchor head M = {M}")
    # Exact critical total released source: T = (999/1000) M - dhat0_cap.
    T = F(999 * M, 1000) - D0MAX
    # Exact critical ratio: mu* = 1 - c0_cap / T  (closed form, reduced).
    mu = 1 - F(C0MAX) / T
    d, c = mu.denominator, mu.numerator
    check(f"critical source total T = {T} equals c0*d/(d-c) = {F(C0MAX * d, d - c)}",
          T == F(C0MAX * d, d - c))
    check("c0/(1 - mu*) == T (defining relation of mu*)", F(C0MAX) / (1 - mu) == T)
    # Boundary identity: (999 M - 10^9)(d - c) == C0 * 1000 * d.
    lhs = (999 * M - 10 ** 9) * (d - c)
    rhs = C0MAX * 1000 * d
    check(f"boundary identity (999M-1e9)(d-c) == C0*1000*d  [{d - c} * {999 * M - 10 ** 9}]",
          lhs == rhs)
    # Saturation: (1000/999)(dhat0_cap + c0*d/(d-c)) == M exactly.
    check("saturating limit (1000/999)(dhat0 + T) == M exactly",
          F(1000, 999) * (D0MAX + T) == M)
    # Placement: V1 yes-constant <= mu* <= ThresholdNo no-constant.
    check(f"V1 yes-constant {float(nu):.8f} <= mu* = {float(mu):.8f} "
          f"(gap {float(nu - mu):+.3e})", nu <= mu)
    check(f"ThresholdNo no-constant {float(rho):.6f} >= mu* (gap {float(rho - mu):+.3e})",
          rho >= mu)
    # Critical trajectory: exact recursion, caps attained; never exceeds at any window.
    c_traj = [F(C0MAX) * mu ** k for k in range(2000)]
    d_traj = [F(D0MAX)]
    for k in range(1999):
        d_traj.append(d_traj[-1] / 1000 + c_traj[k])
    pref = 0
    sup = F(0)
    for val in d_traj:
        pref += val
        sup = max(sup, pref)
    check(f"sup over K<=2000 of prefix sum = {float(sup):.6f} <= head {M}", sup <= M)
    # Untouched band from above: (mu*, rho).
    print(f"  unresolved band above the boundary: (mu*, rho) width = {float(rho - mu):.3e}")
    print()

print("Exact critical ratios (closed form):")
for M, _, _ in ANCHORS:
    T = F(999 * M, 1000) - D0MAX
    mu = 1 - F(C0MAX) / T
    print(f"  head {M}: mu* = {mu.numerator}/{mu.denominator} = {float(mu):.10f}")
print()
print("ALL CHECKS PASS" if ok else "FAILURES PRESENT")
