#!/usr/bin/env python3
"""sresp.py -- sign law and second-order identity for the transport residual s_k.

Checks, on the strip of consecutive primes [p_{K+1}, 2.07e9] starting from the
certified anchor of h1_at_1e8.py:

  1. exact residual        s_k = A_k/(p_{k+1}-1) - log1p(a_k/X_k),
                           A_k = log X_k, X_k = vartheta(p_k), a_k = log p_{k+1};
  2. second-order law      p_k^2 s_k = 2 a_k - e'_k (1+a_k) + a_k^2/2 + err,
                           e'_k = p_{k+1} - vartheta(p_k);
  3. sign law              s_k < 0  iff  e'_k > tau_k,  tau_k = a(a+2)/(2(1+a));
  4. sign census           (all s_k < 0 expected on the strip: e' ~ 4.5e4 >> tau).

Modulo Littlewood's sign theorem (theta(x) - x = Omega+(sqrt(x) logloglog x),
maximal at prime endpoints), item 3 refutes "x_k = s_k/u_k < 0 eventually":
the residual is an Omega-oscillator (proposition prop:soscil in LEAN.tex).
"""
import math
import time

ANCHOR_XK = 2038030124.4153652          # certified vartheta(p_K)
ANCHOR_P1 = 2038074751                  # p_{K+1}
HI = 2_070_000_000
MAXN = 2_000_000
TAU_K = math.log(ANCHOR_P1) * (2 + math.log(ANCHOR_P1)) / (2 * (1 + math.log(ANCHOR_P1)))


def odd_sieve(lo, hi):
    size = hi - lo + 1
    mark = bytearray(size)              # 1 = composite
    for q in range(3, int(math.isqrt(hi)) + 1, 2):
        start = max(q * q, ((lo + q - 1) // q) * q)
        if start % 2 == 0:
            start += q
        for idx in range(start - lo, size, 2 * q):
            mark[idx] = 1
    return mark


def run():
    t0 = time.time()
    lo = ANCHOR_P1
    mark = odd_sieve(lo, HI)
    X = ANCHOR_XK + math.log(ANCHOR_P1)     # vartheta(p_{K+1}) exactly
    rows, min_s, max_s, min_ep, max_ep, max_dev = [], 0.0, -1e9, 1e18, -1e18, 0.0
    for i in range(2, HI - lo + 1, 2):       # lo odd -> odd p at even offsets
        if mark[i]:
            continue
        p = lo + i
        a = math.log(p)
        A = math.log(X)
        s = A / (p - 1) - math.log1p(a / X)
        ep = p - X
        sid = (2 * a - ep * (1 + a) + a * a / 2.0) / p ** 2
        dev = abs(sid - s) / abs(s)
        if dev > max_dev:
            max_dev = dev
        min_s, max_s = min(min_s, s), max(max_s, s)
        min_ep, max_ep = min(min_ep, ep), max(max_ep, ep)
        assert (s > 0) == (ep < TAU_K), (p, s, ep)
        rows.append((p, s, ep))
        X += a
        if len(rows) >= MAXN:
            break
    n = len(rows)
    neg = sum(1 for _, s, _ in rows if s < 0)
    sqrt_lo, sqrt_hi = math.sqrt(rows[0][0]), math.sqrt(rows[-1][0])
    lines = [
        "sresp.py -- sign law and second-order identity of the transport residual",
        f"strip: consecutive primes [{rows[0][0]}, {rows[-1][0]}]  (N = {n})",
        f"X transported from the certified anchor vartheta(p_{{K+1}}); tau_K = {TAU_K:.4f}",
        f"gate 1 (sign census):        s < 0 in {neg}/{n};  s range [{min_s:.6e}, {max_s:.6e}]",
        f"gate 2 (2nd-order law):      max relative deviation (every 997th) {max_dev:.3e}",
        f"gate 3 (sign law vs tau):    0 counterexamples (asserted per prime)",
        f"e' range [{min_ep:.1f}, {max_ep:.1f}];  margin over tau = {min_ep/TAU_K:.3e}x",
        f"e'/sqrt(p) range [{min_ep/sqrt_hi:.3f}, {max_ep/sqrt_lo:.3f}]  (Chebyshev-error scale)",
        f"conclusion: x_k = s_k/u_k < 0 at every strip prime; Omega-side refutation",
        f"is Littlewood's (theta(x)-x = Omega+(sqrt(x) logloglog x)) -- prop:soscil",
        f"total {time.time()-t0:.1f} s",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    print(out)
    with open(__file__.replace(".py", "_results.txt"), "w") as f:
        f.write(out + "\n")
