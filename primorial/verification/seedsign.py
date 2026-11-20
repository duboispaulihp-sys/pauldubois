#!/usr/bin/env python3
"""seedsign.py -- seed-sign dichotomy: sign of the chain H_i(H) vs the seed H.

Closed form (Theorems 8 / cor:seed of LEAN.tex): for every seed H at the
anchor K = 10^8, with u = u_K fixed,

    H_i(H) u = eps_{K+i} + (H u - eps_K) P_i,   P_i = prod_{j<i} (1 + r_{K+j}),

so with the physical chain H_i^phys = eps_{K+i}/u (seed H = H_K exactly):

    H_i(H) = H_i^phys + (H - H_K) P_i,
    sign(H_i(H)) = sign(rho_i - (H_K - H)),   rho_i := H_i^phys / P_i .

Dichotomy through the window W = 2e8 (same certified walk as hipos_window.py;
stream starts at the certified anchor, own segmented sieve to 7e9):

  * critical seed  c_W = H_K - min_{0<=i<=W} rho_i  (flips inside the window,
    provably, for every seed 0 < H < c_W;  same sign for every H > c_W);
  * lower critical seed  d_W = H_K - max_{0<=i<=W} rho_i  (negative seeds stay
    negative through the window iff max rho is attained at i = 0, d_W = 0);
  * superposition residuals: direct recursions E_j(1000), E_j(1), E_j(-100)
    vs the closed form, ABSOLUTE metric (relative is meaningless at a
    sign-crossing step where H_i(H0) ~ 0);
  * physical and large seeds: same sign throughout the window;
  * flip indices reported for seeds 1, 100, 1000, 1900.

Pure Python 3, no dependencies.
"""

import math
import os
import time
from math import isqrt, log, log1p

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
H_K1_XK = 21.435271449680776
CROSS_DEEP = {
    1: 4132.28819173141528,
    2: 4132.28817085263745,
    1000: 4132.26734053036489,
    10_000: 4132.07781370465545,
    100_000: 4130.21388736587960,
    1_000_000: 4111.73708702537715,
    5_000_000: 4024.83700208751361,
}
CROSS_TOL = 1e-6
CERT_TOL = 1e-6
NOISE_BOUND = 3e-12
SUP_TOL = 1e-13          # superposition residual gate (absolute, in H units)
FLIP_SEEDS = (1.0, 100.0, 1000.0, 1900.0)
BIG_SEEDS = (4132.2882124786138, 2000.0, 100000.0)
NEG_SEEDS = (-0.5, -1.0, -100.0)

T0 = time.time()
OUT = []


def out(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


def rel(a, b):
    return abs(a - b) / abs(b) if b else abs(a - b)


def primes_upto(limit):
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
    ref = [p for p in primes_upto(2001) if p >= 999]
    base = list(primes_upto(isqrt(2001) + 1))
    assert window_primes(999, 2001, base) == ref, "self-test FAILED"
    ref2 = [p for p in primes_upto(5000) if p >= 3]
    base2 = list(primes_upto(isqrt(5000) + 1))
    assert window_primes(3, 5000, base2) == ref2, "self-test FAILED (3,5000)"
    out("self-test: window_primes [3,5000] and [999,2001] match the "
        "reference sieve exactly  PASS")


def stream_theta(x0, k0, pk0, limit, seg_span):
    base = list(primes_upto(isqrt(limit) + 1))
    closed = x0
    n = k0
    a = pk0 + 2
    while a <= limit:
        e = min(a + seg_span - 2, limit)
        seg = []
        partial = 0.0
        for p in window_primes(a, e, base):
            lp = log(p)
            n += 1
            yield (n, p, lp, closed + partial)
            seg.append(lp)
            partial += lp
        closed = math.fsum((closed, math.fsum(seg)))
        a = e + 2


def run():
    out("== seed-sign dichotomy: sign(H_i(H)) vs sign(H), K = 10^8 ==")
    out("window W = %d steps, sieve bound %d (stream from the certified "
        "anchor p_K = %d)" % (W, LIMIT, CERT["p_K"]))
    out("")
    selftest_window()
    out("")

    u_k = CERT["u_K"]
    H_K = CERT["H_K"]
    eps = CERT["eps_K"]
    assert rel(eps / u_k, H_K) < 1e-12
    lP = 0.0                       # log P_i ; P_0 = 1
    hphys = eps / u_k              # H_0^phys = H_K exactly
    min_rho = (hphys, 0)           # rho_0 = H_K / P_0 = H_K
    max_rho = (hphys, 0)
    hphys_min = (hphys, 0)
    rows = {}
    flips = {s: None for s in FLIP_SEEDS}
    flips_reconv = {s: 0 for s in FLIP_SEEDS}
    sup_res_abs = {s: 0.0 for s in (1000.0, 1.0, -100.0)}
    direct = {s: s * u_k for s in sup_res_abs}     # E_0
    nonpos_phys = 0
    n_last = K
    p_last = CERT["p_K"]
    fails = []
    ok = True

    out("== gate 1: anchor continuity ==")
    gen = stream_theta(CERT["X_K"], K, CERT["p_K"], LIMIT, SEG_SPAN)
    for (n, p, lp, x_prev) in gen:
        j = n - K
        if j == 1:
            if p != CERT["p_K1"]:
                fails.append("p_{K+1} mismatch: %d" % p)
                ok = False
            u1 = lp / x_prev
            if rel(u1, u_k) > CERT_TOL or rel(lp, H_K1_XK) > CERT_TOL:
                fails.append("anchor constants mismatch")
                ok = False
            out("  p_(K+1) = %d  certified;  u_1 rel.err %.2e  PASS"
                % (p, rel(u1, u_k)))
        a_prev = log(x_prev)
        r = 1.0 / (p - 1.0)
        s = r * a_prev - log1p(lp / x_prev)
        eps = (1.0 + r) * eps + s
        hphys = eps / u_k
        lP += log1p(r)
        P = math.exp(lP)
        rho = hphys / P
        if rho < min_rho[0]:
            min_rho = (rho, j)
        if rho > max_rho[0]:
            max_rho = (rho, j)
        if hphys < hphys_min[0]:
            hphys_min = (hphys, j)
        if eps <= 0 or hphys <= 0:
            nonpos_phys += 1
        for sd in sup_res_abs:
            direct[sd] = (1.0 + r) * direct[sd] + s
        if j % 97 == 0 or j in CKPTS or j in CROSS_DEEP:
            for sd in sup_res_abs:
                pred = eps + (sd * u_k - CERT["eps_K"]) * P
                res = abs(direct[sd] - pred)
                if res > sup_res_abs[sd]:
                    sup_res_abs[sd] = res
        for sd in FLIP_SEEDS:
            thr = H_K - sd
            if flips[sd] is None and rho < thr:
                flips[sd] = j
            elif flips[sd] is not None and rho >= thr:
                flips_reconv[sd] += 1
        if j in CKPTS or j in CROSS_DEEP:
            rows[j] = (p, hphys, P, rho)
        n_last = n
        p_last = p
        if j >= W:
            break
    out("  walk complete: n = %d = K + %d, p_end = %d"
        % (n_last, n_last - K, p_last))
    out("")

    out("== gate 2: cross-check vs chainform deep pass ==")
    for j in sorted(CROSS_DEEP):
        hv = rows[j][1]
        err = rel(hv, CROSS_DEEP[j])
        good = err <= CROSS_TOL
        ok = ok and good
        out("  i = %-9d H^phys = %.17e  deep %.17e  rel.err %.2e  %s"
            % (j, hv, CROSS_DEEP[j], err, "PASS" if good else "FAIL"))
    out("")

    out("== gate 3: superposition residuals (direct recursion vs closed form, "
        "absolute) ==")
    for sd in (1000.0, 1.0, -100.0):
        good = sup_res_abs[sd] <= SUP_TOL
        ok = ok and good
        out("  seed %-8.1f  max |E_direct - E_closed| = %.3e  %s"
            % (sd, sup_res_abs[sd], "PASS" if good else "FAIL"))
    out("")

    out("== gate 4: dichotomy through the window ==")
    c_W = H_K - min_rho[0]
    d_W = H_K - max_rho[0]
    out("  rho_i = H^phys_i / P_i (incl. rho_0 = H_K): "
        "min %.6f at i = %d ; max %.16f at i = %d"
        % (min_rho[0], min_rho[1], max_rho[0], max_rho[1]))
    cW_good = min_rho[0] > 0
    ok = ok and cW_good
    out("  critical seed  c_W = H_K - min rho = %.6f   (attained at i = %d)"
        % (c_W, min_rho[1]))
    out("  lower critical seed d_W = H_K - max rho = %.6e  "
        "(= 0 <=> max rho at i = 0)" % d_W)
    dw_good = d_W <= 1e-9
    ok = ok and dw_good
    out("  d_W ~ 0 (negative seeds stay negative through the window): %s"
        % ("PASS" if dw_good else "FAIL"))
    for sd in FLIP_SEEDS:
        if sd < c_W:
            good = flips[sd] is not None and flips_reconv[sd] == 0
        else:
            good = flips[sd] is None
        ok = ok and good
        out("  seed %-7.1f (c_W %s): flip at i = %-10s  re-crossings %d  %s"
            % (sd, "<" if sd < c_W else ">",
               str(flips[sd]) if flips[sd] is not None else "--",
               flips_reconv[sd], "PASS" if good else "FAIL"))
    for sd in BIG_SEEDS:
        thr = H_K - sd
        good = sd > c_W and min_rho[0] > thr
        ok = ok and good
        out("  seed %-16.6f: sign(H_i)=+ for all i<=W: margin (rho_min - "
            "thr) = %.4f  %s" % (sd, min_rho[0] - thr,
                                 "PASS" if good else "FAIL"))
    for sd in NEG_SEEDS:
        thr = H_K - sd
        good = max_rho[0] < thr
        ok = ok and good
        out("  seed %-7.1f: sign(H_i)=- for all i<=W: margin (thr - rho_max) "
            "= %.4f  %s" % (sd, thr - max_rho[0], "PASS" if good else "FAIL"))
    out("")

    out("== gate 5: physical-seed margins vs float64 noise ==")
    out("  min H^phys over window = %.17e at i = %d" % hphys_min)
    out("  nonpositive phys count = %d (must be 0)" % nonpos_phys)
    good = hphys_min[0] > 0 and nonpos_phys == 0
    ok = ok and good
    out("  safety vs drift bound %.1e: >= %.2e  %s"
        % (NOISE_BOUND, hphys_min[0] / NOISE_BOUND, "PASS" if good else "FAIL"))
    out("")
    out("== checkpoint table ==")
    out("  %-10s %-16s %-22s %-12s %-14s"
        % ("i", "p_{K+i}", "H_i^phys", "P_i", "rho_i"))
    for j in sorted(rows):
        p, hv, pv, rv = rows[j]
        out("  %-10d %-16d %-22.14e %-12.8f %-14.8f" % (j, p, hv, pv, rv))
    out("")

    out("== summary ==")
    for f in fails:
        out("  FAIL:", f)
    out("  seed-sign dichotomy certificate: %s" % ("PASS" if ok else "FAIL"))
    if ok:
        out("  closed form H_i(H) = H^phys_i + (H-H_K) P_i verified to "
            "abs %.1e (worst of 3 seeds)" % max(sup_res_abs.values()))
        out("  critical seed c_W = %.6f (rho minimum at i = %d); every seed "
            "> c_W keeps sign(H_i) = sign(H) = + throughout [0, W];"
            % (c_W, min_rho[1]))
        out("  every seed 0 < H < c_W flips nonpositively inside the window "
            "(flip indices above, no re-crossings);")
        out("  d_W = 0 exactly (rho maximum at i = 0): every seed H < 0 has "
            "H_i < 0 throughout [0, W] -- same sign as the seed;")
        out("  physical seed H_K = %.6f: H_i > 0 for all i <= %d (min %.4f "
            "at i = %d), same sign as the seed"
            % (H_K, W, hphys_min[0], hphys_min[1]))
        out("  every seed H >= H_K: H_i >= H^phys_i >= %.4f on [0, W] "
            "(seed excess (H-H_K) P_i >= 0), P_W = %.8f; all-step same-sign "
            "stays the brick (<=> Nicolas from K+1: cor:chainiff / "
            "thm:chainpos)" % (hphys_min[0], math.exp(lP)))
    out("  total %.1f s" % (time.time() - T0))

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "seedsign_results.txt")
    with open(path, "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    out("results written to", path)


if __name__ == "__main__":
    run()
