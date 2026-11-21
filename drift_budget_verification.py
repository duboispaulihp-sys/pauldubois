#!/usr/bin/env python3
"""Verification suite for Dubois's drift-budget arithmetic.

Independent recomputation of: band endpoints, budget roots D_max(sigma),
the fixed-point bound (Lemma B with decaying source), the feasible region
in (q, c0, mu), the (E1) exponent thresholds alpha_min(sigma), and the
constant-source falsification control. Pure stdlib; exact constants.
"""
import math

EPS = 1 / 30            # launch defect epsilon_prof
C0 = 1.3e-3             # recorded settling-transient seed
Q = 1e-3                # recorded per-window contraction
MU = 2 ** -0.5          # recorded source decay per stage
BAND_LO = 4 * math.log(25 / 4)
BAND_HI = 4 * ((5 / 2) * math.log(2) + math.log(5 / 4))


def rhs(D, eps=EPS):
    return math.log(4) + 2 * math.log((1 + eps + D) / (1 - eps - D))


def lhs(D, sigma):
    return (0.25 - 5.51 * D * D) * sigma


def dmax(sigma, eps=EPS):
    """Root of (6a.7) in (0, 7/90) by bisection; None if crossover passed."""
    a, b = 0.0, 7 / 90
    if lhs(b, sigma) >= rhs(b, eps):
        return None
    for _ in range(200):
        m = 0.5 * (a + b)
        if (lhs(a, sigma) - rhs(a, eps) > 0) == (lhs(m, sigma) - rhs(m, eps) > 0):
            a = m
        else:
            b = m
    return 0.5 * (a + b)


def fixed_point(q, c0, mu, launch=EPS):
    return launch / (1 - q) + c0 / ((1 - q) * (1 - mu))


def alpha_min(c0, q, budget, launch=EPS):
    """Smallest per-stage decay exponent alpha (level lambda^alpha, lambda=1/2)."""
    inv = 1 - c0 / ((1 - q) * (budget - launch / (1 - q)))
    return -math.log2(inv) if 0 < inv < 1 else math.inf


def main():
    print("band: (%.4f, %.4f)" % (BAND_LO, BAND_HI))
    anchors = (BAND_LO, 0.5 * (BAND_LO + BAND_HI), BAND_HI)
    roots = []
    for s in anchors:
        D = dmax(s)
        roots.append(D)
        margin0 = 0.25 * s - rhs(0)
        print("sigma=%.4f  D_max=%.4f  margin(D=0)=%.4f" % (s, D, margin0))

    B = fixed_point(Q, C0, MU)
    print("fixed-point bound = %.6f ; occupancy %.1f%% / %.1f%%"
          % (B, B / roots[0] * 100, B / roots[2] * 100))

    print("c0 ceiling at recorded q,mu: %.4e (%.2fx recorded)"
          % (c0_max := (1 - Q) * (1 - MU) * (roots[0] - EPS / (1 - Q)),
             c0_max / C0))
    q_ceiling = 1 - (EPS + C0 / (1 - MU)) / roots[0]
    print("q ceiling at recorded c0,mu: %.4f" % q_ceiling)
    for s, tag in zip(anchors, ("low", "mid", "high")):
        a = alpha_min(C0, Q, roots[s == anchors[0] and 0 or anchors.index(s)])
        print("alpha_min(%.4f, %s) = %.4f ; mu_max = %.4f" % (s, tag, a, 2 ** -a))

    N = 1000
    tot, d = EPS, EPS
    for _ in range(N):
        d = Q * d + C0
        tot += d
    print("constant-source control: sum after %d windows = %.4f ; d* = %.6f"
          % (N, tot, C0 / (1 - Q)))


if __name__ == "__main__":
    main()
