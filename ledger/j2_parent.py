#!/usr/bin/env python3
"""j2_parent.py -- assemble rung k from the four worker partials; run the
full certification set and append the row to j2_diagonal.txt (Note-H/Note-I
format, identical to j2_diagonal.py).  Usage: python3 j2_parent.py K."""
from fractions import Fraction as Frc
from math import factorial
from decimal import Decimal, getcontext
import json, sys, time

import capq_engine as E
import norm_route as NR
import j2_diagonal as J

OUT = open("j2_diagonal.txt", "a")


def say(m=""):
    print(m, flush=True)
    OUT.write(m + "\n")
    OUT.flush()


def fshow(x, d=4):
    return f"{float(x):.{d}f}"


def cens_from_partials(k):
    t0 = time.time()
    n = k
    live = NR.routeC(k, n, 4)
    assert live.denominator == 1
    live = int(live)
    ledger = E.ledger_q(k, n, 4)
    P = live - ledger

    bvec = {}
    for i in range(4):
        d = json.load(open(f"partial_b_{k}_{i}.json"))
        assert d["k"] == k and d["i"] == i
        for sig, hv in d["entries"]:
            sig = tuple(sig)
            v = int(hv, 16)
            bvec[sig] = bvec.get(sig, 0) + v

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
    say(f"| {k} | {n} | {len(str(P))} | {fshow(D)} | {cos:.4f} | {n*err:.3f} |"
        f"   ({time.time()-t0:.1f}s)  certs {''.join('T' if c else 'F' for c in (cert_a, cert_b, cert_c, cert_d))}  [4-way]")
    return all((cert_a, cert_b, cert_c, cert_d))


if __name__ == "__main__":
    ok = True
    for k in [int(a) for a in sys.argv[1:]] or [38]:
        ok &= cens_from_partials(k)
    print("rung certified:", "PASS" if ok else "FAIL")
    OUT.close()
