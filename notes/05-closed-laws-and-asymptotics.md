# Note F — Closed Laws and Exact Asymptotics for the Dubois Ledger

**Status:** Phase 4 of the working session on *"The Harmless Subgroup and the
F-Closure Lemma"* (Paul Dubois, work-session draft). This note upgrades the
ledger model's variational pattern — previously established rung-by-rung and
certified inductively (Notes D, E) — to **closed form**: polynomiality in $n$
with exact degree $2k$, exact leading coefficients proved by the Robinson–
Schensted–Knuth (RSK) correspondence, a complete zero/closure law with a
constructive positivity witness, and a certified closed-law atlas extended to
rungs $k = 9, 10$.

**Citation flags** as in Notes A–E: [proved] = full proof below;
[proved-cited] = proof below relying on one explicitly named classical
theorem; [cert] = machine-certified exact-arithmetic statement (engine:
`ledger/ledger_engine.py`, cross-arbitrated in `calibrate.py`);
[program] = programmatic, not proved.

**Companion artifacts:** `closed_laws.py` / `closed_laws.txt` (F.2 + F.3 +
F.4, with full Newton forms), `pre_register2.py` / `pre_register2.txt`
(§6 below). All arithmetic exact (Python big ints, `fractions.Fraction`);
no floating point.

---

## 0. Summary of results

For fixed $k \ge 1$ let (Note D conventions, recalled in §1):

* $\mathrm{live}(k,n)$ = number of $n\times n$ nonneg-integral matrices of
  total $k$ with every row and column sum $\le 4$;
* $\mathrm{ledger}(k,n) = \sum_{\mu_1\le 4} s_\mu(1^n)^2$ (hook-square);
* $P_k(n) = \mathrm{live}(k,n) - \mathrm{ledger}(k,n)$.

The results:

* **Theorem F.1** (polynomiality): all three are polynomials in $n$ with
  rational coefficients and degree $\le 2k$; for $k \ge 5$ the degree is
  exactly $2k$. [proved]
* **Theorem F.2** (exact leading constants): with $f_\sigma := K_{\sigma,
  (1^k)}$ = number of standard Young tableaux of shape $\sigma$, and
  $\sum_\sigma f_\sigma^2 = k!$ (RSK),
  $$
  \mathrm{live}(k,n) = \frac{n^{2k}}{k!} + O(n^{2k-1}),\qquad
  \mathrm{ledger}(k,n) = \frac{\bigl(\sum_{\mu_1\le 4} f_\mu^2\bigr)
  \, n^{2k}}{(k!)^2} + O(n^{2k-1}),\qquad
  P_k(n) = \frac{\bigl(\sum_{\sigma_1\ge 5} f_\sigma^2\bigr)\, n^{2k}}
  {(k!)^2} + O(n^{2k-1}).
  $$
  The $n\to\infty$ shares $P_k/\mathrm{live} \to \sum_{\sigma_1\ge5} f^2/k!$
  are $n$-independent constants — the model's variational pattern **freezes**
  into exact representation-theoretic constants. For $k=5$: $1/120$.
  Top coefficients certified digit-exactly for $k = 5..10$. [proved][cert]
* **Theorem F.3** (zero/closure law): $P_k(n) = 0$ **iff** $k \le 4$ or
  $k \ge 4n+1$; and $P_k(n) > 0$ for all $5 \le k \le 4n$, by an explicit
  witness pair $(\sigma,\mu)$. [proved][cert]
* **Theorem F.4** (closed-law atlas): exact Newton forward forms for
  $\mathrm{ledger}(5..8,\cdot)$, $\mathrm{live}(5..9,\cdot)$,
  $P_{6..10}(\cdot)$, each certified on $2k$ fresh points with top
  coefficient matching F.2. [cert]
* **§6**: pre-registration extended to rungs $P_9, P_{10}, P_{11}$ at columns
  $n = 36..40$ (square counts $12, 19, 29$; all internal law assertions
  pass), plus the one-row maturation law $b_{(k)}$ for $k = 5..9$ at these
  columns (document's verified range was $n = 4..26$). [cert]

---

## 1. Notation and standing facts

Everything here is from Note D / the document's Appendix D.5; recalled for
completeness.

* $\mathcal P_k$ = partitions of $k$ (descending tuples);
  $\mathcal P_k^{(\le 4)} = \{\mu \in \mathcal P_k : \mu_1 \le 4\}$;
  $\ell(\mu)$ = length; $m_j(\mu)$ = multiplicity of part $j$.
* $K_{\sigma\mu}$ = Kostka number = number of semistandard Young tableaux
  (SSYT) of shape $\sigma$ and content $\mu$; $K_{\sigma\mu} > 0$ iff
  $\sigma$ **dominates** $\mu$ ($\sigma \trianglerighteq \mu$:
  $\sum_{j\le i}\sigma_j \ge \sum_{j\le i}\mu_j$ for all $i$, equal totals)
  — classical; used as [proved-cited] throughout.
* $s_\mu(1^n)$: Schur function at $1^n$; $s_\mu(1^n) = 0$ for
  $\ell(\mu) > n$.
* $C_\mu(n) = \dfrac{n!\,}{(n - \ell(\mu))!\, \prod_j m_j(\mu)!}
  = \dfrac{n^{\underline{\ell(\mu)}}}{\prod_j m_j(\mu)!}$, where
  $n^{\underline r} = n(n-1)\cdots(n-r+1)$ and the empty product is $1$;
  this counts the ways to realize the multiset of positive row-sums $\mu$ on
  $n$ labeled rows. $C_\mu(n) = 0$ iff $\ell(\mu) > n$.
* $b_\sigma(n) = \sum_{\mu \in \mathcal P_k^{(\le 4)}} C_\mu(n)\,
  K_{\sigma\mu}$ (content $\mu_1 \le 4$ = column-sum cap).
* **b-law** [proved, Note D Thm.]: $\mathrm{live}(k,n) =
  \sum_{\sigma \in \mathcal P_k} b_\sigma(n)^2$.
* **Square-count law** [proved, Note D Thm.]: $P_k(n) =
  \sum_{\sigma_1 \ge 5} b_\sigma(n)^2$ for all $k, n$ (in particular
  $P_k(n) \geq 0$ and $P_k(n) = 0$ for $k \le 4$).
* Engine reach used here: Route-B $b$-law and hook-square ledger are exact
  for $k \le 10$ at $n \le 41$ (seconds), and were cross-arbitrated
  (Route A $T$-matrix, brute force $n \le 4$, GT-vs-SSYT Kostka) in
  `calibrate.py` — ALL GREEN.

---

## 2. Theorem F.1 — polynomiality in $n$, degree exactly $2k$

**Lemma F.1.1** (falling-factorial form of $C_\mu$). *For fixed $\mu$,
$C_\mu(n) = n^{\underline{\ell(\mu)}}/\prod_j m_j(\mu)!$ is a polynomial in
$n$ with rational coefficients, degree $\ell(\mu)$, and leading coefficient
$1/\prod_j m_j(\mu)! \ge 1$.*

*Proof.* Immediate from the definition: $n^{\underline r}$ is a monic
polynomial of degree $r$; dividing by the positive integer
$\prod_j m_j!$ scales coefficients without changing degree. ($C_\mu$ as
defined by the factorial quotient also makes sense for all integers, and the
falling-factorial expression is the unique polynomial agreeing with it for
$n \ge \ell(\mu)$.) $\blacksquare$ [cert: matches the engine's exact
integer evaluation on every sampled $(\mu, n)$.]

**Lemma F.1.2** (hook–content). *For fixed $\mu \vdash k$,
$s_\mu(1^n) = \prod_{(i,j)\in\mu} \frac{n + j - i}{h(i,j)}$, a polynomial in
$n$ of degree $|\mu| = k$ with rational coefficients and leading
coefficient $1/H_\mu$, where $H_\mu = \prod_{(i,j)\in\mu} h(i,j)$.*

*Proof.* The hook–content formula [proved-cited: classical; see Stanley,
*EC2*, Cor. 7.21.4] expresses $s_\mu(1^n)$ as that product. The numerator is
a product of $|\mu|$ linear factors of $n$; the denominator
$H_\mu$ is a nonzero constant independent of $n$; the factor $n + j - i$
never vanishes identically, so the product has degree exactly $|\mu|$ with
leading coefficient $\prod 1/h(i,j) = 1/H_\mu > 0$. $\blacksquare$

**Lemma F.1.3** (hook–length formula). *$H_\mu \cdot f_\mu = k!$, where
$f_\mu = K_{\mu,(1^k)}$ is the number of standard Young tableaux (SYT) of
shape $\mu$.* [proved-cited: Frame–Robinson–Thrall; Stanley *EC2*,
Cor. 7.21.6.]

**Theorem F.1.** *Fix $k \ge 1$. Then $b_\sigma(n)$,
$\mathrm{live}(k,n)$, $\mathrm{ledger}(k,n)$ and $P_k(n)$ are polynomials in
$n$ with rational coefficients and*
$$\deg b_\sigma \le k,\qquad \deg \mathrm{live} \le 2k,\qquad
\deg \mathrm{ledger} = 2k,\qquad \deg P_k \le 2k,$$
*and for $k \ge 5$, $\deg P_k = 2k$ with the explicit leading coefficient of
Theorem F.2.*

*Proof.* By the b-law, $\mathrm{live} = \sum_\sigma b_\sigma^2$; the sum is
finite ($|\mathcal P_k|$ terms) and each $b_\sigma$ is a finite
$\mathbb Q$-linear combination of the polynomials $C_\mu(n)$
(Lemma F.1.1), hence is a polynomial of degree $\le \max_{\mu_1\le4}
\ell(\mu) \le k$; squares and finite sums keep degree $\le 2k$. For the
ledger, every term $s_\mu(1^n)^2$ has degree $2k$ with strictly positive
leading coefficient $(1/H_\mu)^2$ (Lemma F.1.2, $|\mu| = k$ for all terms in
the sum), so the sum has degree exactly $2k$ and positive leading
coefficient. For $P_k = \mathrm{live} - \mathrm{ledger}$: degree $\le 2k$
a fortiori; for $k \ge 5$ write (square-count law) $P_k =
\sum_{\sigma_1 \ge 5} b_\sigma^2$, whose leading coefficient is computed
exactly in Theorem F.2 and is $> 0$ there (nonempty sums of positive
rationals: $f_\sigma \ge 1$ and $\sigma_1 \ge 5$ exists), so the degree is
exactly $2k$. For $k \le 4$ the square-count sum is empty and $P_k \equiv 0$
(a polynomial of formal degree $-\infty$; in particular "polynomiality"
holds trivially). $\blacksquare$ [proved]

**Integer-valuedness.** At every $n \in \mathbb Z_{\ge 0}$ the values are
nonnegative integers ($C_\mu(n)$ counts injections; $s_\mu(1^n)$ counts
SSYT): the polynomials are integer-valued, which is what makes exact
Newton interpolation at integer points legitimate and finite.

---

## 3. Theorem F.2 — exact leading constants via RSK

**Lemma F.2.1** ($f$ = SYT count). *$K_{\sigma,(1^k)}$ = number of standard
Young tableaux of shape $\sigma$.*

*Proof.* An SSYT of shape $\sigma$ and content $(1^k)$ uses each of the
labels $1, \dots, k$ exactly once; semistandardness (rows weakly, columns
strictly increasing) applied to distinct labels is exactly standardness.
$\blacksquare$ [proved]

**Lemma F.2.2** (RSK). *$\sum_{\sigma \in \mathcal P_k} f_\sigma^2 = k!$.*

*Proof.* The Robinson–Schensted correspondence assigns to each permutation
$\pi \in S_k$ a pair $(P_\pi, Q_\pi)$ of SYT of one common shape $\sigma
\vdash k$, and is a bijection onto the disjoint union over $\sigma$ of
$\mathrm{SYT}(\sigma) \times \mathrm{SYT}(\sigma)$ [proved-cited: Knuth,
*TP OLAP* Vol. 3, §5.1.4]. Counting both sides:
$k! = \sum_\sigma f_\sigma \cdot f_\sigma$. $\blacksquare$

[cert: for $k = 5..10$ the engine computes
$\sum f^2 = 120, 720, 5040, 40320, 362880, 3628800$ = $k!$, True in all six
cases (`closed_laws.txt`, F.2 block).]

**Theorem F.2** (exact leading constants). *Fix $k \ge 1$.*

**(a)** *For every $\sigma \vdash k$: as a polynomial identity in
coefficient extraction,* $b_\sigma(n) = \frac{f_\sigma}{k!}\, n^k +
O(n^{k-1})$.

*Proof.* Write $b_\sigma(n) = \sum_{\mu_1 \le 4} C_\mu(n)\,K_{\sigma\mu}$.
By Lemma F.1.1, $\deg C_\mu = \ell(\mu)$. A summand contributes to the
$n^k$-coefficient only when $\ell(\mu) = k$; the only partition of $k$ with
length $k$ is $\mu = (1^k)$, which has $m$-multiplicities
$m_1 = k$, so $C_{(1^k)}(n) = n^{\underline k}/k!$ with leading coefficient
$1/k!$; and $K_{\sigma,(1^k)} = f_\sigma$. Hence the $n^k$-coefficient of
$b_\sigma$ is exactly $f_\sigma/k!$. All other summands have degree
$\le k - 1$. $\blacksquare$ [proved]

**(b)** $\mathrm{live}(k,n) = \dfrac{n^{2k}}{k!} + O(n^{2k-1})$,
i.e. the $n^{2k}$-coefficient of the polynomial $\mathrm{live}(k,n)$ is
exactly $1/k!$.

*Proof.* By the b-law and (a), the $n^{2k}$-coefficient is
$\sum_\sigma (f_\sigma/k!)^2 = \frac{1}{(k!)^2}\sum_\sigma f_\sigma^2
= \frac{k!}{(k!)^2} = \frac{1}{k!}$ by Lemma F.2.2. $\blacksquare$ [proved]

**(c)** $\mathrm{ledger}(k,n) = \dfrac{\bigl(\sum_{\mu_1 \le 4}
f_\mu^2\bigr) n^{2k}}{(k!)^2} + O(n^{2k-1})$.

*Proof.* By Lemma F.1.2, the $n^{2k}$-coefficient of $s_\mu(1^n)^2$ is
$1/H_\mu^2 = (f_\mu/k!)^2$ (Lemma F.1.3). Summing over
$\mu_1 \le 4$ gives the claim. $\blacksquare$ [proved]

**(d)** For $k \ge 5$: $P_k(n) = \dfrac{\bigl(\sum_{\sigma_1 \ge 5}
f_\sigma^2\bigr) n^{2k}}{(k!)^2} + O(n^{2k-1})$.

*Proof.* Apply the square-count law $P_k = \sum_{\sigma_1\ge5} b_\sigma^2$
and (a). $\blacksquare$ [proved]

**(e)** *(Share law.)* Combining (b)–(d):
$$\lim_{n\to\infty} \frac{P_k(n)}{\mathrm{live}(k,n)}
= \frac{\sum_{\sigma_1\ge5} f_\sigma^2}{k!},\qquad
\lim_{n\to\infty} \frac{\mathrm{ledger}(k,n)}{\mathrm{live}(k,n)}
= \frac{\sum_{\mu_1\le4} f_\mu^2}{k!},$$
*and the two shares sum to $1$.* [proved — the sum statement is the
tautology $\sum_{\sigma_1 \ge 5} + \sum_{\mu_1 \le 4} = \sum_{\text{all}}
= k!$ over the disjoint cover of $\mathcal P_k$; it doubles as an
exhaustiveness check of the two censuses.]

**Constant table** (exact, from `closed_laws.txt` F.2 block; every row's
middle columns sum to $k!$):

| $k$ | $k!$ | $\sum_{\sigma_1\ge5} f_\sigma^2$ | $\sum_{\mu_1\le4} f_\mu^2$ | $P_k/\mathrm{live} \to$ | ledger-share $\to$ |
|---|---|---|---|---|---|
| 5 | 120 | 1 | 119 | **1/120** | 119/120 |
| 6 | 720 | 26 | 694 | 13/360 | 347/360 |
| 7 | 5040 | 458 | 4582 | 229/2520 | 2291/2520 |
| 8 | 40320 | 6996 | 33324 | 583/3360 | 2777/3360 |
| 9 | 362880 | 101072 | 261808 | 6317/22680 | 16363/22680 |
| 10 | 3628800 | 1438112 | 2190688 | 44941/113400 | 68459/113400 |

**Corollary F.2.b** (the $k = 5$ birth constant). $P_5(n) =
(C(n+4,5) - n)^2$ (document's birth law), so
$P_5/\mathrm{live} \to 1/120$, confirming Theorem F.2(e) at $k=5$ against an
independent closed form: $b_{(5)}(n) = \binom{n+4}{5} - n$ has exact leading
term $n^5/120 = f_{(5)}\,n^5/5!$ with $f_{(5)} = 1$. [proved]

**Corollary F.2.c** (frozen density / convergence rate). The shares are
approached at rate $O(1/n)$. Exact engine series for
$P_5(n)/\mathrm{live}(5,n)$:

| $n$ | 10 | 16 | 24 | 30 | 40 |
|---|---|---|---|---|---|
| $P_5/\mathrm{live}$ | 0.04317 | 0.02518 | 0.01796 | 0.01556 | 0.01341 |

monotonically decreasing toward $1/120 = 0.008333$, matching the slow
convergence observed independently in Phase 3 (E-note model calibration) —
there explained inductively, here a corollary of the exact $O(n^{2k-1})$
error term. [cert]

---

## 4. Theorem F.3 — the zero/closure law

**Theorem F.3.** *For all $n \ge 2$ and $k \ge 1$:*
$$P_k(n) = 0 \iff k \le 4 \ \text{ or } \ k \ge 4n + 1,$$
*and $P_k(n) > 0$ for every $5 \le k \le 4n$.*

*Proof.* **($k \le 4$.)** By the square-count law $P_k = \sum_{\sigma_1
\ge 5} b_\sigma^2$ and the absence of shapes $\sigma \vdash k$ with
$\sigma_1 \ge 5$, the sum is empty. [proved, Note D]

**($k \ge 4n+1$.)** Every $\mu \vdash k$ with $\mu_1 \le 4$ has
$\ell(\mu) \ge \lceil k/4 \rceil \ge n+1 > n$, hence $C_\mu(n) = 0$ for all
admissible $\mu$, hence $b_\sigma(n) = 0$ for **every** $\sigma$, hence
$\mathrm{live}(k,n) = \sum b_\sigma^2 = 0$ by the b-law — indeed no $n
\times n$ matrix with all row sums $\le 4$ can have total $> 4n$,
structurally. Likewise $\mathrm{ledger}(k,n) = \sum_{\mu_1\le4}
s_\mu(1^n)^2 = 0$ since each admissible $\mu$ has $\ell(\mu) > n$ and
Schur specializations vanish beyond the rectangle. So $P_k = 0 - 0 = 0$.
[proved]

**($5 \le k \le 4n$: witness construction.)** Write $k = 4t + r$ with
$0 \le r \le 3$, $t \ge 1$. Define:

* if $r \in \{1,2,3\}$: $\sigma = (5,\, 4^{\,t-1},\, r-1)$ (omit the
  trailing part when $r - 1 = 0$), $\quad\mu = (4^{\,t},\, r)$;
* if $r = 0$ (so $k = 4t \ge 8$): $\sigma = (5,\, 4^{\,t-2},\, 3)$,
  $\quad\mu = (4^{\,t})$.

**Claims:** (i) $\sigma, \mu \vdash k$, both sorted, $\sigma_1 = 5 \ge 5$,
$\mu_1 = 4 \le 4$; (ii) $\ell(\sigma), \ell(\mu) \le n$; (iii)
$\sigma \trianglerighteq \mu$; (iv) hence $K_{\sigma\mu} > 0$
(Kostka-dominance criterion [proved-cited]) and $C_\mu(n) > 0$, so
$b_\sigma(n) \ge C_\mu(n) K_{\sigma\mu} > 0$ and $P_k(n) \ge b_\sigma(n)^2
> 0$ by the square-count law.

*Checks.* (i) Sums: $5 + 4(t-1) + (r-1) = 4t + r = k$ and $4t = k$;
sort order holds since the parts after the initial $5$ are at most $4$
($r - 1 \le 2$, and $3 < 4$ in the $r=0$ case); lengths: $\ell(\sigma) =
t + [r \ge 2]$ resp. $t$, in all cases $\le \lceil k/4 \rceil \le n$;
$\ell(\mu) = \lceil k/4 \rceil \le n$. (iii) Prefix sums: for $i \le t$
(resp. $\le t-1$ in the $r=0$ case) the $\sigma$-prefix is $4i + 1 > 4i =
\mu$-prefix; at the common final index the prefixes both equal $k$; in
the $r \ge 2$ cases $\sigma$'s last part is smaller but the *total* is what
the final prefix sees, and one checks directly:
$r=2$: $\sigma = (5,4^{t-1},1)$, $\mu = (4^t,2)$ — prefixes match
$4i+1$ vs $4i$ through $i = t$, then both $= 4t + 2$ at $i = t+1$;
$r=3$ analogously with $1,2$ vs $2,3$ final excess; $r = 0$: at $i = t$
both are $4t$. (ii)–(iv) done: in all cases every prefix of $\mu$ is
$\le$ the corresponding prefix of $\sigma$, with equality only at the
final index. $\blacksquare$ [proved]

**Remark F.3.a** (the witness recovers the birth law). At $k = 5$ ($t=1,
r=1$): $\sigma = (5)$, $\mu = (4,1)$ — and indeed $b_{(5)}(n) =
\binom{n+4}{5} - n$, the document's birth "maturation" value; the witness
generalizes it to all rungs. [proved]

**Remark F.3.b** (machine certificate). The witness was verified
symbolically-and-exactly through the engine for **every** $(n, k)$ with
$n = 2..12$, $5 \le k \le 4n$: dominance (prefix inequalities), $K_{\sigma
\mu} > 0$ (exact GT count), $C_\mu(n) > 0$ — **ALL PASS**, plus engine
spot-checks: interior positivity for $k \le \min(4n, 11)$ ALL PASS and
closure $P_{4n+1}, P_{4n+2}, P_{4n+3} = 0$ for $k \le 26$ ALL PASS
(`closed_laws.txt`, F.3 block). [cert]

---

## 5. Theorem F.4 — the closed-law atlas

**Method (and an honesty note).** By Theorem F.1 the value functions *are*
polynomials of degree $\le 2k$, so their Newton forward forms through the
$2k+1$ exact points $n = 1 .. 2k+1$ (coefficients $c_j = \Delta^j
P(1)/j!$, evaluation $P(m) = \sum_j c_j\, \mathrm{falling}(m-1, j)$) *are*
the value functions — this is interpolation uniqueness, not an extra
conjecture. The machine work therefore serves two strictly different
purposes: (α) **certification of the engine**: the Newton form must
reproduce the engine on fresh points $n = 2k+2 .. 4k+1$ ($2k$ points);
(β) **exhibit** the closed forms and verify their top coefficients
against the *independent* RSK computation of Theorem F.2 — a nontrivial
cross-check, since the Newton coefficients come from one algorithm
(Kostka b-law + hook-square) and the constants from another
(hook-length/RSK combinatorics). [cert]

**Theorem F.4.** *For each entry of the atlas, the exact Newton form has:*
$\mathrm{self\text{-}fit}$ on calibration points, equality with the engine
on all fresh certification points, and $n^{2k}$-coefficient equal to the
RSK constant of Theorem F.2.* — ALL PASS in all 14 entries
(`closed_laws.txt`).*

**The atlas** (top coefficients from the run; $P$-rungs $6..10$ and
$\mathrm{live}$-rungs $5..9$ with $k = 9, 10$ new in this Phase):

| entry | deg | fresh pts | top coefficient ($n^{2k}$) | RSK constant |
|---|---|---|---|---|
| $\mathrm{ledger}(5,n)$ | 10 | 10 | 119/14400 | $(\sum_{\mu_1\le4} f^2)/(5!)^2 = 119/14400$ ✓ |
| $\mathrm{ledger}(6,n)$ | 12 | 12 | 347/259200 | 694/720² = 347/259200 ✓ |
| $\mathrm{ledger}(7,n)$ | 14 | 14 | 2291/12700800 | 4582/5040² = 2291/12700800 ✓ |
| $\mathrm{ledger}(8,n)$ | 16 | 16 | 2777/135475200 | 33324/40320² = 2777/135475200 ✓ |
| $\mathrm{live}(5,n)$ | 10 | 10 | 1/120 | $1/5!$ ✓ |
| $\mathrm{live}(6,n)$ | 12 | 12 | 1/720 | $1/6!$ ✓ |
| $\mathrm{live}(7,n)$ | 14 | 14 | 1/5040 | $1/7!$ ✓ |
| $\mathrm{live}(8,n)$ | 16 | 16 | 1/40320 | $1/8!$ ✓ |
| $\mathrm{live}(9,n)$ | 18 | 18 | 1/362880 | $1/9!$ ✓ |
| $P_6(n)$ | 12 | 12 | 13/259200 | 26/720² ✓ |
| $P_7(n)$ | 14 | 14 | 229/12700800 | 458/5040² ✓ |
| $P_8(n)$ | 16 | 16 | 583/135475200 | 6996/40320² ✓ |
| $P_9(n)$ | 18 | 18 | 6317/8230118400 | 101072/362880² ✓ |
| $P_{10}(n)$ | 20 | 20 | 44941/411505920000 | 1438112/3628800² ✓ |

The full Newton forms (falling-factorial basis at $n = 1$) are recorded
machine-readably in `closed_laws.txt`; for example
$$P_{10}(m) = \tfrac{44941}{411505920000}\,\mathrm{falling}(m-1,20) +
\tfrac{9497}{391910400}\,\mathrm{falling}(m-1,19) + \cdots$$
with 20 further terms (leading two shown; the $c_0, c_1$ terms vanish since
$P_{10}(1) = P_{10}(2) = 0$ by the zero law F.3 — indeed all $P_r$, $r \le
4$, vanish at $m = 1$).

**Observation F.4.a** (degrees, again). Every entry has the maximal
degree $2k$ predicted by Theorem F.1 — no entry degenerates; consistent
with Theorem F.2's positive leading coefficients.

**Observation F.4.b** (low-order zeros, exact — all three families).
The row/column-cap mechanism gives a uniform minimal-column law: for
every $k \ge 5$ and each of the three functions $g \in \{\mathrm{live},
\mathrm{ledger}\} \cup \{P_k\}$,
$$g(k, m) = 0 \text{ exactly for } m = 1, \dots, \lfloor (k-1)/4 \rfloor,
\qquad g(k, m) > 0 \text{ for } m \ge m_0 := \lceil k/4 \rceil.$$ [proved + cert;
for $P_k$ this is Theorem F.3; for $\mathrm{live}$ it is structural — an
$n\times n$ matrix with rows $\le 4$ cannot carry total $k > 4n$; and at
$m \ge m_0$ the content $\mu = (4^{\lfloor k/4\rfloor}, r)$ fits and
gives a nonzero square. For $\mathrm{ledger}$ the same content provides a
nonzero term since an SSYT of shape $\mu$ with content $\mu$ exists
($\mu \trianglerighteq \mu$).] In Newton terms, with $v = g(k, m_0) > 0$:
$c_j = 0$ for $j \le m_0 - 2$ and $c_{m_0 - 1} = v/(m_0-1)! \ne 0$, so the
first nonzero Newton coefficient of **every** atlas entry sits at level
$j = \lceil k/4 \rceil - 1$. Check against the printed forms: the
degree-$20$ form for $P_{10}$ begins with
$(1971/2)\cdot\mathrm{falling}(m-1,2) = P_{10}(3)/2$ ($m_0 = 3$, level
$j = 2$), and the same level $\lceil k/4 \rceil - 1$ opens
$\mathrm{live}$ and $\mathrm{ledger}$ forms. The zero mechanism and the
Newton data agree on every sampled point. [cert]

---

## 6. Extended pre-registration: rungs 9–11 at columns $n = 36..40$

`pre_register2.py` / `pre_register2.txt`, extending `pre_register.py`
(Phase 2) and the document's own verified range (through $n = 35$, with a
stray pre-registered print at $n = 36$). Every line is internally asserted
against the engine:

**(6.1) One-row maturation law** $b_{(k)}(n) = \sum_{j \ge 0}
(-1)^j \binom{n}{j}\binom{n + k - 5j - 1}{k - 5j}$ for $k = 5..9$ at $n =
36..40$ — matches the engine's $b_\sigma((k), n)$ in all $25$ cells
[cert]; the document verified this law for $n = 4..26$.

| $n$ | $b_{(5)}$ | $b_{(6)}$ | $b_{(7)}$ | $b_{(8)}$ | $b_{(9)}$ |
|---|---|---|---|---|---|
| 36 | 657 972 | 4 495 092 | 26 954 352 | 144 704 817 | 705 969 472 |
| 37 | 749 361 | 5 244 417 | 32 198 103 | 176 894 484 | 882 781 705 |
| 38 | 850 630 | 6 095 010 | 38 292 410 | 215 177 755 | 1 097 868 070 |
| 39 | 962 559 | 7 057 531 | 45 349 200 | 260 517 075 | 1 358 283 875 |
| 40 | 1 085 968 | 8 143 460 | 53 491 880 | 313 998 295 | 1 672 170 240 |

**(6.2) Rung totals** $P_9, P_{10}, P_{11}$ (square-count $p(k) - p_4(k) =
12, 19, 29$ shapes $\sigma_1 \ge 5$; all shapes present, i.e. every
$b_\sigma > 0$, at $n = 36$ — consistent with positivity F.3 far beyond its
witness obligation) [cert]:

| $n$ | $P_9(n)$ | $P_{10}(n)$ | $P_{11}(n)$ |
|---|---|---|---|
| 36 | 11 391 597 974 214 155 518 784 | 2 014 928 565 165 590 890 560 120 | 296 986 558 980 657 956 793 729 120 |
| 37 | 18 477 309 157 602 179 926 070 | 3 455 751 044 697 537 065 658 194 | 538 533 693 269 019 625 214 962 106 |
| 38 | 29 593 147 711 977 752 918 720 | 5 843 447 717 453 716 955 691 242 | 961 348 960 636 187 287 343 424 368 |
| 39 | 46 829 880 029 755 735 213 509 | 9 748 890 092 136 728 969 711 379 | 1 690 794 223 093 278 199 417 227 408 |
| 40 | 73 264 642 972 143 010 960 000 | 16 058 028 236 920 252 224 723 328 | 2 932 007 986 933 198 494 031 984 000 |

Each row was asserted three ways: $\sum_{\sigma_1 \ge 5} b_\sigma^2 = P_k(n)
= \mathrm{live}_B(k,n) - \mathrm{ledger}(k,n)$ — the square-count law and
the defining law agree digit-exactly at all $15$ new $(k, n)$ points.
Full per-shape square decompositions ($12 + 19 + 29$ squares per column)
are in `pre_register2.txt`.

**Fingerprints at $n = 40$** (for future audits): largest square
$P_9$: $\sigma = (5,2,1,1)$; $P_{10}$: $(5,3,1,1)$; $P_{11}$: $(5,3,2,1)$;
smallest: the one-row $(k)$ — newborn-rung pattern of Phase 2 persists.

**(6.3)** Consistency with the atlas: $P_9, P_{10}$ here are the same
functions as Theorem F.4's Newton forms. The fresh-point windows are $n =
20..37$ ($k = 9$) and $n = 22..41$ ($k = 10$); so the $P_{10}$ values at $n
= 36..40$ and the $P_9$ values at $n = 36, 37$ lie inside certified windows
— while the $P_9$ values at $n = 38, 39, 40$ are direct engine
computations agreeing with the law $P_9 = \sum_{\sigma_1 \ge 5}b^2 =
\mathrm{live} - \mathrm{ledger}$, hence (unique-interpolation, F.1) with
the $P_9$ polynomial itself; $P_{11}$ has no Newton form yet (out-of-scope
register, §8). [cert]

---

## 7. What this gives the VHC program

[program] In Notes D–E the model's "variational" behaviour — the
harmless/ledger share vs. the syzygy squares per rung — was tabulated
inductively, rung by rung and column by column, with falsifiable
pre-registrations. Phase 4 converts that inductive picture into closed
form:

1. **Exact degree.** The variational defect is a polynomial of degree
   exactly $2k$ (Theorems F.1, F.2) — not merely "eventually polynomial":
   the exact Newton forms and their certified fresh-point behaviour leave
   no inductive residue for $k \le 10$.
2. **Frozen constants.** The $n \to \infty$ shares are exact rationals
   built from SYT counts $f_\sigma$ over shapes $\sigma_1 \ge 5$
   (Theorem F.2e, table in §3). The Phase-3 "density table" and slot
   counts ($1, 2, 4, 7, 12$ for $k = 5..9$, plus $19$ at $k = 10$) are the
   $n$-transients of a frozen representation-theoretic constant: the model
   remembers only $\sum_{\sigma_1 \ge 5} f_\sigma^2 / (k!)^2$ at infinity.
3. **Exact closure.** The zero law $P_k = 0$ on $k \le 4$ and $k \ge 4n+1$
   with constructive interior positivity (Theorem F.3) is the complete
   "shape of the variational window" — the model's analogue of the
   window in which a VHC-type statement can even be formulated.
4. **VHC reading.** For the actual variational Hodge conjecture the
   message is calibrated caution: the model's variational pattern is fully
   deterministic and commutative-algebra-flavored (squares of Kostka
   data), i.e. the model can only *model* the bookkeeping of variational
   defects, not their geometry. The two genuinely open gates from Note E
   remain: (G-T1) weight-graded limit comparison and (G-Detect)
   detection of the defect by a computable invariant. What F adds is that
   any candidate detection functional should itself have a **frozen
   leading constant** of RSK type in a family of degenerations; a,
   detection scheme whose asymptotic share varies with the degeneration
   parameter is, by the model's law, modeling the wrong quantity.
   [program]

---

## 8. Out-of-scope register

* **Rungs $k \ge 11$ beyond $n = 40$**: only the decomposition rows (§6.2)
  and the theorem-level statements cover these; no Newton forms were
  computed for $k \ge 11$ (cost: $P_{11}$'s $\mathrm{live}_B$ rung costs
  minutes/column; $k \ge 12$ grows fast).
* **Columns $n \ge 41$**: not pre-registered; the maturation row (§6.1)
  covers through $n = 40$ only.
* **$\mathrm{live}$ for $k \ge 10$ at scale**: Route-B reach is comfortable
  to $k = 10$, $n \le 41$ (the whole F.4 run: < 2 min); the $k = 20$
  regime remains the ~30 min/column deep-water zone used in the Phase-2
  power audits.
* **Geometric glue.** Nothing here touches the actual geometry; the
  model↔geometry dictionary of Note E (Props. E.1–E.4, Thms. E.5/E.7/E.9)
  is the standing interface, and the VHC gates G-T1/G-Lim/G-Detect remain
  open. This note's contribution is that the model side of that interface
  is now closed-form and exactly certified.
* **The 42 SKIP entries** of the Phase-2 audit (families outside engine
  reach: $k > 20$ chains, $n > 40$ columns) remain out of reach; they do
  not overlap the present theorems.

---

*Companion files: `ledger/closed_laws.py`, `ledger/closed_laws.txt`
(F.2/F.3/F.4 + Newton forms), `ledger/pre_register2.py`,
`ledger/pre_register2.txt` (§6). Upstream: Note D
(`03-ledger-verification.md`) for the b-law, square-count law, T-identity,
birth law; Note E (`04-paths-to-vhc.md`) for the VHC program and model
calibration.*
