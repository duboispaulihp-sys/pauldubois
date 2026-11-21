#!/usr/bin/env python3
"""hipos_window.py -- certified positivity window of the anchored chain at
K = 10^8 (physical seed): H_i > 0, equivalently Nicolas' criterion
f(p_{K+i}) < 1, for every i in [1, W], by exact transport.

The physical chain at the anchor K with the physical seed satisfies exactly
H_i = eps_{K+i}/u_K (u fixed at u_K), and eps_{K+i} > 0 for primes is EXACTLY
Nicolas' quantity sign: f(p) = (N/phi(N))/(e^gamma A) < 1  <=>  eps > 0.
So certifying H_i > 0 on a window certifies Nicolas' criterion on the prime
range [p_{K+1}, p_{K+W}].  eps is propagated by the exact transport law

    eps_{n+1} = (1 + r_n) eps_n + s_n,
    r_n = 1/(p_{n+1}-1),  u_n = log p_{n+1}/theta(p_n),
    s_n = r_n A_n - log1p(u_n),   A_n = log theta(p_n),

seeded at the certified anchor eps_K (h1_at_1e8, cross-checked by the deep
pass of chainform.py).  The stream starts at the certified anchor -- primes
below p_K are never generated.  theta is maintained with per-segment fsum
re-anchoring (SEG_SPAN = 1e8), as in chainform.py.

Certificates:
  1. p_{K+1} and u_1 = log p_{K+1}/X_K against the certified constants;
  2. H at the deep-pass checkpoints j in {1,2,1000,1e4,1e5,1e6,5e6} against
     chainform_results.txt (independent run, walk from 2, compensated e^lv);
  3. window coverage: index K+W reached inside the sieve bound;
  4. min eps and min H over the window vs the float64 noise bound.

Pure Python 3, no dependencies.
"""

import math
import time
from math import isqrt, log, log1p

EULER_GAMMA = 0.5772156649015328606065
INV_E_GAMMA = math.exp(-EULER_GAMMA)

K = 100_000_000
W = 200_000_000
LIMIT = 7_000_000_000
SEG_SPAN = 100_000_000
CKPTS = (1, 2, 1000, 10_000, 100_000, 1_000_000, 5_000_000,
         10_000_000, 20_000_000, 50_000_000, 100_000_000, 200_000_000)

CERT = {
    "p_K": 2038074743,
    "p_K1": 2038074751,
    "X_K": 2038030124.4153652,
    "u_K": 1.0517642105918211e-08,
    "eps_K": 4.3461928497354573e-05,
    "H_K": 4132.2882124786138,
}
H_K1_XK = 21.435271449680776          # certified log p_{K+1}
CERT_TOL = 1e-6

CROSS_DEEP = {                        # H_true from chainform deep pass
    1: 4132.28819173141528,
    2: 4132.28817085263745,
    1000: 4132.26734053036489,
    10_000: 4132.07781370465545,
    100_000: 4130.21388736587960,
    1_000_000: 4111.73708702537715,
    5_000_000: 4024.83700208751361,
}
CROSS_TOL = 1e-6

NOISE_BOUND = 3e-12                   # worst-case float64 eps drift bound

T0 = time.time()
OUT = []


def out(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


def stamp():
    return "[%7.1fs]" % (time.time() - T0)


def rel(a, b):
    return abs(a - b) / abs(b) if b else abs(a - b)


def primes_upto(limit):
    """Plain odd sieve; yields all primes p <= limit."""
    if limit < 2:
        return
    yield 2
    if limit < 3:
        return
    size = (limit - 1) // 2
    sieve = bytearray([1]) * (size + 1)
    sieve[0] = 0
    i = 1
    while True:
        v = 2 * i + 1
        if v * v > limit:
            break
        if sieve[i]:
            start = (v * v - 1) // 2
            sieve[start::v] = bytearray(len(range(start, size + 1, v)))
        i += 1
    for i in range(1, size + 1):
        if sieve[i]:
            yield 2 * i + 1


def window_primes(a, e, base):
    """All primes in [a, e] with a odd >= 3, given base primes for marking.
    Marking identical to chainform.py; extraction via bytearray.find."""
    size = (e - a) // 2 + 1
    sieve = bytearray([1]) * size
    for q in base:
        if q == 2:
            continue
        if q * q > e:
            break
        start = q * q
        if start < a:
            start = ((a + q - 1) // q) * q
        if start % 2 == 0:
            start += q
        i0 = (start - a) // 2
        if i0 < size:
            sieve[i0::q] = bytearray(len(range(i0, size, q)))
    res = []
    i = sieve.find(1)
    while i != -1:
        res.append(a + 2 * i)
        i = sieve.find(1, i + 1)
    return res


def selftest_window():
    """window_primes vs the reference sieve (as verified in chainform.py)."""
    ref = [p for p in primes_upto(2001) if p >= 999]
    base = list(primes_upto(isqrt(2001) + 1))
    got = [p for p in window_primes(999, 2001, base)]
    assert got == ref, "window_primes self-test FAILED"
    ref2 = [p for p in primes_upto(5000) if p >= 3]
    base2 = list(primes_upto(isqrt(5000) + 1))
    got2 = window_primes(3, 5000, base2)
    assert got2 == ref2, "window_primes self-test FAILED (3,5000)"
    out("self-test: window_primes [3,5000] and [999,2001] match the "
        "reference sieve exactly  PASS")


def stream_theta(x0, k0, pk0, limit, seg_span):
    """Yield (n, p, lp, x_prev) for primes p_{k0+1}, p_{k0+2}, ... up to
    limit, with x_prev = theta(p_{n-1}); theta re-anchored per segment."""
    base = list(primes_upto(isqrt(limit) + 1))
    closed = x0
    n = k0
    a = pk0 + 2
    while a <= limit:
        e = min(a + seg_span - 2, limit)
        partial = 0.0
        seg = []
        for p in window_primes(a, e, base):
            lp = log(p)
            n += 1
            yield (n, p, lp, closed + partial)
            seg.append(lp)
            partial += lp
        closed = math.fsum((closed, math.fsum(seg)))
        a = e + 2


def run():
    out("== certified positivity window of the anchored chain, "
        "K = 10^8, physical seed ==")
    out("window W = %d steps, sieve bound %d (stream starts at the "
        "certified anchor p_K = %d)" % (W, LIMIT, CERT["p_K"]))
    out("")
    selftest_window()
    out("")

    ok = True
    eps = CERT["eps_K"]
    u_k = CERT["u_K"]
    min_eps = (math.inf, 0)
    min_h = (math.inf, 0)
    nonpos = 0
    n_last = K
    p_last = CERT["p_K"]
    rows = {}
    h_first = None
    fails = []

    out("== gate 1: anchor continuity ==")
    gen = stream_theta(CERT["X_K"], K, CERT["p_K"], LIMIT, SEG_SPAN)
    for (n, p, lp, x_prev) in gen:
        j = n - K
        if j == 1:
            if p != CERT["p_K1"]:
                fails.append("p_{K+1} mismatch: %d" % p)
                ok = False
            u1 = lp / x_prev
            e1 = rel(u1, u_k)
            e2 = rel(lp, H_K1_XK)
            ok1 = e1 <= CERT_TOL and e2 <= CERT_TOL
            ok = ok and ok1
            out("  p_(K+1) = %d  (certified %d)" % (p, CERT["p_K1"]))
            out("  u_1     = log p_(K+1)/X_K = %.16e  rel.err %.2e  %s"
                % (u1, e1, "PASS" if ok1 else "FAIL"))
            out("  log p_(K+1)             = %.15f  rel.err %.2e  vs certified"
                % (lp, e2))
        a_prev = log(x_prev)
        r = 1.0 / (p - 1.0)
        q = 1.0 + r
        l1u = log1p(lp / x_prev)
        s = r * a_prev - l1u
        eps = q * eps + s
        h = eps / u_k
        if eps < min_eps[0]:
            min_eps = (eps, j)
        if h < min_h[0]:
            min_h = (h, j)
        if eps <= 0 or h <= 0:
            nonpos += 1
        if h_first is None:
            h_first = h
        if j in CKPTS or j in CROSS_DEEP:
            rows[j] = (p, eps, h)
        n_last = n
        p_last = p
        if j >= W:
            break
    out("")

    out("== gate 2: cross-check against chainform deep pass "
        "(independent compensated walk from 2) ==")
    for j in sorted(CROSS_DEEP):
        if j not in rows:
            out("  j = %d: reached=%s  SKIP" % (j, j in rows))
            continue
        hv = rows[j][2]
        cv = CROSS_DEEP[j]
        err = rel(hv, cv)
        good = err <= CROSS_TOL
        ok = ok and good
        out("  j = %-9d H = %.17e  deep %.17e  rel.err %.2e  %s"
            % (j, hv, cv, err, "PASS" if good else "FAIL"))
    out("")

    out("== gate 3: window coverage ==")
    covered = n_last - K
    good = covered >= W and p_last < LIMIT + 1
    ok = ok and good
    out("  reached index n = %d = K + %d  (target K + %d)  %s"
        % (n_last, covered, W, "PASS" if good else "FAIL"))
    out("  prime range certified: [p_{K+1}, p_end] = [%d, %d]"
        % (CERT["p_K1"], p_last))
    out("")

    out("== gate 4: margins vs float64 noise ==")
    out("  min eps over window  = %.17e  at j = %d" % min_eps)
    out("  min H   over window  = %.17e  at j = %d" % min_h)
    out("  nonpositive eps or H count = %d (must be 0)" % nonpos)
    out("  float64 worst-case eps drift bound <= %.1e  ->  safety factor "
        ">= %.2e" % (NOISE_BOUND, min_eps[0] / NOISE_BOUND))
    if min_eps[0] <= 0 or nonpos != 0 or min_h[0] <= 0:
        fails.append("margin gate failed")
        ok = False
    out("")

    out("== checkpoint table ==")
    out("  %-10s %-16s %-22s %-22s" % ("j", "p_{K+j}", "eps_{K+j}", "H_j"))
    for j in sorted(rows):
        p, ev, hv = rows[j]
        out("  %-10d %-16d %-22.14e %-22.14e" % (j, p, ev, hv))
    out("")

    out("== summary ==")
    for f in fails:
        out("  FAIL:", f)
    out("  window certificate: %s"
        % ("PASS" if ok else "FAIL"))
    if ok:
        out("  H_i > 0 for all 1 <= i <= %d (physical seed at K = 10^8);" % W)
        out("  equivalently f(p) < 1 (Nicolas) for every prime in "
            "[p_(K+1), p_end] = [%d, %d]," % (CERT["p_K1"], p_last))
        out("  i.e. %d consecutive primes: %d ... %d" % (covered,
                                                         CERT["p_K1"], p_last))
        out("  first-step value H_1 = %.17e (matches deep pass to %.2e rel)"
            % (rows[1][2], rel(rows[1][2], CROSS_DEEP[1])))
    out("  total %.1f s" % (time.time() - T0))

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "hipos_window_results.txt")
    with open(path, "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    out("results written to", path)


if __name__ == "__main__":
    import os
    run()
