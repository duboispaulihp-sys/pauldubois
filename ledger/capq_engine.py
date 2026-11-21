"""capq_engine.py -- the generalized column-cap-q family of ledger models.

Phase 6 of the F-closure working session.  Appendix D.5 of "The Harmless
Subgroup and the F-Closure Lemma" fixes the column cap q = 4 (the h^4 slot
of the geometric model).  This module replaces the constant 4 by a free
parameter q >= 1 and re-arbitrates every load-bearing law of the cap-4
framework at q = 1, 2, 3 and (for consistency) 4:

  live_q(k,n)   = # of n x n nonnegative-integer matrices of total k whose
                  row sums and column sums are all <= q.

  Route A:  live_q(k,n) = sum_{mu,nu |- k, mu_1,nu_1 <= q}
              C_mu(n) C_nu(n) T_q(mu,nu),
            C_mu(n) = n!/((n-l(mu))! prod_j m_j!) counts placements of the
            margin multiset mu on the labeled rows (resp. columns), and
            T_q(mu,nu) counts contingency matrices with sorted margins
            (entries are automatically <= q when the margins are).

  Route B (b-law):  live_q(k,n) = sum_{sigma |- k} b_q(sigma,n)^2,
            b_q(sigma,n) = sum_{mu |- k, mu_1 <= q} C_mu(n) K_{sigma,mu}.

  ledger_q(k,n) = sum_{mu |- k, mu_1 <= q, l(mu) <= n} s_mu(1^n)^2
                (hook-square form; at q = 4 this is the document's ledger).

  P^q_k(n) = live_q(k,n) - ledger_q(k,n)   ("generalized syzygies").

Laws re-arbitrated per q (the battery below prints PASS/FAIL for each):
  H.1  T-identity   T(mu,nu) = sum_sigma K_{sigma mu} K_{sigma nu}
                    (cap-free; underpins Route B).
  H.2  Routes A == B, and both == direct brute force at small n, and
       consistency of the parameterized code with the cap-4 engine.
  H.3  Split identity  sum_{sigma_1 <= q} b_q^2 = ledger_q(k,n)
       -- equivalently the square-count law
          P^q_k(n) = sum_{sigma_1 >= q+1} b_q(sigma,n)^2.
       This is the load-bearing step; it is tested as an EXACT polynomial
       identity in n (degree <= 2k; equality at 2k+1 points is equality
       for all n) and additionally at fresh larger n.
  H.4  Zero law: P^q_k(n) = 0 for k <= q and for k >= qn+1 (trivial ends),
       interior positivity on the certified windows; witness certificate
       sigma = (q+1, q^{t-1}, r-1), mu = (q^t, r) for k = qt + r.
  H.5  Birth law  P^q_{q+1}(n) = (C(n+q, q+1) - n)^2.
  H.6  Maturation (one-row) law
            b_q((k,),n) = [x^k](1+x+...+x^q)^n
         via its inclusion-exclusion closed form for all k <= 20.
  H.7  Exact top coefficients (Newton interpolation in exact arithmetic):
            [n^{2k}] P_q  = (sum_{sigma_1 >= q+1} f_sigma^2)/(k!)^2
            [n^{2k}] ledger_q(q+) = N_k(q)/(k!)^2,  [n^{2k}] live_q = 1/k!.
  H.8  Gessel-parameter family N_k(q) = sum_{mu_1 <= q} f_mu^2 (LIS <= q);
       split of k!, Catalan anchor at q = 2, anchor N_k(1) = 1, Regev-type
       standardized ratios for q = 3.

Everything exact (Python int / fractions.Fraction); floats only for display.

Defense conventions carried over: partitions is a GENERATOR (wrap in list()),
C_mu has no falling-factorial decrement bug, Kostka in the pinned type
convention K_{sigma mu} = # SSYT of shape sigma whose content is the
multiset mu (mu_j = # of copies of the j-th smallest letter), engine values
trusted over hand counts, hand counts arbitrated by brute force.
"""

import sys
import time
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb, factorial

sys.path.insert(0, "/workspace/fclosure/ledger")
from ledger_engine import (partitions, conjugate, dominates, C_mu,  # noqa: E402
                           kostka_gt, kostka_ssyt, s_mu_one, T_table,
                           live_A, live_B, ledger, P_k)

Fr = Fraction
out = []


def dom_padded(sigma, mu):
    """Dominance order with zero padding: sigma >= mu iff every partial
    sum of sigma reaches that of mu (the shorter side zero-padded).
    This is the convention under which K_{sigma mu} > 0 <=> sigma >= mu.
    (ledger_engine.dominates requires len(sigma) >= len(mu) and is still
    used, calibrated, elsewhere; the zero-trim of trailing 1-parts makes
    it too strict for the q-family witnesses.)"""
    Ls, Lm = len(sigma), len(mu)
    ps = pm = 0
    for i in range(max(Ls, Lm)):
        ps += sigma[i] if i < Ls else 0
        pm += mu[i] if i < Lm else 0
        if ps < pm:
            return False
    return True


def say(msg=""):
    print(msg, flush=True)
    out.append(str(msg))


# ==================== unit fraction grids for display ====================

def fshow(x, d=6):
    return f"{float(x):.{d}f}" if isinstance(x, Fraction) else str(x)


# ============ parameterized core: T_q (pruned contingency DP) ============

def _comps_capped(s, rem):
    """Compositions of s into len(rem) parts with part j <= rem[j]."""
    if len(rem) == 0:
        if s == 0:
            yield ()
        return
    for a in range(min(s, rem[0]) + 1):
        for rest in _comps_capped(s - a, rem[1:]):
            yield (a,) + rest


def T_q(mu, nu):
    """# of nonnegative integer matrices with row margins mu (in order) and
    column margins nu (in order); entries <= min margins automatically."""
    mu = tuple(x for x in mu if x)
    nu = tuple(x for x in nu if x)
    if sum(mu) != sum(nu):
        return 0
    if not mu:
        return 1 if not nu else 0
    if not nu:
        return 0

    @lru_cache(maxsize=None)
    def go(i, rem):
        if i == len(mu):
            return 1 if not any(rem) else 0
        total = 0
        for comp in _comps_capped(mu[i], rem):
            total += go(i + 1, tuple(r - c for c, r in zip(comp, rem)))
        return total

    return go(0, nu)


def t_by_kostka(mu, nu):
    """cap-free identity side: sum_sigma K_{sigma mu} K_{sigma nu}."""
    k = sum(mu) if mu else sum(nu)
    return sum(kostka_gt(sig, mu) * kostka_gt(sig, nu)
               for sig in partitions(k))


# ============ parameterized live / ledger / b / P ============

def live_A_q(k, n, q):
    """live by the T-matrix identity, cap q."""
    total = 0
    for mu in partitions(k, q):
        cm = C_mu(n, mu)
        if cm == 0:
            continue
        for nu in partitions(k, q):
            cn = C_mu(n, nu)
            if cn == 0:
                continue
            t = T_q(mu, nu)
            if t:
                total += cm * cn * t
    return total


@lru_cache(maxsize=None)
def b_q(sigma, n, q):
    """b_q(sigma,n) = sum_{mu |- k, mu_1 <= q} C_mu(n) K_{sigma mu}."""
    sigma = tuple(x for x in sigma if x)
    total = 0
    for mu in partitions(sum(sigma), q):
        if len(mu) > n:
            continue
        kk = kostka_gt(sigma, mu)
        if kk:
            total += C_mu(n, mu) * kk
    return total


def live_B_q(k, n, q):
    """live by the b-law (Route B), cap q."""
    return sum(b_q(sigma, n, q) ** 2 for sigma in partitions(k))


def oneside_q(k, n, q, lo):
    """sum of b_q^2 over shapes sigma with sigma_1 >= lo."""
    return sum(b_q(sigma, n, q) ** 2
               for sigma in partitions(k) if sigma[0] >= lo)


def ledger_q(k, n, q):
    """hook-square ledger with shape cap q (transpose Gessel parameter)."""
    return sum(s_mu_one(mu, n) ** 2
               for mu in partitions(k, q) if len(mu) <= n)


def P_q(k, n, q):
    return live_B_q(k, n, q) - ledger_q(k, n, q)


def brute_live_q(n, q, kmax=None):
    """Direct enumeration: n x n matrices, all row and column sums <= q.
    Entries are bounded by their row sum (<= q), NOT by n -- the pool cap
    is q (a first draft capped at n and miscounted whenever n < q)."""
    row_pool = [c for s in range(q + 1)
                for c in set(_comps_capped(s, (min(q, s),) * n))]
    hist = {}
    for rows in product(row_pool, repeat=n):
        cols = [0] * n
        tot = 0
        ok = True
        for r in rows:
            cols = [c + v for c, v in zip(cols, r)]
            tot += sum(r)
            if any(x > q for x in cols):
                ok = False
                break
        if ok:
            hist[tot] = hist.get(tot, 0) + 1
    if kmax is None:
        kmax = q * n
    return {k: v for k, v in hist.items() if 0 <= k <= kmax}


def f_syt(sigma):
    """# SYT of shape sigma = k! / prod of hook lengths (exact)."""
    k = sum(sigma)
    hook = 1
    rows = len(sigma)
    for i in range(rows):
        for j in range(sigma[i]):
            right = sigma[i] - j - 1
            down = sum(1 for r in range(i + 1, rows) if sigma[r] > j)
            hook *= right + down + 1
    return factorial(k) // hook


def N_k_q(k, q):
    """N_k(q) = sum_{mu_1 <= q} f_mu^2 = # permutations w/ LIS <= q (RSK)."""
    if k == 0:
        return 1
    return sum(f_syt(mu) ** 2 for mu in partitions(k, q))


def b_one_row_q(k, n, q):
    """b_q((k,),n) at cap q via inclusion-exclusion (maturation law):
    b^q_(k)(n) = sum_j (-1)^j C(n,j) C(n + k - (q+1)j - 1, k - (q+1)j)."""
    total = 0
    j = 0
    while k - (q + 1) * j >= 0:
        total += (-1) ** j * comb(n, j) * comb(n + k - (q + 1) * j - 1,
                                               k - (q + 1) * j)
        j += 1
    return total


def gf_one_row_q(k, n, q):
    """[x^k](1+x+...+x^q)^n by direct polynomial power (exact)."""
    base = [1] * (min(q, k) + 1)
    res = [1]
    b = base[:]
    e = n
    while e:
        if e & 1:
            res = _polymul(res, b, k)
        b = _polymul(b, b, k)
        e >>= 1
    return res[k] if k < len(res) else 0


def _polymul(a, bb, k):
    r = [0] * (k + 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(bb):
            if i + j > k:
                break
            if y:
                r[i + j] += x * y
    return r


# ============ exact Newton interpolation (degree <= 2k polynomials) ======

def falling(x, j):
    r = Fraction(1)
    for i in range(j):
        r *= Fraction(x - i)
    return r


def newton(vals_by_n, deg):
    """Exact forward-difference interpolation from n = 1; returns
    (coeffs, evaluator).  Equality with any degree-<=deg polynomial at
    n = 1..deg+1 certifies identity for ALL n."""
    n0 = 1
    vs = [Fr(vals_by_n[i]) for i in range(n0, n0 + deg + 1)]
    diffs = [vs]
    for _ in range(deg):
        prev = diffs[-1]
        diffs.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])
    coeffs = [diffs[j][0] / factorial(j) for j in range(deg + 1)]

    def eval_at(m):
        x = m - n0
        return sum(coeffs[j] * falling(x, j) for j in range(deg + 1))

    return coeffs, eval_at


# ======================================================================
#                                 BATTERY
# ======================================================================

def run_battery():
    t_start = time.time()
    fails = []

    def check(tag, ok):
        if not ok:
            fails.append(tag)
        say(f"      [{'PASS' if ok else 'FAIL'}] {tag}")

    # ---------------------------------------------------------- H.0 T-identity
    say("== H.0: T-identity T(mu,nu) = sum_sigma K_{sigma mu} K_{sigma nu} "
        "(cap-free) ==")
    bad = 0
    tot = 0
    for k in range(1, 8):
        for mu in partitions(k):
            for nu in partitions(k):
                tot += 1
                if len(mu) > 6 or len(nu) > 6:
                    continue
                if T_q(mu, nu) != t_by_kostka(mu, nu):
                    bad += 1
    say(f"   all (mu,nu) |- k, k <= 7, l <= 6: {tot} pairs, mismatches {bad}")
    check("H.0 T-identity cap-free", bad == 0)
    # cross-check vs the cap-4 engine's unpruned T_table
    bad = 0
    for k in range(1, 7):
        for mu in partitions(k, 4):
            for nu in partitions(k, 4):
                if T_q(mu, nu) != T_table(mu, nu):
                    bad += 1
    say(f"   T_q vs cap-4 engine T_table (k<=6, capped): mismatches {bad}")
    check("H.0b T_q == T_table on cap-4 range", bad == 0)

    # ---------------------------------------- H.1 three-route arbitration
    say("\n== H.1: Routes A == B, both == brute force, per q ==")
    brute_scopes = {1: 7, 2: 5, 3: 4}
    for q in (1, 2, 3):
        nb = brute_scopes[q]
        bad = 0
        tot = 0
        for n in range(1, nb + 1):
            bf = brute_live_q(n, q)
            for k in range(0, q * n + 1):
                tot += 1
                want = bf.get(k, 0)
                if k == 0:
                    got = 1
                else:
                    got = live_B_q(k, n, q)
                if got != want:
                    bad += 1
                if n <= 3 and k <= 8:
                    gotA = live_A_q(k, n, q)
                    if gotA != want:
                        bad += 1
                if n <= 4:
                    gotA = live_A_q(k, n, q)
                    if gotA != want:
                        bad += 1
        say(f"   q={q}: brute n<= {nb}, A-vs-brute n<=4, B-vs-brute n<={nb}: "
            f"{tot} values, mismatches {bad}")
        check(f"H.1 q={q} brute/A/B three-route", bad == 0)
        # A == B on a wider window (beyond brute reach)
        bad = 0
        for n in range(1, 7):
            for k in range(1, min(8, q * n) + 1):
                if live_A_q(k, n, q) != live_B_q(k, n, q):
                    bad += 1
        say(f"   q={q}: Route A == Route B, n <= 6, k <= 8: mismatches {bad}")
        check(f"H.1 q={q} A==B wide", bad == 0)
    # consistency with the cap-4 engine
    bad = 0
    for n in (2, 3, 5, 17, 35):
        for k in range(1, 10):
            if (live_B_q(k, n, 4) != live_B(k, n) or
                    ledger_q(k, n, 4) != ledger(k, n) or
                    live_A_q(k, n, 4) != live_A(k, n)):
                bad += 1
    say(f"   q=4 parameterized vs cap-4 engine (k<=9, n in 2,3,5,17,35): "
        f"mismatches {bad}")
    check("H.1b q=4 consistency with Phase-2 engine", bad == 0)
    check("H.1c settling anchors live(3,2)=20,P_3(2)=0,P_5(2)=b_(5)^2",
          live_B(3, 2) == 20 and P_k(3, 2) == 0 and
          P_k(5, 2) == b_q((5,), 2, 4) ** 2)

    # ---------------------------------------- H.2 split / square-count law
    say("\n== H.2: SPLIT identity sum_{sigma_1<=q} b^2 == ledger_q, and")
    say("   square-count law P^q = sum_{sigma_1>=q+1} b^2 "
        "(exact polynomial certificates) ==")
    for q in (1, 2, 3, 4):
        for k in range(1, 11):
            deg = 2 * k
            big = [s for s in partitions(k) if s[0] >= q + 1]
            les = [s for s in partitions(k) if s[0] <= q]
            # ledger side values
            led = {}
            for n in range(1, deg + 2):
                led[n] = ledger_q(k, n, q)
            sq = {}
            for n in range(1, deg + 2):
                sq[n] = sum(b_q(s, n, q) ** 2 for s in les)
            split_ok = all(led[n] == sq[n] for n in range(1, deg + 2))
            # square-count law via live and P
            Pvals = {}
            for n in range(1, deg + 2):
                Pvals[n] = live_B_q(k, n, q) - led[n]
            syz = {}
            for n in range(1, deg + 2):
                syz[n] = sum(b_q(s, n, q) ** 2 for s in big)
            law_ok = all(Pvals[n] == syz[n] for n in range(1, deg + 2))
            # fresh spot points beyond the certificate window
            badf = []
            for n in range(deg + 2, min(deg + 9, 41)):
                if (ledger_q(k, n, q) != sum(b_q(s, n, q) ** 2 for s in les)
                        or (live_B_q(k, n, q) - ledger_q(k, n, q)) !=
                        sum(b_q(s, n, q) ** 2 for s in big)):
                    badf.append(n)
            tag = f"q={q},k={k}"
            check(f"H.2 {tag} split identity at n=1..{deg+1}", split_ok)
            check(f"H.2 {tag} square-count law at n=1..{deg+1}", law_ok)
            check(f"H.2 {tag} fresh points n={deg+2}..{min(deg+8,40)}",
                  not badf)

    # ---------------------------------------- H.3 zero law + witnesses
    say("\n== H.3: zero law P^q = 0 for k <= q and k >= qn+1; and ==")
    say("   interior positivity with witness (q+1, q^{t-1}, r-1)/(q^t, r) ==")
    for q in (1, 2, 3):
        bad0 = 0
        badq = 0
        badw = 0
        nw = 0
        pqn = []
        for n in range(1, 9):
            # zero windows: k <= q
            for k in range(0, q + 1):
                if P_q(k, n, q) != 0:
                    bad0 += 1
                # end: k >= qn+1
            for k in (qn_element(q, n) + 1, qn_element(q, n) + 2):
                if live_A_q(k, n, q) != 0 or ledger_q(k, n, q) != 0 \
                        or P_q(k, n, q) != 0:
                    bad0 += 1
            # top corner k = qn: record only (NOT asserted to vanish)
            pqn.append(P_q(qn_element(q, n), n, q))
            # interior witnesses
            for k in range(q + 1, qn_element(q, n) + 1):
                r = (k - 1) % q + 1
                t = (k - r) // q
                sig = tuple(x for x in (q + 1,) + (q,) * (t - 1) +
                            ((r - 1,) if r > 1 else ()) if x)
                mu = (q,) * t + (r,)
                if len(mu) > n:
                    continue
                nw += 1
                if not (dom_padded(sig, mu) and kostka_gt(sig, mu) > 0
                        and C_mu(n, mu) > 0):
                    badw += 1
        say(f"   q={q}: zero checks k<=q & k>=qn+1 (n<=8): bad {bad0}; "
            f"P^q_qn(n), n=1..8: {pqn}; witnesses (n<=8): "
            f"{nw} checks, bad {badw}")
        check(f"H.3 q={q} zero window + witnesses",
              bad0 == 0 and badw == 0)
        cq = all(P_q(qn_element(q, n), n, q) > 0 for n in range(2, 9))
        check(f"H.3 q={q} top corner k=qn positive (n=2..8)", cq)
        # interior positivity on the small certified window
        bad = 0
        for n in range(2, 6):
            for k in range(q + 1, qn_element(q, n)):
                if P_q(k, n, q) <= 0:
                    bad += 1
        check(f"H.3 q={q} interior positivity P^q > 0 (n<=5)", bad == 0)
        # witnesses at deeper n (cheap: Kostka at fixed shapes)
        bad = 0
        nw2 = 0
        for n in range(2, 13):
            for k in range(q + 1, qn_element(q, n)):
                r = (k - 1) % q + 1
                t = (k - r) // q
                sig = tuple(x for x in (q + 1,) + (q,) * (t - 1) +
                            ((r - 1,) if r > 1 else ()) if x)
                mu = (q,) * t + (r,)
                nw2 += 1
                if not (kostka_gt(sig, mu) > 0 and C_mu(n, mu) > 0):
                    bad += 1
        say(f"   q={q}: witness certificate n=2..12: {nw2} checks, bad {bad}")
        check(f"H.3 q={q} witness certificate n=2..12", bad == 0)
    check("H.3d q=4 control witness (5,4^{t-1},r-1)/(4^t,r) n<=12, k<=q*n",
          _witness_q4_check())

    # ---------------------------------------- H.3m mirror (box duality)
    say("\n== H.3m: mirror law ledger_q(k,n) = ledger_q(qn-k, n) ==")
    for q in (1, 2, 3, 4):
        bad = 0
        tot = 0
        for n in range(1, 11):
            for k in range(0, q * n + 1):
                tot += 1
                if ledger_q(k, n, q) != ledger_q(q * n - k, n, q):
                    bad += 1
        say(f"   q={q}: n<=10, k=0..qn: {tot} values, mismatches {bad}")
        check(f"H.3m q={q} mirror law", bad == 0)

    # ---------------------------------------- H.4 birth law
    say("\n== H.4: birth law P^q_{q+1}(n) = (C(n+q, q+1) - n)^2 ==")
    for q in (1, 2, 3, 4):
        bad = 0
        for n in range(1, 26):
            want = (comb(n + q, q + 1) - n) ** 2
            if P_q(q + 1, n, q) != want:
                bad += 1
        # also: (q+1) is the ONLY shape with sigma_1 >= q+1 at k = q+1,
        # and maturation gives b_(q+1) = C(n+q,q+1) - n
        bads = 0
        for n in (2, 3, 5, 8, 17, 24):
            if b_q((q + 1,), n, q) != comb(n + q, q + 1) - n:
                bads += 1
        say(f"   q={q}: birth law n=1..25 bad {bad}; "
            f"b_(q+1) closed form bad {bads}")
        check(f"H.4 q={q} birth + one-row at k=q+1", bad == 0 and bads == 0)

    # ---------------------------------------- H.5 maturation law
    say("\n== H.5: maturation law b^q_(k)(n) = [x^k](1+x+...+x^q)^n ==")
    for q in (1, 2, 3, 4):
        bad = 0
        tot = 0
        for n in (2, 3, 5, 8, 17):
            for k in range(1, 21):
                tot += 1
                if b_q((k,), n, q) != b_one_row_q(k, n, q):
                    bad += 1
                if gf_one_row_q(k, n, q) != b_one_row_q(k, n, q):
                    bad += 1
        say(f"   q={q}: b_( k ) vs IE form and vs generating function "
            f"(k=1..20, n in 2,3,5,8,17): {tot*2} checks, bad {bad}")
        check(f"H.5 q={q} maturation law", bad == 0)

    # ---------------------------------------- H.6 exact top coefficients
    say("\n== H.6: exact top coefficients [n^{2k}] (Newton, exact) ==")
    say("      q  k   [n^2k] live_q / (1/k!)  [n^2k] ledger_q*k!^2 / N_k(q)")
    for q in (1, 2, 3, 4):
        for k in (5, 6, 7, 8):
            if k > q:
                deg = 2 * k
                lv = {}
                ld = {}
                for n in range(1, deg + 2):
                    lv[n] = live_B_q(k, n, q)
                    ld[n] = ledger_q(k, n, q)
                cl, _ = newton(lv, deg)
                cd, _ = newton(ld, deg)
                Nkq = N_k_q(k, q)
                ok_live = cl[deg] == Fr(1, factorial(k))
                ok_led = cd[deg] == Fr(Nkq, factorial(k) ** 2)
                pf = Fr(0)
                for s in partitions(k):
                    if s[0] >= q + 1:
                        pf += f_syt(s) * f_syt(s)
                pv = Fr(pf, factorial(k) ** 2)
                topP_pred = cl[deg] - cd[deg]
                say(f"   'P top coeff vs sum_big f^2/(k!)^2': q={q},k={k}: "
                    f"{'PASS' if topP_pred == pv else 'FAIL'} "
                    f"([n^(2k)]P = {topP_pred}, predicted {pv})")
                say(f"      q={q} k={k}: live top ok {ok_live}, "
                    f"ledger top ok {ok_led}, N_k({q}) = {Nkq}, "
                    f"big sum = {pf}")
                check(f"H.6 q={q} k={k} top coefficients",
                      ok_live and ok_led and topP_pred == pv)

    # ------------------------------------------------ H.7 Gessel family
    say("\n== H.7: Gessel-parameter family N_k(q) = sum_{mu_1<=q} f_mu^2 ==")
    say("      k      N_k(1)   N_k(2)=Cat   N_k(3)        N_k(4)      sum all = k!")
    Ns = {q: {} for q in (1, 2, 3, 4)}
    for k in range(1, 31):
        Ns[4][k] = N_k_q(k, 4)
        Ns[3][k] = N_k_q(k, 3)
        Ns[2][k] = N_k_q(k, 2)
        Ns[1][k] = N_k_q(k, 1)
        if k in (5, 10, 15, 20, 25, 30):
            say(f"  {k:4d}  {Ns[1][k]:8d}  {Ns[2][k]:10d}  {Ns[3][k]:12d}  "
                f"{Ns[4][k]:>14d}   "
                f"{'PASS' if Ns[4][k] + _bigsum(k, 4) == factorial(k) else 'FAIL'}")
    cat = [comb(2 * i, i) // (i + 1) for i in range(31)]
    ok1 = all(Ns[1][k] == 1 for k in range(1, 31))
    ok2 = all(Ns[2][k] == cat[k] for k in range(1, 31))
    oksplit = all(Ns[q][k] + _bigsum(k, q) == factorial(k)
                  for q in (1, 2, 3, 4) for k in range(1, 31))
    say(f"   N_k(1) = 1 for all k (LIS<=1):         {'PASS' if ok1 else 'FAIL'}")
    say(f"   N_k(2) = Catalan_k for all k<=30:      {'PASS' if ok2 else 'FAIL'}")
    say(f"   shape split sum_all f^2 = k! (q=1..4): "
        f"{'PASS' if oksplit else 'FAIL'}")
    check("H.7 Gessel family anchors + splits", ok1 and ok2 and oksplit)
    say("\n   Regev-type standardized v_k^(q) = N_k(q)*k^{(q^2-1)/2}/q^{2k}"
        " (floats, trend [program]; Regev exponent (d^2-1)/2, anchored")
    say("   by the Catalan slope at q = 2 and consistent with Note G at q = 4):")
    say("      k    v^(2)      v^(3)      v^(4)")
    for k in (5, 10, 15, 20, 25, 30):
        v2 = Ns[2][k] * float(k) ** 1.5 / 4 ** k
        v3 = Ns[3][k] * float(k) ** 4.0 / 9 ** k
        v4 = Ns[4][k] * float(k) ** 7.5 / 16 ** k
        say(f"  {k:4d}  {v2:9.4f}  {v3:10.4f}  {v4:11.4f}")

    # --------------------------------------------- H.8 joint (k,n) regime
    say("\n== H.8: joint (k,n) regime census, cap-4 model ==")
    say("   D_k(n) = P_k(n)*(k!)^2 / (sum_big f^2 * n^(2k));  D -> 1 as n grows")
    say("   cos   = cosine between actual b^2-shares and frozen f^2-shares")
    say("   n*mE  = n * max |share - frozen|  (freezing rate, cf. Note G)")
    say("      k   n    live_k(n)                  digitsP       D_k(n)   cos(n)   n*mE")
    joint = []
    for k in range(5, 13):
        bigsum = _bigsum(k, 4)
        for n in (k, 2 * k, 3 * k):
            t0 = time.time()
            lv = live_B(k, n)
            ld = ledger(k, n)
            P = lv - ld
            D = Fr(P * factorial(k) ** 2, bigsum * n ** (2 * k))
            froz = {}
            totf = 0
            for s in partitions(k):
                if s[0] >= 5:
                    froz[s] = f_syt(s)
            totf = sum(x * x for x in froz.values())
            froz = {s: Fr(x * x, totf) for s, x in froz.items()}
            act = {s: Fr(b_q(s, n, 4) ** 2, P) for s in froz}
            dot = sum(act[s] * froz[s] for s in froz)
            na = (sum(x * x for x in act.values())) ** Fr(1, 2)
            nf = (sum(x * x for x in froz.values())) ** Fr(1, 2)
            cosf = dot / (na * nf)
            merr = n * max(abs(act[s] - froz[s]) for s in froz)
            say(f"  {k:4d} {n:4d}  {lv}  {len(str(P))}  "
                f"{fshow(D)}  {fshow(cosf, 4)}  {fshow(merr, 3)}  "
                f"({time.time() - t0:.1f}s)")
            joint.append((k, n, D, cosf, merr))
    say("\n   D_k(k) as k grows (joint regime, trend [program]):")
    dkk = [fshow(D[2], 3) for D in joint if D[1] == D[0]]
    ckk = [fshow(D[3], 4) for D in joint if D[1] == D[0]]
    say("     D_k(k): " + "  ".join(dkk))
    say("     cos(k,k): " + "  ".join(ckk))
    say("\n   reading (all rows engine-certified; trend claims [program]):")
    say("     - at n = k and n = 2k the frozen profile is already close, but the")
    say("       cosine DECREASES with k at n = k (freezing lags in the joint")
    say("       regime; n = 3k rows recover it); [program]")
    say("     - the joint-regime window is engine-bound (Route B reach).")

    # ---------------------------------------------------------- summary
    say("\n== SUMMARY ==")
    if fails:
        say(f"   {len(fails)} FAIL: " + "; ".join(fails))
        say("   *** SYSTEMS: NOT ALL GREEN -- see failures above ***")
    else:
        say("   ALL CHECKS PASS (H.0-H.8)")
    say(f"   total runtime {time.time() - t_start:.0f}s")
    say("\nend of capq_engine")


def qn_element(q, n):
    return q * n


def _bigsum(k, q):
    """sum_{sigma_1 >= q+1} f_sigma^2."""
    tot = 0
    for s in partitions(k):
        if s[0] >= q + 1:
            f = f_syt(s)
            tot += f * f
    return tot


def _witness_q4_check():
    """Control: at q=4 the Phase-4 witness (5,4^{t-1},r-1)/(4^t,r)."""
    for n in range(2, 13):
        for k in range(5, qn_element(4, n)):
            r = (k - 1) % 4 + 1
            t = (k - r) // 4
            sig = tuple(x for x in (5,) + (4,) * (t - 1) +
                        ((r - 1,) if r > 1 else ()) if x)
            mu = (4,) * t + (r,)
            if len(mu) > n:
                continue
            if not (kostka_gt(sig, mu) > 0 and C_mu(n, mu) > 0):
                return False
    return True


if __name__ == "__main__":
    run_battery()
    with open("/workspace/fclosure/ledger/capq.txt", "w") as fh:
        fh.write("\n".join(out) + "\n")
    print("written capq.txt", file=sys.stderr)
