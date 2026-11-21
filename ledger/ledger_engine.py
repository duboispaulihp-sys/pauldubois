"""ledger_engine.py — Independent exact-arithmetic engine for the ledger of
Appendix D.5 of "The Harmless Subgroup and the F-Closure Lemma".

Framework (conventions as defined in the document; the routes below are
*independent* implementations, so agreement is a nontrivial check):

  live(k,n) = # of n x n nonnegative-integer matrices of total k with every
              row and column sum <= 4.

  Route A (T-matrix identity):  live(k,n) = sum_{mu,nu |- k, mu_1,nu_1<=4}
              C_mu(n) C_nu(n) T(mu,nu), with C_mu(n) the row-assignment count
              n!/((n-l(mu))! prod m_j!) and T(mu,nu) the contingency-table
              count for ordered margins (mu, nu).

  Route B (b-law):  live(k,n) = sum_{sigma |- k} b_{k,sigma}^2 with
              b_{k,sigma} = sum_{mu |- k, mu_1 <= 4} C_mu(n) K_{sigma,mu},
              K = # of SSYT of shape sigma with content mu.

  Route C (histogram DP): row-by-row DP over column-level histograms.

  ledger(k,n) = sum_{mu |- k, mu_1 <= 4} s_mu(1^n)^2   (hook-square form).

  P_k(n) = live(k,n) - ledger(k,n)  ("syzygies"); claimed = sum_{sigma_1>=5}
           b^2, which explains the square-count law #{lambda: lambda_1>=5}
           = p(k) - p_4(k).

All arithmetic exact (Python int / fractions.Fraction).
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb, factorial


# ---------------------------------------------------------------- partitions

def partitions(k, max_part=None):
    """All partitions of k as descending tuples, largest part <= max_part."""
    if max_part is None:
        max_part = k
    if k == 0:
        yield ()
        return
    for first in range(min(max_part, k), 0, -1):
        for rest in partitions(k - first, first):
            yield (first,) + rest


def conjugate(mu):
    if not mu:
        return ()
    return tuple(sum(1 for p in mu if p > j) for j in range(mu[0]))


def dominates(sigma, mu):
    """True iff sigma (partition of |sigma|) dominates mu (|sigma| = |mu|)."""
    if len(sigma) < len(mu):
        return False
    return all(sum(sigma[:i + 1]) >= sum(mu[:i + 1]) for i in range(len(mu)))


# ------------------------------------------------------------- C_mu(n)

@lru_cache(maxsize=None)
def C_mu(n, mu):
    """# of ways to realize the multiset mu as row sums on n labeled rows
    (rest zero):  n!/((n - len(mu))! * prod_j m_j!)."""
    l = len(mu)
    if l > n:
        return 0
    res = comb(n, l) * factorial(l)
    for c in Counter(mu).values():
        res //= factorial(c)
    return res


# ------------------------------------------------------------------ Kostka

def kostka_gt(sigma, mu):
    """K_{sigma,mu} = # of SSYT of shape sigma with content mu, via the
    Gelfand–Tsetlin interlacing DP: chains () = lam^(0) <= ... <= lam^(L) = sigma
    with |lam^(i)| = sum_{j<=i} mu_j and horizontal-strip differences."""
    sigma = tuple(x for x in sigma if x)
    mu = tuple(x for x in mu if x)
    if sigma and len(sigma) > len(mu):
        return 0
    if sum(sigma) != sum(mu):
        return 0
    if not sigma:
        return 1
    L = len(mu)
    cur = {(): 1}
    size = 0
    for i in range(1, L + 1):
        size += mu[i - 1]
        nxt = {}
        for lam, cnt in cur.items():
            for lam2 in _hstrips(lam, sigma, size):
                nxt[lam2] = nxt.get(lam2, 0) + cnt
        cur = nxt
        if not cur:
            return 0
    return cur.get(sigma, 0)


def _hstrips(lam, sigma, size):
    """partitions lam2 of `size` with lam <= lam2 <= sigma componentwise and
    lam2/lam a horizontal strip."""
    out = []
    for cand in partitions(size):
        if len(cand) > len(sigma):
            continue
        ok = True
        for j in range(max(len(sigma), len(lam))):
            a = lam[j] if j < len(lam) else 0
            b = cand[j] if j < len(cand) else 0
            c = sigma[j] if j < len(sigma) else 0
            if b < a or b > c:
                ok = False
                break
        if not ok:
            continue
        cc, ca = conjugate(cand), conjugate(lam)
        for j in range(max(len(cc), len(ca))):
            if (cc[j] if j < len(cc) else 0) - (ca[j] if j < len(ca) else 0) > 1:
                ok = False
                break
        if ok:
            out.append(cand)
    return out


def kostka_ssyt(sigma, mu):
    """# of SSYT of shape sigma, content mu — direct backtracking enumeration
    (independent arbitration partner for kostka_gt)."""
    sigma = tuple(x for x in sigma if x)
    mu = tuple(x for x in mu if x)
    if sum(sigma) != sum(mu):
        return 0
    if sigma and len(sigma) > len(mu):
        return 0
    rows = len(sigma)
    remaining = list(mu)

    def fill(i, j, cur_row, prev_row, rem):
        if i == rows:
            return 1
        low = 1
        if j > 0:
            low = max(low, cur_row[j - 1])
        if prev_row is not None and j < len(prev_row):
            low = max(low, prev_row[j] + 1)
        total = 0
        for v in range(low, len(mu) + 1):
            if rem[v - 1] == 0:
                continue
            r2 = list(rem)
            r2[v - 1] -= 1
            if j + 1 < sigma[i]:
                total += fill(i, j + 1, cur_row + (v,), prev_row, tuple(r2))
            else:
                total += fill(i + 1, 0, (), cur_row + (v,), tuple(r2))
        return total

    return fill(0, 0, (), None, tuple(remaining))


# ------------------------------------------------- hook-content s_mu(1^n)

@lru_cache(maxsize=None)
def s_mu_one(mu, n):
    """s_mu(1^n) by the hook-content formula, exact."""
    mu = tuple(x for x in mu if x)
    if not mu:
        return 1
    muc = conjugate(mu)
    r = Fraction(1)
    for i, w in enumerate(mu):
        for j in range(w):
            hook = (mu[i] - j) + (muc[j] - i) - 1
            r *= Fraction(n - i + j, hook)
    assert r.denominator == 1, (mu, n, r)
    return int(r)


# ------------------------------------------------- contingency table count

@lru_cache(maxsize=None)
def T_table(mu, nu):
    """# of nonnegative integer matrices with ordered row margins mu and
    ordered column margins nu (entries automatically <= 4 when margins <= 4)."""
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
            return 1 if all(x == 0 for x in rem) else 0
        s = mu[i]
        total = 0
        for comp in _compositions(s, len(rem)):
            if all(c <= r for c, r in zip(comp, rem)):
                total += go(i + 1, tuple(r - c for c, r in zip(comp, rem)))
        return total

    return go(0, nu)


def _compositions(s, L):
    if L == 0:
        yield () if s == 0 else ()
        return
    if L == 1:
        yield (s,)
        return
    for a in range(s + 1):
        for rest in _compositions(s - a, L - 1):
            yield (a,) + rest


# ------------------------------------------------------- live / ledger / P_k

@lru_cache(maxsize=None)
def live_A(k, n):
    """live by the T-matrix identity."""
    total = 0
    for mu in partitions(k, 4):
        cm = C_mu(n, mu)
        if cm == 0:
            continue
        for nu in partitions(k, 4):
            cn = C_mu(n, nu)
            if cn == 0:
                continue
            t = T_table(mu, nu)
            if t:
                total += cm * cn * t
    return total


@lru_cache(maxsize=None)
def b_sigma(sigma, n):
    """b_{k,sigma}(n) = sum_{mu |- k, mu_1 <= 4} C_mu(n) K_{sigma,mu}."""
    total = 0
    for mu in partitions(sum(sigma), 4):
        if len(mu) > n:
            continue
        kk = kostka_gt(sigma, mu)
        if kk:
            total += C_mu(n, mu) * kk
    return total


@lru_cache(maxsize=None)
def live_B(k, n):
    """live by the b-law (Route B)."""
    return sum(b_sigma(sigma, n) ** 2 for sigma in partitions(k))


@lru_cache(maxsize=None)
def ledger(k, n):
    """hook-square ledger."""
    return sum(s_mu_one(mu, n) ** 2
               for mu in partitions(k, 4) if len(mu) <= n)


@lru_cache(maxsize=None)
def syzygy_shape_sum(k, n):
    """sum_{sigma |- k, sigma_1 >= 5} b^2 — the claimed closed form of P_k(n)."""
    return sum(b_sigma(sigma, n) ** 2
               for sigma in partitions(k) if sigma[0] >= 5)


def P_k(k, n):
    return live_B(k, n) - ledger(k, n)


# ------------------------------------------------- brute force arbitration

def brute_live(n, kmax=None):
    """Direct enumeration of n x n matrices with margins <= 4 (feasible n<=4);
    returns dict k -> count."""
    row_pool = [c for s in range(5) for c in set(_compositions(s, n))]
    hist = Counter()
    for rows in product(row_pool, repeat=n):
        cols = [0] * n
        tot = 0
        for r in rows:
            cols = [c + v for c, v in zip(cols, r)]
            tot += sum(r)
            if any(x > 4 for x in cols):
                break
        else:
            hist[tot] += 1
    if kmax is None:
        kmax = 4 * n
    return {k: v for k, v in hist.items() if 0 <= k <= kmax}


# ------------------------------------------------- correction law (document)

def correction_law_live(k, n):
    """The document's inclusion–exclusion law for k <= 8:
    live = C(n^2-1+k, k) - 2n*sum_{e=5}^{k} C(n+e-1, e) C(n^2-n+k-e-1, k-e)
           + n^2 * sum_{t+a>=5, t+b>=5, t+a+b<=k}
                  C(a+n-2, n-2) C(b+n-2, n-2) C((n-1)^2+k-t-a-b-1, k-t-a-b)."""
    if n < 2:
        raise ValueError
    res = comb(n * n - 1 + k, k)
    res -= 2 * n * sum(comb(n + e - 1, e) * comb(n * n - n + k - e - 1, k - e)
                       for e in range(5, k + 1))
    pair = 0
    for t in range(0, k + 1):
        for a in range(0, k - t + 1):
            for b in range(0, k - t - a + 1):
                if t + a >= 5 and t + b >= 5 and t + a + b <= k:
                    pair += (comb(a + n - 2, n - 2) * comb(b + n - 2, n - 2) *
                             comb((n - 1) ** 2 + k - t - a - b - 1,
                                  k - t - a - b))
    res += n * n * pair
    return res


# ------------------------------------------------- one-row b-law (IE letters)

def b_one_row(k, n):
    """b_{k,(k)}(n) = number of ways to put k units on n labeled rows with
    every row <= 4  =  sum_j (-1)^j C(n, j) C(n+k-5j-1, k-5j)
    (the document's 'maturation law': letter j is born at k = 5j)."""
    return sum((-1) ** j * comb(n, j) * (comb(n + k - 5 * j - 1, k - 5 * j)
               if k - 5 * j >= 0 else 0)
               for j in range(0, k // 5 + 1))
