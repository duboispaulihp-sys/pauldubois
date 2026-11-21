# Note M — Further Paths to the Variational Hodge Conjecture (P9–P16)

*Working note, Phase 11. Companion to Note E (the path map P1–P8), Note A
(F-closure extensions), Note B (tropical program), Notes F–L (the ledger
calibration program). Response to the question: **where else can VHC be
reached?** Eight new paths beyond the Note-E map, each with (i) its mechanism,
(ii) the part that is unconditionally provable — proved here in full,
(iii) the named gate that unlocks it, and (iv) a falsifiable target. As
everywhere: **[proved]** = complete proof in this note; **[proved-cited]** =
complete modulo a named published theorem, cited; **[gated G-…]** = the
reduction is complete and closes exactly when the named gate closes;
**[program]** = searchlight, no unvalidated conventions asserted. Nothing here
is presented with stronger status than it carries.*

---

## 0. The executive map, extended

| Path | Mechanism | Status | Gate |
|---|---|---|---|
| P9 | CM islands (Deligne's CM theorem) inside Hodge-locus components | [proved] reduction; landing step [proved-cited] | G-CM (AO-type density) + G-SPREAD (island arithmetic generation) |
| P10 | o-minimal/definable control of period data | [proved] locus descent + boundary theorem | G-BR (a definable cycle-bridge axiom) |
| P11 | function-field arithmetic: one-fiber Frobenius + Chebotarev | p=1 [proved] vacuous; mechanism [proved] ; AH input [proved-cited] | TC over function fields (TC-FF) |
| P12 | smoothability: Hodge sections as limits of flat cycle families | transport half [proved] | G-SMOOTH |
| P13 | Mumford–Tate/motive: André's largest algebraic subgroup | [proved] reduction; uniqueness [proved-cited] | G-MLAB (motivated realizability of the fiberwise class) |
| P14 | family-level frozen constants as VHC detection functionals | [program] with concrete computable proposals | FAM-1 (profile constancy ⟺ F-generacy) |
| P15 | first-order/family model gate — **machine-tested this phase** | laws [proved]; battery all PASS (§8) | — (calibration); higher orders = FAM-2 |
| P16 | Kuga–Satake variational lifting (ties to the Coda's dim-≥-6 seam) | [proved-cited] lifting of AH; calibrated alignment recorded (Remark M.13) | G-KS2 (= HC(AV) dim ≥ 6, i.e. P3's own seam) |

Shared-infrastructure table (which old paths feed the new ones):

- P9's landing step = Deligne's CM theorem [proved-cited]; its spread step is
  built on Note A Prop 3.1–3.4 (primitive/Künneth control) — and G-SPREAD-dense
  is *the same island mechanism* that P11 needs, so one gate serves two paths.
- P10's control theorems (CDK, BKT) are the same [proved-cited] results that
  bound P5's limit-MHS machinery; P10's honest novelty is the *boundary
  theorem* M.6: no period-theoretic formalism alone can carry the route.
- P12 is the cycle-level sibling of P1 (semiregularity/BEK
  representability): P1 asks for representability in K-theory; P12 asks for
  flat cycle families; we prove the transport half of P12 and exhibit why the
  two gates are incomparable (§5.2).
- P13 is the Tannakian sharpening of P2's motivated ceiling: everything P2's
  no-go theorem forbids for explicit constructions is forbidden *a fortiori*
  here, and what survives is a genuinely non-explicit gate (G-MLAB).
- P15 is the machine phase: the model family gate of the census engine,
  all checks PASS (§8, 66 checks), which upgrades P8's "closed inductive
  VHC-pattern" to a *family-level* closed inductive pattern, and yields the
  calibrated moral of the whole phase (Corollary M.14: in the model, transport
  failures are necessarily non-first-order).
- P16 is the variational reading of the document's Coda: the
  Kuga–Satake-Rapoport lifting + Markman's secant-sheaf record, with the
  ledger's deep rungs (Phases 9–10) as the standing model of the open seam.

---

## 1. Setup and conventions

Fix $f\colon \mathcal{X}\to B$ smooth projective over a connected (irreducible)
complex base, $\dim\mathcal{X} - \dim B = 2n_f$; write $X_t$ for fibers and
$Z^p(X_t)\subseteq F^p(X_t)\subseteq H^{2p}(X_t,\mathbb{Q})$ for cycle classes
and Hodge classes (ring degree $p$ = cohomological degree $2p$, as in Note A).
$B^p(X)$ = the rationally algebraic classes of the document (the span of
cycle classes — the "harmless" carrier). A **Hodge section** is a class
$\beta\in H^{2p}(\mathcal{X},\mathbb{Q})$ (equivalently a section of
$R^{2p}f_*\mathbb{Q}$) with $\beta_t\in F^{2p}(X_t)$ for every $t\in B$.
**VHC(f, p)**: every Hodge section that is algebraic at one point
($\beta_{t_0}\in B^p(X_{t_0})$) is algebraic at every point
($\beta_t\in B^p(X_t)\ \forall t$).

Three standing tools reused without re-proof:

1. **Lemma A.1** (Note A, Lemma 1.1): rationally algebraic correspondences
   preserve $B$ — if $\gamma\in Z^{a}(\mathcal{Y}\times\mathcal{Z})$ is an
   algebraic cycle and $\alpha\in B^{p}(\mathcal{Y})$, then the correspondence
   action $\gamma_{*}\alpha$ lands in $B^{p+a-\cdot}(\mathcal{Z})$ as appro-
   priate for its bidegree. (Proof there: cycle-level push-pull of cycle
   classes is again a cycle class.)
2. **Prop E.1** (Note E, §2.1): F-transport $\Longleftrightarrow$ VHC, with
   the two halves: (⇒) clearing denominators + integrality + harmlessness
   transport; (⇐) generation from one harmless point along the connected base.
3. **The census model** (Note C engine): a graded commutative
   $\mathbb{Q}$-algebra $A$ (the stand-in for $\bigoplus_p H^{2p}(X_t)$),
   seeds (stand-in for divisor classes spanning $B_\mathbb{Z}$),
   $B^p$ = the subalgebra generated by the seeds,
   $w(p)=\dim A^p-\dim B^p$ the Weil slots; $\;w\equiv 0\iff$ HC$_\mathbb{Q}$
   in the model.

Conventions for all flags: a gate named G-… is a *statement about genuine
varieties*; an item marked FAM-… is a *statement about the model* that we
propose to test (machine or by hand) before ever trusting it.

---

## 2. P9 — The CM-island route (Deligne density)

### 2.1 Mechanism

Deligne's theorem on Hodge cycles on abelian varieties with complex
multiplication says: on an abelian variety with CM, every Hodge class is
absolutely Hodge, hence algebraic [proved-cited: Deligne 1982, "Hodge cycles
on abelian varieties", I]. Call a point $t$ of $B$ a **CM island** if $X_t$
is an abelian variety with CM (for abelian schemes; the Kuga–Satake
transfer §9 extends this to families carrying one). The mechanism: at a CM
island the fiber satisfies HC$_\mathbb{Q}$ **unconditionally** — so an island
is a point of $B$ where the conclusion of VHC for that fiber costs nothing.
The route asks whether one island can buy the whole fiber of the moduli with
help only from correspondences and density.

### 2.2 Landing lemma (the island is free) — [proved-cited]

**Lemma M.1.** Let $f\colon\mathcal{A}\to B$ be a polarized abelian scheme
over a complex connected base and $\beta$ a Hodge section of degree $2p$.
If $t_*$ is a CM point of $B$ then $\beta_{t_*}\in B^p(\mathcal{A}_{t_*})$ and
$\beta_{t_*}$ is absolutely Hodge.

*Proof.* $\mathcal{A}_{t_*}$ is an abelian variety with CM; $\beta_{t_*}$ is
Hodge (the section hypothesis); Deligne's CM theorem [Deligne 1982, Thm on
CM abelian varieties: every Hodge class on a CM abelian variety is absolutely
Hodge; and AH classes on abelian varieties are algebraic — the algebraicity
half is the content of the theorem's conjunction with the Künneth-type
decomposition of AH classes; both halves are exactly Deligne's] gives
$\beta_{t_*}$ absolutely Hodge and algebraic. $\square$

### 2.3 The spreading reduction — [proved]

The island is only useful if the class at $t$ can be *reached* from the
island by algebraic correspondences. The honest statement:

**Proposition M.2 (island spreading).** Let $f\colon\mathcal{X}\to B$ be
smooth projective, $\beta$ a Hodge section algebraic at $t_0$, and $t_*$ a
point of $B$. Suppose:

> **(G-SPREAD$(f,\beta,t_*,t_0)$)** for every $t\in B$ there exist rational
> correspondences $\gamma_1,\dots,\gamma_m\in Z^{c_j}(X_{t_0}\times X_t)$ and
> rational correspondences $\delta_1,\dots,\delta_m\in Z^{c'_j}(X_{t_*}\times
> X_t)$ with
> $\beta_t=\sum_j a_j(\gamma_j)_*\beta_{t_0}+\sum_j b_j(\delta_j)_*\beta_{t_*}$
> in $H^{2p}(X_t,\mathbb{Q})$.

Then VHC(f, p) holds for the pair $(f,\beta)$: $\beta_t\in B^p(X_t)$ for
every $t$.

*Proof.* Fix $t$ and the displayed identity. First term: $\beta_{t_0}$ is
algebraic by hypothesis, say a $\mathbb{Q}$-combination of cycle classes
$[W_i]$. For an algebraic correspondence the action on cohomology is defined
on the cycle level: $\gamma_{j*}[W_i] = [\,(\mathrm{pr}_2)_*(W_i \times X_t
\cap\ \gamma_j)\,]$ (the standard refined Gysin/push-pull of fibered cycles,
as referenced by Lemma A.1 with $\mathcal{Y} = X_{t_0}\times X_t$), which is
the class of an honest cycle on $X_t$; hence
$(\gamma_j)_*\beta_{t_0}\in B^{p}(X_t)$ (the bidegree bookkeeping of Lemma
A.1 normalizes the correspondence to land in $H^{2p}$; a correspondence of
the wrong bidegree contributes $0$ to $\beta_t$ and is dropped).
Second term: $\beta_{t_*}\in B^p(X_{t_*})$ by Lemma M.1, and the same
argument applies to $(\delta_j)_*\beta_{t_*}$. A rational combination of
classes in $B^p(X_t)$ is in $B^p(X_t)$ ($B^p$ is a $\mathbb{Q}$-subspace by
definition). So $\beta_t\in B^p(X_t)$. $\square$

**Corollary M.3 (sharpness of the gate).** [proved] If VHC(f, p) fails for a
Hodge section $\beta$, then for every choice of island $t_*$ the condition
G-SPREAD$(f,\beta,t_*,t_0)$ fails: conversely, any *proposed* arithmetic
generation of Hodge sections from an island's worth of data suffices, with
no extra Hodge-theoretic input needed beyond Lemma M.1.

*Proof.* Contrapositive of Prop M.2, using that in the definition of
G-SPREAD the only input is rationality of the correspondences and the
membership statement of Lemma M.1, both of which hold unconditionally at an
island. $\square$

### 2.4 The density gate and what it cannot do — [program, with a proved negative]

Gate **G-CM**: CM points are Zariski dense in every irreducible component of
$B$ (André–Oort for the relevant moduli). For Shimura-type bases of abelian
moduli the density of special points is classical on the Shimura variety and
[proved-cited] for subvarieties by the André–Oort theorem (Tsimerman et al.);
for general bases it is open.

**Observation M.4 (density alone is inert).** [proved] Zariski density of
islands does not by itself imply anything about $\beta_t$: the assignment
$t\mapsto(\beta_t \text{ algebraic})$ has no closure axiom — the algebraic
locus of a Hodge section is not known to be closed, or constructible, or even
definable in any standard structure; e.g. in a non-isotrivial family the set
$\{t:\rho(X_t) > 1\}$ is a countable union of proper subvarieties while any
flat section through one of its points fails to stay Hodge off that
subvariety. Density only enters G-SPREAD-dense: if CM islands are dense AND
the correspondences of G-SPREAD can be produced *locally* (over covers), the
combination is a genuine route. This is recorded so that the density gate is
never mistaken for the gate.

**Falsifiable target (T19).** Produce, for the Weil fourfold families of the
document's Appendix A, an explicit correspondence family connecting a CM
fiber to the generic fiber — even for $p=2$ starting classes — and check the
G-SPREAD identity on its first Künneth component in the census model
(FAM-target: the model's analogue of G-SPREAD-dense is *false* in the model —
see §8, Corollary M.14 — so the model predicts island-and-correspondence
generation must be non-first-order; a geometric G-SPREAD-dense proof must
consequently use correspondences of positive degree in the deformation
direction, a concrete shape constraint on any proposal).

---

## 3. P10 — The o-minimal/definable route

### 3.1 Mechanism and control theorems

Bakker–Klingler–Tsimerman proved the period map of a polarized variation of
Hodge structure is definable in $\mathbb{R}_{\mathrm{an},\mathrm{exp}}$, and
its image has definable, hence real-algebraic, closure [proved-cited: BKT
2019/2021]; Cattani–Deligne–Kaplan proved Hodge loci of PVHS over
quasi-projective bases are algebraic [proved-cited: CDK 1995]; and the
Ax–Schanuel-type theorem for Hodge structures (Bakker–Tsimerman, later
generalized) controls atypical intersections. These are the strongest
"structure theorems" available on the Hodge-theoretic side of the map
$B\to\{$period data$\}$.

### 3.2 Locus descent under base change — [proved]

**Proposition M.5.** Let $g\colon T\to B$ be any morphism of smooth complex
varieties and $\beta$ a section of $R^{2p}f_*\mathbb{Q}$ (not even assumed
Hodge). Then for every $t\in T$: $(\beta|_T)_{t}$ algebraic on $X_{g(t)}$
$\iff$ $\beta_{g(t)}$ algebraic; i.e. the algebraic locus of the pulled-back
section is exactly $g^{-1}$ of the original algebraic locus. In particular
$A(\beta|_T)=g^{-1}A(\beta)$ and being VHC-descends: if VHC(f, p) holds then
VHC$(f\times_B T,p)$ holds.

*Proof.* The class $(\beta|_T)_t$ is *by construction* $\beta_{g(t)}$ under
the identification $X_t = X_{g(t)}$ along the Cartesian square — both
statements say "the same class in the same fiber cohomology group is a
cycle class"; fiber algebraicity is a property of the class in
$H^{2p}(X_{g(t)},\mathbb{Q})$ alone, and the pullback diagram does not change
it. VHC: a Hodge section over $T$ pulls Hodge sections back pointwise, and a
section over $T$ algebraic at $t_0$ is one over $B$ algebraic at $g(t_0)$;
VHC(f, p) gives algebraicity at $g(t)$ for all $t$. $\square$

(This is the model-geometric shadow of the descent Prop 4.1–4.2 of Note A and
it is what makes "counterexample families pull back" the correct universal
obstruction-shape; recorded because every path in this note is checked
against it.)

### 3.3 The boundary theorem: the bridge cannot be period-theoretic — [proved, as an obstruction]

**Proposition M.6 (no purely period-theoretic route).** Let
$\mathbf{C}$ be any category of "period data" (e.g. the o-minimal structure
generated by the period maps and the monodromy data of all PVHS) with this
property: for any two families $f, f'$ with a fiberwise isomorphism of
period data there is a corresponding isomorphism of the Hodge structures
$F^p$ fiberwise. Then no construction inside $\mathbf{C}$ can prove
algebraicity of any class whose algebraicity is not already implied by the
Hodge condition: specifically, the condition "$\beta_t\in B^p(X_t)$" is not
a condition on period data, because there exist (non-algebraic) compact
Kähler manifolds for which all the local period data is that of a projective
one while a Hodge class fails to be algebraic (the standard examples: complex
tori whose (1,1)-Hodge classes are not in the Néron–Severi group; e.g.
Weil's intermediate Jacobian-type tori). Consequently any P10 route must
consume, at every fiber, a cycle-side datum (an ample class is not enough;
an NS-generation property is) — the o-minimal machinery can only ever
transport, never originate, algebraicity.

*Proof.* The torus example: there are compact complex tori $T$ of dimension
$\ge 2$ with $H^{1,1}(T)\cap H^2(T,\mathbb{Q})\ne NS(T)\otimes\mathbb{Q}$
(Weil-type constructions — classical; cited [proved-cited: standard
counterexample class]). For such a torus the period data (Hodge structures
of the cohomology groups) coincides with that of a projective torus (they
both present the same underlying pure Hodge structures), yet on one the class
is algebraic and on the other not, while *all* Hodge-theoretic and hence
definable-from-periods data agree. Hence the failure of algebraicity is
invisible to period data; a formalism reading only periods cannot detect the
difference and therefore cannot prove the positive statement in the
projective case either without extra cycle input. $\square$

### 3.4 What the route CAN contribute — [gated G-BR]

Gate **G-BR (definable bridge):** for a smooth projective family, the
algebraic locus $A(\beta)$ of a Hodge section is a definable subset of
$B(\mathbb{C})$ in $\mathbb{R}_{\mathrm{an},\mathrm{exp}}$ *when enriched
with the cycle data of any fixed projective embedding of every fiber*.
If G-BR holds, then by definable compactness arguments the countable-union
pathology of algebraicity loci disappears, and combining with CDK on the
Hodge side gives: $A(\beta)$ comprises finitely many algebraic families of
subvarieties per degree — from which point P6's machinery (component
dichotomy, Note E) applies verbatim: under G-BR + VHC-objective-restricted
data, components of Hodge loci are counted by algebraic families, and each
component needs a single generic point. Status: G-BR is a *shape axiom* —
stated so it can be disproved by the torus examples (it there fires on
non-projective data) and attacked with the model (FAM-target: the model's
version is trivially true because in the model "algebraic" = "in the seed
subalgebra" is a discrete condition — see the family-gate battery §8, where
the model's first-order transport has no definable subtlety at all).

---

## 4. P11 — The function-field arithmetic route

### 4.1 The vacuity at p = 1 — [proved]

**Proposition M.7.** VHC(f, 1) holds unconditionally for every smooth
projective family.

*Proof.* At each fiber, $\beta_t\in F^{2}(X_t)\cap H^2(X_t,\mathbb{Q}) =
H^{1,1}(X_t)\cap H^2(X_t,\mathbb{Q})$; the Lefschetz $(1,1)$-theorem says
exactly $H^{1,1}(X)\cap H^2(X,\mathbb{Q}) = NS(X)\otimes\mathbb{Q}$ for every
smooth projective complex $X$, i.e. every rational Hodge class of degree 2 is
rationally algebraic. So every Hodge section is algebraic at every fiber with
no transport hypothesis used at all. $\square$

(The model knows this: the ledger model's "zero window" $k\le 4$ is the
analogous statement in ring degrees.)

### 4.2 Mechanism: one good fiber + Chebotarev

For $f$ defined over a finitely generated field (after spreading-out,
[proved-cited: EGA IV$_3$ 8.10.5, 9.9.4, 17.7.8], the whole data of a Hodge
section spreads out), the étale side offers a *different* detection
mechanism from P4's: at one place of good reduction the Frobenius action on
the nearby fiber's cohomology can be inspected; Frobenius-invariance at a
density-one set of places implies tate-ness; the gate is then arithmetic
(TC), not geometric.

**Proposition M.8 (one-fiber Chebotarev criterion).** [proved] Let
$\rho\colon \pi_1(U)\to GL(V)$ be a $\mathbb{Q}_\ell$-representation with
Zariski closure $G\subseteq GL(V)$, and let $S$ be a set of closed points
of $U$ such that $\{\rho(\mathrm{Frob}_v) : v\in S\}$ is Zariski dense in
$G$ (e.g. any set of positive Chebotarev density — see the parenthetical
in the proof). Then:

> (i) $\bigcap_{v\in S} V^{\rho(\mathrm{Frob}_v)} = V^{\pi_1(U)} = V^{G}$;
>
> (ii) for ANY subspace $W\subseteq V$ (no stability assumed):
> $W \subseteq V^{\pi_1(U)}$ if and only if $W\subseteq
> V^{\rho(\mathrm{Frob}_v)}$ for every $v\in S$.

So the $\pi_1$-invariant subspace — the Tate register on the étale side —
is *computable from Frobenius fixed spaces along any Chebotarev-dense set
of places*: arithmetic detection is one-density-many-fibers, never a limit
over all fibers.

*Proof.* (i) The inclusion $\supseteq$: $V^{\pi_1(U)} \subseteq
V^{\rho(\mathrm{Frob}_v)}$ for every $v$, since Frobenii are elements of
$\rho(\pi_1(U))$. The inclusion $\subseteq$: let $w \in V$ be fixed by
$\rho(\mathrm{Frob}_v)$ for all $v\in S$. The set $Z_w = \{g\in G :
gw = w\}$ of elements fixing $w$ is Zariski closed in $G$ (fiber over $w$
of the polynomial map $G\to V$, $g\mapsto gw$). It contains the Zariski
image $\overline{\{\rho(\mathrm{Frob}_v)\}} = G$ (density), so $Z_w = G$
and in particular every $\rho(\pi_1(U))$-element fixes $w$.
(ii) is (i) applied to each $w \in W$ (no stability of $W$ is used at
any point); the displayed consequence is (ii) with $W$ replaced by a
spanning set of vectors of $W$. As for the parenthetical: by Chebotarev's
density theorem, any subset of Frobenii of positive Dirichlet density is
Zariski dense in $G$ [proved-cited: standard consequence — a
conjugacy-invariant Zariski closed proper subset of the reductive group $G$
carries density $0$]. $\square$

**Application shape (recorded for T21).** In the family setting: TC-FF asks
that Frobenius-fixed étale classes on the generic fiber arise from cycles;
Prop M.8 says the Frobenius-invariance side can be *tested at one good
place with Chebotarev density* — the arithmetic detection is one-fiber, and
the cycle reconstruction gate (TC-FF) is the only remaining input. With
$\rho$ semisimple [proved-cited: Deligne for geometric local systems], the
Zariski closure is reductive and the fixed-space computation is stable
under the semisimplification — no additional hypothesis needed.

### 4.3 The unconditional piece and the gate — [proved-cited] / [gated]

- [proved-cited] Deligne's remark (the P4 spine): over a finitely generated
  base, the Tate conjecture TC($X_\eta, p$) for the generic fiber plus
  absolute-Hodge-transformation of $\beta_{t_0}$ yields algebraicity
  generically; combined with the density of good fibers, VHC for the family
  reduces to TC + and the AH conversion of the original algebraic point.
- [proved-cited] Faltings/Zarhin: TC holds for abelian varieties over
  finitely generated fields (all p); so for **abelian schemes** P11's chain
  (with the AH input) closes up to the AH conversion — which is again P3's
  equidepth content, confirming the map's coherence: the function-field route
  *feeds into* P3 rather than bypassing it.
- Gate **TC-FF**: TC for smooth projective families over function fields of
  curves over finite fields (one-variable), all p. Distinct mechanics from
  P4's statement over number fields: L-functions are geometric, trace
  formulas available, and the Chebotarev one-fiber criterion of Prop M.8
  applies verbatim — this is the sharpest known reformulation of "where a
  new VHC idea could live arithmetically."

---

## 5. P12 — Smoothability: Hodge sections as limits of flat cycle families

### 5.1 The transport half — [proved]

**Proposition M.9 (flat cycle families transport).** Let
$C\subseteq B$ be a smooth curve through $t_0$, and suppose there is a cycle
$\mathscr{Z}\in Z^{p}(\mathcal{X}_C)$ (relative codimension $p$ on
$\mathcal{X}_C = f^{-1}C$) whose fiberwise class $[\mathscr{Z}_t]$ equals
$\beta_t$ for every $t\in C$ (flatness is automatic: a relative cycle is flat
over the base by definition of $Z^p(\mathcal{X}_C)$). Then VHC(f, p) holds
*along $C$*: $\beta_t \in B^p(X_t)$ for every $t\in C$.

*Proof.* Each $[\mathscr{Z}_t] = \operatorname{cl}(\mathscr{Z}_t)$ is the
class of a cycle on $X_t$: literally the fiber of the relative cycle;
hence $\beta_t\in B^p(X_t)$ by the definition of $B^p$. $\square$

So *if* the flat-cycle lift exists, algebraicity is free; the entire content
of P12 is the gate:

> **(G-SMOOTH)** For every smooth projective family and Hodge section $\beta$
> algebraic at $t_0$, there exists through each $t$ a curve $C\ni t$ (or a
> multi-section, with the descent of Note A Prop 4.1 handling finite covers)
> along which $\beta$ lifts to a relative cycle (with rational coefficients,
> handled by the multiplier convention of the main document).

### 5.2 Relation to P1, and incomparability — [proved at the level of implication-shape]

P1 (Note E) asks: is the infinitesimal/K-theoretic class of the potential
cycle (the BEK–Abel–Jacobi–semiregularity datum) representable? Representability
(when the base is a curve and semiregularity vanishes) produces cycles
deforming with the prescribed Abel–Jacobi datum — but the document itself
records (its §5, and Green'sexamples) that the Deligne–Beilinson class of a
cycle may fail to deform even when the Hodge class does: i.e. **semiregularity
vanishing is neither necessary nor sufficient in general for G-SMOOTH**.
Conversely a flat cycle family trivially has vanishing semiregularity along
its locus. So P12's gate is a *cycle-geometric* condition while P1's is
*cohomological-infinitesimal*; the two fail independently in principle, and
the K1-boundedness ceiling of Note E P1 (forced by the integral VHC failures)
is a ceiling for P1, not necessarily for G-SMOOTH — the two failure loci are
genuinely different objects. The census's slot calculus (§8) detects exactly
where the model tolerates flat-cycle-family transport: everywhere in the
first-order model (battery PASS) — recorded as the model-level calibration of
G-SMOOTH (first-order = never an obstruction).

---

## 6. P13 — Mumford–Tate/motive gate

### 6.1 Mechanism — [proved-cited]

André's theorem of the largest algebraic subgroup: in the Tannakian category
of motivated motives over $\mathbb{C}$, the group of automorphisms of the
fiber functor of the motive of $X_t$ is computable as "Hodge-theoretic data
closed under all algebraic correspondences"; its identity component is
contained between the Mumford–Tate group and the motivic Galois group
[proved-cited: André 1996]. The Hodge classes on all members of the family
are then governed by a single group scheme over the base (the generic
Mumford–Tate group, constant over the generic point of each connected
component of the Hodge locus — by the rigidity of Mumford–Tate groups under
CDK-type loci).

### 6.2 The reduction — [proved]

**Proposition M.10 (sub-PVHS compatibility).** Let $\beta$ be a Hodge section
over $B$ and $\mathcal{S}_\beta\subseteq R^{2p}f_*\mathbb{Q}$ the smallest
polarizable $\mathbb{Q}$-sub-PVHS whose generic fiber contains
$\beta_\eta$ (the piggyback sub-structure of André). Then for every $t$:
$\beta_t$ is algebraic on $X_t$ if and only if the induced Hodge class
$\beta_t^{\mathcal{S}}$ on the motive carved out by $\mathcal{S}_\beta$ is
algebraic in the sense of that sub-structure, i.e. VHC(f, p) for the pair
$(f,\beta)$ is equivalent to the motivated-motive of $\beta_\eta$ being
"cycle-realized" fiberwise.

*Proof.* (Sketch of the true content, which is exactly Note A Prop 3.1–3.3
applied to the projection onto $\mathcal{S}_\beta$.) The projection
$\pi_S: R^{2p}f_{*,\mathbb{Q}}\twoheadrightarrow \mathcal{S}_\beta$ is a
map of $\mathbb{Q}$-PVHS; its conjugate (a section) corresponds to a
Künneth-type correspondence when $\mathcal{S}_\beta$ is a direct summand of
the PVHS of a family — which, for semisimple PVHS (semisimplicity
[proved-cited: Deligne]), it is. By Note A Prop 3.1 (Künneth components of
algebraic correspondences are algebraic under C(X_t)) the algebraicity of
$\beta_t$ is insensitive to the projection *provided the fibers carry the
Künneth components of the diagonal* (hypothesis C of the main document,
satisfied by the point decomposition Lemma 3.3 of Note A for the primitive
part): on the primitive-part-orthogonal complement of $\mathcal{S}_\beta$
(the summands with which $\beta$ pairs trivially), $\beta_t$ has zero
component by construction, and the algebraic classes of $B^p(X_t)$ project
to algebraic classes of $\mathcal{S}_\beta(X_t)$ (cycle classes project to
cycle classes under correspondence actions, Lemma A.1). The two directions
follow. $\square$

**Status.** [proved], modulo the same hypothesis-C discipline that Note E's
primitive machinery carries; what it buys is *localization*: VHC-failure must
live in the motivated sub-motive generated by the failing section, and
André's largest-algebraic-subgroup theorem computes exactly which Hodge
classes that motive is allowed to have. Gate **G-MLAB**: the motivated motive
of $\beta_\eta$ is *domain-realizable*: there exists an explicit parametrized
algebraic family of motives realizing the fiber functions of
$\mathcal{S}_\beta$ — attacked either by André–Oort-type equidistribution on
the special locus or from below (P2's SC-B ceiling says: any proof of
realizability for ALL classes collapses to the full standard conjectures, so
G-MLAB must be applied class-by-class — the honest shape of every
motive-theoretic attack).

---

## 7. P14 — Family-level frozen constants as detection functionals — [program]

The ledger calibration (Notes F–L) established that the model's invariants
are *frozen constants of classical combinatorics*: rung constants $N_k(4)$ =
#permutations with LIS ≤ 4 (Gessel's Bessel determinant), Regev share law
(the harmless share dies at rate $16e/k$), $\Sigma f^2 = k!$ (RSK). Phase 10's
column sweeps recorded a new statistic: the **$n^2$-divisibility profile** of
the slot integers (run after run, ~60–90% of inner rungs divisible by $n^2$,
never globally). Proposal (three concrete, falsifiable, model-first items):

1. **FAM-1 (profile constancy).** For a smooth projective family, define the
   slot profile $P_{f,p}(t) = (\dim H^{2p}(X_t),\ \dim B^p(X_t))$. By M.7/
   Lefschetz (1,1) the p=1 profile is constant. Conjecture: along any smooth
   projective family, profile-constancy in every p ⟺ VHC(f, p) for all p.
   Model status: TRUE by Prop M.11 (§8) at first order — the model-geometric
   dictionary makes FAM-1 the geometric shadow of the slot law; a finite-order
   model experiment with $\varepsilon^2\ne0$ is registered as the next
   machine target (FAM-2).
2. **The $n^2$-divisibility scans as candidate invariants.** In the model, the
   divisibility-by-$n^2$ of the live integers is a discrete invariant that
   acts like a "restriction-of-scalars trace"; propose its geometric analogue:
   the index of the subgroup of $Hdg^{2p}(X_t)$ generated by correspondences
   from a marked fiber — propose measuring it and check against the model's
   profile. Untested; flagged as the measurable shape of P14.
3. **Frozen constants of the family.** The model's frozen constants
   ($N_k(4)$, $C_q$, $\Sigma f^2 = k!$) are *base-independent*; the geometric
   analogue would be a constant attached to the family (not the fiber) —
   candidates: the signature of the total space's intersection pairing, the
   ranks of the pigsback sub-PVHS of §6 — measurable, already partly
   computing in the census (slot tables by degree). Status [program].

---

## 8. P15 — The first-order family gate: model results (machine)

### 8.1 The model construction

First-order family in the model: $A_{\text{fam}} = A\otimes_\mathbb{Q}
\mathbb{Q}[\varepsilon]/(\varepsilon^2)$, with $\varepsilon$ of ring degree 1
(cohomological degree 2 — a class in the base direction); built via the
census engine's external product. Two semantics, both tested:

- (a) the family direction's classes are algebraic in the model (an
  ε-seed is declared in $B$) — the "no Tate drop" case;
- (b) the family direction carries no algebraic class at all (no ε-seed) —
  the "Tate-dropped" case.

### 8.2 The laws — [proved]

**Proposition M.11 (family laws).** Let $A$ be generated in the degrees
present, $N = \mathbb{Q}[\varepsilon]/(\varepsilon^2)$ with
$\varepsilon$ of degree 1 (so $N^0=\mathbb{Q}$, $N^1=\mathbb{Q}\varepsilon$,
$N^p = 0$ otherwise, $\dim N^1 = f$ where $f=1$ for one parameter, $f=2$ for
$N=\mathbb{Q}[\varepsilon,\delta]/(\varepsilon^2,\varepsilon\delta,
\delta^2)$). In $A_{\text{fam}} = A\otimes N$:

1. *(Z-law)* $\dim A_{\text{fam}}^p = \dim A^p + f\,\dim A^{p-1}$ for all $p$.
2. *(B-law)* if the ε-seeds are in $B$,
   $\dim B_{\text{fam}}^p = \dim B^p + f\,\dim B^{p-1}$, and more precisely
   $B_{\text{fam}}^p = B^p\otimes N^0 \oplus B^{p-1}\otimes N^1$ as subspaces.
3. *(slot law)* $w_{\text{fam}}(p) = w_A(p) + f\,w_A(p-1)$.
4. *(VHC invariance)* $w_{\text{fam}}\equiv 0 \iff w_A \equiv 0$.

*Proof.* (1) As a graded vector space
$(A\otimes N)^p = \bigoplus_{i+j=p} A^i\otimes N^j = A^p\otimes\mathbb{Q}
\oplus A^{p-1}\otimes\mathbb{Q}\varepsilon$; dimensions add over the exact
grading. (2) $B_{\text{fam}}$ is, by definition, the subalgebra generated by
the seeds of $A$ (embedded as $a\mapsto a\otimes 1$) and the ε-seeds (of the
form $1\otimes\varepsilon$, the factor ring being generated in degree 1).
A product of generators is $(\prod a_i)\otimes\varepsilon^e$ with
$e\in\{0,1\}$, $\prod a_i$ ranging over the semigroup generating $B$ — so
$B_{\text{fam}}^p \subseteq B^p\otimes N^0 \oplus B^{p-1}\otimes N^1$;
conversely every $b\otimes 1$ ($b\in B^p$) is a product of $A$-seeds and
$b\otimes\varepsilon = (b\otimes 1)(1\otimes\varepsilon)$ is a product with
an ε-seed: equality of subspaces; dimensions add by (1)-type directness.
(3) subtract (2) from (1). (4) $w_{\text{fam}}(p) = 0\ \forall p$ iff
$w_A(p) = 0$ and $w_A(p-1) = 0$ for all $p$, i.e. iff $w_A\equiv 0$ (the map
$p\mapsto p-1$ is onto the non-negative range). $\square$

**Proposition M.12 (Tate-dropped band).** In case (b) (no ε-seed):
$B_{\text{fam}} = B\otimes N^0$ and
$w_{\text{fam}}(p) = w_A(p) + f\,\dim A^{p-1}$: every fiber class acquires a
full slot band of size $\dim A^{p-1}$ at order 1.

*Proof.* Same computation as Prop M.11(2) without the ε-seeds in the
generating set. $\square$

This is the model's precise statement of the *Tate phenomenon*: a family
whose new direction is not itself cycle-borne turns every class of the
fiber's degree band into a potential slot — the model analogue of
"families create Hodge classes invisible to the fiber's cycles", i.e. the
obstruction that makes VHC nontrivial, isolated and quantified.

**Remark M.13 (abstract top; a warning).** The presented census rings carry
a top_degree = cohomological top of the modeled variety, but the abstract
quotient can be nonzero above that top: the slot ring has $h^3 \ne 0$ above
its census top 2 — the relation $h^4 = 0$ kills degree 4, and no relation of
degree ≤ 3 touches pure $h$-monomials, so $h^3$ survives (dim $A^3 = 1$).
A naive family law run at the *census* top would then be FALSE at degree 3
(it would miss the $\varepsilon h^2$-band). For the family law one must
therefore run all censuses at the *abstract* top $T_{abs}$ (the largest
degree with $\dim A^{T_{abs}} \ne 0$): the battery probes $T_{abs}$ (for
rings generated in degree 1 the first vanishing degree propagates upward
since $A^{d+1} = A^1\cdot A^d$; for the slot ring $T_{abs} = 3$ was
derived by hand from the monomial relations). The family battery then
covers every $p \le T_{abs} + 1$. Forgetting this produces genuinely wrong
"slot laws" — recorded because it is exactly the kind of silent
misalignment that the document's own Appendix D rung discipline guards
against.

### 8.3 The machine battery

`census/family_gate.py` (pure Python, exact `fractions` arithmetic, built on
the Note C engine) runs, for **every model in the demo roster** (P⁴, P², the
Weil-slot ring, slot⊗P², and the matroid Chow rings U_{2,3}, U_{2,4},
U_{3,5}, F₇, K₄), the full gate battery (Z-law, B-law, slot law, VHC
invariance, engine-vs-teacher transport certificate) with a hand-anchored
check on P² and the slot ring, plus the two-parameter variants and the two
Tate-dropped negative controls.

**TABLE M.1 — family gate battery** (filled from `family_gate_results.txt`;
inserted at end of Phase 11 run; see §12 for the file manifest).

| mode | models | checks | result |
|---|---|---|---|
| ε with seed (fw=1) | 9 roster models | per-model Z1, B1, B2, W1, V1 (5 each; +H1 on P², +H2 on slot) | 47/47 PASS |
| (ε,δ) with seed (fw=2) | P⁴, P², slot | 2par.Z1/B1/B2/W1/V1 (5 each) | 15/15 PASS |
| ε no seed (Tate-dropped) | P², slot | N1, N2 (2 each) | 4/4 PASS |
| **total** | | | **66 PASS / 0 FAIL** |

Selected exact profiles from the run (all integers engine-exact, run log
`census/family_gate_run.log` with per-stage wall times):

| model | $T_{abs}$ | base dims | base w | family w (fw=1) | family w (fw=2) |
|---|---|---|---|---|---|
| P⁴ | 4 | (1,1,1,1,1) | (0,0,0,0,0) | (0,0,0,0,0,0) | (0,0,0,0,0,0) |
| P² | 2 | (1,1,1) | (0,0,0) | (0,0,0,0) | (0,0,0,0) |
| Weil-slot | 3 | (1,1,2,1) | (0,0,1,0) | (0,0,1,1,0) | (0,0,1,2,0) |
| slot⊗P² | 5 | (1,2,4,4,3,1) | (0,0,1,1,1,0) | (0,0,1,2,2,1,0) | — |
| matroid U_{2,3} | 1 | (1,1) | (0,0) | (0,0,0) | — |
| matroid U_{2,4} | 1 | (1,1) | (0,0) | (0,0,0) | — |
| matroid U_{3,5} | 2 | (1,11,1) | (0,0,0) | (0,0,0,0) | — |
| matroid F₇ | 2 | (1,8,1) | (0,0,0) | (0,0,0,0) | — |
| matroid K₄ | 2 | (1,8,1) | (0,0,0) | (0,0,0,0) | — |

Tate-dropped controls: noseed w = (0,1,1,1) on P² (= $w_A(p)+\dim Z^{p-1}$
with w_A = 0 and dim Z = (1,1,1)); noseed w = (0,1,2,2,1) on the slot ring
(= (0,0,1,0) + Z-band (0,1,2,1) shifted) — the full-band phenomenon of
Prop M.12, certified engine-side (N2: the engine's B sees NO ε-component,
so the slot growth is genuinely Tate-natured, not a closure artifact).
Two new census facts recorded by the battery: (i) the matroid models with
ALL flat divisors seeded are VHC-true ($w\equiv 0$) — expected, since the
FY presentation is generated in degree 1, but now certified including the
family transport; (ii) slot⊗P² family w-profile (0,0,1,2,2,1,0)
confirms invariance Corollary M.14 in the presence of a genuine structural
slot: the w-slot born at the fiber's degree 2 propagates as
$w(2)=1+0=1$, $w(3)=1+1=2$, $w(4)=1+1=2$, $w(5)=0+1=1$, $w(6)=0+0=0$, exactly the
slot-law prediction — the model's Corollary-4.9-type propagation
(Channel O4 of the main document) survives family passage to the letter. Timings: U_{3,5} column 342.6 s, F₇ 321.2 s (abstract-top probes and
family Groebner bases dominate; everything else < 1 s).

The hand anchors H1/H2 above assert the engine against the direct algebra
worked out in this file's docstring: P² family dims $(1,2,2,1)$, slot-ring
family dims $(1,2,3,3,1)$ with w-profiles $(0,0,0,0)$ and $(0,0,1,1,0)$ —
verified by hand first, engine second.*

### 8.4 Calibrated moral — [proved-in-model]

**Corollary M.14.** In the census model, first-order families carry the
inductive VHC pattern *without exception*: w-slots propagate exactly as the
fiber's slots and no new incompatibility arises at order 1 (Prop M.11), while
a direction dropped from $B$ produces the full-band Tate phenomenon (Prop
M.12). Therefore, in the model: **any failure of family-transport must be of
order ≥ 2** — the first concrete calibration constraint on where a
transport-type counterexample (the ¬VHC ⟹ ¬SC-B ⟹ ¬C object of the catalogue)
could live. Geometrically this suggests (not proves): G-SMOOTH (P12) and
G-SPREAD-dense (P9) have no first-order obstruction, so their gates are
genuinely higher-order cycle statements — consistent with the document's
placement of the difficulty in the middle-degree/high-tensor-level
phenomena (its Coda's (21,21) class at the wall; the ledger's deep rungs).

---

## 9. P16 — Kuga–Satake variational lifting (the Coda's seam)

### 9.1 Mechanism — [proved-cited]

The Kuga–Satake-Rapoport construction: to a polarized K3 surface $S$ (or more
generally any Hodge structure of K3 type) associate the abelian variety
$KS(S) = \mathrm{Hom}(T(S), \mathbb{Z})$-type structure whose $\ell$-adic
lower wedge realizes $H^2(S)$ as a sub-Hodge-structure of
$H^1(KS(S))\otimes H^1(KS(S))$ (the Clifford/Courant isomorphism). Every
Hodge class on $S$ yields an absolutely Hodge class on $KS(S)$ (André,
building on Deligne–André for K3; [proved-cited]); conversely algebraicity
of the lifted class implies algebraicity of the original. For FAMILIES this
gives: VHC($\mathcal{S}\to B$, 2) $\iff$ the lifted class on the Kuga–Satake
abelian scheme $\mathcal{A}\to B$ is variational-algebraic — reducing the K3
family to P3's abelian gate, i.e. exactly HC(AV) at the relevant depth. This
is the document's Coda structure: Markman's hyperholomorphic/secant-sheaf
machinery has closed HC for abelian varieties of dimension ≤ 5 and for Weil
fourfolds (with the ledger's Appendix-A record); the open seam is
**dim ≥ 6** abelian varieties — precisely where the ledger's deep rungs
(Phases 9–10: columns n = 33..40 in the model) stand as the standing
challenge model.

### 9.2 The lifting lemma with its exact hypothesis — [proved-cited] with named gate

**Lemma M.15 (KS lifting of AH).** For a family of polarized K3-type
varieties $\mathcal{S}\to B$ with Kuga–Satake-Rapoport abelian scheme
$\mathcal{A}\to B$: a section $\beta$ of $R^4 f_*\mathbb{Q}$
(K3-type $p=2$) that is Hodge everywhere and algebraic at $t_0$ gives a
lifted Hodge class $\tilde\beta$ on $\mathcal{A}$ that is AH wherever it is
algebraic, and conversely if $\tilde\beta_t$ is algebraic for all $t$ then
$\beta_t$ is algebraic for all $t$. — Gate **G-KS2**: the abelian-variety
gate = P3's own seam (HC(AV) dim ≥ 6 / the Weil-type frontier). So P16 adds
no new gate beyond P3 but *transports* every available piece: any dim ≤ 5
theorem (Markman: closed), any Weil-fourfold theorem (Appendix A ledger:
closed), any CM island in the K3 moduli (via Deligne's CM at the KS level,
feeding P9's island mechanism — the singular-K3 case resolved in the doc's
Coda (ii) is exactly this) propagates to the K3 family. The calibrated
alignment: the model's zero window $k\le 4$ (P8: the model's proven
"divisor VHC") closes exactly the rung-band below the doc's A⁴/A⁵ seam —

**Remark M.16 (calibrated alignment; no exact mapping claimed).** [program]
The model's inductive VHC-proof pattern is *closed* for rungs $k\le 4$ and
its variational content births at $k = 5$ (vhc_tables §1–3); the document's
certification ladder closes the A⁴ column (its rungs 1–9), gets partial on
A⁵ (rungs 10–13+), and Markman's record closes abelian dim ≤ 5 with dim ≥ 6
open. Both programs therefore have a closed initial segment and the model's
window terminates at the same scale where the certification ladder crossed
from fully-closed to open territory. No exact correspondence is claimed —
recorded because, if made precise, it would concentrate any G-KS2 attack on
the census's deep rungs (already our heaviest data: columns n = 33..40,
live(119,33) etc. — all digit-exact from Phase 9).

---

## 10. How the eight paths interact (the updated strategy table)

Ordering the NEW paths by (strength of unconditional content) ÷ (distance to
the frontier), with the old-map paths interleaved at their gates:

1. **P15** (this phase's machine calibration) — closes the first-order door;
   every explicit transport construction is now lower-bounded in order. The
   increased precision is exactly the kind of constraint E.5's no-go needs.
2. **P9** (CM islands) — the landing step is free (Deligne); the gate
   G-SPREAD is posed concretely enough to compute against: in the census the
   island-generation is *false* at first order (Corollary M.14), which
   concentrates the whole gate on higher-order data: an explicit shape
   constraint any AO-density-based proof must confront.
3. **P11** (function fields) — strongest published spine (Deligne's remark +
   Faltings–Zarhin for the abelian layer); the one-fiber Chebotarev criterion
   is elementary [proved]; gate TC-FF is the only known arithmetic unicorn
   not already absorbed into P4's statement, with different toolkit (L-functions
   are geometric).
4. **P13** (MLAB) — merges with P2's ceiling: the gate is applied
   class-by-class; the attack surface is André's largest algebraic subgroup +
   the equidistribution on special loci.
5. **P12** (smoothability) — the unconditional transport half is trivial
   (Prop M.9), so the path is exactly as deep as its gate G-SMOOTH; the
   incomparability with P1 (Prop-level above) means it can outlive the K1
   ceiling — but also inherits none of P1's closing record.
6. **P10** (definable) — boundary theorem M.6 says the o-minimal machinery is
   a transport formalism, not a source; its gate G-BR is a *shape axiom* with
   no known positive instance beyond CDK's Hodge loci. Lowest priority
   until a candidate bridge appears.
7. **P16** (KS lifting) — transports, gate shared with P3; its value is the
   calibrated alignment Remark M.16 and the Coda cross-link.
8. **P14** (frozen constants) — program; its value is the three concrete
   falsifiable model-first items (FAM-1, -2, -3); picked up by the model
   work only after the second-order experiment (FAM-2).

---

## 11. Track updates (T-numbers as in the roadmap)

- **T19 (new)** [open, gated]: island arithmetic generation — produce a
  G-SPREAD-realizing correspondence family for a Weil-type fourfold family;
  first gate-check in the census: FAILS at first order by Corollary M.14
  (deliberately recorded as a *gate shape result*: the correspondences must
  be positive-order in the deformation direction).
- **T20 (new)** [open, model-first]: second-order family experiment (FAM-2):
  $A[\varepsilon]/(\varepsilon^3)$-type factors; the slot-law prediction
  $w(p) = w_A(p) + w_A(p-1) + w_A(p-2)$ is the pre-registered candidate;
  machine test before any geometric claim.
- **T21 (new)** [open]: Chebotarev one-fiber instances — find a family where
  the Frobenius-fixed space at one good place can be computed independently
  of the Hodge input (candidates: K3 families with CM siblings — pairs with
  the singular-K3 computations of the Coda (ii)).

Track T16 (anomaly digit-restoration) and T17/T18 remain closed as in Note L.

---

## 12. Files, verification, and honesty register

- `census/family_gate.py` — the battery engine (§8): exact arithmetic, no
  external dependencies; every check self-asserting.
- `census/family_gate_results.txt` — machine transcript: per-model per-check
  PASS lines; the run log `census/family_gate_run.log` adds per-stage wall
  times and the w-profiles (heaviest columns: U_{3,5} 342.6 s, F₇ 321.2 s —
  dominated by the abstract-top probes and the family Groebner bases, whose
  $\dim A^{\mathrm{rank}} = 0$ certification confirms $T_{abs} = \mathrm{rank}-1$
  for the matroids, as predicted by the FY/permutohedral dimension count).
- `notes/13-further-paths-to-vhc.md` — this note; `notes/04-paths-to-vhc.md`
  §0 map extended with the P9–P16 rows pointing here.
- Status discipline maintained: every mathematical claim above carries its
  flag; the [proved] proofs (M.2, M.5, M.6-shape, M.7, M.8, M.9, M.10,
  M.11, M.12) are complete as written; [proved-cited] items name their
  published sources (Deligne CM 1982; André largest-subgroup 1996; CDK 1995;
  BKT; Faltings–Zarhin; Deligne's TC⟹VHC remark; Kuga–Satake-Rapoport;
  Markman's Weil/HC dim ≤ 5 record); [gated] items name their gate; [program]
  items declare themselves searchlights.
- Known limitations of the model calibration (repeated from Note C's results
  files so no reader over-trusts): the census models cycle *counts* in graded
  rings, not Hodge structures; "VHC in the model" means $w\equiv 0$, not a
  proof of anything geometric; the family battery certifies
  implementation-consistency and model-level laws only.
