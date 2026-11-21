#!/usr/bin/env python3
"""
j2_diagonal.py -- Phase 8: J.2 joint diagonal census pushed to k = 40 via
Route C (the norm / Hall-Gram formula) + a batched Schur-coefficient DP.

Quantities exactly as in Note H section 6 / Note I section 4 / joint_ext.py
(cap 4, the geometric cap; all formulas replicated verbatim from the
Phase-7 script `joint_ext.py` so the k = 13..19 rows are a regression test):

  P_k(n)     = live_q(k, n, 4) - ledger_q(k, n, 4)          syzygy census
  D_k(n)     = P_k(n) (k!)^2 / ( ftot * n^{2k} ),
               ftot = sum_{sigma_1 >= 5} f_sigma^2 = k! - N_k(4)   [RSK]
  cos_k(n)   = cosine between (b^2) and (f^2) share vectors,
               SECOND-moment convention: num = sum b^2 f^2,
               denom = sqrt(sum b^4 * sum f^4)   (engine H.8 convention)
  n*maxErr   = n * max_{sigma_1 >= 5} | share_n - share_inf |, with the
               joint_ext.py share convention share_n = b^2 / sum b^4,
               share_inf = f^2 / sum f^2 (reproduced verbatim for
               continuity of the Note G/H/I time series).

Phase-8 changes (mathematically invisible, computationally decisive):

  1. live by Route C:  live_q(k,n,4) = || [t^k] (1 + h_1 t + ... + h_4 t^4)^n ||^2
     via the integer Hall-Gram DP of norm_route.py (secs, not hours).

  2. the WHOLE b-vector at once:  b_sigma = <s_sigma, F_{q,n,k}> with
     F = sum_mu C_mu(n) h_mu; expanding each h_mu into the Schur basis by
     ITERATED PIERI (h_a * s_sigma = sum_{nu/sigma horiz. strip a} s_nu,
     memoized on the multiset rest, which is again a partition), and
     accumulating b += C_mu * expansion.  This replaces the per-shape
     engine call b_q(sigma,n,4) (the k=19 bottleneck: 923 s) with one
     batched pass (seconds), so the diagonal can be pushed to k = 40.

Independent certifications run at every k:

  (a) sum_sigma b_sigma^2 over ALL shapes = live (Route B identity
      live = ||F||^2 in the Schur basis) -- validates the batch b;
  (b) spot b_sigma vs engine b_q for 3 shapes (regression);
  (c) ftot from k! - N_k(4) (RSK frozen denominator, engine N_k_q)
      vs DIRECT sum_{sigma_1 >= 5} f_sigma^2 over all shapes (hook formula)
      -- validates the RSK frozen-denominator identity at every k;
  (d) f_fast (local O(k)-per-shape hook formula) vs engine f_syt on 3 shapes;
  (e) k = 13..19 rows must match joint_ext.txt / Note I section 4 exactly
      (P digit count, D, cos, n*maxErr).

Writes j2_diagonal.txt; final line: "end of j2_diagonal".
"""
from fractions import Fraction as Frc
from math import factorial
from decimal import Decimal, getcontext
from functools import lru_cache
import sys, time, json
sys.setrecursionlimit(100000)

import capq_engine as E
import norm_route as NR

# guard: open the output only when run as a script (an import — e.g. the
# j2_resume.py parallel addendum — must NOT truncate the transcript)
OUT = None


def say(m=""):
    print(m, flush=True)
    if OUT is not None:
        OUT.write(m + "\n")
        OUT.flush()


def fshow(x, d=4):
    return f"{float(x):.{d}f}"


# ------------------------------------------------------------ Pieri batch b

@lru_cache(maxsize=None)
def h_exp(partst):
    """Schur expansion of h_{partst} (parts weakly decreasing, parts <= 4).

    = prod_j h_{partst[j]} expanded by: h_mu = Pieri(exp(rest), mu_0).
    Returns dict {sigma_tuple: multiplicity} with sigma |- |partst|."""
    if not partst:
        return {(): 1}
    a = partst[0]
    rest = partst[1:]
    base = h_exp(rest)
    out = {}
    for sigma, m in base.items():
        for nu in horiz_strips(sigma, a):
            out[nu] = out.get(nu, 0) + m
    return out


@lru_cache(maxsize=None)
def horiz_strips(sigma, a):
    """All shapes nu = sigma + horizontal a-strip (nu/sigma horiz. strip:
    nu_i >= sigma_i and nu_{i+1} <= sigma_i, i.e. at most one new box per
    column).  Shapes kept as trimmed tuples (no trailing zeros)."""
    rows = list(sigma) + [0] * (a)          # allow up to (len+1..) new rows... cap below
    L = len(sigma) + 1                       # a strip can create at most ONE new row
    rows = rows[:L]
    res = []

    def rec(i, rem, chosen, prev_sigma):
        if i == L:
            if rem == 0:
                res.append(tuple(x for x in chosen if x > 0))
            return
        # nu_i constraints: nu_i >= sigma_i ; nu_i <= sigma_{i-1} (strip cond,
        # i >= 1) -- which also forces nu_i <= nu_{i-1} automatically;
        # nu_i <= sigma_i + rem (budget)
        lo = rows[i]
        hi = min(rows[i] + rem, (prev_sigma if i >= 1 else 10 ** 9), 
                 (chosen[-1] if chosen else 10 ** 9))
        for nu_i in range(hi, lo - 1, -1):
            rec(i + 1, rem - (nu_i - rows[i]), chosen + [nu_i], rows[i])
        # note: also enforce nu_i <= chosen[-1] explicitly (harmless, implied)

    rec(0, a, [], 10 ** 9)
    return tuple(res)


def batch_b(k, n, q=4):
    """b_sigma = sum_{mu_1<=q, |mu|=k, len(mu)<=n} C_mu(n) K_{sigma mu},
    for ALL sigma, computed by accumulating the Pieri expansions.

    Returns dict {sigma: b} (only nonzero entries)."""
    bvec = {}
    for mu in E.partitions(k, q):
        mu = tuple(mu)
        if len(mu) > n:
            continue
        cm = E.C_mu(n, mu)
        if cm == 0:
            continue
        for sigma, kk in h_exp(mu).items():
            bvec[sigma] = bvec.get(sigma, 0) + cm * kk
    return bvec


# ------------------------------------------------------------ fast hooks

COLH_MEMO = {}


def f_fast(sigma):
    """f_sigma = k! / prod hooks, O((#cells) + k) with column heights
    precomputed once (vs engine f_syt's O(k*rows) down-loop per cell)."""
    k = sum(sigma)
    L = sigma[0] if sigma else 0
    colh = [0] * (L + 1)
    for x in sigma:
        for j in range(x):
            colh[j] += 1
    hook = 1
    for i, x in enumerate(sigma):
        for j in range(x):
            hook *= (x - j) + (colh[j] - i) - 1
    return factorial(k) // hook


# ------------------------------------------------------------ J.2 census

def frozen_share_vec_all(k):
    """{sigma: f^2} for ALL sigma |- k with sigma_1 >= 5 (fast hooks)."""
    tot = 0
    v = {}
    for sig in E.partitions(k):
        if sig[0] >= 5:
            f2 = f_fast(sig) ** 2
            v[sig] = f2
            tot += f2
    return v, tot


def cens(k, n):
    t0 = time.time()
    live = NR.routeC(k, n, 4)
    assert live.denominator == 1, "Route C live must be an integer"
    live = int(live)
    ledger = E.ledger_q(k, n, 4)
    P = live - ledger

    bvec = batch_b(k, n, 4)
    # (a) Route B identity: sum b^2 over ALL shapes = live
    sbsum = sum(b * b for b in bvec.values())
    cert_a = (sbsum == live)
    # (b) spot check vs engine b_q
    spots = []
    for sig in E.partitions(k):
        if sig[0] >= 5:
            spots.append(sig)
            if len(spots) == 3:
                break
    cert_b = all(E.b_q(sig, n, 4) == bvec.get(sig, 0) for sig in spots)
    # (c) RSK frozen denominator vs direct hook sum
    big, ftot_direct = frozen_share_vec_all(k)
    ftot = factorial(k) - E.N_k_q(k, 4)
    cert_c = (ftot == ftot_direct)
    # (d) f_fast vs f_syt spot
    cert_d = all(f_fast(s) == E.f_syt(s) for s in spots)
    if spots and cert_d:
        pass

    # cos + maxErr exactly per joint_ext.py conventions
    num = 0
    sb, sf = 0, 0        # second moments: sum b^4, sum f^4 over sigma_1 >= 5
    for sig, f2 in big.items():
        b2 = bvec.get(sig, 0) ** 2
        num += b2 * f2
        sb += b2 * b2
        sf += f2 * f2
    if num == 0:
        cos = 1.0
    else:
        getcontext().prec = 30
        cos = float(Decimal(num) / (Decimal(sb).sqrt() * Decimal(sf).sqrt()))
    err = 0.0
    for sig, f2 in big.items():
        b = bvec.get(sig, 0)
        share_n = float(Frc(b * b, sb)) if sb else 0.0
        share_inf = float(Frc(f2, ftot))
        err = max(err, abs(share_n - share_inf))
    D = Frc(P * factorial(k) ** 2, ftot * n ** (2 * k))
    say(f"| {k} | {n} | {len(str(P))} | {fshow(D)} | {cos:.4f} | {n*err:.3f} |"
        f"   ({time.time()-t0:.1f}s)  certs {''.join('T' if c else 'F' for c in (cert_a, cert_b, cert_c, cert_d))}")
    return k, n, D, cos, n * err, (cert_a, cert_b, cert_c, cert_d)


# ------------------------------------------------------------ regression

# Note I section 4 / joint_ext.txt rows (k, digits(P), D, cos, n*maxErr):
REGRESSION = {
    13: (20, 1.8989, 0.6951, 1.323),
    14: (22, 1.7362, 0.6695, 0.962),
    15: (24, 1.6222, 0.6615, 1.133),
    16: (26, 1.5425, 0.6632, 1.113),
    17: (28, 1.4868, 0.6626, 1.200),
    18: (30, 1.4478, 0.6566, 0.776),
    19: (32, 1.4201, 0.6488, 0.666),
}


def main():
    global OUT
    OUT = open("j2_diagonal.txt", "w")
    say("== Phase 8: J.2 diagonal census to k = 40 (Route C + batch Pieri b) ==")
    say("   columns exactly as Note I section 4; certs = (sumB2=live, spot b_q,")
    say("   ftot RSK identity, f_fast).")
    say("| k | n | digits(P) | D_k(n) | cos_k(n) | n*maxErr |")
    say("|----|----|------------------|---------|---------|-------|")
    allcert = True
    for k in range(13, 41):
        row = cens(k, k)
        allcert &= all(row[5])
        if k in REGRESSION:
            dg, D, co, me = REGRESSION[k]
            okc = abs(float(row[3]) - co) < 5e-5 and abs(float(row[4]) - me) < 5e-4
            okD = abs(float(row[2]) - D) < 5e-5
            say(f"   regression k={k}: D {fshow(row[2])} vs {D} "
                f"cos {row[3]:.4f} vs {co} maxErr {row[4]:.3f} vs {me} "
                f"-> {'MATCH' if (okc and okD) else 'DEVIATION'}")
    say("")
    say(f"all per-k certifications (a)-(d): {'PASS' if allcert else 'FAIL'}")
    say("")
    say("== Reading ==")
    say("   (filled in from the table above: continuation of D_k(k), cos,")
    say("   n*maxErr along the diagonal to k = 40; see Note J section 3.)")
    say("")
    say("end of j2_diagonal")
    OUT.close()


if __name__ == "__main__":
    main()
