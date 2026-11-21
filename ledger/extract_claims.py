import re, json, unicodedata

path = "/mnt/vibefs/uploads/670a0687-c0b7-4b72-8fde-0039fba72653/mqYOSAAl-the-harmless-subgroup-and-the-f-closure-lemma (4).md"
text = open(path, encoding="utf-8").read()

def num(s):
    return int(s.replace(",", "").replace("{", "").replace("}", ""))

claims = {"binomial": [], "birth": [], "P6": [], "P7": [], "misc": [],
          "difflive": [], "total": []}

# 1. binomial phase lines: "a, b, c, d = \binom{N+k}{k} with $N = n^2 - 1$"
for m in re.finditer(r"([0-9{,}]+), ([0-9{,}]+), ([0-9{,}]+), ([0-9{,}]+)\s*=\s*\\binom\{([0-9]+)\+k\}\{k\}", text):
    quad = [num(g) for g in m.groups()[:4]]
    N = int(m.group(5))
    claims["binomial"].append({"N": N, "quad": quad, "line": text[:m.start()].count(chr(10)) + 1})

# 2. birth law: "= ... = X^2$ ... over exactly $Y = \binom{A}{5} - n$"
for m in re.finditer(r"live minus ledger \$?= ?\$?([0-9{,}]+) - ([0-9{,}]+) = ([0-9{,}]+) = ([0-9{,}]+)\^2\$?", text):
    claims["birth"].append({"live": num(m.group(1)), "ledger": num(m.group(2)),
                            "P": num(m.group(3)), "sqroot": num(m.group(4)),
                            "line": text[:m.start()].count(chr(10)) + 1})
# simpler birth forms
for m in re.finditer(r"live minus ledger \$= ([0-9{,}]+) = ([0-9{,}]+)\^2\$ exactly", text):
    claims["birth"].append({"P": num(m.group(1)), "sqroot": num(m.group(2)),
                            "line": text[:m.start()].count(chr(10)) + 1})

# 3. P_6 / P_7 printed claims
for m in re.finditer(r"P_6\(([0-9]+)\) = ([0-9{,}\^+ =]+)", text):
    claims["P6"].append({"n": int(m.group(1)), "expr": m.group(2).strip()})
for m in re.finditer(r"P_7\(([0-9]+)\) = ([0-9{,}\^+ =]+)", text):
    claims["P7"].append({"n": int(m.group(1)), "expr": m.group(2).strip()})

# 3b. subtraction claims: "live(k,n) - ledger(k,n) = A - B"
for m in re.finditer(
        r"\\mathrm\{live\}\(([0-9]+),([0-9]+)\) - \\mathrm\{ledger\}\(([0-9]+),([0-9]+)\)"
        r" = ([0-9{,}]+)(?! ?[-\u2212]) ?[-\u2212] ?([0-9{,}]+)", text):
    claims["difflive"].append({"k": int(m.group(1)), "n": int(m.group(2)),
                               "live": num(m.group(5)), "ledger": num(m.group(6)),
                               "line": text[:m.start()].count(chr(10)) + 1})

# 3c. column totals: "total_n = 2 sum_{k=1}^{K} ledger(k,n) + ledger(n,n) = T"
for m in re.finditer(
        r"\\mathrm\{total\}_\{([0-9]+)\} = 2\\sum_\{k=1\}\^\{([0-9]+)\} "
        r"\\mathrm\{ledger\}\(k,[0-9]+\) \+ \\mathrm\{ledger\}\([0-9]+,[0-9]+\) = ([0-9{,}]+)", text):
    claims["total"].append({"n": int(m.group(1)), "K": int(m.group(2)),
                            "val": num(m.group(3)),
                            "line": text[:m.start()].count(chr(10)) + 1})

# 4. misc exact claims.  The value may continue into a subtraction chain
#    "... = A - B" (the document often writes live - ledger = A - B); in that
#    case the LIVE value is the first number of the chain and the LEDGER value
#    the last.  Matches sitting inside a "2\sum ... + ledger(k,n) = T" context
#    are column totals, not ledger rungs; drop them (captured separately).
for pat, tag in [
    (r"\\mathrm\{live\}\(([0-9]+),([0-9]+)\) = ((?:[0-9{,}]+)(?: ?[-\u2212] ?[0-9{,}]+)*)", "live"),
    (r"\\mathrm\{ledger\}\(([0-9]+),([0-9]+)\) = ((?:[0-9{,}]+)(?: ?[-\u2212] ?[0-9{,}]+)*)", "ledger"),
]:
    for m in re.finditer(pat, text):
        k, n, chain = int(m.group(1)), int(m.group(2)), m.group(3)
        prefix = text[max(0, m.start() - 60):m.start()]
        if "\\sum" in prefix:
            continue  # part of a total_ formula (captured as claims['total'])
        parts = [num(p) for p in re.split(r" ?[-\u2212] ?", chain)]
        if len(parts) >= 2:
            val = parts[0] if tag == "live" else parts[-1]
            claims["difflive"].append({"k": k, "n": n,
                                       "live": parts[0], "ledger": parts[-1],
                                       "line": text[:m.start()].count(chr(10)) + 1,
                                       "src": tag})
        else:
            val = parts[0]
        claims["misc"].append({"kind": tag, "k": k, "n": n, "val": val})

json.dump(claims, open("/workspace/fclosure/ledger/claims.json", "w"), indent=1)
print("binomial:", len(claims["binomial"]), "birth:", len(claims["birth"]),
      "P6:", len(claims["P6"]), "P7:", len(claims["P7"]), "misc:", len(claims["misc"]))
for b in claims["birth"][:6]: print(b)
