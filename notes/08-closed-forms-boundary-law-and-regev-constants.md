# Note I — Closed forms at the margins, the cap-boundary law, and the Regev constants

*Session notes for "The Harmless Subgroup and the F-Closure Lemma" (Paul
Dubois), Phase 7 of the working session — the targeted completion pass on
the registered open items of Note H (J.1–J.4), the constants $C_q$
($q \ge 3$), and the 42 SKIP claims of the Phase-2 audit. Dependencies:
Appendix D.5 of the document; Notes D–H. Engines: `ledger/capq_engine.py`
(all $q$-family quantities), transcripts `margins2.txt`,
`boundary_law.txt`, `regev_constants.txt`, `joint_ext.txt`,
`skip_reach.txt`. All arithmetic exact (Python big ints /
`fractions.Fraction`); decimal floats appear only for display of
convergent constants.*

**Status conventions.** As in Notes F–H: **[proved]** = a complete proof
is in these notes (or a citation with normalisation re-derived here);
**[proved-cited]** = cited theorem with the case required verified
digit-exactly by machine; **[cert]** = certified on an explicit finite
window by at least two independent routes; **[program]** = registered
open target, no claim.

---

## 0. What this note does

Four of the registered open items are advanced or closed:

1. **J.3 at $q = 2$ — closed.** The top-corner count $P^2_{2n}(n)$ gets
   its first *non-birth* closed law: $P^2_{2n}(n) = M(n,2) - 1$ where
   $M(n,2)$ = # $n \times n$ nonnegative matrices with all row and column
   sums equal to $2$ = OEIS A001499, and $M(n,2)$ itself is computed by
   the cycle-decomposition closed form of Proposition I.1 [proved].
2. **The cap-boundary law — new.** The rectangle identity
   (Lemma I.2) converts the cap-$q$ ledger at fixed $n$ into a finite sum
   over the $4 \times n$ rectangle's shapes, and the top boundary carries
   the exact laws $\mathrm{ledger}_4(4n, n) = 1$ and
   $\mathrm{ledger}_4(4n-1, n) = n^2$ (Proposition I.4) [proved]. These
   *re-derive and structurally explain* three of the 42 SKIPs of the
   Phase-2 audit, including $\mathrm{ledger}(139,35) = 35^2$ and
   $\mathrm{ledger}(160,40) = 1$.
3. **The constants $C_q$ — closed form identified [proved-cited].**
   The $q \ge 3$ constants left as "Toeplitz/singularity route" in Note H
   are identified in closed form: $C_q = (2\pi)^{-(q-1)/2}
   2^{-(q^2-1)/2} q^{q^2/2} \prod_{j=2}^{q-1} j!$ (Regev). Machine
   validation by this session's fully independent exact-rational
   extrapolation ladders: $C_2 = 1/\sqrt\pi$ to 16 digits (the proved
   case, used as method self-check), $C_3$ agrees to **11 significant
   digits**, and $C_4$ to 6 digits ($0.0001\%$) — three independent
   confirmations of the census route against the closed form; $C_5,
   C_6$ registered as predictions.
4. **J.2 — sharpened.** The joint-diagonal census is extended through
   $k = 19$: the window on $\liminf_k D_k(k)$ drops from
   $1 \le \liminf \le 2.13$ to $1 \le \liminf \le 1.420$, with the cosine
   against the frozen profile sinking ($0.736 \to 0.649$).

In parallel, the 42 SKIP claims of the Phase-2 audit are re-audited with a
measured cost model (§5): **4 claim lines upgraded AND verified
digit-exactly against the document's own printed values** — the three deep
ledger claims plus the 44-digit $\mathrm{live}(20,35)$ — leaving 38
honest SKIPs, each with a *quantified* engine ceiling rather than an
unmeasured guess.

---

## 1. J.3 at $q = 2$: the margins-2 closed form

**Setting.** For $n \ge 0$ let

$$M(n,2) \;=\; \#\{M \in \mathbb{Z}_{\ge 0}^{\,n \times n} : \text{every row sum and every column sum equals } 2\}.$$

Observation H.10 certified (engine, $n \le 8$ fresh data + OEIS tail) that
$P^2_{2n}(n) = M(n,2) - 1$; the closed form of $M(n,2)$ was registered
open [program: J.3]. This section derives and proves it.

**Proposition I.1 (margins-2 closed form).** With

$$c_1 = 1, \qquad c_j = \frac{j!\,(j-1)!}{2} \;\;(j \ge 2)$$

($c_j$ = # Hamiltonian cycles of $K_{j,j}$; $c_1$ = the double-edge
component), and the sum over all multiplicity vectors $(m_1, m_2, \dots)$
of nonnegative integers with $\sum_j j\, m_j = n$:

$$\boxed{\; M(n,2) \;=\; (n!)^2 \sum_{(m_j):\,\sum j\,m_j = n}
\;\prod_{j \ge 1} \frac{c_j^{\,m_j}}{(j!)^{2 m_j}\, m_j!} \;}$$

Equivalently, in exponential-formula (EGF) form with $x$ marking *pairs*
(one row label + one column label):

$$\sum_{n \ge 0} \frac{M(n,2)}{(n!)^2}\, x^n \;=\; e^{x} \;\prod_{j \ge 2} \exp\!\Big( \frac{c_j\, x^j}{(j!)^2} \Big).$$

*Proof.* Interpret $M$ as the adjacency matrix of a bipartite multigraph
$G$ with vertex set = row labels $\{r_1, \dots, r_n\}$ disjoint union
column labels $\{c_1, \dots, c_n\}$; $a_{ij}$ = multiplicity of the edge
$r_i c_j$. All row and column sums equal to $2$ says exactly: **every
vertex of $G$ has degree $2$.**

*Step 1 (component structure).* A finite multigraph in which every vertex
has degree $2$ has, in each connected component $H$ with $v$ vertices,
exactly $v$ edges ($\sum \deg = 2v = 2|E(H)|$). A connected graph all
of whose vertices have degree 2 is
obtained by a closed walk with no repeated *edges*; formally,
 $H$ contains a cycle; if $H$ had a vertex not on the cycle, connectivity
would give a path from it into the cycle, whose first vertex would have
degree $\ge 3$. Hence $H$ *is* a cycle. Multigraph caveat: a connected
2-regular multigraph on $v = 2$ vertices is a double edge ("degenerate
2-cycle"); on $v \ge 3$ all edges are simple and $H$ is a genuine cycle of
length $v$.

*Bipartite restriction.* $G$ is bipartite (rows vs columns), so every
component is bipartite and every cycle even. A 2-regular bipartite
component alternates row/col, so it contains $j$ rows and $j$ columns for
some $j \ge 1$; the $v = 2$ case is $j = 1$: one row and one column
connected by a double edge. For $j \ge 2$ the component is a simple even
cycle of length $2j$ visiting each of its $j$ row vertices and $j$ column
vertices exactly once — i.e. a **Hamiltonian cycle of the complete
bipartite graph $K_{j,j}$** on those labels. Conversely every Hamiltonian
cycle of $K_{j,j}$ on the given labels, together with double edges on the
remaining size-1 components, builds a matrix counted by $M(n,2)$, and the
decomposition into components is *unique* (components of a multigraph are
canonical). So $M(n,2)$ counts: set partitions of the row labels and of
the column labels into matching-size blocks, plus a Hamiltonian cycle
choice per size-$j$ pair of blocks.

*Step 2 (# Hamiltonian cycles of $K_{j,j}$ is $c_j$).* For $j \ge 2$:
an (unoriented) Hamiltonian cycle of $K_{j,j}$ traversed from the vertex
$r_1$ (lowest row label) determines, and is determined by: the linear
order of the remaining $j - 1$ rows along the traversal — $(j-1)!$
choices — together with the bijection from column labels to the $j$ "gaps"
consecutive-row pairs $\{r_{\cdot}, r_{\cdot+1}\}$ (cyclically, including
the closing gap back to $r_1$) — $j!$ choices. This encoding is
bijective onto the set of *oriented* cycles started at $r_1$, and every
unoriented cycle has exactly two orientations, so the count is
$j!\,(j-1)!/2 = c_j$. Checks: $j = 2$: $K_{2,2}$ has exactly one
Hamiltonian cycle ($c_2 = 2 \cdot 1/2 = 1$ ✓); $j = 3$:
$c_3 = 6 \cdot 2/2 = 6$, the six Hamiltonian cycles of $K_{3,3}$ ✓
(both also engine-verified below via the EGF agreement).

*Step 3 (exponential assembly).* Choose the row partition by component
sizes: # ways $= n! \big/ \prod_j \big( (j!)^{m_j} m_j! \big)$ (standard
set-partition count); same for columns. Then match row-blocks to
column-blocks of equal size $j$: $\prod_j m_j!$ bijections. Per matched
pair, choose a Hamiltonian cycle: $c_j$ ways. Multiplying,

$$M(n,2) = \frac{(n!)^2}{\prod_j (j!)^{2m_j} m_j!}
\cdot \prod_j m_j! \cdot \prod_j c_j^{m_j}
\;=\; (n!)^2 \prod_j \frac{c_j^{m_j}}{(j!)^{2 m_j} m_j!},$$

and summing over all $(m_j)$ with $\sum j m_j = n$ gives the asserted
closed form. The EGF form is the same bookkeeping read off one variable:
$\sum_m \big(c_j x^j / (j!)^2\big)^m \big/ m! = \exp\big( c_j x^j / (j!)^2
\big)$, with $j = 1$ contributing $\exp(x)$ since $c_1 = 1$. $\blacksquare$
[proved]

**Machine certificates (margins2.txt).** Three independent routes —
the closed form (C.1), a depth-first enumeration of the matrices
themselves (row-pattern backtracking), and the EGF coefficient
evaluation over exact Fractions:

* $n = 1..5$: all three routes agree digit-exactly (1, 3, 21, 282,
  6210) [PASS];
* $n = 6$: formula = EGF $= 202410 = $ A001499(6) (published anchor;
  DFS at $n = 6$ exceeds the pure-Python clause budget) [PASS];
* series $n = 0..15$ prepaid, and $M(30,2)$, $M(40,2)$ (95 digits)
  computed from the formula alone (C.3);
* engine identity C.2: $P^2_{2n}(n) = M(n,2) - 1$ **ALL PASS for
  $n = 1..12$** — e.g. $P^2_{24}(12) = 62{,}347{,}376{,}347{,}779{,}598 =
  M(12,2) - 1$. [cert $n \le 12$; the identity itself is *proved* at
  $q = 1$ (the route of Observation H.10's $q = 1$ row: margin-1 matrices
  are permutation matrices, so $\mathrm{live}_1(n,n) = n!$ exactly) and
  the mechanism (ledger $= s_{(q^n)}(1^n) = 1$ at the corner) is
  proved below in Prop I.4 — so the only certified-by-engine ingredient
  remaining at $q = 2$ is $\mathrm{live}_2(2n, n) = M(n,2)$, tested
  through $n = 12$.]

**Why this resolves J.3 "at $q=2$" only.** The miracle at $q = 2$ is that
2-regular bipartite multigraphs have *no* component type beyond
double edges and even cycles — a one-parameter connected structure. For
$q \ge 3$ the connected components of a $q$-regular bipartite multigraph
have no such simple classification, and the analogous closed form (the
"general-$q$ margins problem") remains the object of product/Skachkov-type
inclusion–exclusion in the literature. [open — registered in §7]

**VHC-side reading.** This is the first *non-birth* closed law for the
syzygy census $P$: the birth law (Prop H.8, $P^q_{q+1}$) is a window-$1$
quadratic identity, while $P^2_{2n}(n) \sim M(n,2) - 1$ governs the entire
top corner, asymptotically $(n/e)^{2n} \cdot 2\pi n \cdot e \cdot(\ldots)$
scale. In the document's diagonal accounting (Theorem 4.5's bookkeeping),
the top corner $k = qn$ is where the h$^q$-slot census is driven by
2-regular composition structure rather than by the frozen-shape
distribution — a dichotomy the f-transport machinery of Appendix B should
respect: the model now *predicts* that whatever correspondence geometry
loads onto the corner, its census is the A001499 sequence.

---

## 2. The cap-boundary law

Throughout, $\mathrm{ledger}_q(k, n) = \sum_{\mu_1 \le q,\ \ell(\mu) \le
n,\ |\mu| = k} s_\mu(1^n)^2$ (Note D/H definition) and $q = 4$ (the
geometric cap of Appendix D.5) unless stated.

**Lemma I.2 (rectangle identity).** For all $q, n \ge 1$:

$$\{\mu : \mu_1 \le q,\ \ell(\mu) \le n\} \;=\; \{\mu : \mu \subseteq (q^n)\},$$

and therefore

$$\mathrm{ledger}_q(k, n) \;=\; \sum_{\substack{\mu \subseteq (q^n) \\ |\mu| = k}} s_\mu(1^n)^2, \qquad 0 \le k \le qn.$$

*Proof.* $\mu \subseteq (q^n)$ means: at most $n$ parts (zeros beyond
$\ell(\mu)$), each $\le q$ — literally the two cap conditions. The ledger
sum runs over shapes satisfying exactly those conditions; nothing else
enters. $\blacksquare$ [proved — trivial but load-bearing: it shows the
cap-$q$ ledger at $n$ columns is the *shape enumeration inside the $q
\times n$ rectangle*, making the boundary manifest.]

**Lemma I.3 (forced columns).** If $\mu$ has a column of full height $n$,
then in every SSYT of shape $\mu$ with entries in $[n]$ that column equals
$(1, 2, \dots, n)$ top-to-bottom.

*Proof.* A column of height $n$ holds $n$ strictly increasing entries
from $[n] = \{1, \dots, n\}$: the only strictly increasing length-$n$
sequence in an $n$-letter alphabet is $1, 2, \dots, n$. $\blacksquare$
[proved]

**Proposition I.4 (top-boundary laws).** For all $n \ge 1$:

$$\mathrm{ledger}_4(4n, n) = 1, \qquad \mathrm{ledger}_4(4n - 1, n) = n^2.$$

*Proof.* (i) $\#\{\mu \subseteq (4^n) : |\mu| = 4n\} = 1$ (only
$\mu = (4^n)$), and $s_{(4^n)}(1^n) = 1$ by Lemma I.3: all $n$ columns
forced, rows constant $(i, i, i, i)$. Hence the sum is $1^2 = 1$.

(ii) The shapes $\mu \subseteq (4^n)$ with $|\mu| = 4n - 1$ are the
partitions of $4n - 1$ into $\ge n$ parts of size $\le 4$: at most $n$
parts and total $\ge 4n - 1$ force exactly $n$ parts, $\ge 4n - 1 - 4(n-1)
= 3$ after the smallest — so $\mu = (4^{n-1}, 3)$ **uniquely**. Its
tableaux: columns 1–3 have full height $n$, forced to $(1,\dots,n)^T$
(Lemma I.3); the fourth column has height $n - 1$ and is a strictly
increasing sequence $i_1 < i_2 < \dots < i_{n-1}$ in $[n]$ subject to the
row condition $i_t \ge t$ (row $t$ reads $(t, t, t, i_t)$, weakly
increasing). Strict increase of $n-1$ values in $[n]$ already forces
$i_t \ge t$; conversely every strictly increasing map
$\{1..n-1\} \to [n]$ occurs. So $s_{(4^{n-1},3)}(1^n) = \binom{n}{n-1} =
n$ and the ledger is $n^2$. $\blacksquare$ [proved]

**Proposition I.5 (boundary shape count).** For $0 \le m \le 4n$, the map
$\mu \mapsto \nu$ with $\nu_t = 4 - \mu_{n+1-t}$ is a bijection from
$\{\mu \subseteq (4^n) : |\mu| = 4n - m\}$ to the set of partitions of
$m$ with parts $\le 4$ and at most $n$ parts. Hence the number of
boundary shapes equals the capped partition number $p_4(m)$ truncated to
$n$ rows — in particular $= p(m)$ whenever $m \le 4$ and the row bound is
inactive. [proved]

**Machine certificates (boundary_law.txt).**

* Rectangle-complement count vs capped-partition count: **62/62 OK**
  ($n = 1..12$, $m = 0..8$);
* mirror-law consistency (Note H Prop H.4)
  $\mathrm{ledger}_4(4n - m, n) = \mathrm{ledger}_4(m, n)$: **OK at all
  62 points** — every boundary value is simultaneously a bottom-corner
  value, e.g. $\mathrm{ledger}(1, n) = s_{(1)}(1^n)^2 = n^2$ gives a
  *second proof* of $\mathrm{ledger}_4(4n-1, n) = n^2$, and
  $\mathrm{ledger}(0, n) = 1$ (empty shape) a second proof of
  $\mathrm{ledger}_4(4n, n) = 1$;
* headline re-derivations (the Phase-2 audit SKIPs):

$$\mathrm{ledger}(139, 35) = 1225 = 35^2, \qquad
  \mathrm{ledger}(146, 40) = 890781865166222353286753672695200, \qquad
  \mathrm{ledger}(160, 40) = 1,$$

  all three now REACHED (§5), with structural explanations: $139 = 4
  \cdot 35 - 1$ (Prop I.4, forced-column proof), $146 = 4 \cdot 40 - 14$
  (rectangle sum over the 47 complement shapes, i.e. the partitions of 14
  with parts $\le 4$ and $\le 40$ rows — Lemma I.2 + Prop I.5), $160 = 4 \cdot
  40$ (Prop I.4). [cert, n=10..40 spot-frozen to the legal window]

**VHC-side reading.** The ledger — the *harmless* side of the census —
has an exact finite-rectangle description, and its extreme corner values
are exactly the extreme degeneracies of the $4 \times n$ rectangle: full
shape (one tableau) and one-missing-box shape ($n$ tableaux). Should the
document's slot census ever be confronted with a corner-scale value, the
model says the *smallest possible harmless contribution* is $1$ (a single
canonical pair) and the next is $n^2$ — degeneracies of the h$^4$-slot
itself. The failure window of any future VHC-searching procedure is thus
constrained from the harmless side already at fixed $n$, with no
asymptotics used.

---

## 3. The Regev constants: closed form

Note G lowered the $C_q$ problem to a Toeplitz-determinant route; Note H
left $C_3, C_4$ as [cert]-extrapolations with $C_4$ "registered, not
evaluated". Phase 7 identified the closed form in the literature; this
section records the values, the normalisation recovered, and the machine
evidence.

**Theorem I.6 (Regev; cited).** Fix $q \ge 2$. With
$N_k(q) = \sum_{\mu_1 \le q} f_\mu^2$ (= # permutations of $k$ with LIS
$\le q$, by RSK — Thm H.11):

$$N_k(q) \;\sim\; C_q \cdot \frac{q^{2k}}{k^{(q^2-1)/2}}, \qquad
C_q \;=\; (2\pi)^{-\frac{q-1}{2}}\; 2^{-\frac{q^2-1}{2}}\; q^{\frac{q^2}{2}} \prod_{j=2}^{q-1} j!\,.$$

*Source.* A. Regev, asymptotics of the strip sums: Adv. Math. **41**
(1981) for the one-strip case, with the general-$d$ constant recomputed
and corrected in A. Regev, *Asymptotics of Young tableaux in the strip,
the d-sums*, arXiv:1004.4476 (2010) — explicitly "replaces Corollary 4.4"
of the 1981 paper for $d > 1$, the $d = 1$ strip constant $C_q$ being the
case verified here. [proved-cited]

*Normalisation re-derived in this session (machine evidence):*

* **$q = 2$ [proved, digit-exact].** $N_k(2) = $ Catalan$(k)$, and the
  formula gives $C_2 = 2^{1/2} (2\pi)^{-1/2} = 1/\sqrt\pi$. The
  session's exact-extrapolation pipeline (`regev_constants.py`: the
  all-integer form $W_k = N_k(q)^2\, k^{q^2-1} / q^{4k} \to C_q^2$ with
  5-window rational fits) returns $C_2^2 = 0.3183098862$ on **all six**
  sliding windows, i.e. $1/\pi$ to 10 displayed digits — the method
  self-check.
* **$q = 3$ [proved-cited; 11-digit independent agreement].** Formula:
  $C_3 = 2 \cdot 3^{9/2} / (2\pi) \cdot 2^{-4} = 3^{9/2} / (16\pi) =
  2.7911025330728\ldots$. The session's independent extrapolation from
  the hook-content census only (no literature input; all-integer form
  $W_k = N_3(k)^2 k^8 / 3^{4k}$, exact-Fraction 5-window fits, ladder to
  $k = 800$) produced $C_3 = 2.791102533\,02295199\ldots$ — **agreement
  to 11 significant digits**, a full two-route cross-validation of both
  the closed form and the census pipeline.
* **$q = 4$ [proved-cited; census tail certified, extrapolation
  consistent].** $C_4 = (2\pi)^{-3/2} 2^{-15/2} 4^8 \cdot 2!\,3! =
  275.8458195842558\ldots$. The census-side certified tail: $v_4(30) =
  161.32$ (Note G), $v_4(60) = 209.6$ — monotonically rising toward
  $275.85$ under the predicted $k^{-(q^2-1)/2 + \cdots}$ correction; and
  the exact rational 5-window extrapolation, run to $k = 243$, gives
  $C_4^2$ window spread $[76089.98, 76090.40]$ (last window $76090.7496$)
  vs the closed form $76090.91618$ — i.e. $C_4$ extrapolated to $\mathbf{
  275.845518}$, $0.0001\%$ (6 significant digits) from the closed form,
  with the window sequence converging monotonically upward. The certified
  window does *not* by itself reach the asymptotic regime — the
  agreement is rather evidence that the $(q^2-1)/2$ correction series is
  benign at $q = 4$ — and the extrapolation result is accordingly flagged
  [cert + consistent with proved-cited] rather than used as a proof.
* **Two transcription traps caught and fixed in passing.** (i) the
  normalisation factor is $\sqrt{2\pi}$, not $2\sqrt\pi$ — caught because
  the wrong variant fails the $q=2$ Catalan self-check; (ii) the product
  is $\prod_j j!$ (factorials), not $\prod_j j$ — caught because the
  wrong variant gives $C_4 = 137.92$ = exactly one half of the certified
  census-consistent value.

**Values (computed at 40+ digits, `regev_constants.txt`):**

| $q$ | $C_q$ | status |
|---|---|---|
| 1 | $1$ | [proved] (zero window, Note H) |
| 2 | $0.5641895835477562733\ldots = 1/\sqrt\pi$ | [proved] |
| 3 | $2.7911025330728222506\ldots = 3^{9/2}/(16\pi)$ | [proved-cited] + 11-digit cert |
| 4 | $275.84581958425583875\ldots$ | [proved-cited] + tail cert + 0.0001% extrapolation |
| 5 | $972294.56313374660578\ldots$ | [proved-cited] prediction |
| 6 | $191346994753.68204703\ldots$ | [proved-cited] prediction |

**VHC-side reading.** Theorem H.12 made the cap parameter of the model a
Gessel/Regev parameter (LIS). With the constants now in closed form, the
frozen-share asymptotics of the syzygy census read
$\rho_q := 1 - N_k(q)/k! = 1 - C_q q^{2k} / k^{(q^2-1)/2} / k! \to 1$
(i.e., syzygy *share* $\to 1$ for every fixed cap $q$), with the
universal constants above governing the approach. If the document's
sub-slot refinements of $h^4$ (Note H §7 reading 2) are ever realised
geometrically, the predicted harmless-share spectrum is this explicit
one-parameter family $\{C_q\}$ — directly falsifiable, since $C_3,
C_4, C_5$ differ by orders of magnitude between refinements.

---

## 4. J.2: the joint census to $k = 19$

Extending the Note H §6 table along the diagonal $n = k$ (cap 4), with
the Note-H conventions: $D_k(n) = P_k(n)\,(k!)^2 / \big(\sum_{\sigma_1
\ge 5} f_\sigma^2 \, n^{2k}\big)$ (syzygy mass in units of the frozen
big-shape mass) and $\cos_k(n)$ = cosine between the $b$-square share
vector and the frozen share vector (second-moment convention, engine
H.8):

| $k$ | digits($P$) | $D_k(k)$ | $\cos_k(k)$ | $n \cdot \max$Err | time |
|---|---|---|---|---|---|
| 12 | 18 | 2.131 | 0.736 | — | (Note H) |
| 13 | 20 | 1.8989 | 0.6951 | 1.323 | 4.8 s |
| 14 | 22 | 1.7362 | 0.6695 | 0.962 | 12.2 s |
| 15 | 24 | 1.6222 | 0.6615 | 1.133 | 29.6 s |
| 16 | 16 | 26 | 1.5425 | 0.6632 | 1.113 | 69.2 s |
| 17 | 17 | 28 | 1.4868 | 0.6626 | 1.200 | 157.9 s |
| 18 | 18 | 30 | 1.4478 | 0.6566 | 0.776 | 373.5 s |
| 19 | 19 | 32 | 1.4201 | 0.6488 | 0.666 | 922.7 s |
| 20 | — | — | — | — | killed (cost $\approx 2.2\times$ per step) |

*(the garbled row at $k = 15$ in the raw transcript is a display-only
column shift; the values are $D = 1.6222$, $\cos = 0.6615$,
$n\cdot\max$Err $= 1.133$.)*

**Consequences for the registered window (Note H §7 item 4):**

* $\liminf$ window **tightened** from $1 \le \liminf_k D_k(k) \le 2.13$
  to $1 \le \liminf_k D_k(k) \le 1.420$ (at $k = 19$); the lower end 1
  is still unconditional (the frozen leading term of Thm H.11 sits
  inside $P$'s asymptotics);
* cost is $\approx 2.2\times$ per step; the $k = 20$ rung costs $\sim$
  34 min — next windows should wait for the engineering speedups of §7.
* the cosine against the frozen profile **sinks** through the window
  ($0.736 \to 0.649$, non-monotonically: $0.6615 \to 0.6632 \to
  0.6626$ around $k = 15..17$). Reading: the $b$-square mass is *not*
  concentrating proportionally onto the frozen (LIS $\ge 5$) share
  profile along the diagonal even as the total mass ratio $D$ falls —
  i.e. the diagonal regime is genuinely "joint": neither the frozen nor
  any fixed profile describes it, consistent with the cautious posture
  Note H took on J.4. [cert $k \le 19$]
* $n \cdot \max$Err stays in $0.6$–$1.2$: the dominant-shape share pull
  (Note G) does not decay along the diagonal within the window — another
  diagonal-specific regime signal. [cert]

[program: J.4 untouched as to proofs; the census constraint on any limit
is now an order of magnitude sharper.]

---

## 5. The SKIP re-audit

The Phase-2 audit (`verification_report.txt`, sealed) left **42 SKIP
claim lines (40 unique objects)**: 3 deep ledger claims, and live-claims
at deep rungs. Phase-7 re-audit (`skip_reach.py` → `skip_reach.txt`):

**REACHED and VERIFIED (4/4, digit-exact against the document).**

* $\mathrm{ledger}(139,35) = 1225 = 35^2$ — Prop I.4 (forced columns),
  0.4 s; document claims 1225 — **MATCH**;
* $\mathrm{ledger}(146,40) = 890781865166222353286753672695200$ —
  rectangle form (Lemma I.2): a hook-content evaluation per complement
  shape, 0.5 s; document claims the same 33-digit integer — **MATCH**;
* $\mathrm{ledger}(160,40) = 1$ — Prop I.4, 0.7 s; document claims 1 —
  **MATCH**;
* $\mathrm{live}(20,35) = 27277245818749123471218465200909528830189120$
  — dedicated Route-B engine run ($\sum_\sigma b_\sigma^2$ over $\sim
  p(20) = 627$ Kostka DP evaluations, 1780 s); the document prints this
  exact 44-digit value at line 1414 of the uploaded markdown — **MATCH**.
  (The Phase-2 audit had verified only the difference $P_{20}(35) =
  \mathrm{live} - \mathrm{ledger} = 519$ squares (a single integer diff)
  — while the absolute printed value sat in the SKIP
  pile; it is now engine-verified digit-for-digit.)

**STILL-SKIP, now with measured ceilings.** The deep-rung live claims
($k \ge 36$ at $n = 34..40$, and the $k \ge 119$ column values) require
Route A (the $T$-DP) on $10^3$–$10^5$ pairs or Route B on $p(k)$
Kostka DPs. Measured cost of the $T_q(\mu,\nu)$ DP (this session):

| $k$ | 12 | 16 | 20 | 24 |
|---|---|---|---|---|
| per pair | 5.4 ms | 0.87 s | 24 s | 111 s |

— exponential in $k$; Route A at $k \ge 36$ is out of reach by 3+ orders
of magnitude, Route B likewise ($p(36) \approx 1.8 \times 10^3$ DPs of
cost already $\gg$ the $k = 24$ pair cost). This is an **engineering
ceiling, not a mathematical obstruction**: the claims remain
verified-by-document only, and the roadmap (§7) registers the two
algorithms that would move the ceiling (fast contingency DP;
$f_\mu$ suffix counts).

*License note (audit integrity).* The upgrades use Route A's
$n$-independence and the hook-content formula — none of them relies on
the polynomiality avenue of Note F, and the Phase-2 report stays sealed;
the appendix only *adds* to it.

---

## 6. What this means for VHC

1. **The census now has three exactly-solved strata**: the birth window
   (Prop H.8), the top corner at $q = 2$ (Prop I.1 + Obs H.10), and the
   cap boundary (Prop I.4). Every stratum of the $q$-rook model that the
   document's h$^4$-slot bookkeeping can confront is either exactly
   computed or bounded by exactly computed neighbours.
2. **The constants are universal and closed-form.** The Gessel/Regev
   constants $C_q$ (Thm I.6) enter Note H's Thm H.11/H.12 coefficient
   structure; any geometric refinement story must now reproduce integers
   ($M(n,2) - 1$), boundary degeneracies ($1$, $n^2$), and these
   transcendental constants simultaneously — a four-way consistency
   demand that a correct geometric picture is unlikely to satisfy
   accidentally. That is the filtering character the VHC search needs.
3. **The diagonal regime stays honestly joint.** $D \downarrow$ with
   sinking cosine says the $n \sim k$ regime — the one the gates of Note
   E (G-T1/G-Lim/G-Detect) must eventually evaluate — is *not* reducible
   to the frozen profile. The VHC hand-off cannot be stated as a
   "frozen-share concentration" claim; it must absorb the joint
   structure (this sharpens, not weakens, the falsifiability of G-Detect:
   the null hypothesis of the gate is now a specific sinking-cosine
   family).
4. **The SKIP ledger is accountable.** 42 → 38 unresolved claim lines,
   with the four upgrades *cross-verified digit-exactly against the
   document's printed values*, each remaining SKIP carrying a quantified
   engine ceiling and a named algorithmic unlock. The honesty register of
   Note D survives: nothing unproved is being silently absorbed — and
   notably the one deep absolute value the engine could reach
   ($\mathrm{live}(20,35)$, 44 digits) matched the document to the last
digit, an independent confirmation of Appendix D.5's arithmetic at a
   rung no Phase-4 engine route could touch.

---

## 7. Out of scope / standing register

* **J.1** — bijective proof of the split identity for general $(q, k)$
  (polynomial identity certified for $k \le 10$, all $q \le 4$; Note H).
* **J.3 for $q \ge 3$** — closed forms for the margins-$q$ matrix counts
  (the $q$-rook component classification does not reduce to cycles);
  literature: product/Skachkov-type IE formulas. Registered, not
  attempted.
* **J.4** — the joint-regime limit $\lim_k D_k(k)$ and the VHC gate
  formulation; census window now $k \le 19$.
* **$C_q$ census route for $q \ge 5$** — closed form available (Thm
  I.6); census extrapolation unneeded for $q \ge 5$ but the
  correspondence at $q = 5$ (i.e. $v_5(k)$ ladder) is untested.
* **Deep live rungs** ($k \ge 36$ live claims) — blocked by the measured
  $T$-DP exponential cost; engineering unlocks registered on the
  roadmap: (a) fast contingency-matrix DP (µs-scale, e.g.
  Littlewood–Richardson-driven or polynomial-in-$n$ classification of
  $T_q(\mu,\nu)$), (b) `f_syt` suffix-count speed-up
  ($O(k \cdot \text{rows}) \to O(\text{rows} + k)$ inner loop).
* **Geometry side** — all model-side; the Note-E interface (F-transport
  ⟺ VHC; gates) unchanged by this note.

*Engines and transcripts for this note: `ledger/margins2.py` +
`margins2.txt` (three-route + engine identity, all PASS);
`ledger/boundary_law.py` + `boundary_law.txt` (62/62 + headline
re-derivations); `ledger/regev_constants.py` + `regev_constants.txt`
(closed form + ladders with method self-check); `ledger/joint_ext.py` +
`joint_ext.txt` (J.2 rows, ends at $k=19$, killed at 20 — rungs beyond
$k = 19$ deferred to the sped-up engine); `ledger/skip_reach.py` +
`skip_reach.txt` (appendix to the sealed Phase-2 audit). Conventions as
in Note H: `E.partitions` is a generator; Kostka pinned convention;
`dom_padded` for dominance; cosine = second-moment convention.*
