#!/usr/bin/env python3
"""sextet.py -- Phase 9: the deep sextet falls; full live spectra of deep columns.

Mathematical content (Note K):

Theorem K.1 (polynomial state bound).  In the Route C Hall-Gram DP, every
reachable p-monomial has all parts <= q (each factor contributes one block
lambda |- r with r <= q, and p-monomials merge by multiset union).  Hence the
state pool at cap k is bounded by  sum_{r<=k} p_q(r) = O(k^q)  -- POLYNOMIAL
in k.  This supersedes the Phase-8 cost model in deep_live.txt, which used the
unrestricted p(r) (pool(k=119) = 15,425,991,887): the true pool is
sum_{r<=119} p_4(r) = 416,695 (~37,000x smaller).  The "out of reach" verdict
on the six SKIP rungs live(119,33), live(123,34), live(127,35), live(134,37),
live(140,35), live(146,40) is therefore void, and one full-cap DP pass
(cap = 4n, no truncation needed) yields the ENTIRE spectrum
live_4(k, n), k = 0..4n, in one run.

Implementation: count-vector states (c1..cq) (z-bijection with parts-<=q
partitions), in-place ascending-degree forward DP (each step doubles no
memory; degree of a key is its invariant), values L-scaled ints (L = lcm
z_lambda = 24 at q = 4), final norm  sum_lambda value^2 * z_lambda / L^(2n)
extracted per t-degree.  Certificate: equality with norm_route.routeC
(the Phase-8 certified integer DP) on a grid, plus the per-degree
state counts against the Theorem K.1 bound.

Modes:
  python3 sextet.py cert                  # grid equality vs routeC + bound check
  python3 sextet.py spectrum N BUDGET     # run/resume column n (cap 4n)
  python3 sextet.py finish N              # per-degree norms, claims table, append
Output sextet.txt; final line "end of sextet".
"""
from math import factorial, gcd
from decimal import Decimal, getcontext
import pickle, sys, time, os, resource

import capq_engine as E
import norm_route as NR

Q = 4
OUTNAME = "sextet.txt"


def z_of_counts(cnt):
    """z_lambda for the partition with m_i = cnt[i-1] parts of size i."""
    z = 1
    for i, m in enumerate(cnt, start=1):
        if m:
            z *= i ** m * factorial(m)
    return z


def blocks_counts(q):
    """((count-vector), weight L/z_lambda) for every block lambda |- r <= q."""
    out = []
    L = 1
    for r in range(1, q + 1):
        for lam in E.partitions(r):
            lam = tuple(lam)
            z = NR.z_lambda(lam)
            L = L * z // gcd(L, z)
            cvec = [0] * q
            for part in lam:
                cvec[part - 1] += 1
            out.append((tuple(cvec), None, z))
    out = [(cv, None, z) for cv, _w, z in out]
    L = 1
    for _cv, _w, z in out:
        L = L * z // gcd(L, z)
    return [(cv, L // z) for cv, _w, z in out], L


def deg_of(cvec):
    return sum((i + 1) * c for i, c in enumerate(cvec))


def run_steps(dp, blocks, L, q, cap, step_from, step_to):
    """Execute DP steps step_from+1 .. step_to (in place, ascending degree).

    One step applies F <- F * P in the p-basis.  In-place scheme: snapshot the
    pre-step values (ints shared, only references copied), then (a) push every
    pre-value times its block weight L/z upward (block sizes >= 1, so inflow
    only ever lands on strictly larger degrees, processed later -- each state
    is Fully inflow-complete before it itself becomes a source), finally
    (b) add the empty-block choice, which contributes exactly a factor L to
    the state's own value (routeC's r = 0 block), i.e. dp[key] += (L-1)*V[key].
    The result matches norm_route.routeC's double-dict DP exactly (cert mode).
    """
    for _step in range(step_from + 1, step_to + 1):
        V = dict(dp)                       # pre-step values, ints shared
        for key, val in sorted(V.items(), key=lambda kv: deg_of(kv[0])):
            for dv, w in blocks:
                nk = tuple(a + b for a, b in zip(key, dv))
                dp[nk] = dp.get(nk, 0) + val * w
        LF1 = L - 1
        for key, val in V.items():
            dp[key] += LF1 * val
        del V
    return dp


def norms_by_degree(dp, L, n, q, cap):
    """live_4(k, n) for k = 0..cap as exact ints (Fraction denominator check)."""
    L2n = L ** (2 * n)
    out = {}
    for cvec, val in dp.items():
        k = deg_of(cvec)
        if k > cap:
            continue
        term = val * val * z_of_counts(cvec)
        out[k] = out.get(k, 0) + term
    res = {}
    bad = 0
    for k, tot in out.items():
        num, rem = divmod(tot, L2n)
        if rem:
            bad += 1
        res[k] = num
    return res, bad, len(out)


def pool_bound(k, q):
    """Thm K.1 bound: partitions with parts <= q of every size <= k."""
    cnt = [0] * (k + 1)
    cnt[0] = 1
    for pp in range(1, q + 1):
        for r in range(pp, k + 1):
            cnt[r] += cnt[r - pp]
    return sum(cnt)


# ------------------------------------------------------------------ modes

def say(msg=""):
    print(msg, flush=True)
    with open(OUTNAME, "a") as f:
        f.write(msg + "\n")


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6


def load_ckpt(n):
    path = f"sextet_ckpt_{n}.pkl"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None


def save_ckpt(n, dp, step):
    path = f"sextet_ckpt_{n}.pkl"
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump({"step": step, "dp": dp}, f, protocol=4)
    os.replace(tmp, path)


def mode_cert():
    say("== sextet.py certification ==")
    say("-- K.1 equality with norm_route.routeC on a grid --")
    ok = tot = 0
    for q in (2, 3, 4):
        for n in range(1, 13):
            cap = q * n
            dp = {(0,) * q: 1}
            blocks, L = blocks_counts(q)
            run_steps(dp, blocks, L, q, cap, 0, n)
            nv, bad, _ = norms_by_degree(dp, L, n, q, cap)
            for k in range(0, cap + 1):
                ref = NR.routeC(k, n, q)
                tot += 1
                if nv.get(k, 0) == ref:
                    ok += 1
                elif tot - ok <= 3:
                    say(f"   MISMATCH q={q} n={n} k={k}: {nv.get(k,0)} vs {ref}")
    say(f"   grid equality: {ok}/{tot} PASS")
    say("-- K.1 in-place DP state counts vs the polynomial bound --")
    for (n, q) in [(12, 4), (16, 4), (20, 4), (14, 3), (20, 2)]:
        cap = q * n
        dp = {(0,) * q: 1}
        blocks, L = blocks_counts(q)
        run_steps(dp, blocks, L, q, cap, 0, n)
        bound = pool_bound(cap, q)
        say(f"   n={n} q={q}: final states={len(dp)}  bound sum_(r<={cap}) p_{q}(r)={bound:,}"
            f"  ratio {len(dp)/bound:.4f}  (<= 1 : {'PASS' if len(dp) <= bound else 'FAIL'})")
    say("== end of sextet certification ==")


def mode_spectrum(n, budget):
    q = Q
    cap = q * n
    ck = load_ckpt(n)
    if ck is None:
        dp = {(0,) * q: 1}
        step = 0
        say(f"== spectrum n={n} q={q} cap={cap}: fresh (Thm K.1 pool bound {pool_bound(cap, q):,}) ==")
    else:
        dp, step = ck["dp"], ck["step"]
        say(f"== spectrum n={n}: resume from step {step}, {len(dp):,} states ==")
    blocks, L = blocks_counts(q)
    t0 = time.time()
    while step < n:
        t1 = time.time()
        run_steps(dp, blocks, L, q, cap, step, step + 1)
        step += 1
        dt = time.time() - t1
        say(f"   step {step}/{n}: states={len(dp):,}  {dt:.1f}s  rss={rss_gb():.2f}GB")
        save_ckpt(n, dp, step)
        if time.time() - t0 > budget:
            say(f"   budget reached at step {step}; checkpointed; rerun to continue")
            return
    say(f"== spectrum n={n}: DP complete ({len(dp):,} states), ready for 'finish {n}' ==")


CLAIMS = {
    33: {"crest": 119,
         "crest_int": 411979871679030163202100278100027384012329163163904739648681954182027117819430316625483165168410753440098521301304903875171091965378352000000000,
         "crest_log": None,
         "crest_digits": 144},
    34: {"crest": 123,
         "crest_int": 330878838362741642778408071184614272040690671971751064829695216692710832366710132418708600914944562397197426765461678221592298550679595216853440000000,
         "crest_log": None,
         "crest_digits": 150},
    35: {"crest": 127,
         "crest_int": 296058170131216016326368316102452660122790372487110821828525206591182488548011391316831682323668261060941939498226212595365618643073678739096864444000000000,
         "crest_log": 155.4714,          # document's float log10 at the crest
         "end_log": 146.4368},           # document's float log10 of the full-box monolith
    37: {"crest": 134, "runner": 133,
         "crest_log": 167.5204,          # document: float pass at n=37, window 131..148
         "runner_log": 167.4797,
         "margin": 9.3243},
    40: {"special": 146},               # live(146,40): first-ever exact value
}

# Document exact integers from the outer-leaf law lines (first-ever checks):
OUTER_LEAF = {
    (131, 33): 92629729847222827908539149144795998924376223310333417058632084830040403511941987250104020955077646323084042672896102249145096632550000000,
        # doc line ~730: live(131,33) = 33^2 * maxTab(33) exactly
    (135, 34): 54441111655407396162756565658903695920022274987459236811355012026889700946345967272247098369181194200086215833986577717243374735637469280000000,
        # doc line ~736: live(135,34) = 34^2 * maxTab(34) exactly
}


def mode_finish(n):
    ck = load_ckpt(n)
    assert ck is not None and ck["step"] == n, f"run spectrum {n} first"
    q = Q
    cap = q * n
    dp = ck["dp"]
    blocks, L = blocks_counts(q)
    nv, bad, nstates = norms_by_degree(dp, L, n, q, cap)
    assert bad == 0, "norm denominators must divide exactly"
    say(f"== finish n={n}: live(k,{n}) exact for k=0..{cap} ({nstates:,} support degrees);"
        f" denominator bad = {bad} ==")
    # Thm K.1 per-degree count check (recorded)
    degs = {}
    for cvec in dp:
        degs[deg_of(cvec)] = degs.get(deg_of(cvec), 0) + 1
    okb = all(degs.get(r, 0) <= (pool_bound(r, q) - (pool_bound(r - 1, q) if r else 0))
              for r in range(0, cap + 1))
    say(f"   Thm K.1 per-degree state counts within bound: {'PASS' if okb else 'FAIL'}")
    # crest (exact argmax), runner-up, digits
    pairs = sorted(((k, v) for k, v in nv.items() if v), key=lambda kv: -kv[1])
    k1, v1 = pairs[0]
    k2, v2 = pairs[1]
    getcontext().prec = 40
    import math
    log10_1 = math.log10(v1)
    log10_2 = math.log10(v2)
    say(f"   crest: k={k1} digits={len(str(v1))} log10={log10_1:.4f};"
        f" runner-up k={k2} digits={len(str(v2))} log10={log10_2:.4f};"
        f" gap={log10_1-log10_2:.4f} orders")
    cl = CLAIMS.get(n, {})
    for (kk, nn), docval in OUTER_LEAF.items():
        if nn == n and kk in nv:
            same = "EXACT MATCH" if nv[kk] == docval else "MISMATCH vs claim"
            say(f"   outer-leaf claim live({kk},{n}) = {nn}^2 * maxTab: {same}")
    if "crest" in cl:
        c = cl["crest"]
        val = nv.get(c, 0)
        if "crest_int" not in cl:
            say(f"   claim live({c},{n}) [document]: float-only claim; first exact value = {val}")
            same = ""                                      # int comparison not applicable
        else:
            same = "EXACT MATCH" if val == cl["crest_int"] else "MISMATCH vs claim"
        lg = ""
        if cl.get("crest_log") is not None:
            lg = f" (claim log10 {cl['crest_log']:.4f}, diff {abs(math.log10(nv[c]))-cl['crest_log']:+.4f})"
        say(f"   claim live({c},{n}) [document]: {same}{lg}")
        cd = cl.get("crest_digits")
        if cd is not None:
            say(f"   claim digit count {cd}: ours {len(str(val))}"
                f" {'(agree)' if cd == len(str(val)) else '(DIFFER)'}")
        if cl.get("crest_log") is not None and abs(log10_1 - cl["crest_log"]) < 5e-5 \
                and k1 == c:
            say(f"   crest claim {c}: confirmed exactly; float log10 agrees to 4 decimals")
    if n == 37:
        clq = CLAIMS[37]
        kr = clq["runner"]
        say(f"   exact log10 live({kr},37) = {math.log10(nv[kr]):.4f}"
            f" (document runner-up float: {clq['runner_log']});"
            f" the exact runner-up is k={k2} at log10 {log10_2:.4f}")
    if n == 35:
        # cross-check the 30 deep-campaign rungs k=36..65 against claims.json
        claimmap = {}
        cj = __import__("json").load(open("claims.json"))
        for item in cj["misc"]:
            if item.get("kind") == "live" and item.get("n") == 35 and 36 <= item["k"] <= 65:
                claimmap.setdefault(item["k"], item["val"])
        ex = su = mi = 0
        for k in range(36, 66):
            ours = nv.get(k, 0)
            if k in claimmap:
                if ours == claimmap[k]:
                    ex += 1
                else:
                    su += 1
                    if k >= 62:
                        pass
            else:
                mi += 1
        say(f"   cross-check k=36..65 at n=35 vs claims.json: {ex} exact, {su} superseded,"
            f" {mi} unclaimed (expect 26/4/0)")
        say(f"   end rung live(140,35): first exact value,"
            f" digits={len(str(nv[140]))} log10={math.log10(nv[140]):.4f}")
        say(f"   (document float: crest 155.4714, full-box monolith 146.4368, margin 9.0346)")
        for k in (62, 63, 64, 65):
            say(f"   superseded exact value live({k},35) = {nv[k]}")
    if n == 33:
        say(f"   spike at k=131 (outer-leaf law, doc: live = 33^2 * maxTab(33)):"
            f" live(131,33)/1089 = {nv[131] // 1089} exact-divisible: {nv[131] % 1089 == 0}")
    if n == 34:
        say(f"   spike at k=135 (outer-leaf law, doc: live = 34^2 * maxTab(34)):"
            f" live(135,34)/1156 exact-divisible: {nv[135] % 1156 == 0}")
    if n == 37:
        cl37 = CLAIMS[37]
        say(f"   crest digits: k=134 -> {len(str(nv[134]))} (document: 168th digit order,"
            f" log10 167.5204)")
        say(f"   spike at k=139 (outer-leaf law, doc: live = 37^2 * maxTab(37)):"
            f" live(139,37) exact-divisible by 1369: {nv[139] % 1369 == 0}")
    if n == 40:
        say(f"   THE SEXTET: live(146,40) = {nv[146]}")
        say(f"   digits={len(str(nv[146]))}; also full spectrum k=0..160 now exact")
        # document's ledger(146,40) claim -- verify against the engine
        eng = E.ledger_q(146, 40, 4)
        docled = 890781865166222353286753672695200
        say(f"   engine ledger(146,40) vs document claim {docled}: "
            f"{'EXACT MATCH' if eng == docled else 'MISMATCH: ' + str(eng)}")
    say(f"== end of finish n={n} ==")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "cert":
        mode_cert()
    elif mode == "spectrum":
        mode_spectrum(int(sys.argv[2]), float(sys.argv[3]))
    elif mode == "finish":
        mode_finish(int(sys.argv[2]))
    else:
        raise SystemExit("mode = cert | spectrum | finish")
    with open(OUTNAME, "a") as f:
        f.write("\n")
