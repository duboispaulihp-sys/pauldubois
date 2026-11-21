#!/usr/bin/env python3
"""j2_worker.py -- one slice of the b-vector mu-loop, for rung k (4-way).

Usage: python3 j2_worker.py K I     (I in 0..3)
Writes partial_b_K_I.json -- values stored as hex strings for JSON safety.
Assembled by j2_parent.py, which performs the certifications and appends
the row to j2_diagonal.txt.
"""
import json
import sys

import capq_engine as E
# imports the FUNCTIONAL pieces of j2_diagonal WITHOUT its OUT file (guarded)
import j2_diagonal as J


def main():
    k = int(sys.argv[1])
    i = int(sys.argv[2])
    Wn = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    n = k
    mus = list(E.partitions(k, 4))
    lo = i * len(mus) // Wn
    hi = (i + 1) * len(mus) // Wn
    bvec = {}
    for idx in range(lo, hi):
        mu = tuple(mus[idx])
        if len(mu) > n:
            continue
        cm = E.C_mu(n, mu)
        if cm == 0:
            continue
        for sigma, kk in J.h_exp(mu).items():
            bvec[sigma] = bvec.get(sigma, 0) + cm * kk
    out = {
        "k": k, "i": i, "lo": lo, "hi": hi,
        "entries": [[list(sig), format(v, "x")] for sig, v in bvec.items()],
    }
    with open(f"partial_b_{k}_{i}.json", "w") as f:
        json.dump(out, f)
    print(f"worker k={k} i={i}: mus [{lo},{hi}), {len(bvec)} shapes, done")


if __name__ == "__main__":
    main()
