"""AB-driven bridge verification: the geometric mechanism demonstrated with the
Alpöge-Buckmaster convergence rate (1.6) as the drive. Pure stdlib; exact constants.

Verifies (independently of the session's other computations):
  1. the bridge constant budget: C_max(kappa) = e^{k sigma0} (1 - e^{-k S}) D_min;
  2. the stage-by-stage AB-driven window table at kappa = 1/4, S = log 2;
  3. exactness of the total: Sigma_inf = (1 - mu) D_min / (1 - mu) = D_min at C = C_max;
  4. the misfit chain: eps_prof + Sigma_inf <= 1/9 with headroom;
  5. the exact integer ground inequality used by the Lean instance
     (D = 3e7, X = 25226893 = ceil(2^{-1/4} D), launch cap 245230, head 1541354).
"""
import math

SIGMA0 = 7.3303             # band start (launch)
SIGMA1 = 7.8240             # band end
S = math.log(2)             # stage width (lambda = 1/2), Dubois cascade
D_MIN = 0.05137848          # precise root of (6a.7) at SIGMA0
D_UP = 0.06426717           # precise root at SIGMA1
EPS_PROF = 1 / 30
KAPPA = 0.25                # maximal AB rate


def cmax(kappa):
    """Bridge constant budget: largest C for which the AB-driven window cascade
    stays inside the tightest budget head on the band."""
    return math.exp(kappa * SIGMA0) * (1 - math.exp(-kappa * S)) * D_MIN


def stage_table(kappa=KAPPA, n=8):
    mu = 2 ** (-kappa)          # e^{-kappa S} with S = log 2
    d0 = (1 - mu) * D_MIN       # launch reading at C = C_max(kappa)
    rows, tot = [], 0.0
    for i in range(n):
        d = d0 * mu ** i
        tot += d
        rows.append((i, SIGMA0 + i * S, d, tot, EPS_PROF + tot))
    return rows, tot, d0 / (1 - mu)


def main():
    print("bridge constant budget C_max(kappa)")
    for k in (0.25, 0.2, 0.15, 0.1, 0.05, 0.01):
        print("  kappa=%5.2f  C_max=%.6f  launch delta_0<=%.7f" %
              (k, cmax(k), math.exp(-k * SIGMA0) * cmax(k)))

    rows, part, s_inf = stage_table()
    print("\nAB-driven stage table (kappa=1/4, S=log 2, mu=2^{-1/4}=%.8f)" % 2 ** -0.25)
    for i, sig, d, tot, eps0 in rows:
        print("  n=%d  sigma=%.4f  delta_n=%.6f  cum=%.6f  eps_0=%.6f" %
              (i, sig, d, tot, eps0))

    ok_dmin = abs(s_inf - D_MIN) < 1e-12
    ok_budget = EPS_PROF + s_inf <= 1 / 9
    head = (1 / 9 - (EPS_PROF + D_MIN)) / (1 / 9)
    print("\nSigma_inf = C e^{-k sigma0}/(1-e^{-kS}) = %.8f  == D_min: %s" %
          (s_inf, ok_dmin))
    print("eps_prof + Sigma_inf = %.8f <= 1/9: %s  (headroom %.2f%%)" %
          (EPS_PROF + s_inf, ok_budget, head * 100))

    D, X, M, CAP = 30000000, 25226893, 1541354, 245230
    P = D - X
    mu_exact = 2 ** -0.25
    assert X == math.ceil(mu_exact * D) and X / D >= mu_exact
    ground = D * CAP <= M * P
    print("\nLean instance: X=%d  (1-mu)D=%d  launch cap=%d  head=%d" %
          (X, P, CAP, M))
    print("  ground D*cap = %d <= M*(D-X) = %d : %s (slack %d)" %
          (D * CAP, M * P, ground, M * P - D * CAP))
    print("  interval check: mu <= X/D < mu + 1/D: %s" %
          (mu_exact <= X / D < mu_exact + 1 / D))
    assert ok_dmin and ok_budget and ground


if __name__ == "__main__":
    main()
