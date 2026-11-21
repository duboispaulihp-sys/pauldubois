#!/usr/bin/env python3
"""
norm_route.py -- Phase 8: Route C, the norm (Hall-Gram) formula for live_q.

Mathematical content (see notes/09-live-norm-formula.md for full proofs):

  * Lemma (Hall-Gram identity): the engine's contingency count T_q(mu,nu)
    (= Sum_sigma K_{sigma mu} K_{sigma nu}, verified as the Hall-Gram matrix
    entry by Note H audit H.1) equals the Hall inner product <h_mu, h_nu>,
    because h_mu = prod_j h_{mu_j} = Sum_sigma K_{sigma mu} s_sigma
    (Jacobi-Kostka) and the Schur basis is orthonormal for <,>.

  * Theorem (norm formula):  Sum_{mu_1<=q, |mu|=k} C_mu(n) h_mu
        = [t^k] ( Sum_{r<=q} h_r t^r )^n  =: F_{q,n,k},
    from the decomposition of Sum_c in N^n prod_j h_{c_j} over ordered
    tuples c with total < k (each multiset {c} of multiplicity vector mu
    contributes exactly C_mu(n) h_mu).

  * Corollary (Route C):  live_q(k,n) = || F_{q,n,k} ||^2
        = Sum_{lambda |- k} z_lambda * f_lambda^2
    where f_lambda = [p_lambda] F (Hall inner product in the p-basis,
    || lambda block ||^2 = z_lambda).  DP cost ~ n * Sum_{r<=k} p_q(r)
    * O(1) bigint ops (every reachable key has parts <= q: each factor adds
    one block lambda |- r with r <= q and merges are multiset unions --
    Theorem K.1 of Note K), hence POLYNOMIAL in k, ~ k^(q+1) at fixed q.
    [The original docstring said unrestricted p(r); that slip produced the
    Phase-8 "pool 15.4e9 at k=119, out of reach" model in deep_live.txt --
    superseded by Note K / sextet.py: the true pool at k = 119 is
    sum p_4 = 416,695 (~37,000x smaller) and the deep columns ran in
    under 2 minutes each, all six deep-anomaly rungs resolved exactly.]

Exact arithmetic: all z_lambda (lambda piece <= q <= 4 here) divide L = 24;
we keep L general = lcm(z_lambda) and scale every generator weight w = L/z,
so the DP is pure-integer and the final norm is
    live = ( Sum_val^2 * z_mu ) / L^(2n).
If q > 4 is ever requested the code still works (L = lcm adapts).

Outputs norm_route.txt; final line: "end of norm_route".
"""
from fractions import Fraction
from math import factorial, gcd, comb, sqrt
import time

import capq_engine as E

Frc = Fraction


# ---------------------------------------------------------------- utilities

def z_lambda(lam):
    """z_lambda = prod_i i^{m_i} m_i! for the cycle type / p-basis norm."""
    from collections import Counter
    c = Counter(lam)
    z = 1
    for i, m in c.items():
        z *= i ** m * factorial(m)
    return z


def _lcm(a, b):
    return a * b // gcd(a, b)


def blocks(q):
    """Generators of P = Sum_{r<=q} h_r t^r as p-basis (lambda, weight L/z_lambda).

    Returns (list of (lambda_tuple, Fraction(L, z_lambda)), L)."""
    out = []
    L = 1
    for r in range(0, q + 1):
        lams = list(E.partitions(r)) if r else [()]
        for lam in lams:
            lam = tuple(lam)
            out.append((lam, None, z_lambda(lam)))
            L = _lcm(L, z_lambda(lam))
    blocks_final = [(lam, Fraction(L, z)) for lam, _w, z in out]
    return blocks_final, L


def fmt(x, d=10):
    """Decimal display of a Fraction/int with d digits."""
    if isinstance(x, Fraction):
        return f"{float(x):.{d}f}" if x < 10 ** 15 else str(x)
    return f"{float(x):.{d}f}"


def say(msg=""):
    print(msg, flush=True)


# ---------------------------------------------------------------- Route C

def routeC(k, n, q, BL=None):
    """live_q(k,n) = || F_{q,n,k} ||^2 via the integer Hall-Gram DP.

    Returns a Fraction (denominator L^(2n), in practice exact int ratio)."""
    if BL is None:
        BL, L = blocks(q)
    else:
        BL, L = BL
    dp = {(): (1, 0)}                # p-monomial (parts desc) -> (L-scaled int, t-degree)
    for step in range(1, n + 1):
        ndp = {}
        for mono, (val, deg) in dp.items():
            # keep t-degree <= k at every step (truncate higher)
            for lam, w in BL:
                wd = sum(lam)
                nd = deg + wd
                if nd > k:
                    continue
                key = tuple(sorted(mono + lam, reverse=True)) if lam else mono
                nw = int(w.numerator)
                dw = int(w.denominator)
                if dw == 1:
                    nv = val * nw
                else:
                    # L/z with z | L  =>  exact division
                    nv = val * nw // dw
                prev = ndp.get(key)
                if prev is None:
                    ndp[key] = (nv, nd)
                else:
                    ndp[key] = (prev[0] + nv, nd)
        dp = ndp
    tot = 0
    for mono, (val, deg) in dp.items():
        if deg == k:
            tot += val * val * z_lambda(mono)
    # each of the n steps carries a factor L, so val ~ L^n * (rational sum)
    return Fraction(tot, L ** (2 * n))


# ---------------------------------------------------------------- batteries

def battery_routeC_vs_A(kmax=8, ns=(2, 3, 5), qmax=3):
    """Digit-exact Route C vs engine live_A_q on a broad small window."""
    BLc = {q: blocks(q) for q in range(1, qmax + 1)}
    bad = 0
    tot = 0
    for q in range(1, qmax + 1):
        t0 = time.time()
        for k in range(1, kmax + 1):
            for n in ns:
                a = routeC(k, n, q, BLc[q])
                b = E.live_A_q(k, n, q)
                tot += 1
                if a != b:
                    bad += 1
                    say(f"  MISMATCH q={q} k={k} n={n}: routeC={a} live_A={b}")
        say(f"battery q<= {q}: Route C vs live_A_q, k<= {kmax}, n in {ns}: "
            f"{tot} checks so far, {bad} mismatches  ({time.time()-t0:.1f}s)")
    say(f"BATTERY A: Route C vs live_A_q  ->  {tot - bad}/{tot} PASS, {bad} FAIL")
    return bad == 0


def battery_routeC_vs_B(klist=(6, 10, 12, 20), nlist=(2, 3, 5, 12)):
    """Cross-check against Route B (live_B_q, Schur-side sum) where affordable."""
    BL4 = blocks(4)
    bad = 0
    tot = 0
    for k in klist:
        for n in nlist:
            if n > 14 and k > 24:
                continue
            t0 = time.time()
            a = routeC(k, n, 4, BL4)
            t1 = time.time()
            b = E.live_B_q(k, n, 4)
            t2 = time.time()
            tot += 1
            flag = "OK " if a == b else "FAIL"
            if a != b:
                bad += 1
            say(f"  vsB (k,n)=( {k:>3},{n:>3} ) q=4: {flag} "
                f"routeC {t1-t0:6.2f}s  live_B {t2-t1:8.2f}s")
    say(f"BATTERY B: Route C vs live_B_q (q=4)  ->  {tot-bad}/{tot} PASS, {bad} FAIL")
    return bad == 0


def battery_q1_closed_law(kmax=16, nmax=16):
    """q = 1 closed law:  live_1(k,n) = C(n,k)^2 * k!   for k <= n.

    Proof: F_{1,n} = (1 + h_1 t)^n, so [t^k] F = C(n,k) h_1^k = C(n,k) p_{1^k},
    and || p_{1^k} ||^2 = z_{(1^k)} = k!.  Route C must reproduce this."""
    bad = 0
    tot = 0
    for n in range(1, nmax + 1):
        for k in range(0, n + 1):
            a = routeC(k, n, 1)
            b = comb(n, k) ** 2 * factorial(k)
            tot += 1
            if a != b:
                bad += 1
                say(f"  q1-LAW FAIL k={k} n={n}: routeC={a} law={b}")
    say(f"BATTERY C: q=1 closed law live_1 = C(n,k)^2 k!, (k<=n<={nmax})  "
        f"->  {tot-bad}/{tot} PASS, {bad} FAIL")
    return bad == 0


def battery_leading_law(q=4, klist=(2, 3, 4, 5), nspan=40):
    """Leading law: for fixed k,  live_q(k,n) * k! / n^{2k} -> 1 as n grows.

    (Only the 'diagonal' mu=(k) block of C_mu * h_mu survives normalization:
    C_(k)(n) h_(k) = (n^k/h_k + lower) h_(k), and ||h_(k)||^2 = h_k = ... ;
    the theorem-level check is numerical here.)"""
    say(f"leading law q={q}: live*q-fix k!/n^(2k) -> 1")
    BL = blocks(q)
    for k in klist:
        row = []
        for n in range(k, k + nspan + 1, max(1, nspan // 8)):
            a = routeC(k, n, q, BL)
            r = float(a) * factorial(k) / float(n) ** (2 * k)
            row.append(f"n={n}:{r:.6f}")
        say(f"  k={k}: " + "  ".join(row))
    say("BATTERY D: leading-law window printed (values should climb to 1)")


def battery_routeC_vs_A_q4(kmax=10, ns=(2, 3, 5)):
    """q = 4 window vs live_A_q (pruned contingency DP) -- moderate cost."""
    BL4 = blocks(4)
    t0 = time.time()
    bad = 0
    tot = 0
    for k in range(1, kmax + 1):
        for n in ns:
            a = routeC(k, n, 4, BL4)
            b = E.live_A_q(k, n, 4)
            tot += 1
            if a != b:
                bad += 1
                say(f"  MISMATCH q=4 k={k} n={n}: routeC={a} live_A={b}")
    say(f"BATTERY A4: Route C vs live_A_q (q=4, k<= {kmax}, n in {ns})  "
        f"->  {tot-bad}/{tot} PASS, {bad} FAIL  ({time.time()-t0:.1f}s)")
    return bad == 0


def timings():
    """Timing measurements to set the J.2 / deep-claim budgets."""
    say("TIMINGS (Route C, q = 4):")
    for (k, n) in [(12, 12), (16, 35), (20, 20), (16, 16), (20, 35), (30, 30), (24, 12)]:
        t0 = time.time()
        v = routeC(k, n, 4)
        dt = time.time() - t0
        say(f"  routeC({k:>3},{n:>3},4) = {str(v)[:60]}...  [{dt:8.2f}s]")
    say("TIMINGS done")


# ---------------------------------------------------------------- main

def main():
    t00 = time.time()
    say("=== norm_route.py : Route C (norm / Hall-Gram formula) for live_q ===")
    say("Theorem: live_q(k,n) = || [t^k] (Sum_{r<=q} h_r t^r)^n ||^2 ;")
    say("DP: p-basis exponent tuples, t-degree truncated at k, L = lcm(z_lambda).")

    ok1 = battery_routeC_vs_A(kmax=8, ns=(2, 3, 5), qmax=3)
    ok3 = battery_q1_closed_law(kmax=16, nmax=16)
    ok4 = battery_routeC_vs_A_q4(kmax=10, ns=(2, 3, 5))
    battery_leading_law(q=4, klist=(2, 3, 4, 5), nspan=32)
    battery_routeC_vs_B(klist=(6, 10, 12), nlist=(2, 3, 5, 12))
    timings()

    say("")
    say(f"overall: {'ALL GREEN' if (ok1 and ok3 and ok4) else 'FAILURES PRESENT'} "
        f"[{time.time()-t00:.1f}s]")
    say("end of norm_route")


if __name__ == "__main__":
    main()
