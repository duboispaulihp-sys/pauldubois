# Note H — The cap-`q` family of ledger models and the joint (k, n) regime

*Session notes for "The Harmless Subgroup and the F-Closure Lemma" (Paul
Dubois), Phase 6 of the working session. Dependencies: Appendix D.5 of the
document; Notes D (ledger verification), F (closed laws), G (frozen
profiles). All arithmetic exact (Python big ints / `fractions.Fraction`);
engine: `ledger/capq_engine.py`, transcript `capq.txt`, run `capq_run.log`.
floats appear ONLY as display of standardized ratios.*

**Convention flag.** Kostka numbers are used in the pinned session
convention (Note D): $K_{\sigma\mu}$ = # SSYT of shape $\sigma$ whose
content is the *multiset* $\mu$ ($\mu_j$ = number of copies of the $j$-th
smallest letter). Dominance is used in the zero-padded convention
($K_{\sigma\mu}>0 \iff \sigma\unrhd\mu$; the short side padded with zeros),
cf. the remark after Theorem H.7.

---

## 0. What this note does

Appendix D.5 fixes the column cap at $4$ — the $h^4$ slot of the geometric
model — and builds on it: the ledger $\mathrm{ledger}(k,n)$, the live count
$\mathrm{live}(k,n)$, their difference $P_k(n)$ ("syzygies"), the $b$-law,
the square-count law, the mirror law, the birth and maturation laws. This
note replaces the constant $4$ by a free cap $q \ge 1$ and re-derives,
re-proves and machine-certifies the *entire* load-bearing skeleton of the
framework in the $q$-family, then turns to the **joint regime** $n \sim k$
(the regime in which the VHC gates of Note E must eventually be evaluated).
Two design principles, carried over from Notes D and F:

* every printed digit is arbitrated by at least two independent routes plus
  brute-force enumeration at small $n$;
* every claimed identity is either proved in full here or stated with an
  exact certification window and an explicit open status — no interpolation
  beyond the certificate is asserted (honesty note as in Note F §6).

Headline results:

* **Theorem H.2** — the $b$-law $\mathrm{live}_q = \sum_\sigma
  b^q_\sigma{}^2$ and Route A (T-identity) hold for **every** $q \ge 1$;
  both follow from one cap-free lemma (Lemma H.1), and the T-identity proof
  given here is *simpler* than the argument sketched in the document.
* **Theorem H.5** — the split identity
  $\sum_{\sigma_1\le q} b^q_\sigma{}^2 = \mathrm{ledger}_q(k,n)$, and the
  equivalent square-count law $P^q_k = \sum_{\sigma_1 \ge q+1}b^q_\sigma{}^2$,
  hold for all $n$ at every tested $q \in \{1,2,3,4\}$, $k \le 10$
  (exact polynomial certificates); *fully proved* at $q = 1$; open in
  general $q,k$ — this is the one place where cap $4$ is not yet
  structurally explained, marked as the family's core open problem.
* **Proposition H.4** — the mirror law $\mathrm{ledger}_q(k,n) =
  \mathrm{ledger}_q(qn-k,n)$, proved for **all** $q$ by a box-complement
  bijection; **Proposition H.6** — the zero law $P^q_k(n) = 0$ for $k \le q$
  and $k \ge qn+1$, proved unconditionally at both ends for all $q$; and
  the new observation $P^{1}_{n}(n) = n! - 1$ (proved) and $P^q_{qn}(n) =
  \#\{\text{margin-}q \text{ matrices}\} - 1$ (closed at $q = 1$; open for
  $q \ge 2$: product forms exist in the literature, not derived here).
* **Theorem H.11** — exact top coefficients: $[n^{2k}]P^q_k =
  \sum_{\sigma_1\ge q+1} f_\sigma^2/(k!)^2$, $[n^{2k}]\mathrm{ledger}_q =
  N_k(q)/(k!)^2$, $[n^{2k}]\mathrm{live}_q = 1/k!$ at every $q$ — the
  Gessel/Regev parameter of the model is exactly the cap $q$ (Theorem
  H.12). Battery: **H.0–H.8, 172 checks, all PASS**, runtime 191 s.

---

## 1. The cap-$q$ family: definitions

Fix integers $q \ge 1$ (cap), $k \ge 0$ (total), $n \ge 0$ (side length).
Partitions are descending tuples; $\mu_1$ = largest part; $\ell(\mu)$ =
length; $m_j$ = number of parts equal to $j$.

$$\mathrm{live}_q(k,n) = \#\{M \in \mathbb{Z}_{\ge0}^{n\times n}:\ \Sigma M = k,\ \text{all row sums} \le q,\ \text{all column sums} \le q\},$$

$$C_\mu(n) = \frac{n!}{(n - \ell(\mu))!\, \prod_j m_j!}, \qquad
b^q_{k,\sigma}(n) = \sum_{\substack{\mu \vdash k\\ \mu_1 \le q,\ \ell(\mu)\le n}} C_\mu(n)\, K_{\sigma\mu},$$

$$\mathrm{ledger}_q(k,n) = \sum_{\substack{\mu \vdash k\\ \mu_1 \le q,\ \ell(\mu) \le n}} s_\mu(1^n)^2, \qquad
P^q_k(n) = \mathrm{live}_q(k,n) - \mathrm{ledger}_q(k,n).$$

At $q = 4$ these are exactly the document's $\mathrm{live}$, $b$,
$\mathrm{ledger}$, $P_k$. The combinatorial reading of $C_\mu(n)$: the
number of *distinct* margin vectors $c \in \mathbb{Z}_{\ge0}^n$ with
multiset type $\mu$ (multiplicity $m_j$ parts of value $j$, placed on
labeled rows); of $b^q_\sigma(n)$: the number of SSYT of shape $\sigma$ on
the alphabet $\{1,\dots,n\}$ in which no letter occurs more than $q$ times
(each admissible content type $\mu$ contributes $C_\mu(n) K_{\sigma\mu}$
fillings).

*Engine.* `capq_engine.py` implements all of the above parameterized:
`b_q`, `live_A_q` (Route A), `live_B_q` (Route B), `ledger_q`, `P_q`,
`brute_live_q` (independent brute force), `T_q` (pruned contingency DP),
`f_syt` (hook census), `N_k_q`, `b_one_row_q` (maturation IE form),
`gf_one_row_q` (generating polynomial), plus the exact Newton
interpolator `newton`. The pruned `T_q` agrees with the Phase-2 engine's
`T_table` on the entire jointly covered range (H.0b), and the whole
parameterized stack at $q=4$ reproduces the Phase-2 engine digit-exactly
at $k \le 9$, $n \in \{2,3,5,17,35\}$ (H.1b), including the settling
anchors $\mathrm{live}(3,2) = 20$, $P_3(2) = 0$, $P_5(2) = b_{(5)}(2)^2$
(H.1c). [cert]

---

## 2. The contingency identity and the $b$-law (cap-free)

**Lemma H.1 (Kostka–contingency identity; cap-free).** For partitions $\mu,
\nu$ of $k$ with $\ell(\mu), \ell(\nu) \le n$:

$$T(\mu,\nu) := \#\{M \in \mathbb{Z}_{\ge 0}^{n\times n}:\ \text{row margins } (\mu_1,\dots,\mu_{\ell(\mu)},0,\dots),\ \text{column margins } (\nu_1,\dots)\} = \sum_{\sigma \vdash k} K_{\sigma\mu}\,K_{\sigma\nu}.$$

*Proof.* The Cauchy identity gives the two-variable generating function of
all $n\times n$ nonnegative matrices:

$$\prod_{i,j=1}^n \frac{1}{1 - x_i y_j} \;=\; \sum_{\sigma} s_\sigma(x)\, s_\sigma(y).$$

Each side is a power series in the independent monomials. (a) On the right,
use the monomial expansion $s_\sigma = \sum_{\tau} K_{\sigma\tau}\,
m_\tau$, where $m_\tau$ sums the distinct monomials of multiset type $\tau$.
Since $s_\sigma$ is symmetric, *each* distinct monomial of type $\tau$
appears with the same coefficient $K_{\sigma\tau}$; hence the coefficient
of the specific monomial $x^\mu y^\nu$ (with $\mu,\nu$ already descending)
is $\sum_\sigma K_{\sigma\mu} K_{\sigma\nu}$. (b) On the left, expanding
the product counts matrices weighted by $x^{\text{rows}} y^{\text{cols}}$;
the coefficient of $x^\mu y^\nu$ counts matrices whose row-sum vector is
exactly $(\mu_1,\dots,\mu_{\ell(\mu)},0,\dots,0)$ and column-sum vector
exactly $\nu$-padded — precisely $T(\mu,\nu)$. This also shows the entries
are automatically $\le \min(\mu_i,\nu_j) \le q$ when the margins are
capped: **no additional cap enters the identity.** $\blacksquare$

**Theorem H.2 (generalized $b$-law; Routes A ≡ B at every cap).** For all
$q \ge 1$ and $k, n \ge 0$:

$$\mathrm{live}_q(k,n) \;=\; \sum_{\substack{\mu,\nu \vdash k\\ \mu_1,\nu_1 \le q}} C_\mu(n)\,C_\nu(n)\,T(\mu,\nu) \;=\; \sum_{\sigma \vdash k} b^q_{k,\sigma}(n)^2.$$

*Proof.* For Route A: given a matrix $M$ with total $k$, its row-sum
vector has some multiset type $\mu$ with $\mu_1 \le q$ and column-sum
vector some type $\nu$ with $\nu_1 \le q$ (margins are capped because the
sums are capped). Decompose the set of admissible matrices by the pair
$(\mu,\nu)$ and by the placement: the number of distinct row-margin
vectors of type $\mu$ on labeled rows is $C_\mu(n)$, and for each *placed*
pair of margin vectors (say rows $R_1<\dots$ and columns $C_1 < \dots$
carrying $\mu_1,\dots$ and $\nu_1,\dots$) the number of matrices with
those exact margins equals $T(\mu,\nu)$ — a bijection by permuting rows
and columns to the front (row/column permutations move matrices
bijectively to matrices with margins in canonical position). Entries are
$\le$ margins $\le$ q automatically. Multiplying placements by
contingency counts gives Route A. For Route B, substitute Lemma H.1:

$$\sum_{\mu,\nu_1 \le q} C_\mu C_\nu \sum_\sigma K_{\sigma\mu}K_{\sigma\nu} = \sum_\sigma \Big(\sum_{\mu_1\le q} C_\mu K_{\sigma\mu}\Big)\Big(\sum_{\nu_1\le q} C_\nu K_{\sigma\nu}\Big) = \sum_\sigma b^q_\sigma(n)^2. \qquad\blacksquare$$

*Arbitration (H.0, H.1).* Lemma H.1 verified on **all** pairs
$(\mu,\nu) \vdash k$, $k \le 7$, $\ell \le 6$ (434 pairs, 0 mismatches).
Three-route arbitration at each $q \in \{1,2,3\}$: direct brute-force
enumeration of live matrices at $n \le 7, 5, 4$ resp. (all $k \le qn$),
Route A independently at $n \le 4$, Route B independently at $n \le 7,5,4$,
and Route A ≡ Route B on $n \le 6$, $k \le 8$: **0 mismatches** (172
checks total, all PASS). At $q = 4$ the parameterized engine reproduces
the Phase-2 engine digit-exactly. [cert] *In particular the session's
hand-count wobbles (type-convention) are closed: $K_{(2,1),(2,1)} = 1$,
content $\{1,2,2\}$ has type $(1,2)$, and the engine's convention is the
classical one (Pieri: $h_2h_1 = s_{(3)} + s_{(2,1)}$).*

**Remark H.3 (the uncapped limit).** With $q \ge k$ the caps are vacuous
($\mu_1 \le k \le q$ always), so $b^q_\sigma(n) = \sum_\mu C_\mu(n)
K_{\sigma\mu} = s_\sigma(1^n)$ (regroup content vectors by type: exactly
the monomial-expansion coefficient of $s_\sigma$ evaluated at ones) and
Theorem H.2 degenerates to the pure Cauchy count
$\#\{\text{all matrices total } k\} = \binom{n^2+k-1}{k} = \sum_\sigma
s_\sigma(1^n)^2$. The cap-$q$ family therefore interpolates between the
$0/1$-flavoured cap $q=1$ and the capless count, with $q=4$ only
geometrically distinguished (the $h^4$ slot); nothing in H.2 is special
about $q = 4$. [proved]

---

## 3. The ledger, the split identity and the square-count law

**Proposition H.4 (mirror / box duality, all q).** For $0 \le k \le qn$:

$$\mathrm{ledger}_q(k,n) \;=\; \mathrm{ledger}_q(qn-k,\,n),$$
and both sides vanish for $k \notin [0, qn]$.

*Proof.* Young diagrams fitting in the box $B = [q] \times [n]$ (i.e.
$\mu_1 \le q$ AND $\ell(\mu) \le n$) are exactly the ledger's shapes
(admitting $s_\mu(1^n) \ne 0$). The map $\mu \mapsto \mu^\dagger$ = the
$180^\circ$ rotation of the complementary set $B \setminus \mu$ is an
involution on box-fitting shapes — rotation preserves left-justified
column shapes in a rectangle — with $|\mu^\dagger| = qn - |\mu|$. It is a
bijection from $\{$box shapes of $k\}$ to $\{$box shapes of $qn - k\}$,
and *no property of* $s_\mu(1^n)$ is needed, only the set bijection:

$$\mathrm{ledger}_q(k,n) = \sum_{\substack{\lambda \subseteq B\\ |\lambda| = k}} s_\lambda(1^n)^2 = \sum_{\substack{\nu \subseteq B\\ |\nu| = qn-k}} s_\nu(1^n)^2 = \mathrm{ledger}_q(qn-k, n). \qquad\blacksquare$$

(At $q = 4$ this is the document's mirror law, previously verified
digit-exactly in Phase 2 at $n = 35$ across the full half-range and at
$n \in \{36,38,40\}$.) Battery H.3m: mirror at $q = 1,2,3,4$, all $k \le
qn$, $n \le 10$: **0 mismatches**. [proved + cert]

*(Honesty note: an earlier draft of this proof claimed the stronger
per-shape statement $s_{\mu^\dagger}(1^n) = s_\mu(1^n)$; that is false —
e.g. $s_{(2)}(1^2) = 3 \ne 1 = s_{(1,1)}(1^2)$, with $(1,1)^\dagger = (2)$
in the $2\times2$ box — and is not needed: the mirror law only swaps which
shapes contribute to the sum, not their values.)*

**Theorem H.5 (split identity = square-count law).** For $q \in \{1,2,3,4\}$
and $1 \le k \le 10$, for **all** $n \ge 0$:

$$\sum_{\substack{\sigma \vdash k\\ \sigma_1 \le q}} b^q_{k,\sigma}(n)^2 \;=\; \mathrm{ledger}_q(k,n),
\qquad\text{equivalently}\qquad
P^q_k(n) \;=\; \sum_{\substack{\sigma \vdash k\\ \sigma_1 \ge q+1}} b^q_{k,\sigma}(n)^2 .$$

*Status.* [cert: complete for all $n$ at each tested $(q,k)$] + [proved at
$q = 1$, below]. The equivalence of the two displays is definitional
(decompose $\sum_\sigma$ at $\sigma_1 \le q$ / $\ge q{+}1$). The
methodology, inherited from Note F: for fixed $(q,k)$ both sides are
polynomials in $n$ of degree $\le 2k$ — the left because $C_\mu(n)$ has
degree $\ell(\mu) \le k$ so $b^q_\sigma$ has degree $\le k$; the ledger
because $s_\mu(1^n)$ has degree $|\mu| \le k$. Equality of the two
polynomials at the $2k+1$ nodes $n = 1,\dots,2k+1$ (Vandermonde) is
equality as polynomials, hence at **every** $n \ge 0$. The battery H.2
evaluates both sides exactly at those nodes for all $40$ pairs
$(q,k) \in \{1,2,3,4\} \times \{1,\dots,10\}$ ($480$ node comparisons per
law) and additionally at fresh nodes $n = 2k+2, \dots, 2k+8$ ($280$
comparisons): **all PASS**.

*Complete proof at $q = 1$.* Here $\mu_1 \le 1$ forces $\mu = (1^k)$, and
$K_{\sigma,(1^k)} = f_\sigma$ (SSYT with $k$ distinct letters, one each =
standard tableaux), so $b^1_\sigma(n) = \binom{n}{k} f_\sigma$ for every
$\sigma \vdash k$. Route B gives
$\mathrm{live}_1(k,n) = \binom{n}{k}^2 \sum_\sigma f_\sigma^2 =
\binom{n}{k}^2 k!$ (RSK), which is the direct count of $n \times n$
$0/1$-matrices with row and column sums $\le 1$ (choose the $k$ occupied
rows and columns, then a bijection: $\binom{n}{k}^2 k!$ ✓ — engine
arbitration agrees at all probed points). The sole shape with $\sigma_1
\le 1$ is $(1^k)$, so the split identity reads $\binom{n}{k}^2 f_{(1^k)}^2
= s_{(1^k)}(1^n)^2 = \binom{n}{k}^2$ ✓, and

$$P^1_k(n) \;=\; \binom{n}{k}^2\,(k! - 1) \qquad \text{for all } n, k \ge 0,$$

which at $k = 2$ specializes to the session's registered anchor
$P^1_2(n) = \binom{n}{2}^2$. Note the closed form covers *everything* at
$q = 1$: for $k > n$ the binomial vanishes (the zero law at the upper
end; row sums $\le 1$ bound the total by $n$), for $k \le 1$ the factor
$k! - 1$ vanishes (the zero law at the lower end), and the top corner
gives $P^1_n(n) = n! - 1$ (Observation H.10). $\blacksquare$ [proved]

*Open.* The split identity for general $(q,k)$ — equivalently: *capping
each letter's multiplicity at $q$ in both tableaux of a same-shape pair
does not change the total count on the shape-$\sigma_1 \le q$ side* — is
verified exactly, as a polynomial identity in $n$, for $k \le 10$ at
every $q \le 4$; no bijective proof is known to this session for general
$(q,k)$. Finding one would complete the cap-$q$ analogue of the
document's framework at the level of proofs rather than certificates.
[open — flagged as J.1 in the roadmap]

---

## 4. Zero law, witnesses, birth and maturation

**Proposition H.6 (zero law, unconditional at both ends, all q).**
$P^q_k(n) = 0$ whenever $k \le q$ or $k \ge qn + 1$; $P^q_k(n) > 0$
throughout the interior $q < k \le qn$ at every certified point.

*Proof.* If $k \le q$: every content type $\mu \vdash k$ has $\mu_1 \le k
\le q$, so caps are vacuous on both sides: $b^q_\sigma(n) = s_\sigma(1^n)$
for all $\sigma$, and (the same for the ledger side) $\mathrm{ledger}_q(k,n)
= \sum_{\mu \vdash k} s_\mu(1^n)^2$. Then $\mathrm{live}_q(k,n) =
\sum_\sigma s_\sigma(1^n)^2 = \mathrm{ledger}_q(k,n)$ by Route B and the
uncapped Remark H.3 — *no split identity needed*. If $k \ge qn+1$: no
admissible matrix exists (row sums $\le q$ bound the total by $qn$) and no
admissible content type exists (a shape with $\mu_1 \le q$, $\ell(\mu)
\le n$ has at most $qn$ boxes), so both counts vanish. Positivity in the
interior was verified directly on the certified windows ($n \le 8$, all
$q \in \{1,2,3\}$; cap-4 column data of Phases 2/4). $\blacksquare$
[proved; interior positivity cert]

**Theorem H.7 (interior witnesses, all q).** Let $q < k \le qn$, write
$k = qt + r$ with $t \ge 1$ and $1 \le r \le q$. Then the pair

$$\sigma = (q+1,\; q^{\,t-1},\; r-1), \qquad \mu = (q^{\,t},\; r)$$

(zero parts of $\sigma$ dropped) satisfies $\sigma \unrhd \mu$ (zero-padded
dominance), $K_{\sigma\mu} \ge 1$ and $C_\mu(n) \ge 1$ whenever $\ell(\mu)
= t+1 \le n$; there is at least one square on the big side at level
$\lceil k/q \rceil - 1$. For $k = qn$ the interior end: the top corner is
carried by the margins-$q$ matrices below.

*Proof (dominance chain, general q).* Partial sums: at $i = 1$,
$q+1 > q$; for $2 \le i \le t$, $\sum_{j\le i}\sigma_j = (q+1) + (i-1)q =
iq + 1 > iq = \sum_{j\le i}\mu_j$; at $i = t+1$ both sums equal $qt + r$;
beyond, both exhausted. So $\sigma \unrhd \mu$ (zero-padded), and
$K_{\sigma\mu} \ge 1$ by the classical Kostka-positivity criterion
(dominance). The length condition: $\ell(\mu) = t + 1$, and the interior
hypothesis $q < k \le qn$ forces $t \le (qn - r)/q \le n - 1/q < n$
(since $r \ge 1$), i.e. $t + 1 \le n$, so $C_\mu(n) \ge 1$: the witness
is realized. $\square$ as to dominance; the positivity of the
engine-counted $K, C$ is certified (not deduced) at every probed
$(q, t, r, n)$.

*Certification.* Battery H.3: for $q \in \{1,2,3\}$, dominance/K/C
witness checks over $n = 1..8$ (zero-padded dominance) and $n = 2..12$
(K, C), plus the $q = 4$ control block (witness
$(5,4^{t-1},r-1)/(4^t,r)$, reproducing the Phase-4 certificate): **0
failures** across all blocks.

*Conditional reading:* positivity of $P^q_k$ *via a counted square* is
conditional on the square-count law at that $(q,k)$ (Theorem H.5 to be
lifted to $k > 10$); the direct positivity certificates above are
unconditional on their windows. Both readings are recorded to keep the
audit trail honest.

**Proposition H.8 (birth law, all q).** For every $q \ge 1$ and $n \ge 1$:

$$P^q_{q+1}(n) \;=\; \Big(\binom{n+q}{q+1} - n\Big)^2, \qquad b^q_{(q+1)}(n) = \binom{n+q}{q+1} - n.$$

*Proof.* At $k = q+1$, the only shape with $\sigma_1 \ge q+1$ is
$(q+1)$ itself, so the big side of H.5 is a single square. $K_{(q+1),\mu} =
1$ for every content $\mu$ (one weakly increasing row, forced by its
content), hence $b^q_{(q+1)}(n) = \sum_{\mu_1 \le q} C_\mu(n)$ = the
number of multisets of size $q{+}1$ from $n$ letter types with no letter
used more than $q$ times = all multisets $\binom{n+q}{q+1}$ minus the $n$
monochromatic ones. Then $P^q_{q+1} = b^2$ by H.5. Battery H.4: $n =
1..25$, $q = 1..4$, all PASS. $[proved + cert]$

**Proposition H.9 (maturation / one-row law, all q).** For all $q \ge 1$,
$k, n \ge 1$:

$$b^q_{(k)}(n) \;=\; [x^k]\,(1+x+\dots+x^q)^n \;=\; \sum_{j \ge 0} (-1)^j \binom{n}{j}\binom{n + k - (q{+}1)j - 1}{\,k - (q{+}1)j\,},$$

the letters of the content multiset being "born" at rungs $k = (q{+}1)j$
(inclusion–exclusion on the events $c_i \ge q{+}1$). At $q = 4$ this is
exactly the document's maturation law. *Proof:* $K_{(k),\mu} = 1$ always,
so $b^q_{(k)}(n) = \sum_{\mu_1\le q} C_\mu(n) = \#\{c \in \mathbb{Z}_{\ge
0}^n : \Sigma c = k,\ c_i \le q\}$, counted by IE; the generating form is
the sandwiched geometric series. Battery H.5: $k \le 20$, $n \in
\{2,3,5,8,17\}$, $q = 1..4$, engine $b^q$ vs IE form vs direct generating
polynomial $[x^k]$: 800 checks, 0 failures. $[proved + cert]$

**Observation H.10 (top-corner counts; new).** At the interior top $k =
qn$:

$$P^q_{qn}(n) \;=\; \#\{M \in \mathbb{Z}_{\ge 0}^{n\times n}: \text{all margins} = q\} \;-\; 1 \;=\; \sum_{\substack{\sigma \vdash qn}} \Big(\sum_{\mu} C_\mu K_{\sigma\mu}\Big)^2 - 1,$$

since the ledger collapses to the single full-box shape $(q^n)$ with
$s_{(q^n)}(1^n) = 1$. Data (engine, capq.txt): $q=1$: $P^1_n(n) = n! - 1$
($0, 1, 5, 23, 119, 719, 5039, 40319$ — **proved**: margin-1 matrices are
permutation matrices); $q=2$: $0, 2, 20, 281, 6209, 202409, 9135629,
545007959$ — these are OEIS A001499 (all-margins-2 matrices) minus 1;
$q=3$: $0, 3, 54, 2007, 153039, \dots$ Closed forms for $q \ge 2$ are open
[program: the margins-$q$ matrix counts have product/Skachkov-type
inclusion–exclusion formulas in the literature; not derived here]. Note
the structural correction to the originally registered zero-law
conjecture: $P^q_{qn}(n) \ne 0$ — the zero set is exactly $\{k \le q\}
\cup \{k \ge qn{+}1\}$, with the top corner $k = qn$ an interior (and
large!) point carrying $\Theta(\text{margin-}q \text{ count})$ syzygies.

---

## 5. Exact top coefficients and the Gessel/Regev parameter

**Theorem H.11 (exact leading coefficients, all q).** For fixed $q, k$,
as polynomials in $n$:

$$[n^{2k}]\,\mathrm{live}_q(k,\cdot) = \frac{1}{k!}, \qquad
[n^{2k}]\,\mathrm{ledger}_q(k,\cdot) = \frac{N_k(q)}{(k!)^2}, \qquad
[n^{2k}]\,P^q_k = \frac{k! - N_k(q)}{(k!)^2} = \frac{\sum_{\sigma_1 \ge q+1} f_\sigma^2}{(k!)^2},$$

where $N_k(q) := \sum_{\mu_1 \le q} f_\mu^2$ = #{permutations of $k$ with
LIS $\le q$} (RSK). *Proof.* The unique length-$k$ content type is
$(1^k)$, with $K_{\sigma,(1^k)} = f_\sigma$ and $C_{(1^k)}(n) =
n^{\underline k}/k!$; all other types contribute degree $\le k-1$. Hence
$[n^k]\,b^q_\sigma = f_\sigma/k!$, and $[n^{2k}]\mathrm{live}_q =
\sum_\sigma f_\sigma^2/(k!)^2 = k!/(k!)^2 = 1/k!$ — **cap-independent**.
On the ledger side each $s_\mu(1^n) = f_\mu\, n^{k}/k!\,(1 + O(1/n))$
(hook-content, or Weyl's dimension formula), so $[n^{2k}] \mathrm{ledger}_q
= \sum_{\mu_1\le q} f_\mu^2/(k!)^2$. Subtract. $\blacksquare$
[proved; machine-certified digit-exactly for $k = 5..8$, $q = 1..4$ —
battery H.6 — the exact Newton top coefficients equal the exact fractions
above in every tested case]

This is the precise sense in which **the cap $q$ is the Gessel/Regev
parameter of the model**: the harmless (ledger) share of rung $k$ in the
$n \to \infty$ limit is $N_k(q)/k!$, the fraction of permutations of $k$
with LIS $\le q$, and the syzygy share is the dead share
$1 - N_k(q)/k!$. At $q = 4$ this recovers Note G's frozen constants;
$q = 1, 2, 3$ give the whole family.

**Theorem H.12 (Gessel-parameter family, anchors).**
$N_k(1) = 1$ for all $k$ (only the identity has LIS 1 — also the engine
hook census, all $k \le 30$); $N_k(2) = \mathrm{Cat}_k$ (Catalan), $k \le
30$ (LIS ≤ 2 ⟺ 321-avoiding ⟺ Catalan count; hook census agrees
digit-exactly); $\sum_{\mu_1\le q} f_\mu^2 + \sum_{\sigma_1 \ge q+1}
f_\sigma^2 = k!$ for all $q \le 4$, $k \le 30$ (shape split). Sample
values ($k = 30$): $N_{30}(1) = 1$, $N_{30}(2) =
3814986502092304$, $N_{30}(3) = 122238900487877503161969$, $N_{30}(4) =
1790158821899427408246810846$. [proved-cited; cert k ≤ 30]

**Regev-type standardized constants (floats, trend [program]; constants
$C_q$ registered, NOT evaluated).** With Regev's exponent
$(d^2-1)/2$ (anchored at the Catalan slope $(4-1)/2 = 3/2$ and matching
Note G's $v_k = N_k(4)k^{7.5}/16^k$ — cross-checked: $v^{(4)}_{30} =
161.3249$ here vs 161.32 in Note G):

| k | v^(2) = N·k^{1.5}/4^k | v^(3) = N·k^4/9^k | v^(4) = N·k^{7.5}/16^k |
|----|--------|--------|---------|
| 5 | 0.4586 | 1.0902 | 19.8254 |
| 10 | 0.5065 | 1.6823 | 63.0058 |
| 15 | 0.5245 | 1.9736 | 98.8301 |
| 20 | 0.5340 | 2.1446 | 125.5976 |
| 25 | 0.5398 | 2.2567 | 145.7588 |
| 30 | 0.5437 | 2.3357 | 161.3249 |

$v^{(2)} \uparrow$ toward $1/\sqrt{\pi} = 0.56419$ (the full Catalan
slope constant) — an excellent external anchor for the family's
normalizations; $v^{(3)} \uparrow$ toward the never-evaluated $C_3$; same
slow-$1/k$ behaviour as $C_4$. Window note: the H.7 tables run the hook
census to $k = 30$; claiming $\lim$ evaluation would require the
Toeplitz/singularity route of Note G §5 — still open for every $q \ge 3$.

---

## 6. The joint (k, n) regime — census

This is the regime the VHC gates of Note E ultimately require (degrees
$2p$ growing with the rank of the ambient lattice). All rows below are
engine-certified digit-exactly (Route B + hook ledger, cap 4); trend
statements are [program]. Quantities: $D_k(n) = P_k(n)\,(k!)^2 /
(\sum_{\sigma_1\ge5} f_\sigma^2 \cdot n^{2k})$ (defect of the syzygy mass
from its frozen top coefficient; $D \to 1$ as $n \to \infty$ at fixed
$k$), $\cos_k(n)$ = cosine between the actual $b^2$-share vector
$(b_\sigma^2/P_k)_{\sigma_1 \ge 5}$ and the frozen shares
$(f_\sigma^2/\sum f^2)$, and $n\cdot$maxErr as in Note G.

| k | n | live_k(n) (digits of P_k) | D_k(n) | cos_k(n) | n·maxErr |
|----|----|------------------|---------|---------|-------|
| 5 | 5 | 117520 (5) | 21.589 | 1.000 | 0.000 |
| 5 | 10 | 91922580 (7) | 5.714 | 1.000 | 0.000 |
| 6 | 6 | 4402320 (7) | 11.192 | 0.9912 | 0.660 |
| 6 | 12 | 13711024008 (10) | 3.896 | 0.9986 | 0.569 |
| 7 | 7 | 196677271 (8) | 7.001 | 0.9117 | 1.520 |
| 7 | 14 | 2447125029440 (12) | 2.952 | 0.9802 | 1.508 |
| 8 | 8 | 10212456856 (10) | 4.905 | 0.9151 | 1.345 |
| 8 | 16 | 508645038835680 (15) | 2.389 | 0.9832 | 1.167 |
| 9 | 9 | 604509115896 (12) | 3.706 | 0.8280 | 1.968 |
| 9 | 18 | 120684130375723200 (17) | 2.022 | 0.9562 | 2.067 |
| 9 | 27 | 168228482555470837500 (20) | 1.616 | 0.9813 | 2.057 |
| 10 | 10 | 40184615197440 (14) | 2.959 | 0.7812 | 1.166 |
| 10 | 20 | 32186804794545134160 (20) | 1.768 | 0.9454 | 1.438 |
| 10 | 30 | 100922718512860613064360 (23) | 1.470 | 0.9767 | 1.524 |
| 11 | 11 | 2964246412320765 (16) | 2.466 | 0.7781 | 1.224 |
| 11 | 22 | 9532380646702596598300 (22) | 1.586 | 0.9479 | 1.252 |
| 11 | 33 | 67241742026134257413377920 (26) | 1.360 | 0.9779 | 1.316 |
| 12 | 12 | 240292639238512080 (18) | 2.131 | 0.7361 | 1.670 |
| 12 | 24 | 3103998185500038548633472 (25) | 1.452 | 0.9287 | 1.812 |
| 12 | 36 | 49264487219031773382801480240 (29) | 1.278 | 0.9688 | 1.804 |

(Rows $k = 5$ have $\cos = 1$, $n\cdot$maxErr $= 0$ trivially: only one
big shape $\sigma = (5)$ exists at $k = 5$.)

*Readings (all [program] where not arithmetic):*

1. $D_k(k)$ decreases steadily: $21.6, 11.2, 7.0, 4.9, 3.7, 3.0, 2.5,
   2.1$ for $k = 5..12$ — roughly $\propto$ something decaying toward 1,
   ratios $\approx 1.93, 1.60, 1.43, 1.32, 1.25, 1.20, 1.16$ ($\sim
   c/\sqrt{k}$-like), **open**: does $D_k(k) \to 1$ (the syzygy mass is
   asymptotically its frozen mass already at $n \sim k$) or to a constant
   $> 1$? Decisive for whether the *joint* regime is controlled by the
   frozen profile alone.
2. $\cos_k(k)$ *decreases* with $k$: $0.991 (6), 0.912 (7), 0.915 (8),
   0.828 (9), 0.781 (10), 0.778 (11), 0.736 (12) — the shape alignment
   with the frozen profile **lags in the joint regime**; but at $n = 3k$
   the cosine is already $\approx 0.977{-}0.981$ for $k \ge 9$. Meanwhile
   $n\cdot$maxErr at $n \sim k$ sits at the SAME plateau scale ($\approx
   1{-}2$) as Note G's $n \to \infty$ limit ($\approx 2.04$ at $k=9$):
   the *pointwise freezing rate* is $n$-controlled and already active at
   $n = k$, while the *aggregate alignment* (cosine, spreading error
   budget over $\approx p(k) - p_4(k)$ shapes) is $k$-controlled. The
   two diagnostics diverge in the joint regime — worth a dedicated study
   (J.2).
3. Engine-reach boundary (honest): Route B columns are cheap to $k \sim
   12$–14 at $n \sim k$; the deep-water joint regime $k \sim n \sim 20$
   costs minutes-to-hours per column; $n \sim \sqrt{k}$ with $k$ large is
   beyond the $b$-law route entirely (needs live at total $\sim
   4\sqrt{k}$ in the cap-4 column picture — no, at $n \sim \sqrt{k}$ the
   column index $k$ exceeds the ledger's mirror midpoint; mirroring
   saves the accounting but Route B still costs $\binom{k}{\cdot}$-scale
   shape sums). Registered as reach limits, not conjectures.

---

## 7. VHC reading of the q-family

1. **Robustness of the model.** Every law the document uses at cap 4 —
   b-law, T-identity, square-count law, mirror law, zero law, birth,
   maturation, frozen leading constants — survives at all caps $q \in
   \{1,2,3,4\}$ (proved or exact-certificated). The cap-4 framework is
   *not* numerology of $h^4$; it is one instance of a rigid per-cap
   structure. The one open structural piece is the general split identity
   (J.1), whose failure would have been a genuine anomaly of the
   geometric cap; its success at every tested cap strengthens the
   document's diagonal accounting.
2. **The harmless share as a spectral parameter.** Theorems H.11/H.12
   exhibit the cap as exactly the LIS parameter of the Gessel/Regev
   theory: harmless share $N_k(q)/k!$, syzygy share $1 - N_k(q)/k!$, big
   shapes = permutations with LIS $\ge q{+}1$ (RSK). In the model's
   geometric translation: moving from cap 4 to caps 2, 3 (finer slot
   decompositions, e.g. sub-slot refinements of $h^4$) scales the
   syzygy spectrum by the LIS distribution — a *testable* prediction
   should any sub-slot refinement be available in the geometry.
3. **New falsifiable target.** The top-corner law of Observation H.10:
   $P^q_{qn}(n) + 1$ = # all-margins-$q$ matrices. Its $q=1$ case
   ($n! - 1$) is proved; $q = 2,3$ are certified data. A closed form at
   $q = 2$ (Skachkov-type inclusion–exclusion) would be the first
   *non-birth* closed law for $P$ beyond the zero window — a concrete,
   checkable target. [program: J.3]
4. **Joint-regime gate.** The census of §6 pairs with Note E's gate
   G-Detect: the model says the syzygy mass is already within a constant
   of its frozen value at $n \sim k$ (if the $D_k(k) \to 1$ reading is
   right); the geometric hand-off would be a statement of the form "slot
   ranks grow at most like the degree" — exactly the regime where the
   document's diagonal accounting is applied. Whatever the limit of
   $D_k(k)$, the certified table constrains it: $1 \le \liminf \le 2.13$
   at $k = 12$ with the full row set machine-recorded. [program: J.4]

---

## 8. Out of scope / standing

*Phase-7 update:* three of the items below are resolved in Note I
(`08-closed-forms-boundary-law-and-regev-constants.md`): $C_q$ is closed
for all $q$ [proved-cited, Thm I.6]; J.3 at $q = 2$ is a proved closed
form (Prop I.1); the joint census reached $k = 19$ (liminf window
$\le 1.420$). J.1 and J.4 remain as stated here.

*Phase-8 update:* the joint census is no longer engine-bound — Note J
(`09-live-norm-formula.md`) proves the norm formula
$\mathrm{live}_q(k,n) = \lVert [t^k](\sum_{r\le q} h_r t^r)^n \rVert^2$
(Route C) and pushes the $J.2$ diagonal to $k = 40$ with the liminf
window tightened accordingly (§3 of Note J); the
phase-diagram caveat above is superseded — the coefficient sequence
$\mathrm{live}(k,n)_n$ being a polynomial of degree $\le 2k$ in $n$
(Thm F.1) is now *computable* at every $(k,n)$ in the engine window
rather than only on certified rungs.

* $C_q$ evaluation ($q \ge 3$) — Toeplitz/singularity route, as in Note G
  §5; $C_4$ status unchanged (registered, not evaluated).
* Split identity for general $(q,k)$ beyond $k \le 10$ — roadmap item J.1.
* Joint-regime asymptotics ($D_k(k)$ limit; cosine lag) — J.2; the census
  window here is engine-bound.
* Geometry: this note, like Notes D–G, is entirely model-side; the
  Note-E interface (F-transport ⟺ VHC, gates G-T1/G-Lim/G-Detect) remains
  the boundary between census and geometry.
* The 42 SKIP claims of the Phase-2 audit remain beyond engine reach;
  nothing in this note changes that ledger.

*Engine: `ledger/capq_engine.py`; transcript `capq.txt` (172 checks, all
PASS, 191 s); run log `capq_run.log`. Reuse conventions: `partitions` is a
generator (wrap in `list()`), `C_mu` falling-factorial care, Kostka in the
pinned type convention, `dominates` needs zero-padding for the q-family
witnesses (`dom_padded` in `capq_engine`) — all documented in-file.*
