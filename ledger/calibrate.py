"""calibrate.py — cross-arbitration of all engine routes + document gates."""
import sys, time
sys.path.insert(0, "/workspace/fclosure/ledger")
from ledger_engine import (partitions, C_mu, kostka_gt, kostka_ssyt, s_mu_one,
                          T_table, live_A, live_B, ledger, P_k, syzygy_shape_sum,
                          brute_live, b_one_row, b_sigma)
from math import comb

ok = True

def check(label, got, want, tol_ok=True):
    global ok
    good = (got == want)
    if not good:
        ok = False
    print(f"{'PASS' if good else 'FAIL':4s} {label}: got {got}" + ("" if good else f", want {want}"))

# --- 1. Kostka: GT-DP vs direct SSYT enumeration, all sigma, mu |- k <= 7
t0 = time.time()
pairs = bad = 0
for k in range(1, 8):
    for sig in partitions(k):
        for mu in partitions(k, 4):
            a, b = kostka_gt(sig, mu), kostka_ssyt(sig, mu)
            pairs += 1
            if a != b:
                bad += 1
                print("  KOSTKA MISMATCH", sig, mu, a, b)
print(f"kostka arbitration: {pairs} pairs, {bad} mismatches ({time.time()-t0:.1f}s)")
ok = ok and (bad == 0)

# --- 2. brute force n=2,3,4 vs live_A vs live_B vs live_C
t0 = time.time()
for n, kmax in [(2, 8), (3, 12), (4, 9)]:
    bf = brute_live(n, kmax)
    for k in range(1, kmax + 1):
        a, b = live_A(k, n), live_B(k, n)
        want = bf.get(k, 0)
        got = (a, b)
        check(f"live({k},{n}) all-routes", got, (want, want))
print(f"brute arbitration ({time.time()-t0:.1f}s)")
check("doc gate live(8,2)", live_A(8, 2), 5)
check("doc gate live(8,3)", live_A(8, 3), 3906)

# --- 3. binomial phase live(k,n)=C(n^2-1+k,k), k<=4
badb = 0
for n in range(2, 31):
    for k in range(1, 5):
        if live_B(k, n) != comb(n * n - 1 + k, k):
            badb += 1
            print(f"  BINOMIAL FAIL n={n} k={k}: {live_B(k,n)} vs {comb(n*n-1+k,k)}")
print("binomial phase k=1..4, n=2..30:", "ALL PASS" if badb == 0 else f"{badb} FAILURES")
ok = ok and badb == 0

# --- 4. birth law: P_5(n) == (C(n+4,5) - n)^2 == b_(5)^2 == syzygy_shape_sum
badb = 0
for n in range(2, 31):
    v = P_k(5, n)
    want = (comb(n + 4, 5) - n) ** 2
    if v != want or syzygy_shape_sum(5, n) != want:
        badb += 1
        print(f"  BIRTH FAIL n={n}: {v} vs {want}")
print("birth law (k=5, n=2..30):", "ALL PASS" if badb == 0 else f"{badb} FAILURES")
ok = ok and badb == 0

# --- 5. syzygy = sum_{sigma_1>=5} b^2 for k = 5..9, various n
badb = 0
for n in (6, 10, 17, 35):
    for k in range(5, 10):
        if P_k(k, n) != syzygy_shape_sum(k, n):
            badb += 1
            print(f"  SYZGY-SPLIT FAIL n={n} k={k}: {P_k(k,n)} vs {syzygy_shape_sum(k,n)}")
print("syzygy shape split (k=5..9):", "ALL PASS" if badb == 0 else f"{badb} FAILURES")
ok = ok and badb == 0

# --- 6. one-row letters law: b_(k)(n) == C_mu-aggregate == IE law
badb = 0
for n in (6, 17, 35):
    for k in range(1, 26):
        via_kostka = b_sigma((k,), n)
        via_ie = b_one_row(k, n)
        if via_kostka != via_ie:
            badb += 1
            print(f"  ONE-ROW FAIL n={n} k={k}: {via_kostka} vs {via_ie}")
print("one-row letters/IE law:", "ALL PASS" if badb == 0 else f"{badb} FAILURES")
ok = ok and badb == 0

# --- 7. T-matrix == kappa identity spot checks: T(mu,nu) == sum_sigma K^2
badb = 0
for k in range(1, 7):
    for mu in partitions(k, 4):
        for nu in partitions(k, 4):
            want = sum(kostka_gt(s, mu) * kostka_gt(s, nu) for s in partitions(k))
            if T_table(mu, nu) != want:
                badb += 1
                print(f"  T-IDENTITY FAIL k={k} {mu} {nu}: {T_table(mu,nu)} vs {want}")
print("T(mu,nu) = sum_sigma K*K (k<=6):", "ALL PASS" if badb == 0 else f"{badb} FAILURES")
ok = ok and badb == 0

print("\n==== CALIBRATION", "ALL GREEN" if ok else "FAILURES PRESENT", "====")
