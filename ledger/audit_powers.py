"""Audit the document's deep syzygy-power claims (P_9(24), P_10(25), P_11(26),
P_20(35)) at the level of individual squares: every printed base must equal a
b_sigma value (sigma |- k, sigma_1 >= 5), the multiset of printed bases must
cover all such shapes, and the printed sum must equal the engine's P_k(n).

Pure-Python exact arithmetic; uses ledger_engine's b_sigma (Route B) and
ledger (hook-square).
"""
import re, time
from collections import Counter
from ledger_engine import partitions, b_sigma, ledger, live_B

MD = ("/mnt/vibefs/uploads/670a0687-c0b7-4b72-8fde-0039fba72653/"
      "mqYOSAAl-the-harmless-subgroup-and-the-f-closure-lemma (4).md")
LINES = [(1266, 9, 24), (1278, 10, 25), (1290, 11, 26), (1414, 20, 35)]

nl = [l.rstrip("\n") for l in open(MD, encoding="utf-8")]

out = []
def say(msg):
    print(msg)
    out.append(msg)

def num(s):
    return int(s.replace(",", "").replace("{", "").replace("}", ""))

for ln, k, n in LINES:
    line = nl[ln - 1]
    # some lines print several claims (e.g. line 1290 also prints P_6(26),
    # P_7(26)); keep only this claim's own chunk when it is addressed by name
    key = f"P_{{{k}}}({n})"
    if key in line:
        line = line[line.find(key):]
    t0 = time.time()
    # printed square bases (numeric tokens only)
    bases = [num(m) for m in re.findall(r"([0-9{,}]*[0-9])\^2", line)]
    # printed total (if the numeric chain ends '= T')
    total_doc = None
    for chunk in line.split("$"):
        cb = [num(m) for m in re.findall(r"([0-9{,}]*[0-9])\^2", chunk)]
        if len(cb) >= 2 and "=" in chunk:
            tail = chunk.split("=")[-1].strip()
            if re.fullmatch(r"[0-9{,}]+", tail):
                total_doc = num(tail)
    say(f"== P_{k}({n}) (md line {ln}): {len(bases)} printed squares"
        + (f", printed total {total_doc}" if total_doc is not None else ""))

    # engine: b_sigma over all shapes of k
    bs5 = {}
    for i, s in enumerate(partitions(k)):
        v = b_sigma(s, n)
        if s[0] >= 5 and v > 0:
            bs5[s] = v
        if (i + 1) % 100 == 0:
            say(f"   ... {i+1} shapes done ({time.time()-t0:.0f}s)")
    engine_multiset = Counter(bs5.values())
    printed_multiset = Counter(bases)
    say(f"   shape count: printed {len(bases)} vs engine {len(bs5)} "
        f"(p({k})-p_4({k}) = {len(list(partitions(k)))}-{len(list(partitions(k,4)))})")
    say(f"   base multiset identical: {engine_multiset == printed_multiset}")
    only_doc = printed_multiset - engine_multiset
    only_eng = engine_multiset - printed_multiset
    if only_doc:
        say(f"   MISMATCH bases printed only: {dict(only_doc)}")
    if only_eng:
        say(f"   MISMATCH bases engine only: {dict(only_eng)}")
    s_printed = sum(b * b for b in bases)
    s_engine = P = sum(v * v for v in bs5.values())
    say(f"   sum of printed squares == engine P_{k}(n): {s_printed == s_engine}")
    if total_doc is not None:
        say(f"   printed total == engine P_{k}(n): {total_doc == s_engine}")
    if k == 20:
        # live(20,35) = sum over ALL shapes of b^2 : verify the printed
        # 'live - ledger' difference to the digit.
        lv = live_B(k, n)
        lg = ledger(k, n)
        say(f"   live(20,35) engine == printed (27.277e...): {lv == num('27{,}277{,}245{,}818{,}749{,}123{,}471{,}218{,}465{,}200{,}909{,}528{,}830{,}189{,}120')}")
        say(f"   ledger(20,35) engine == printed (42.185e...): {lg == num('42{,}185{,}191{,}927{,}758{,}873{,}531{,}355{,}693{,}813{,}215{,}446{,}041{,}104')}")
        say(f"   live - ledger == P_20(35): {lv - lg == s_engine}")
    else:
        lv = live_B(k, n)
        say(f"   (cross) live_B({k},{n}) - ledger({k},{n}) == P: "
            f"{lv - ledger(k, n) == s_engine}")
    say(f"   ({time.time()-t0:.0f}s)\n")

open("/workspace/fclosure/ledger/powers_audit.txt", "w").write("\n".join(out) + "\n")
print("written powers_audit.txt")
