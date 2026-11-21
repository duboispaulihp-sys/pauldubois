#!/usr/bin/env python3
"""
deep_live.py -- Phase 8: the deep-rung live campaign.  All 30 still-SKIP
document claims live(k, 35), k = 36..65, are recomputed EXACTLY by Route C
(the norm / Hall-Gram formula, norm_route.py):

    live_q(k,n,4) = || [t^k] (1 + h_1 t + ... + h_4 t^4)^n ||^2

and compared digit-for-digit with the document claims extracted in
claims.json (misc entries, kind "live").

Also handled honestly:
  * live(119,33), live(123,34), live(127,35), live(134,37), live(140,35),
    live(146,40) (the k >= 119 quintet/sextet): still out of reach -- the
    Route C state space is bounded by sum_{r<=k} p(r) ~ e^{pi sqrt(2k/3)}/(4k sqrt 3),
    which is ~10^8 at k = 119 and already beyond budget here; we print the
    Hardy-Ramanujan cost model line for the record.
  * the anomaly register: claims whose "value" is a small integer (167 at
    (134,37), 146 at (140,35)) are recorded AS CLAIMED; exact comparison
    decides each on its own terms.

Provenance self-check inside: routeC(20,35,4) must equal the Phase-7
Route B value of the difflive claim (44 digits, 1780 s there; 0.12 s here).

Writes deep_live.txt; final line: "end of deep_live".
"""
import json
import time

import norm_route as NR

OUT = open("deep_live.txt", "w")


def say(m=""):
    print(m)
    OUT.write(m + "\n")
    OUT.flush()


def main():
    t00 = time.time()
    say("== Phase 8: deep-rung live campaign via Route C (norm formula) ==")

    # provenance self-check
    from json import load
    claims = load(open("claims.json"))
    difflive = {e["k"]: e["live"] for e in claims["difflive"] if e["k"] == 20}
    v20 = NR.routeC(20, 35, 4)
    assert v20.denominator == 1
    ok20 = int(v20) == difflive[20]
    say(f"provenance: routeC(20,35,4) == Route B difflive value: "
        f"{'OK' if ok20 else 'FAIL'}  ({str(v20)[:20]}..., 44 digits)")

    # gather the 30 claims k = 36..65 at n = 35
    seen = {}
    for e in claims["misc"]:
        if e.get("kind") == "live" and 36 <= e["k"] <= 65 and e["n"] == 35:
            seen.setdefault(e["k"], set()).add(e["val"])
    keys = sorted(seen)
    say(f"claims loaded: {len(keys)} distinct k values "
        f"({keys[0]}..{keys[-1]} at n=35)")

    say("")
    say("| k | n | digits(claim) | digits(Route C) | verdict | time |")
    say("|----|----|----|----|----|----|")
    n_match = n_miss = 0
    for k in keys:
        (n,) = {e["n"] for e in claims["misc"]
                if e.get("kind") == "live" and e["k"] == k}
        vals = seen[k]
        t0 = time.time()
        v = NR.routeC(k, n, 4)
        assert v.denominator == 1
        v = int(v)
        dt = time.time() - t0
        if len(vals) == 1 and v in vals:
            verdict = "EXACT MATCH"
            n_match += 1
        else:
            verdict = "MISMATCH vs claim"
            n_miss += 1
        say(f"| {k} | {n} | {len(str(list(vals)[0]))} | {len(str(v))} | "
            f"{verdict} | {dt:.1f}s |")

    say("")
    say(f"deep rungs k=36..65 at n=35: {n_match} EXACT, {n_miss} MISMATCH "
        f"[{time.time()-t00:.1f}s total]")

    # the unreachable quintet/sextet, with cost model for the record
    # (state bound = sum_{r<=k} p(r), computed exactly by Euler's recurrence)
    K = 150
    p = [0] * (K + 1)
    p[0] = 1
    for m in range(1, K + 1):
        s = 0
        g = 1
        while True:
            g1 = g * (3 * g - 1) // 2
            g2 = g * (3 * g + 1) // 2
            if g1 > m and g2 > m:
                break
            sign = 1 if g % 2 else -1
            if g1 <= m:
                s += sign * p[m - g1]
            if g2 <= m:
                s += sign * p[m - g2]
            g += 1
        p[m] = s
    pool65 = sum(p[:66])
    pool119 = sum(p[:120])
    say("")
    say("still out of reach (Route C state bound = sum_{r<=k} p(r), exact):")
    say("  live(119,33), live(123,34), live(127,35), live(134,37),")
    say("  live(140,35), live(146,40) --")
    say(f"  pool at k=65 : sum_(r<=65) p(r) = {pool65:,}  (measured: k=65,35 -> 10.4 s, RSS 0.05 GB)")
    say(f"  pool at k=119: sum_(r<=119) p(r) = {pool119:,}  p(119) = {p[119]:,};")
    say(f"  ratio ~ {pool119/pool65:.0f}x states, i.e. hundreds of GB of dictionary --")
    say("  out of reach on this machine; needs ~1000x state-space reduction or")
    say("  a closed form for [t^k] P_4(t)^n at n ~ k/4 fixed, q = 4.")
    say("")
    say("end of deep_live")
    OUT.close()
    print(f"total {time.time()-t00:.1f}s")


if __name__ == "__main__":
    main()
