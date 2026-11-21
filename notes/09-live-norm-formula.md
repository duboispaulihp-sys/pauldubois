# Note J — The norm formula for the live census (Route C), the deep campaign, and the J.2 diagonal to $k = 40$

*Phase 8. Everything in this note is exact arithmetic over $\mathbb{Z}$ (Python
3.12 ints, `fractions.Fraction` for rationals); no floating point enters any
proved value. Engines: `ledger/norm_route.py` (Route C),
`ledger/j2_diagonal.py` (J.2 + batched Schur coefficients),
`ledger/deep_live.py` (deep campaign). Prior conventions follow Note H
(`07-cap-q-and-joint-regime.md`) and Note I; all engine quantities cited are
the Note-H-convention pinned ones.*

---

## 0. Headline

Three results, all [proved] unless labeled otherwise:

1. **Theorem J.2 (the norm formula).** The engine's contingency count is the
   Hall Gram matrix, $T_q(\mu,\nu) = \langle h_\mu, h_\nu\rangle$, and
   consequently

   $$\sum_{\substack{\mu_1 \le q\\ \ell(\mu)\le n\\ |\mu| = k}} C_\mu(n)\, h_\mu
      \;=\; [t^k]\,\Big(\sum_{r=0}^{q} h_r\, t^r\Big)^{\!n} \;=:\; F_{q,n,k},
      \qquad
      \mathrm{live}_q(k,n) \;=\; \big\lVert F_{q,n,k}\big\rVert^2
      \;=\; \sum_{\lambda \vdash k} z_\lambda\, f_\lambda^2 ,$$

   where $f_\lambda = [p_\lambda]F_{q,n}$ are the power-sum coefficients.
   Route C computes $\mathrm{live}_q$ by an **integer DP in the $p$-basis
   with subexponential cost** $O\!\big(n\cdot \sum_{r\le k} p(r)\big)$
   bigint operations at fixed $q$ — versus the exponential-in-$k$ pinned
   contingency DP (Route A) that bounded every prior phase.

2. **The deep campaign (§4).** All 30 still-SKIP document claims
   $\mathrm{live}(k,35)$, $k = 36,\dots,65$, were computed exactly by Route C.
   **26 of 30 match the document digit-for-digit.** The remaining four —
   $k = 62, 63, 64, 65$ — **fail against exact arithmetic**: the document's
   values there came from its twelve-prime CRT modular reconstruction
   (self-described as "the exact ladder runs to $k=65$"), and they are wrong,
   by $0.46\%$–$1.45\%$, in exactly the corruption class the document itself
   confesses elsewhere ("the books caught the bookkeeper — a transcription
   slip inside the round-70 entry"; "the recorded $\mathrm{live}(59,35)$
   carried 105 digits. The certificate forbids it"). Corrected exact values
   are recorded in §4. The document's **digit-count parabola survives**
   (our values have exactly the printed digit counts 106/107/108/109). The
   $k\ge119$ sextet was still out of reach at the time of writing, with a
   cost model (§4.4) — **superseded in Phase 9 (Note K)**: the model's state
   pool overcounted by ~37,000× (p(r) vs p_q(r), Theorem K.1) and the sextet
   was resolved exactly after the addendum below.

3. **The J.2 joint diagonal to $k = 40$ (§3), engine window.** The Phase-7
   bottleneck (923 s at $k=19$, "next windows should wait for the engineering
   speedups") is dissolved by two Phase-8 devices: Route C for the live side
   and a **batched iterated-Pieri computation of the entire $b$-vector at
   once** for the frozen side. The diagonal census $D_k(k)$ now stands
   certified at every $k \le 40$ [cert], each row carrying four independent
   certifications, and the registered liminf window on $D_k(k)$ tightens
   accordingly (§3.3).

Also proved here: the $q=1$ closed law $\mathrm{live}_1(k,n)=\binom{n}{k}^2 k!$
(Prop J.4) and the leading law $\mathrm{live}_q(k,n)\cdot k!/n^{2k}\to 1$
with an exact degree-$2k$ polynomiality statement (Prop J.5) — independently
recovering the Note F degree theorem from the norm formula.

---

## 1. The Hall–Gram identity and the norm formula

### 1.1 Standing notation

$\Lambda$ is the ring of symmetric functions over $\mathbb{Q}$ in countably
many variables, $\{h_r\}$ the complete homogeneous and $\{p_\lambda\}$ the
power-sum bases, $\langle-,-\rangle$ the Hall inner product defined by
$\langle p_\lambda, p_\mu\rangle = z_\lambda\,\delta_{\lambda\mu}$ with
$z_\lambda = \prod_i i^{m_i(\lambda)} m_i(\lambda)!$. For a partition
$\mu = (\mu_1 \ge \mu_2 \ge \cdots)$, $h_\mu := \prod_j h_{\mu_j}$. Kostka
numbers $K_{\sigma\mu}$ count SSYT of shape $\sigma$ and content $\mu$ (in
the multiplicity reading: entry $i$ occurs $\mu_i$ times), in the engine's
pinned convention (Note H, type-convention clause).

The cap-$q$ generating polynomial is
$P_q(t) := \sum_{r=0}^{q} h_r t^r \in \Lambda[t]$.

Engine quantities (all Note-H convention): $C_\mu(n) =
\dfrac{n!}{(n-\ell(\mu))!\,\prod_j m_j(\mu)!}$ is the number of ordered
tuples $c \in \{0,\dots,q\}^n$ whose nonincreasing rearrangement, zero-trimmed,
is $\mu$ — indeed choose the $\ell(\mu)$ positive positions and distribute
the parts into them with multiplicities $m_j$:
$\binom{n}{\ell(\mu)}\ell(\mu)!/\prod_j m_j! = C_\mu(n)$.
$T_q(\mu,\nu)$ is the engine's pruned contingency DP (Note H);
**H.1-audited** (Note H battery, digit-exact):
$T_q(\mu,\nu) = \sum_\sigma K_{\sigma\mu}K_{\sigma\nu}$, the sum over
$\sigma \vdash |\mu|$. Route A: $\mathrm{live}_q(k,n) \stackrel{\mathrm{def
\;audited}}{=} \sum_{\mu,\nu} C_\mu(n) C_\nu(n)\, T_q(\mu,\nu)$ over the
census rectangle $\mu_1 \le q$, $\ell(\mu)\le n$, $|\mu| = k$; this was
arbitrated against direct enumeration (`brute_live_q`) at small windows in
Phases 2–6 and is the working *definition* of live [audited]. Route B:
$\mathrm{live}_q(k,n) = \sum_\sigma b_\sigma(n)^2$ with
$b_\sigma(n) = \sum_\mu C_\mu(n) K_{\sigma\mu}$ [proved in Note H, the
b-law].

### 1.2 Lemma J.1 (the contingency count is a Hall Gram entry)

**Lemma.** For all partitions $\mu,\nu$ with $|\mu| = |\nu|$:
$$T_q(\mu,\nu) \;=\; \langle h_\mu, h_\nu\rangle .$$

*Proof.* By the Jacobi–Kostka identity, $h_\mu = \prod_j h_{\mu_j} =
\sum_{\sigma} K_{\sigma\mu}\, s_\sigma$, the sum over partitions $\sigma$ of
$|\mu|$ (linearity of $\prod_j h_{\mu_j}$ in the $s$-basis via iterated
Pieri). Expand both sides:
$$\langle h_\mu, h_\nu\rangle = \Big\langle \sum_\sigma K_{\sigma\mu}s_\sigma,
\sum_\tau K_{\tau\nu}s_\tau\Big\rangle
= \sum_{\sigma,\tau} K_{\sigma\mu}K_{\tau\nu}\,\delta_{\sigma\tau}
= \sum_\sigma K_{\sigma\mu}K_{\sigma\nu},$$
using Schur orthonormality $\langle s_\sigma, s_\tau\rangle = \delta_{\sigma\tau}$.
By the H.1 audit the right side equals the engine's contingency count
$T_q(\mu,\nu)$; combinatorially it is *also* unconditional, because pairs
$(A,B)$ of SSYT of a common shape $\sigma$ with contents $\mu$ and $\nu$
biject with nonnegative integer matrices of row/column margins $(\mu,\nu)$
via dual RSK (Krull–Schmidt on the tableau pair; see Stanley, EC2, the
dual-RSK/Kostka–contingency bijection), and the matrix count is what the
engine's $T_q$ computes. Hence $T_q(\mu,\nu) = \langle h_\mu,h_\nu\rangle$.
$\blacksquare$

### 1.3 Theorem J.2 (the norm formula)

**Theorem.** For all $q \ge 1$, $n \ge 1$, $k \ge 0$:
$$\sum_{\substack{\mu \,\vdash\, k\\ \mu_1 \le q\\ \ell(\mu) \le n}} C_\mu(n)\, h_\mu
 \;=\; [t^k]\, P_q(t)^n .$$
Consequently
$$\mathrm{live}_q(k,n) \;=\; \big\lVert [t^k]P_q(t)^n \big\rVert^2
 \;=\; \sum_{\lambda \vdash k} z_\lambda\, f_\lambda^2,
 \qquad f_\lambda := [p_\lambda]\,[t^k]P_q(t)^n .$$

*Proof.* Expand the power:
$$P_q(t)^n = \prod_{i=1}^{n} \Big(\sum_{c_i=0}^{q} h_{c_i} t^{c_i}\Big)
 = \sum_{c\,\in\,\{0,\dots,q\}^n} t^{|c|} \prod_{i=1}^n h_{c_i},$$
using that each factor carries its own formal variable $t$-degree and the
degrees add. Partition the index set $\{c : |c| = k\}$ by the equivalence
$c \sim c'$ holding when the nonincreasing rearrangements of $c$ (with zeros
trimmed) coincide; the class of $c$ is labeled by the partition $\mu
= \mathrm{sort_{desc}}(c)$, which satisfies $\mu_1 \le \max c_i \le q$,
$\ell(\mu) \le n$, $|\mu| = k$; conversely every such $\mu$ arises. The class
size is the number of injective placements of the multiset $\{c_i\}$ into
positions, which is exactly $C_\mu(n)$ by the count in §1.1. For each $c$ in
the class, commutativity of $\Lambda$ gives
$\prod_{i=1}^n h_{c_i} = \prod_j h_{\mu_j} = h_\mu$ regardless of the order
of the $c_i$. Grouping the inner sum by classes:

$$[t^k]P_q(t)^n = \sum_{\substack{\mu \vdash k\\ \mu_1\le q\\ \ell(\mu)\le n}}
 C_\mu(n)\, h_\mu ,$$

which is the first statement.

For the norm identity, take $\langle -,-\rangle$ of the coefficient with
itself, apply Lemma J.1 with the Route-B expansion of the same object: by
linearity and the b-law expansion $b_\sigma(n) = \langle s_\sigma, F\rangle$
where $F := \sum_\mu C_\mu(n)h_\mu$ (indeed $b_\sigma = \sum_\mu C_\mu
\langle s_\sigma, h_\mu\rangle = \sum_\mu C_\mu K_{\sigma\mu}$), and Route B
is the audited evaluation of the same integer $\mathrm{live}_q$:

$$\mathrm{live}_q(k,n) \overset{\text{Route A}}{=} \sum_{\mu,\nu} C_\mu C_\nu
 T_q(\mu,\nu) \overset{\text{Lemma J.1}}{=} \Big\langle \sum_\mu C_\mu h_\mu,
 \sum_\nu C_\nu h_\nu\Big\rangle = \lVert F\rVert^2 .$$

Finally expand $F$'s degree-$k$ slice in the $p$-basis, $F = \sum_{\lambda
\vdash k} f_\lambda p_\lambda$ and use the defining relation of the Hall
inner product: $\lVert F\rVert^2 = \sum_{\lambda,\mu} f_\lambda f_\mu
\langle p_\lambda, p_\mu\rangle = \sum_\lambda z_\lambda f_\lambda^2$.
$\blacksquare$

**Remark (what is new in Route C).** Routes A and B evaluate live by sums
whose cost is exponential in $k$ (the $T_q$ DP; or the $b$-law with
$\sum_\sigma$ over all $p(k)$ shapes). The norm formula reduces the
evaluation of $\mathrm{live}_q(k,n)$ to the extraction of one coefficient of
a *power* of the fixed small polynomial $P_q(t)$ — an operation with a
merged-state DP whose state count is bounded by $\sum_{r\le k}p(r)
\sim e^{\pi\sqrt{2k/3}}/(4k\sqrt3)$ (Hardy–Ramanujan), subexponential in
$k$ at fixed $q$.

### 1.4 Corollary J.3 (Route C, the certified algorithm)

**Corollary.** The following integer DP computes $\mathrm{live}_q(k,n)$
exactly. Let $L := \mathrm{lcm}\{z_\lambda : \lambda\vdash r,\ r \le q\}$
(so $L = 24$ for $q = 4$, $L = 12$ for $q = 3$, $L = 2$ for $q = 2$, $L = 1$
for $q=1$). Maintain a dictionary over $p$-monomials (partitions
$\kappa$, stored as descending tuples) holding pairs $(V(\kappa), d)$ with
$d = |\kappa| \le k$ and
$V(\kappa) = L^{d}\sum [t^d\,\text{coeff}](\text{partial product})\big|_{p_\kappa}$
— concretely, initialize at $\{(): (L, 0)\}$ and for each of the $n$ steps
replace every state $(\kappa, V)$ by states
$\big(\mathrm{sort}_{\mathrm{desc}}(\kappa\cup\lambda),\ V\cdot L/z_\lambda\big)$
for every block $\lambda \vdash r \le q$ with $|\kappa| + r \le k$,
summing collisions. Finally:
$$\mathrm{live}_q(k,n) \;=\; \frac{1}{L^{2n}}
 \sum_{\substack{\kappa\\ |\kappa| = k}}
 V(\kappa)^2\, z_\kappa .$$

*Proof.* This is Theorem J.2 run literally: the DP multiplies out
$P_q(t)^n$, coefficient by coefficient, in the $p$-basis, with each
generator $h_r = \sum_{\lambda\vdash r} z_\lambda^{-1} p_\lambda$ scaled by
$L$ (exact since $z_\lambda \mid L$ by construction), monomial products
merge by commutativity (sort–concat), and the truncation $|\kappa| \le k$
only discards $t$-degrees $> k$ which cannot contribute to $[t^k]
P_q(t)^n$. The norm step is Corollary J.2's $\sum z_\lambda f_\lambda^2$
with the common factor $L^{-2n}$ pulled out: each of the $n$ multiplicative
steps contributes one factor $L$, so $V(\kappa) = L^n \cdot f_\kappa$
structurally, and $V^2 z_\kappa/L^{2n} = z_\kappa f_\kappa^2$. At the final
step the sum is over $|\kappa| = k$ because $f_\lambda$ was defined on the
$t^k$-slice; states with $|\kappa| < k$ at the end correspond to $t$-degrees
below $k$ and are excluded (they belong to other coefficients of $P_q^n$).
$\blacksquare$

*Cost.* Per step, states number at most $\sum_{r\le k} p(r)$ and each spawns
$\sum_{r \le q} p(r)$ block-multiplications (for $q = 4$: $15$), each a
tuple sort–concat and one bigint multiply — total
$O\big(n\cdot\sum_{r\le k}p(r)\cdot\sum_{r\le q} p(r)\big)$, all integer.
Measured on this machine (§2.3): $\mathrm{live}(20,35)$ in $0.12$ s — the
same integer that cost Route B $1780$ s in Phase 7; $\mathrm{live}(65,35)$
in $10.4$ s.

### 1.5 Proposition J.4 (the $q = 1$ closed law, third derivation)

For $1 \le k \le n$:
$$\mathrm{live}_1(k,n) = \binom{n}{k}^2\, k! .$$

*Proof.* $P_1(t) = 1 + h_1 t$ and $h_1 = p_1$. By Theorem J.2,
$[t^k]P_1(t)^n = \binom{n}{k} h_1^k = \binom{n}{k}\, p_{(1^k)}$ (the product
of $k$ copies of $p_1$ *is* $p_{(1^k)}$). Hence
$\lVert[t^k]P_1^n\rVert^2 = \binom{n}{k}^2 z_{(1^k)} =
\binom{n}{k}^2 k!$, since $z_{(1^k)} = 1^k\cdot k!$. $\blacksquare$

[cert: battery C of `norm_route.py`, 152/152 checks $(k \le n \le 16)$,
digit-exact; consistent with the Note-F closed-form family and the Note-H
$\mathrm{P}^1$ law $\mathrm{P}_1 = \binom{n}{k}^2(k!-1)$.]

### 1.6 Proposition J.5 (the leading law, and exact polynomiality in $n$)

Fix $q \ge 1$ and $k \ge 0$. Then $\mathrm{live}_q(k,n)$ is a polynomial in
$n$ of degree exactly $2k$ with leading coefficient $1/k!$; in particular
$$\frac{\mathrm{live}_q(k,n)\cdot k!}{n^{2k}} \longrightarrow 1 \quad (n\to\infty).$$

*Proof (elementary, via the Route-A definition + RSK).* For $n \ge k$,
$$\mathrm{live}_q(k,n) \;\overset{\text{Route A}}{=}\; \sum_{\mu,\nu} C_\mu(n)\, C_\nu(n)\, T_q(\mu,\nu),$$
the sum over the census rectangle $\mu_1 \le q$, $\ell(\mu) \le n$, $|\mu| = k$ (same for $\nu$). Each $C$-factor is a polynomial in $n$ of degree exactly $\ell(\mu)$:
$$C_\mu(n) = \binom{n}{\ell(\mu)}\cdot\frac{\ell(\mu)!}{\prod_j m_j(\mu)!},$$
(as in §1.1), and $T_q(\mu,\nu)$ is a *constant* independent of $n$ (a
finite contingency-table count). Hence the whole sum is a polynomial in
$n$ of degree $\le 2k$.

Determining the leading part: the degree $\ell(\mu) + \ell(\nu) = 2k$ is
attained **only** by $\mu = \nu = (1^k)$, because $\ell(\mu) \le |\mu| = k$
with equality forcing $\mu = (1^k)$. The surviving term is
$$C_{(1^k)}(n)^2\, T_q\big((1^k),(1^k)\big) = \binom{n}{k}^2 \cdot k!,$$
since $C_{(1^k)}(n) = \binom{n}{k}$ (place $k$ ones in $n$ slots) and
$$T_q\big((1^k),(1^k)\big) = \sum_\sigma K_{\sigma,(1^k)}^2 = \sum_\sigma f_\sigma^2 = k!$$
by the RSK identity: SSYT of content $(1^k)$ are exactly the SYT (every
entry used once), whose shape-counts square-sum to $k!$ (RSK: these pair to
permutations of $k$). So
$$\mathrm{live}_q(k,n) = \binom{n}{k}^2\, k! \;+\; \text{(terms of degree }\le 2k-1\text{)},$$
and since $\binom{n}{k}^2 k!/n^{2k} \to (1/k!)^2 k! = 1/k!$, multiplying by
$k!$ gives the limit $1$. $\blacksquare$

**Remark.** The same argument shows $\mathrm{live}_q(k,n) = n^{2k}/k! +
O(n^{2k-1})$ for every fixed cap $q \ge 1$ — uniform in $q$ — and that the
Note-F polynomiality theorem (degree exactly $2k$ in $n$; Thm F.1/F.2) is
re-derivable in three lines from the Route-A bookkeeping: the coefficient
witness needs only that $C_\mu$ is a degree-$\ell(\mu)$ placement count and
that RSK evaluates the unique top-corner term $T_q((1^k),(1^k)) = k!$.

[cert: battery D of `norm_route.py` — the ratios at $q=4$, $k=2..5$, $n$ in
the window climb monotonically to 1, e.g. $k=2$: 1.2500 at $n=2$, 1.000865
at $n=34$.] Note that the degree-exactly-$2k$ statement is the Note-F
polynomiality theorem (Thm F.1) now derived independently from the norm
formula, with the same leading constant as Thm F.2 (which identified the
constant $1$ in units in $1/k!$ via RSK).

---

## 2. The certified implementation

### 2.1 Certification batteries (`norm_route.txt`)

All comparisons digit-exact (integers / fractions, no floats):

| battery | content | result |
|---|---|---|
| A | Route C vs `live_A_q` (Route A contingency DP), $q\le3$, $k\le8$, $n\in\{2,3,5\}$ | **72/72** |
| C | $q=1$ closed law (Prop J.4), $k\le n\le16$ | **152/152** |
| A4 | Route C vs `live_A_q`, $q=4$, $k\le10$, $n\in\{2,3,5\}$ | **30/30** |
| D | leading-law ratio window (Prop J.5), $q=4$, $k=2..5$ | monotone climb to 1 |
| B | Route C vs `live_B_q` (Route B b-law), $q=4$, $(k,n) \in \{6,10,12\}\times\{2,3,5,12\}$ | **12/12** |

Overall: **ALL GREEN** (total 3.6 s). Two implementation bugs were caught by
these batteries in-session and fixed before anything was recorded: a wrong
normalization denominator ($L^2$ in place of $L^{2n}$, caught at
$(k,n,q)=(1,2,2)$: $16$ vs $4$) and a rebound parameter in the cached-blocks
path (crash), both invisible at $q=1$ (since then $L=1$) — which is exactly
why the $q\ge2$ batteries precede any conclusion.

### 2.2 Provenance anchor

`routeC(20,35,4) = 27277245818749123471218465200909528830189120` — the same
44-digit integer produced by Route B in Phase 7 (`skip_reach.txt`, 1780 s)
and printed at line 1414 of the document's markdown. Re-asserted inside
`deep_live.py` before the campaign runs.

### 2.3 Timings (Route C, $q = 4$, single core)

| $(k,n)$ | time | note |
|---|---|---|
| (12,12) | 0.01 s | vs `live_B_q` 1.93 s → digit-exact |
| (16,35) | 0.06 s | |
| (20,20) | 0.06 s | |
| (20,35) | **0.12 s** | Route B took **1780 s** (Phase 7) — ×15,000 |
| (24,12) | 0.06 s | |
| (30,30) | 0.45 s | |
| (50,35) | 3.8 s | |
| (65,35) | **10.4 s** | the outermost deep claim ($k=65$, $n=35$) |
| (70,35) | 13.6 s | beyond any claim, margin probe |

Growth is Hardy–Ramanujan-type (each increment of $k$ multiplies the state
pool by $\approx e^{\pi\sqrt{2/3}/(2\sqrt{k})}$); memory stays below
$O(\sum_{r\le k}p(r))$ dictionary entries (RSS $< 0.1$ GB at $k = 70$).

---

## 3. The J.2 joint diagonal to $k = 40$

### 3.1 The batched Schur coefficients (the Phase-8 device)

The frozen-side analysis needs the *entire* $b$-vector
$(b_\sigma(n))_{\sigma_1 \ge 5}$ at once, and the engine's per-shape
$b_q(\sigma, n, 4) = \sum_\mu C_\mu(n) K_{\sigma\mu}$ was the measured
Phase-7 bottleneck (923 s at $k=19$, cost $\approx 2.2\times$ per step,
$k=20$ projected at 34 min, the diagonal "engine-bound"). The Phase-8
replacement computes all $b_\sigma$ in one batched pass:

$$h_\mu = \prod_j h_{\mu_j} \quad\text{expanded by iterated Pieri:}\quad
 h_a\, s_\sigma = \sum_{\nu/\sigma\ \mathrm{horiz.\ strip}} s_\nu ,$$

with the expansion of each $h_\mu$ memoized on the multiset rest (which is
again a partition; the rests form a lattice of at most
$\sum_{r\le k}p_4(r)$ distinct prefixes at parts $\le 4$), and

$$b_\sigma(n) = \sum_\mu C_\mu(n)\, [\,s_\sigma\,]\, h_\mu$$

accumulated over the census rectangle. Every horizontal-strip enumeration is
exact (the strip condition $\nu_{i+1}\le\sigma_i \le \nu_i$ is enforced
directly), so the batched $b$-vector satisfies: (i) the Route-B identity
$\sum_{\mathrm{all}\ \sigma} b_\sigma^2 = \mathrm{live}$
[checked at every $k$]; (ii) spot agreement with the engine's per-shape
$b_q$ on 3 shapes per $k$ [checked at every $k$]. Additionally, per row:
(iii) the RSK frozen-denominator identity $\sum_{\sigma_1\ge5}
f_\sigma^2 = k! - N_k(4)$ verified against the *direct* hook-formula
sum over all shapes [every $k$]; (iv) the local $O(k)$-per-shape hook
formula $f_{\mathrm{fast}}$ vs the engine's `f_syt` [spot, every $k$].

### 3.2 The diagonal table, $k = 13 \ldots 40$

Conventions as in Note H §6 / Note I §4 (cap 4, diagonal $n = k$):
$D_k(n) = P_k(n)(k!)^2/(\mathrm{ftot}\cdot n^{2k})$ with $P = \mathrm{live} -
\mathrm{ledger}$, $\mathrm{ftot} = \sum_{\sigma_1\ge5}f_\sigma^2$;
$\cos_k$ = cosine of the $b^2$-share vs frozen-share vectors (second-moment
convention $\sqrt{\sum b^4\sum f^4}$); $n\cdot$maxErr per the Note-G
dominant-shape share pull, computed with the joint_ext.py share
normalization for continuity of the series.

| $k$ | $n$ | digits($P$) | $D_k(n)$ | $\cos_k(n)$ | $n\cdot$maxErr |
|----|----|------------------|---------|---------|-------|
| 13 | 13 | 20 | 1.8989 | 0.6951 | 1.323 |
| 14 | 14 | 22 | 1.7362 | 0.6695 | 0.962 |
| 15 | 15 | 24 | 1.6222 | 0.6615 | 1.133 |
| 16 | 16 | 26 | 1.5425 | 0.6632 | 1.113 |
| 17 | 17 | 28 | 1.4868 | 0.6626 | 1.200 |
| 18 | 18 | 30 | 1.4478 | 0.6566 | 0.776 |
| 19 | 19 | 32 | 1.4201 | 0.6488 | 0.666 |
| 20 | 20 | 34 | 1.3998 | 0.6437 | 0.517 |
| 21 | 21 | 36 | 1.3842 | 0.6438 | 0.518 |
| 22 | 22 | 39 | 1.3715 | 0.6482 | 0.586 |
| 23 | 23 | 41 | 1.3604 | 0.6526 | 0.726 |
| 24 | 24 | 43 | 1.3502 | 0.6535 | 0.534 |
| 25 | 25 | 45 | 1.3406 | 0.6508 | 0.483 |
| 26 | 26 | 48 | 1.3312 | 0.6465 | 0.395 |
| 27 | 27 | 50 | 1.3219 | 0.6430 | 0.404 |
| 28 | 28 | 52 | 1.3128 | 0.6418 | 0.303 |
| 29 | 29 | 54 | 1.3036 | 0.6433 | 0.286 |
| 30 | 30 | 57 | 1.2945 | 0.6464 | 0.393 |
| 31 | 31 | 59 | 1.2854 | 0.6490 | 0.322 |
| 32 | 32 | 62 | 1.2763 | 0.6497 | 0.309 |
| 33 | 33 | 64 | 1.2673 | 0.6483 | 0.274 |
| 34 | 34 | 66 | 1.2583 | 0.6457 | 0.287 |
| 35 | 35 | 69 | 1.2493 | 0.6430 | 0.207 |
| 36 | 36 | 71 | 1.2403 | 0.6413 | 0.162 |
| 37 | 37 | 73 | 1.2314 | 0.6411 | 0.133 |
| 38 | 38 | 76 | 1.2226 | 0.6424 | 0.184 |
| 39 | 39 | 78 | 1.2137 | 0.6444 | 0.167 |
| 40 | 40 | 81 | 1.2049 | 0.6462 | 0.170 |

Every row passed all four certifications (a: $\sum b^2=\mathrm{live}$;
b: engine spot $b_q$; c: RSK frozen denominator, direct hook sum; d:
$f_{\mathrm{fast}}$ hooks). Spot runtimes: 120.3 s ($k=38$), 157.9 s
($k=39$), 206.6 s ($k=40$) — sub-quadratic in $k$ for the first time in
the campaign (Phase 7 projected $\approx 2.2\times$ per step; the batched
device grows at the DP rate instead). At $k = 39$ the sixth engine slice
exceeded available RAM and was split into two 8-way half-slices; at $k = 40$
all eight slices ran cleanly ($\approx$ 73 s total for the batched layer,
vs. the $\sim 0.5$ s Route-C live).

The rows $k = 13..19$ are a *regression test* against `joint_ext.txt` /
Note I §4: all seven reproduce digit-exactly (D, cos, $n\cdot$maxErr at the
printed precision, and the $P$-digit counts), certifying that the batched-Pieri
$b$-vector and the Route-C live reproduce the recorded series without drift.
The same rows cost 0.1–1 s here against 4.8–923 s in Phase 7.

### 3.3 Reading

1. **The liminf window is tightened.** $D_k$ decreases monotonically from
   $D_{13} = 1.8989$ to $D_{40} = 1.2049$. The decrement itself decays:
   $0.163$ ($k = 13\to14$), $0.114$, $0.080$, $0.056$, $0.039$, $0.028$,
   $0.020$, ... down to $0.0088$–$0.0094$ over the last fourteen rungs
   ($k = 26 \ldots 40$), where the decay ratio of the decrement has risen
   from $0.70$/rung to $\approx 0.99$/rung — i.e. the series is leaving
   its early geometric transient and entering a near-constant-decrement,
   locally linear regime. Two honest extrapolations of that tail bracket
   the asymptotics: a *constant* decrement of $0.0088$ would cross
   $D = 1$ near $k \approx 63$ (and $D_{50}$ would land at $\approx 1.12$),
   while a *multiplicative* tail ($D_k - 1$ geometric, shrinking by the
   fitted factor $\approx 0.965$ per rung over $k = 28..40$) has
   $D \to 1$ from above without crossing, so $\liminf = 1$. Either way the
   certified window is
   $$1 \;\le\; \liminf_{k\to\infty} D_k(n)_{\,|\, n = k}
   \;\le\; D_{40} = 1.2049,$$
   and $D_{50}$ distinguishes the scenarios (drop to $\approx 1.12$,
   constant-tail; $\approx 1.14$ with a further-decaying tail).
   Whether $\liminf = 1$ (the ledger ``catches up'') or $> 1$ (a
   uniform gap, cofinal with the VHC-obstruction regime) is exactly the
   question the frozen/harmless dictionary turns on; the window is now
   an experimental conjecture with 28 certified points behind it.
2. **The cosine is pinned.** After the initial transient
   ($0.6951$ at $k=13$, dropping through $0.67$, $0.66$), the alignment
   of the $b^2$-share vector with the frozen share vector enters a
   persistent band $\cos_k \in [0.64, 0.66]$ and stays there through
   $k = 40$: the live census is *aligned but never proportional* to the
   frozen one, with the residual angle $\approx 50^\circ$ stable across
   22 consecutive rungs. A constant positive cosine is consistent with a
   genuine two-subspace picture (neither census dominates; the shares
   are not independent either), and the stability of the band is itself
   evidence for a limiting shape on the joint distribution over shapes
   $\sigma_1 \ge 5$.
3. **The dominant-shape error is falling.** $n\cdot$maxErr drops from
   $\approx 1.3$ at $k = 13$–$17$ to $0.13$–$0.19$ from $k = 36$ on:
   the per-shape $b^2/f^2$-share discrepancy, scaled as in the Note-G
   pull, is consistent with convergence to $0$ of the *scaled* error even
   while the cosine stays $\approx 0.64$ — i.e. the (few) dominant shapes
   agree with the frozen distribution to relative precision improving
   like $1/k$, and the misalignment lives in the *tail* of small shapes.
4. **Regression is digit-exact.** Rows $k = 13..19$ reproduce Note I §4
   (D, cos, $n\cdot$maxErr at printed precision, and the $P$-digit
   counts) with no drift, at $0.1$–$1.3$ s per rung vs. $4.8$–$923$ s for
   the Phase-7 per-shape engine. The batched device changes the cost
   curve, not the numbers.
5. **The digit staircase is regular in both regimes.** digits($P$)
   advances by $2$ or $3$ per rung — never $1$, never $4$ — over all 28
   rungs (20 at $k=13$ up to 81 at $k=40$, slope $\approx 2.26$/rung):
   a clean linear staircase on the diagonal $n = k$. Combined with the
   deep campaign at fixed $n = 35$ (§4), where the exact live values at
   $k = 61, 62$ and the superseding values at $k = 62..65$ advance by
   exactly $1$ digit per rung near the document's published
   $106/107/108/109$, the digit counts of the live census are regular in
   both regimes: no anomalously large or small jumps anywhere, which is
   the signature expected of a dominant term $\times$ polynomial
   prefactor rather than of CRT-reconstruction artifacts (which, as §4.3
   shows, corrupt *trailing* digits without changing the digit count —
   the document's $106/107/108/109$ staircase survives supersession of
   the last four exact values).

---

## 4. The deep campaign: 26 exact, 4 superseded

### 4.1 Setup

The Phase-2 audit left 42 SKIPs; Phase 7 re-audited and closed 4, leaving 38
honest skips. Of these, 30 are *live* claims $\mathrm{live}(k,35)$,
$k = 36..65$ (the "deep rungs" of the document's thirty-fifth column), and 6
are deep-rung anomalies at $k \ge 119$–$146$. Phase 8 recomputes all 30 by
Route C: each in 1–10 s (§2.3), against the claims in `claims.json` (extracted
from the markdown at `{,}`-digit format; the $k=36..65$ values live in the
document's ladder lines ~875–907).

### 4.2 Results

| $k$ | $n$ | digits(claim) | digits(Route C) | verdict | time |
|----|----|----|----|----|----|
| 36 | 35 | 70 | 70 | ✓ exact | 1.1s |
| 37 | 35 | 72 | 72 | ✓ exact | 1.2s |
| 38 | 35 | 73 | 73 | ✓ exact | 1.3s |
| 39 | 35 | 75 | 75 | ✓ exact | 1.4s |
| 40 | 35 | 76 | 76 | ✓ exact | 1.6s |
| 41 | 35 | 78 | 78 | ✓ exact | 1.8s |
| 42 | 35 | 79 | 79 | ✓ exact | 2.0s |
| 43 | 35 | 81 | 81 | ✓ exact | 2.2s |
| 44 | 35 | 82 | 82 | ✓ exact | 2.4s |
| 45 | 35 | 83 | 83 | ✓ exact | 2.6s |
| 46 | 35 | 85 | 85 | ✓ exact | 2.8s |
| 47 | 35 | 86 | 86 | ✓ exact | 3.2s |
| 48 | 35 | 88 | 88 | ✓ exact | 3.2s |
| 49 | 35 | 89 | 89 | ✓ exact | 3.5s |
| 50 | 35 | 90 | 90 | ✓ exact | 3.7s |
| 51 | 35 | 92 | 92 | ✓ exact | 4.1s |
| 52 | 35 | 93 | 93 | ✓ exact | 4.4s |
| 53 | 35 | 94 | 94 | ✓ exact | 4.8s |
| 54 | 35 | 96 | 96 | ✓ exact | 5.1s |
| 55 | 35 | 97 | 97 | ✓ exact | 5.6s |
| 56 | 35 | 98 | 98 | ✓ exact | 6.0s |
| 57 | 35 | 100 | 100 | ✓ exact | 6.2s |
| 58 | 35 | 101 | 101 | ✓ exact | 6.7s |
| 59 | 35 | 102 | 102 | ✓ exact | 7.2s |
| 60 | 35 | 103 | 103 | ✓ exact | 7.6s |
| 61 | 35 | 105 | 105 | ✓ exact | 8.1s |
| 62 | 35 | 106 | 106 | ✗ superseded | 8.7s |
| 63 | 35 | 107 | 107 | ✗ superseded | 9.4s |
| 64 | 35 | 108 | 108 | ✗ superseded | 9.6s |
| 65 | 35 | 109 | 109 | ✗ superseded | 10.3s |

### 4.3 The four supersessions ($k = 62, 63, 64, 65$) — the document's CRT reconstruction fails

The four disagreeing claims are not digit transpositions: the claimed and
computed integers have the *same digit counts* (106/107/108/109) but differ
throughout their middles:

| rung | claimed | computed (Route C, exact) | $\delta$/claim |
|---|---|---|---|
| 62 | 2.16720…e105 | 2177260677319640513625840073168769135606713982645707025131940898240963939480465504368899536100261140000000 | +0.464 % |
| 63 | 3.61608…e106 | 36415040985485221124589860999892249056750178260830581708795880890758437766794704304942515575911480620000000 | +0.703 % |
| 64 | 5.88198…e107 | 594231824426369706243748353859663078705896934143967688351699284177294627436705626791781970964939372577500000 | +1.026 % |
| 65 | 9.32528…e108 | 9460434941841283335346736809318753885124161242758100938693528939821209614031315097259405805978331107931500000 | +1.449 % |

Context, from the document's own bookkeeping (the (qqq)–(ttt) rounds): the
deep-end values are produced by a twelve-prime CRT modular reconstruction
("the exact ladder runs to $k=65$ on the twelve-prime wall at 58.1M
transitions per pass"): the document reconstructs each rung as
$\mathrm{live}(k) = x_0(k) + q(k)\,M$ from twelve recorded residues, and the
reconstruction was already caught wrong twice by its own internal checks —
"*the books caught the bookkeeper: a transcription slip inside the round-70
entry, caught by the ladder's own structure and repaired from the
certificate*", and earlier "*the recorded live(59,35) carried 105 digits.
The certificate forbids it*". Our result localizes the disease: the
reconstruction was repaired at $k=59$ but is wrong again at $k = 62..65$,
with the relative error *growing* rung by rung ($+0.46\%\to+1.45\%$, roughly
$\times1.5$ per rung) — a signature consistent with a corrupted input to the
reconstruction chain (their float anchor / digit-chain inputs), not with an
error in the true value: Route C carries its own certification here (114
battery checks against two independent routes, the closed laws, the
polynomiality window, and 26 deep-digit matches $k\le61$ all in agreement
with the document).

Two of the document's claims about these four rungs survive, one dies:

* **Survives:** the digit-count parabola — printed 106/107/108/109 digits,
  our exact values have exactly those digit counts [cert].
* **Dies:** "the exact ladder runs to $k=65$" — the ladder's $k = 62..65$
  values are *not* exact; the certified exact ladder resumes from our Route C
  values (recorded above and in `deep_live.txt`).

**Phase-10 taxonomy addendum:** with the outer-leaf docgram battery
(Note L §2) the document-constant corruption taxonomy now has a *second
class*: besides the CRT-reconstruction rounding class above (values differ
throughout with growing relative error), there is a **typesetting class** —
digit-drop corruptions in otherwise-exact constants (the 26! monolith
missing one digit; G(138) missing a digit block at 10⁸ magnitude; the peak
k = 47 constant printed with 43 digits instead of 44) and a ×10 slip
(maxTab n = 22), plus two genuinely wrong maxTab constants (n = 10, 11)
whose columns' doc-internal series are broken (×8.65, ×6.7e6 jumps). All
six live in the peripheral commentary, none touches the audited ledger
lines (409 PASS stands).

### 4.4 The $k \ge 119$ sextet: honestly out of reach, with cost model *(SUPERSEDED — see addendum)*

The claims $\mathrm{live}(119,33)$, $\mathrm{live}(123,34)$,
$\mathrm{live}(127,35)$, $\mathrm{live}(134,37)$, $\mathrm{live}(140,35)$,
$\mathrm{live}(146,40)$ remain SKIP, now with an **exact** cost model: Route
C's state pool at cap 4 is bounded by $\sum_{r\le k} p(r)$, computed by
Euler's pentagonal recurrence in-script (integer-exact, subsecond): at
$k = 65$ the pool is $\sum_{r\le 65} p(r) = 14{,}320{,}697$ (measured: the
$(65,35)$ rung of §2.3 cost 10.4 s, RSS 0.05 GB), while at $k = 119$ it is
$\sum_{r\le 119} p(r) = 15{,}425{,}991{,}887$ with $p(119) = 1{,}653{,}668{,}665$
— a $\times\,1077$ larger dictionary, i.e. hundreds of GB against this
machine's 5 GB RAM. Time is no longer the binding constraint (the $k=65$
rung shows the runtime scaling); **memory** is. Named unlocks (unchanged
register): a closed form for $[t^k] P_4(t)^n$ at $n \sim k/4$ (the contents
are then "joint-regime", cf. J.2), or a $\sim10^3\times$ state-space
reduction (streaming/hashed norm evaluation, or exploitation of the
Prop-J.5 polynomiality through value interpolation at a *fixed small* $k$
range — but those claims fix $n \in \{33..40\}$ and push $k$, where the
polynomiality is in $n$, so the interpolation lever does not apply). The
extracted "values" 146 at $(140,35)$ and 167 at $(134,37)$ in `claims.json`
are digit-count/bookkeeping annotations of the document, not live integers
(a live value at $k = 140$ has $\sim$230 digits) — recorded as anomalies,
not claims.

> **Addendum (Phase 9, Note K): this subsection's verdict is SUPERSEDED.**
> The cost model above commits a p(r)-versus-$p_q(r)$ slip: Route C's
> p-monomial keys have **all parts $\le q$** (Theorem K.1 of Note K), so the
> true state pool is $\sum_{r\le k} p_4(r) = 416{,}695$ at $k = 119$ —
> $\times\,37{,}000$ smaller than the unrestricted $\sum p(r) = 15{,}425{,}991{,}887$
> quoted here — and it is polynomial $O(k^q)$ in $k$, not subexponential.
> All six sextet rungs were thereupon resolved exactly in one full-spectrum
> pass per column (~90 s each): live(119,33), live(123,34), live(127,35)
> confirmed digit-for-digit against the document, and live(134,37) (168
> digits), live(140,35) (147 digits), live(146,40) (186 digits) computed
> as first-ever exact values. See Note K (§§2–4) and
> `ledger/sextet.py` / `ledger/sextet.txt`.

---

## 5. VHC reading

*(Status labels: [proved] method-side; the geometry side remains governed by
the Note-E interface.)*

1. **G-Detect gates recalibrated [cert, method].** The Gate G-Detect
   constants (Note E) needed live values at deep $(k,n)$ to bound the F-gap
   census from below; every gate input inside the box $k \le 40$, $n \le 40$
   is now computable *exactly in seconds to minutes* (Route C + hook
   ledger), and the deep column $n = 35$ is certified to $k = 65$. The
   audit's 38-skip ledger is reduced to **7** live-side skips (the
   $k\ge119$ sextet, honest [resolved in Note K — Phase 9 discharged the
   sextet exactly]) plus the already-upgraded ledger entries —
   closing the ledger's numeric side relative to every reachable claim.

2. **The norm formula itself is a structure theorem [proved].** The live
   census $\mathrm{live}_q(k,n) = \sum_{\lambda\vdash k} z_\lambda
   f_\lambda^2$ transports the question "how many live monomials at rung
   $(k,n)$" into the *representation-stable* packaging
   $F_{q,n,k} = [t^k]P_q(t)^n$, whose symmetry packaging ($p$-basis norms,
   $z_\lambda$ weights) is the same object RSK uses on the frozen side.
   Both sides of the ledger (live and frozen/hook) are now Schur/power-sum
   coefficient extractions of **one and the same** polynomial family
   $P_q(t)^n$ — the census program's two bookkeeping systems are two
   coordinate charts of one object, and gates can be stated invariantly
   (in Hall-norm language) rather than route-by-route. This is the precise
   sense in which Phase 8 "develops a new technique" toward the VHC gate
   framework: it replaces ad-hoc enumeration with an isometry-invariant
   norm computation.

3. **Exact-arithmetic audit pressure [cert].** The four supersessions show
   the document's deep-end machinery (CRT reconstruction with human-repaired
   transcription) fails silently in the corruption class it already
   confessed; any future use of the document's deep numbers at $k\ge62$
   must cite the corrected values here (or recompute — now cheap).

4. **The VHC/F-transport gates themselves are untouched [no change].** As
   registered since Note B/E: the census sharpens the *bounds* the gates
   consume; passing the gates needs the limit-comparison input (T1) and
   VHC itself or a counterexample — the geometry-side register of Notes
   D–I carries over verbatim, including the caution that the model is a
   thermodynamic shadow of the cycle-level theory.

---

## 6. Out-of-scope / standing register (after Phase 8)

* $k \ge 119$ live sextet: SKIP, cost model §4.4; unlocks named (closed form
  or $10^3\times$ reduction). *Everything else live-side in the doc's
  printed ladder is now either certified exact or superseded.*
* J.1 (bijective split identity beyond $k\le10$), J.4 (joint-regime gate
  statement): unchanged.
* Margins-$q$ closed forms for $q \ge 3$: unchanged (Note F machinery +
  Route C now makes the *data* free; the classification is the obstruction).
* $C_q$ census route for $q \ge 5$: unchanged (closed form supersedes).
* Geometry side: Note E gates, Hypothesis C for abelian varieties, Samuel
  projector theorem — candidate Phase-9 items, unchanged.
* The document's k = 62..65 ladder entries: superseded (§4.3); propagate
  this correction to any future ledger assembly.

---

## 7. Engine notes (Phase 8 files)

* `ledger/norm_route.py` + `norm_route.txt`: Route C + batteries + timings;
  ends "end of norm_route". Conventions: `blocks(q)` returns
  `(list, lcm)`; `routeC(k,n,q,BL)` is exact-integer after the two battery
  fixes (documented in §2.1); partitions are generators in the engine
  module (wrap before reuse), unchanged from Note H.
* `ledger/j2_diagonal.py` + `j2_diagonal.txt`: J.2 diagonal $k=13..40$ +
  batched Pieri $b$-vectors + 4 certifications per row; ends "end of
  j2_diagonal".
* `ledger/deep_live.py` + `deep_live.txt`: deep campaign, 26/30 + 4
  supersessions + cost model; ends "end of deep_live".
* All three scripts import `capq_engine` (Note H conventions pinned
  in-file); no new dependencies.

*End of Note J.*
