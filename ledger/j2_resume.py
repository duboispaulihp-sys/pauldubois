#!/usr/bin/env python3
"""
j2_resume.py -- Phase 8 addendum: resume the J.2 diagonal at k = 38..40
(the background run was reaped by the sandbox at the k = 38 rung; rows
k = 13..37 are already recorded in j2_diagonal.txt and were NOT recomputed).

Speedup: the batched b-vector splits the mu-loop across W worker processes
(each with its own h_exp memo); the parent merges, then runs the same
certifications and the same cos / n*maxErr machinery as j2_diagonal.py
(frozen vector by fast hooks; ftot by RSK identity verified against the
direct sum; live by Route C; ledger by the engine).

Rows are APPENDED to j2_diagonal.txt in the identical Note-H/Note-I format,
so the table k = 13..40 is continuous.
"""
from fractions import Fraction as Frc
from math import factorial
from decimal import Decimal, getcontext
from functools import lru_cache
from multiprocessing import Pool
import sys, time

import capq_engine as E
import norm_route as NR
import j2_diagonal as J          # reuse h_exp/f_fast/certs (module-level caches OK)

W = 4
OUT = open("j2_diagonal.txt", "a")


def say(m=""):
    print(m, flush=True)
    OUT.write(m + "\n")
    OUT.flush()


def worker_mu_slice(job):
    """partial b-vector for a slice of the mu rectangle."""
    k, n, q, lo, hi = job
    mus = list(E.partitions(k, q))
    # stable order; slice by index
    bvec = {}
    for idx in range(lo, min(hi, len(mus))):
        mu = tuple(mus[idx])
        if len(mu) > n:
            continue
        cm = E.C_mu(n, mu)
        if cm == 0:
            continue
        for sigma, kk in J.h_exp(mu).items():
            bvec[sigma] = bvec.get(sigma, 0) + cm * kk
    return bvec


def cens_resumed(k):
    t0 = time.time()
    n = k
    live = NR.routeC(k, n, 4)
    assert live.denominator == 1
    live = int(live)
    ledger = E.ledger_q(k, n, 4)
    P = live - ledger

    mus = list(E.partitions(k, 4))
    chunks = [(k, n, 4, i * len(mus) // W, (i + 1) * len(mus) // W) for i in range(W)]
    with Pool(W) as pool:
        parts = pool.map(worker_mu_slice, chunks)
    bvec = {}
    for d in parts:
        for s, v in d.items():
            bvec[s] = bvec.get(s, 0) + v

    sbsum = sum(b * b for b in bvec.values())
    cert_a = (sbsum == live)
    spots = []
    for sig in E.partitions(k):
        if sig[0] >= 5:
            spots.append(sig)
            if len(spots) == 3:
                break
    cert_b = all(E.b_q(sig, n, 4) == bvec.get(sig, 0) for sig in spots)
    big, ftot_direct = J.frozen_share_vec_all(k)
    ftot = factorial(k) - E.N_k_q(k, 4)
    cert_c = (ftot == ftot_direct)
    cert_d = all(J.f_fast(s) == E.f_syt(s) for s in spots)

    num = 0
    sb, sf = 0, 0
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
    say(f"| {k} | {n} | {len(str(P))} | {J.fshow(D)} | {cos:.4f} | {n*err:.3f} |"
        f"   ({time.time()-t0:.1f}s)  certs {''.join('T' if c else 'F' for c in (cert_a, cert_b, cert_c, cert_d))}  [W={W}]")
    return all((cert_a, cert_b, cert_c, cert_d))


if __name__ == "__main__":
    ok = True
    for k in [int(a) for a in sys.argv[1:]] or [38, 39, 40]:
        ok &= cens_resumed(k)
    say(f"resumed rungs certified: {'PASS' if ok else 'FAIL'}")
    say("end of j2_resume")
    OUT.close()
