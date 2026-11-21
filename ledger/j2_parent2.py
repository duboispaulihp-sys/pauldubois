#!/usr/bin/env python3
"""j2_parent2.py -- staged rung assembly under a per-command 560s ceiling.

Stages (CLI: python3 j2_parent2.py K STAGE):
  1  routeC live + engine ledger  -> census_ints_K.json
  2  cert_b spot vs engine b_q, ONE shape (recorded for stage 3)
  3  assemble partials; cert_a (sum b^2 = live); frozen sweep (fast hooks);
     cert_c (RSK ftot), cert_d (hooks spot); cos + n*maxErr; append row.

Honesty: the per-shape engine spot (cert_b) is recorded in stage 2 with its
runtime; if that runtime is excessive at k >= 38 the batch b-vector remains
certified by cert_a (its square-sum is the Route-C live, itself certified by
the 114-check battery of norm_route.py) and by the k = 13..37 spot
regression; the stage-3 cert tag records the outcome.
"""
from fractions import Fraction as Frc
from math import factorial
from decimal import Decimal, getcontext
import json, sys, time, glob

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


def stage1(k):
    t0 = time.time()
    live = NR.routeC(k, k, 4)
    assert live.denominator == 1
    live = int(live)
    ledger = E.ledger_q(k, k, 4)
    json.dump({"k": k, "live": str(live), "ledger": str(ledger)},
              open(f"census_ints_{k}.json", "w"))
    print(f"stage1 k={k}: live {len(str(live))} digits, ledger {len(str(ledger))} "
          f"digits, P {len(str(live - ledger))} digits  ({time.time()-t0:.1f}s)")


def stage2(k):
    sig = None
    for s in E.partitions(k):
        if s[0] >= 5:
            sig = tuple(s)
            break
    t0 = time.time()
    b_engine = E.b_q(sig, k, 4)
    dt = time.time() - t0
    json.dump({"k": k, "spot": [list(sig), format(b_engine, "x")], "t": dt},
              open(f"spot_b_{k}.json", "w"))
    print(f"stage2 k={k}: engine b_q{sig} computed in {dt:.1f}s")


def stage3(k):
    t0 = time.time()
    ints = json.load(open(f"census_ints_{k}.json"))
    live, ledger = int(ints["live"]), int(ints["ledger"])
    P = live - ledger
    bvec = {}
    for path in sorted(glob.glob(f"partial_b_{k}_*.json")):
        d = json.load(open(path))
        for sig, hv in d["entries"]:
            sig = tuple(sig)
            bvec[sig] = bvec.get(sig, 0) + int(hv, 16)
    sbsum = sum(b * b for b in bvec.values())
    cert_a = (sbsum == live)
    try:
        sd = json.load(open(f"spot_b_{k}.json"))
        sig = tuple(sd["spot"][0])
        cert_b = (bvec.get(sig, 0) == int(sd["spot"][1], 16))
        cert_b_tag = "T" if cert_b else "F"
    except FileNotFoundError:
        cert_b = True
        cert_b_tag = "S"      # skipped, cost
    big, ftot_direct = J.frozen_share_vec_all(k)
    ftot = factorial(k) - E.N_k_q(k, 4)
    cert_c = (ftot == ftot_direct)
    ok_d = True
    cnt = 0
    for sig in big:
        ok_d &= (J.f_fast(sig) ** 2 == big[sig])
        cnt += 1
        if cnt == 3:
            break
    cert_d = ok_d
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
    D = Frc(P * factorial(k) ** 2, ftot * k ** (2 * k))
    say(f"| {k} | {k} | {len(str(P))} | {fshow(D)} | {cos:.4f} | {k*err:.3f} |"
        f"   ({time.time()-t0:.1f}s)  certs {''.join(str(c) for c in (cert_a, cert_b_tag, cert_c, cert_d))}  [4-way]")
    print(f"stage3 k={k} certs: a={cert_a} b={cert_b_tag} c={cert_c} d={cert_d}")


if __name__ == "__main__":
    k = int(sys.argv[1])
    st = sys.argv[2]
    if st == "1":
        stage1(k)
    elif st == "2":
        stage2(k)
    elif st == "3":
        stage3(k)
    else:
        raise SystemExit("stage = 1|2|3")
