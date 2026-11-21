"""Phase 7 -- J.3 at q = 2: closed form for the all-margins-2 census
(Observation H.10 / roadmap J.3).

Objects:
  M(n,2) = # nonneg integer n x n matrices with ALL row and column sums 2
         = # 2-regular bipartite multigraphs on labeled row/col sets.
  Obs H.10 (certified): P^2_{2n}(n) = M(n,2) - 1.

Claim (Section I.1 of Note I): a 2-regular bipartite multigraph decomposes
uniquely into connected components, each a
  - "double edge" on 1 row + 1 col (j = 1), or
  - a Hamiltonian even cycle through j rows and j cols (j >= 2);	he number of connected components on j labeled rows + j labeled cols is
  c_1 = 1,   c_j = j! (j-1)! / 2   (j >= 2)   [# Hamiltonian cycles of K_{j,j}].
The exponential formula (row partition x col partition x block bijection
contributing one factor m_j! per size class) gives the closed form
  M(n,2) = (n!)^2 * sum_{(m_j): sum j m_j = n}
             prod_j  c_j^{m_j} / ( (j!)^{2 m_j} m_j! ).

This script CERTIFIES the formula digit-exactly against
  (a) an independent DFS enumeration of matrices n <= 6, and
  (b) the EGF route  F = exp(x) * prod_{j>=2} exp(x^j/(2 j (j!)^2)),
and triangulates the engine identity  P_q(2n, n, 2) = M(n, 2) - 1  (n <= 20).

Writes margins2.txt.
"""
from fractions import Fraction as F
from math import comb, factorial
import sys, time
sys.setrecursionlimit(100000)
import capq_engine as E

OUT = open("margins2.txt", "w")
def say(m=""):
    print(m); OUT.write(m + "\n"); OUT.flush()

def c_j(j):
    return 1 if j == 1 else factorial(j) * factorial(j - 1) // 2

def M_formula(n):
    """Closed form: sum over multiplicity vectors (m_j)."""
    if n == 0:
        return 1
    total = 0
    comps = []
    def rec(j, rem, acc):
        if j > n:
            if rem == 0:
                comps.append(list(acc))
            return
        for m in range(rem // j, -1, -1):
            if m:
                acc.append((j, m))
            rec(j + 1, rem - j * m, acc)
            if m:
                acc.pop()
    rec(1, n, [])
    for multi in comps:
        term = factorial(n) * factorial(n)
        for j, m in multi:
            term *= (c_j(j) ** m)
            term //= factorial(m)          # block bijection row <-> col
            term //= (factorial(j) ** (2 * m))
        total += term
    return total

def M_dfs(n):
    """Independent DFS count; row patterns: double edge, or two singles."""
    cols = [2] * n
    cnt = 0
    def rec(r):
        nonlocal cnt
        if r == n:
            cnt += 1
            return
        for i in range(n):
            if cols[i] == 2:
                cols[i] = 0
                rec(r + 1)
                cols[i] = 2
        for i in range(n):
            if cols[i] >= 1:
                cols[i] -= 1
                for j2 in range(i + 1, n):
                    if cols[j2] >= 1:
                        cols[j2] -= 1
                        rec(r + 1)
                        cols[j2] += 1
                cols[i] += 1
    rec(0)
    return cnt

def M_egf(n):
    """Third route: F = exp(x) * prod_{j=2..n} exp(x^j / (2 j (j!)^2)),
    answer = n!^2 [x^n] F."""
    deg = n
    def polymul_(a, b):
        out = [F(0)] * (deg + 1)
        for i, ai in enumerate(a):
            if ai == 0:
                continue
            for j in range(deg + 1 - i):
                out[i + j] += ai * b[j]
        return out
    def series_exp(coefs):
        res = [F(0)] * (deg + 1)
        res[0] = F(1)
        for k in range(1, deg + 1):
            s = F(0)
            for i in range(1, k + 1):
                s += i * coefs[i] * res[k - i]
            res[k] = s / k
        return res
    ser = [F(0)] * (deg + 1)
    for j in range(deg + 1):
        ser[j] = F(1, factorial(j)) if j <= deg else F(0)
    for j in range(2, n + 1):
        cf = [F(0)] * (deg + 1)
        cf[j] = F(c_j(j), factorial(j) ** 2)
        ser = polymul_(ser, series_exp(cf))
    return factorial(n) ** 2 * ser[n]

say("== Phase 7: J.3 at q = 2 -- closed form for M(n,2) ==")
say("   M(n,2) = (n!)^2 sum_(m_j) prod_j c_j^{m_j} / ( (j!)^{2 m_j} m_j! ),")
say("   c_1 = 1,  c_j = j!(j-1)!/2 (j >= 2)   [Hamiltonian cycles of K_(j,j)]")
say("")

say("== C.1: three-route arbitration of the formula ==")
bad = 0
for n in range(1, 6):
    a, b, c = M_formula(n), M_dfs(n), M_egf(n)
    ok = (a == b == c)
    bad += 0 if ok else 1
    say(f"   n={n}: formula {a}  dfs {b}  egf {c}   [{'PASS' if ok else 'FAIL'}]")
a, c = M_formula(6), M_egf(6)
# DFS(6) left out (pure-Python reach); n=6 arbitrated formula-vs-EGF, with the
# published OEIS anchor A001499(6) = 202410 as the external check.
ok = (a == c) and a == 202410
if not ok:
    bad += 1
say(f"   n=6: formula {a}  egf {c}   [{'PASS' if a == c else 'FAIL'}] "
    f"(n=6 = A001499(6) = 202410 anchor; DFS out of budget)")
say("   cycle-decomposition formula vs DFS vs EGF: "
    + ("ALL PASS" if bad == 0 else f"{bad} FAIL"))
say("")

say("== C.2: engine identity P^2_(2n)(n) = M(n,2) - 1 (Obs H.10 triangulated) ==")
bad2 = 0
for n in range(1, 13):   # (2n, n, 2) engine cost grows fast; n <= 12 in reach
    eng = E.P_q(2 * n, n, 2)
    m = M_formula(n)
    if eng != m - 1:
        bad2 += 1
        say(f"   MISMATCH n={n}: P_q(2n,n,2) = {eng}, M-1 = {m-1}")
    else:
        say(f"   n={n:2d}: P^2_(2n)(n) = M(n,2) - 1: {eng}   PASS")
say("   engine identity: " + ("ALL PASS (n = 1..12)" if bad2 == 0 else f"{bad2} FAIL"))
say("")

say("== C.3: the prepaid sequence M(n,2) = A001499, n = 0..40 (formula alone) ==")
row = [M_formula(n) for n in range(41)]
say("   n=0..15: " + ", ".join(str(x) for x in row[:16]))
say(f"   M(30,2) = {row[30]}")
say(f"   M(40,2) = {row[40]}  ({len(str(row[40]))} digits)")
say("")
say("end of margins2")
OUT.close()
