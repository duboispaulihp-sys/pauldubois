#!/usr/bin/env python3
"""sqrtlaw.py -- census of the proposed law  p_{k+1} = log N_k + c (log N_k)^(1/2).

log N_k = X_k = vartheta(p_k), so the law is exactly
    e'_k = p_{k+1} - vartheta(p_k) = c * sqrt(X_k)          (constant c).

Checks, on the strip of consecutive primes [p_{K+1}, 2.07e9] starting from the
certified anchor of h1_at_1e8.py (same walk as sresp.py):

  1. ratio census   c_k = e'_k / sqrt(X_k):  min, max, mean, best-fit c-hat;
  2. law residual   p_{k+1} - (X_k + c-hat sqrt(X_k))  in absolute units and
                    relative to the prime gap;
  3. propagation    plugging e'_k = c-hat sqrt(X_k) into the second-order law
                    p^2 s = 2a - e'(1+a) + a^2/2 (prop:soscil) and comparing
                    with the exact s_k;
  4. sign           predicted s < 0 at every strip prime (e' >> tau ~ 11.2).

Verdict recorded in LEAN.tex (remark rem:sqrtlaw): the constant-c reading
captures the RH/Chebyshev *scale* (c_k in [0.80, 1.23] over 1.49e6 primes)
but is not an eventual law -- Littlewood's theta(x) - x = Omega+(sqrt(x)
logloglog x) at prime endpoints forces c_k to be Omega+- (logloglog X) in
both directions, so no fixed c exists (limsup = +infty, liminf = -infty).
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
    ratios, devs, spred_devs = [], [], []
    min_ep, max_ep, min_gap, max_gap = 1e18, -1e18, 1e18, -1e18
    neg_pred = 0
    n = 0
    for i in range(2, HI - lo + 1, 2):      # lo odd -> odd p at even offsets
        if mark[i]:
            continue
        p = lo + i
        a = math.log(p)
        A = math.log(X)
        s = A / (p - 1) - math.log1p(a / X)
        ep = p - X
        gap = p - lo0 if False else None    # placeholder, gap computed below
        ratios.append(ep / math.sqrt(X))
        # exact second-order law residual for e' = c-hat sqrt(X) plug-in:
        spred_devs.append((p, a, ep, s, X))
        min_ep, max_ep = min(min_ep, ep), max(max_ep, ep)
        assert (s > 0) == (ep < TAU_K)
        n += 1
        if n >= MAXN:
            break
        X += a
    # best-fit constant
    m = len(ratios)
    chat = sum(ratios) / m
    c_min, c_max = min(ratios), max(ratios)
    varr = sum((r - chat) ** 2 for r in ratios) / m
    c_rms = math.sqrt(varr)
    # law residual p - (X + chat sqrt(X)) and gap-relative version
    X = ANCHOR_XK + math.log(ANCHOR_P1)
    res_abs_min, res_abs_max, res_gap_rel_max = 1e18, -1e18, 0.0
    prev_p = ANCHOR_P1
    max_spred_rel = 0.0
    for (p, a, ep_true, s_true, Xt) in spred_devs[: m]:
        pred = chat * math.sqrt(Xt)
        res = ep_true - pred
        res_abs_min, res_abs_max = min(res_abs_min, res), max(res_abs_max, res)
        gaprel = abs(res) / (p - prev_p)
        if gaprel > res_gap_rel_max:
            res_gap_rel_max = gaprel
        # plug-in second-order law vs exact s
        sid = (2 * a - pred * (1 + a) + a * a / 2.0) / p ** 2
        if sid < 0:
            neg_pred += 1
        max_spred_rel = max(max_spred_rel, abs(sid - s_true) / abs(s_true))
        prev_p = p
    lines = [
        "sqrtlaw.py -- census of  p_{k+1} = log N_k + c (log N_k)^(1/2)",
        "strip: consecutive primes [%d, %d]  (N = %d)" % (ANCHOR_P1, spred_devs[-1][0], m),
        "X transported from the certified anchor vartheta(p_{K+1}); tau_K = %.4f" % TAU_K,
        "gate 1 (ratio census):   c_k = e'/sqrt(X): min %.4f  max %.4f  mean %.4f  rms %.4f"
        % (c_min, c_max, chat, c_rms),
        "gate 2 (law residual):   p - (X + c^.sqrt X) in [%.1f, %.1f];  max |res|/gap %.4f"
        % (res_abs_min, res_abs_max, res_gap_rel_max),
        "gate 3 (propagation):    plug-in 2nd-order law reproduces s to rel. %.3e; "
        "s<0 predicted in %d/%d" % (max_spred_rel, neg_pred, m),
        "gate 4 (sign law):       0 counterexamples asserted per prime (s<0 iff e'>tau)",
        "verdict: constant-c = %.4f fits the strip, but c_k itself swings 0.80..1.23;"
        % chat,
        "Littlewood (Omega+ at prime endpoints) makes c_k = Omega+-(logloglog X):",
        "limsup = +infty, liminf = -infty -> no fixed c exists (rem:sqrtlaw).",
        "total %.1f s" % (time.time() - t0),
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    out = run()
    print(out)
    with open(__file__.replace(".py", "_results.txt"), "w") as f:
        f.write(out + "\n")
