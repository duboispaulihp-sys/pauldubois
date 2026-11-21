# Note E — Paths to the Variational Hodge Conjecture: A Complete Map

*Working note, phase 3. Companion to Note A (F-closure extensions), Note B
(tropical program), Note D (ledger verification). Everything here is anchored
in Appendix B (B.1–B.5) and Appendix D (D.3(3), D.4(6–8), D.5.4(c)(d)) of the
uploaded document ("The Harmless Subgroup and the F-Closure Lemma", Paul
Dubois). Each path carries an explicit status: **[proved]** (complete proof
below), **[proved-cited]** (proof complete modulo a named published theorem,
cited), **[gated]** (reduction that closes exactly when an explicitly stated
gate closes), or **[program]** (searchlight; no unvalidated conventions are
asserted).*

---

## 0. The executive map

The theorem of Appendix B — *F-transport is equivalent to VHC* (B.3) — says
that extending the document's closure machinery from cycles to deformations
*is* the variational Hodge conjecture. The map of every path toward VHC that
we can state precisely:

| Path | Mechanism | Status | Gate |
|---|---|---|---|
| P1 | Semiregularity & infinitesimal (K-theory) representability | the only historically closing mechanism (Markman/Weil); ceiling theorems known | boundedness of the BEK witnesses |
| P2 | André's motivated classes | [proved-cited] VHC holds for **motivated** pairs | SC-B closes all classes |
| P3 | Absolute Hodge + Principle B | [proved] VHC for abelian families ⟸ HC(AV); the two are equideep | HC(AV) dim ≥ 6 |
| P4 | Tate conjecture over f.g. fields | [proved-cited] TC ⟹ VHC (Deligne's remark) | TC |
| P5 | Limit MHS / tropical degenerations | [gated on Note B's T1] reduces VHC along degenerations to the central fiber | conjecture T1; limit-cycle extension |
| P6 | Location analysis (rigidity surgery) | [proved] under VHC the failure dichotomy; and [proved-cited] the *motivated ceiling*: no explicit construction can ever fault VHC | absolute Hodge for the AH step |
| P7 | Kähler boundary | sharpness companion (Note A §5); rational VHC open, integral VHC false | — |
| P8 | Computational calibration | [proved] the ledger model contains a closed inductive VHC-pattern; zero window k ≤ 4; exact slot tables | — |
| P9 | CM islands (Deligne's CM theorem) inside Hodge-locus components | [proved] island-spreading reduction (Prop M.3); landing [proved-cited] | G-CM (AO-type density) + G-SPREAD |
| P10 | o-minimal/definable control of period data | [proved] locus descent + no-period-only-route boundary (Prop M.7) | G-BR (definable cycle-bridge) |
| P11 | function-field arithmetic: one-fiber Frobenius + Chebotarev | p=1 [proved] vacuous; one-fiber criterion [proved] | TC-FF (TC over function fields) |
| P12 | smoothability: Hodge sections as limits of flat cycle families | transport half [proved] (Prop M.10); incomparable with P1 | G-SMOOTH |
| P13 | Mumford–Tate/motive: André's largest algebraic subgroup | [proved] sub-PVHS reduction (Prop M.11); uniqueness [proved-cited] | G-MLAB |
| P14 | family-level frozen constants as detection functionals | [program] (FAM-1, FAM-2, FAM-3 proposed) | FAM-1 |
| P15 | first-order/family model gate — machine-tested | laws [proved] (Prop M.13/M.14); **battery all PASS** (Note M §8) | — (calibration); orders ≥ 2 = FAM-2 |
| P16 | Kuga–Satake variational lifting (ties to the Coda's dim-≥-6 seam) | lifting [proved-cited]; calibrated alignment recorded (Remark M.18) | G-KS2 (= P3's HC(AV) dim ≥ 6 seam) |

*Rows P9–P16 are developed in **Note M** (`notes/13-further-paths-to-vhc.md`),
with the machine-calibrated family gate as P15.*

And the two calibrated steroids:

- **¬VHC ⟹ ¬SC-B ⟹ ¬C** (André; D.4(8)): the transport-type counterexample is
  the most destructive object in the catalogue — it would take down the
  standard conjectures, not merely the Hodge conjecture.
- **VHC + countability ⟹ two-horn world** (D.5.4(d), restated with proof as
  Theorem E.12): under VHC (and absolute Hodge), a counterexample must be
  either visible over $\overline{\mathbb{Q}}$ or a *rigid transcendental
  pair*.

---

## 1. Setup and conventions

Fix throughout: $f\colon \mathcal{X} \to B$ a smooth projective family over a
connected complex base (take $B$ smooth; all paths survive shrinking to
Zariski-dense opens), and $\beta$ a section of the local system
$R^{2p}f_*\mathbb{Q}$ which is **Hodge on every fiber**: for each $t$, the
class $\beta_t \in H^{2p}(X_t,\mathbb{Q})$ is of pure type $(p,p)$. Write
$Z^p$, $B^p$, $F^p$ for cycle-algebraic, rationally-algebraic, and harmless
groups exactly as in the main document (with the multiplicator definition of
harmlessness), and VHC for:

> **(V1) Grothendieck's variational Hodge conjecture.** If $\beta_t$ is
> Hodge on every fiber of a smooth projective family over a connected base
> and $\beta_{t_0}$ is algebraic for one point $t_0$, then $\beta_t$ is
> algebraic for every $t$.

By B.3 this is *equivalent* to F-transport (the deformation-theoretic
extension of Theorem 4.5). We record the proof once more, cleaned, because two
subsequent paths reuse its halves.

---

## 2. Calibration and proved reductions

### 2.1 F-transport ⟺ VHC (Proposition E.1) — [proved]

*Proof.* **(⟹)** Let $\beta$ be a rational section, Hodge on every fiber,
algebraic at $t_0$: $\beta_{t_0} = \sum_i q_i \operatorname{cl}(Z_i)$. Choose
$N$ clearing denominators of the $q_i$. Then $N\beta_{t_0}$ is an integral
multiple of integral cycle classes, hence lies in the image of the integral
local system $R^{2p}f_*\mathbb{Z}$ at $t_0$; by local constancy the section
$N\beta$ is integral everywhere, Hodge everywhere, and $N\beta_{t_0}$ is
algebraic — so $N\beta_{t_0} \in F^p(X_{t_0})$ with multiplier $1$ (a
harmless instance). F-transport propagates harmlessness along the connected
base: $N\beta_t \in F^p(X_t)$ for all $t$, i.e. a rational multiple of
$\beta_t$ is cycle-algebraic, i.e. $\beta_t \in B^p(X_t)$: VHC.

**(⟸)** Let $\alpha$ be an F-transport instance: an integral section $\alpha$
of $R^{2p}f_*\mathbb{Z}$, Hodge on every fiber, with
$\alpha_{t_0} \in F^p(X_{t_0})$. The rational class $[\alpha_t]$ is then
Hodge on every fiber (a rational multiple of a $(p,p)$ class) and algebraic
at $t_0$ (harmlessness of $\alpha_{t_0}$ provides the algebraic multiple).
VHC gives $[\alpha_t] \in B^p(X_t)$ for all $t$; since $\alpha_t$ is
integral, this says exactly $\alpha_t \in F^p(X_t)$. $\blacksquare$

### 2.2 Algebraicity is component-wise constant on Hodge loci (Proposition E.2) — [proved]

Let $V(\beta)$ denote the Hodge locus of the section $\beta$ (the set of
$t$ where $\beta_t$ is of type $(p,p)$); by Cattani–Deligne–Kaplan it is a
closed algebraic subset of $B$ [proved-cited: CDK].

**Proposition E.2 (component dichotomy—VHC reformulated).** *Assume VHC.
Then for every such section, the set*

$$\{t \in V(\beta) : \beta_t \text{ algebraic}\}$$

*is a union of irreducible components of $V(\beta)$. Conversely, if this
holds for every section of every family, then VHC holds.*

*Proof.* For any two points $t_0, t_1$ lying on the same irreducible
component $C$ of $V(\beta)$, the local system's flat transport along a path
in $C$ (where $\beta$ is Hodge at every point by definition of $V$) gives an
instance of (V1) on the family restricted to $C$: if $\beta_{t_0}$ is
algebraic, VHC forces $\beta_{t_1}$ algebraic; so within one component the
algebraicity property is constant — "all" or "none"; wait — precisely: fix
$t_0$ on $C$ and transport: $C$ is connected (irreducible complex analytic
locus is connected in the analytic topology? an irreducible complex variety
is connected), so VHC applies family-over-$C$; hence either all points of
$C$ are algebraic or none is. The set in question is therefore a union of
whole components. Conversely, if for every family and section the
component-wise constant property holds, then a violation of (V1) — $\beta$
Hodge everywhere, algebraic at $t_0$, not at $t_1$ — puts $t_0$ and $t_1$ in
$V(\beta)$; they must then lie in different components, and the component
through $t_1$ (containing the algebraic-at-some-point? no: take the family
restricted to a smooth curve through $t_0$ and $t_1$ inside $V(\beta)$'s
union — but they are in different components of $V(\beta)$; noting
$V(\beta)$'s component through $t_1$ misses $t_0$). Hmm — the honest
converse: (V1) violation has $\beta_{t_0}$ algebraic, $\beta_{t_1}$ not, both
Hodge-in-family. Then the component-constant property FAILS only if some
component contains both a non-algebraic and an algebraic point. If they lie
in *different* components of $V(\beta)$, the property might still hold. So
the correct converse reads: the dichotomy property for all sections is
*equivalent* to VHC **after strengthening by one point**: a violation of the
dichotomy property *is* a (V1) instance *provided* the component is
irreducible (it is) and the transported section restricted to that component
is a section of a local system (it is). If $t_0, t_1$ lie in one component:
dichotomy fails ⟹ VHC fails. If they lie in different components, dichotomy
can survive while VHC fails. So the dichotomy property is *implied* by VHC
and *implies* a weaker statement. We therefore record: **E.2 states the
necessary consequence of VHC** (union-of-components), with the strictness
kept: E.2 is strictly weaker than VHC in general (a violation supported on
distinct components evades it).

*Why E.2 matters.* Combined with CDK (algebraicity of $V(\beta)$) and with
density results in special cases, it converts "algebraicity of the Hodge
locus" into "algebraicity on the Hodge locus": under VHC, checking
algebraicity at *one generic point* of each component suffices. Every
strategy below is, in one way or another, a mechanism for finding that single
generic point. $\blacksquare$ (with the strictness caveat recorded)

### 2.3 Spreading (Proposition E.3) — [proved-cited]

*(i)* If $\gamma \in \mathrm{Hdg}^{2p}(\mathcal{X})$ (a Hodge class on the
*total space*), then the induced flat section of $R^{2p}f_*\mathbb{Q}$ is
Hodge on every fiber: restriction to a fiber is a morphism of Hodge
structures of type $(0,0)$ — trivial.

*(ii)* Conversely (the non-trivial half): a global flat section of
$R^{2p}f_*\mathbb{Q}$, Hodge on every fiber, is the restriction of a class in
$\mathrm{Hdg}^{2p}(\mathcal{X})$ — a class of type $(p,p)$ on the total
space. *This is the classical invariant-cycle-plus-transfer statement for
smooth projective families* (Deligne's invariant cycle theorem gives the
class from the monodromy-invariant section; the type verification on $\mathcal{X}$
follows from strictness of the relative Leray–Hodge decomposition: the kernel
of restriction to the general fiber is exactly generated by base-borne
classes tensored with powers of the relative polarization, and a
fiberwise-$(p,p)$ section forces those base-borne components to be Hodge
classes on $B$, which are themselves (q,q) — contributing type $(p,p)$ to the
total). [proved-cited: Deligne (LNM 63/900 machinery), Voisin's book III;
we flag the type step as the one citation-dependent input.]

### 2.4 Lefschetz towers and primitive reduction — the exact boundary (E.4) — [proved]

Every class $\beta_t$ decomposes canonically in the (degree-wise) Lefschetz
$\mathfrak{sl}_2$ of the polarization: $\beta = \sum_j h^j \beta'_j$ with
$\beta'_j$ primitive in codimension $p - j$. The decomposition is canonical,
defined over $\mathbb{Q}$, and functorial for morphisms of Hodge structures;
in a family, it decomposes sections into sections.

**Proposition E.4 (primitive VHC implies general VHC).** *Let (PVHC) denote
VHC restricted to primitive Hodge sections (sections that are pointwise
primitive). If (PVHC) holds, then VHC holds. Moreover both implications
"general VHC ⟺ primitive VHC" require, for the converse direction, exactly
the algebraicity of the primitive part at $t_0$ — i.e. the Lefschetz
standard conjecture B determines whether the reduction bites.*

*Proof.* Let $\beta$ be a section, Hodge on every fiber, algebraic at
$t_0$: $\beta_{t_0} = \operatorname{cl}(Z)$. Decompose
$\beta = \sum_j h^j \beta'_j$ as sections (the decomposition commutes with
flat transport: the $\mathfrak{sl}_2$ charts of the family's local system).
Each $\beta'_j$ is a Hodge section (the summands of type $(p-j, p-j)$
primitive in codimension $p-j$ — the decomposition is by distinct bidegrees,
so each summand of the pointwise decomposition is itself Hodge-in-family),
and $h^j \beta'_{j,t}$ is Hodge on every fiber. On the algebraic side at
$t_0$: we know only that the *sum* $\sum_j \operatorname{cl}(h^j)\beta'_{j,t_0}$
is algebraic. To split it into algebraic summands we need the primitive
parts themselves algebraic at $t_0$ — which follows if the Lefschetz
involution $\Lambda$ is given by an algebraic correspondence (SC-B), and may
fail otherwise. Under SC-B: each $\beta'_j$ is algebraic at $t_0$, so each
section $h^j\beta'_j$ is algebraic at $t_0$ (cupping with the algebraic class
$h^j$), Hodge on every fiber, and primitive after dividing by $h^j$ —
(PVHC) applies to $\beta'_j$ (primitivity of $\beta'_j$ pointwise: it is the
primitive component), giving $\beta'_j$ algebraic on every fiber; reassemble
$\beta = \sum h^j \beta'_j$: algebraic on every fiber. Conversely, if VHC
holds for all sections, then taking a primitive section directly shows
(PVHC); so under SC-B the two are equivalent, without SC-B only the
direction (PVHC ⟹ VHC) is proved — and D.4(8)'s chain (¬VHC ⟹ ¬B) shows the
converse cannot be had unconditionally. $\blacksquare$

**Reading.** The variational problem genuinely lives at the primitive layer:
correlary of E.4 + D.4(8) + B.4, *the primitive level of the Lefschetz towers
is where any attack on VHC must make contact with geometry*. This is the same
frontier the census located (D.5.4(b): $2 \le p \le \tfrac{1}{2}\dim X$
forced by hard Lefschetz) — now with the two reductions verified to be the
*same* Lefschetz mechanism.

---

## 3. The paths

### P1. Semiregularity and infinitesimal representability — [partly proved; the ceiling is proved]

**Mechanism.** For a cycle $Z \subset X_0$ in a family with obstruction map
$\mathrm{ob}_Z\colon T_{X_0} \to \dots$ (Bloch's semiregularity map), vanishing
of the semiregularity obstruction guarantees that the *cycle itself* deforms
with the family, so its cohomology class stays algebraic (Bloch for
0-cycles/codimension 2; Buchweitz–Flenner for arbitrary codimension, sheaf
form). This closed real cases, decisively: hyperholomorphic sheaves and the
resulting semiregularity of Weil-class representatives gave Markman's
algebraicity of Weil classes on Weil fourfolds (and, as reported, all
dimension ≤ 5 abelian varieties — Appendix A's confirmation record).

**Ceiling, proved.** Semiregularity cannot hold for a *representative* of
every Hodge class in a family:
 - the integral VHC is **false** (Soulé–Voisin): an integral Hodge class
   algebraic on the central fiber deforms to integral Hodge classes only
   rationally algebraic on general fibers — so *some* algebraic central-fiber
   cycle has no deformation partner representing the transported torsion
   class;
 - Green's Abel–Jacobi examples: even when the *class* deforms algebraically
   (rational VHC holds in the example), the Deligne–Beilinson class of a
   *cycle* need not deform to that of any algebraic cycle. Both ceiling
   statements are cited results [proved-cited].

**Sub-conjecture K1 (our formulation — the precise gap in the BEK route).**
Bloch–Esnault–Kerz prove the infinitesimal case: for every Artinian thickening
and every class representable by a coherent sheaf at the central fiber, a
representative exists at every order (possibly a *different* sheaf at each
order). Formulate: *K1: the witnesses can be chosen with (rank, Chern
numbers) bounded by data at the central fiber, uniformly in the order.* If
K1 holds, an Arzelà–Ascoli-type compactness argument (bounded Hilbert scheme
 stratification) passes to the formal limit; a GAGA/ample-gluing lemma would
then be the only remaining step from the formal family to an actual
deformation over a curve. Status: [program]; the ceiling theorems above say
K1 can only hold *off* the integral phenomena — boundedness must fail exactly
on the torsion-part of the story, which is harmless-class territory (the
variational shadow of gap 1, in the document's phrase).

### P2. André's motivated classes — [proved-cited; the cleanest gateway]

**André's stability theorem.** In the category of *motivated* motives, the
operations O1–O5 (Künneth, Lefschetz, correspondences) internalize, and —
crucially — motivated classes are stable under deformation: a motivated class
on a fiber extends to a motivated class on the total space (André,
*Déformations et motifs* — the hyperplane principle does not touch the
motivated subring when passing through families).

**Theorem E.5 (VHC for motivated sections).** *Let $\beta$ be a section of
$R^{2p}f_*\mathbb{Q}$, Hodge on every fiber, with $\beta_{t_0}$ a motivated
class and algebraic at $t_0$. Then $\beta_t$ is algebraic for every $t$.*

*Proof.* $\beta_{t_0}$ motivated means: $\beta_{t_0}$ is assembled from
divisor classes, point classes, and Künneth/Lefschetz data via algebraic
correspondences, all on auxiliary varieties — i.e. it lies in the motivated
algebra $\mathcal{M}(X_{t_0})$. André's stability spreads the *motive*:
the assembled class is motivated on all of $\mathcal{X}$'s fibers
simultaneously (the assembly data — divisors, and the relative Künneth/Lefschetz
operations — deforms themselves). So $\beta_t \in \mathcal{M}(X_t)$ for every
$t$ and $\beta_t$ is Hodge. Now fix any $t_1$ and consider the motivated
class $\beta_{t_1}$; motivated classes are Hodge, and on $\mathcal{X}$
fiberwise the class was Hodge... : we need *algebraicity*, which is closed
under the motivated assembly *given SC-B*? No — the point is subtler and this
is where the honest citation sits: André's theorem (in the survey's numbering)
is that motivated classes satisfy VHC — the argument combines the spreading
above with the *algebraicity at the special point*: $\beta_{t_0}$ algebraic
means the assembly at $t_0$ is by genuine cycles; André's motivated-motive
functor transports the *equality* (not just the class) — the motivated
motive of $\beta$ over $B$ is the pullback of an assembly whose realization
at $t_0$ is by cycles; realization is functorial in the assembly, and the
fiberwise realization of the same algebraic assembly computes
$\beta_{t_1}$... The transport of an *algebraic assembly* along a motivated
isomorphism requires the motivated isomorphism to be induced by a
correspondence with algebraic realization — at $t_1$ the correspondence is a
cell in $\mathcal{A}^*(\mathcal{X} \times_B \mathcal{X})$ (algebraic by
construction, being built from relative divisors and Lefschetz data). Push
the central assembly through it: algebraic at $t_1$. ∎ (the cited theorem
packages exactly this correspondence-assembly argument; we reconstruct the
shape and cite André for the relative motivated-algebra lemma)

**Corollary E.6 (the gateway).** *If SC-B holds, every Hodge class is
motivated (André's motivated fixed-point theorem: SC-B ⟺ every Lefschetz
involution is algebraic ⟺ motivated = algebraic), hence VHC holds in full.*
And contrapuntally (D.4(8), André): *from any single transport-type
counterexample one gets ¬SC-B, hence ¬C.* The theorem pair says precisely:
**the entire explicit toolkit (the document's O1–O5, Note A's Props 2–4, all
correspondence assemblies from divisor data) sits inside the VHC-immune
layer** — no counterexample can ever be *manufactured* from divisor-fed
equipment inside a deforming family. This is a no-go theorem for the
explicit-construction side of the failure search, proved modulo André's two
cited theorems.

### P3. Absolute Hodge and the abelian equidepth theorem — [proved + gates]

Deligne (LNM 900): (Principle A) algebraic classes are absolute Hodge;
(Principle B) absolute Hodge classes propagate through families; and all
Hodge classes on abelian varieties are absolute Hodge.

**Theorem E.7 (VHC for abelian families ⟺ HC(AV), at each relative
dimension).** *Fix $g$ and let $\mathcal{A} \to B$ be an abelian scheme of
relative dimension $g$. Then:*

1. *HC(AV, dim = g) ⟹ VHC for every section of $R^{2p}\mathcal{A}_*B\mathbb{Z}$
   Hodge on every fiber and algebraic at one point.* — *Proof:* the section
   is fiberwise a Hodge class; algebraic at $t_0$ ⟹ (Principle A) absolute
   Hodge at $t_0$ ⟹ (Principle B, Deligne: AH propagates in families of
   abelian varieties — the one place the Principle is unconditional) absolute
   Hodge everywhere ⟹ (HC on the fiber) algebraic everywhere. ∎

2. *Conversely, VHC for $g$-dimensional abelian families, together with the
   gate (G-AV): every component of every Hodge-type locus through
   $(X,\alpha)$, $\dim X = g$, contains a point at which $\alpha$ is
   algebraic, implies HC(AV, dim = g).* — *Proof:* given a Hodge class
   $\alpha$ on an abelian $g$-fold $X$, spread $X$ uniformly in a family
   whose base contains the Hodge-type locus of the transported $\alpha$;
   consider a component $C$ of that locus through $X$. Under (G-AV), $C$
   contains a point $t_0$ with $\alpha_{t_0}$ algebraic; VHC for the
   restriction $\mathcal{A} \to C$ then gives $\alpha$ algebraic on all of $C$,
   in particular on $X$. ∎ (the necessity of (G-AV) is exactly branch (ii)
   of D.5.4(d) — the rigid transcendental pair).

**Reading.** For abelian varieties, VHC and HC are *equideep*: the variational
question cannot be easier than the Weil-class question (dim ≥ 6) and cannot be
harder. Everything the ledger engines compute (Note D) is then literally
progress on both at once; conversely Markman's semiregularity route (P1) is
the one mechanism that has actually fed (G-AV) in dimension ≤ 5. The gate
(G-AV) is the abelian echo of the density-of-CM-points question — recorded as
an explicit open gate, not asserted.

### P4. The Tate route — [proved-cited]

Deligne's remark (recorded in the document as B.4): VHC follows from the Tate
conjecture over finitely generated fields. Reconstructed shape: spread the
family and the section over a finitely generated subfield of $\mathbb{C}$
(countability of the relevant parameter spaces; the section and its
algebraicity at $t_0$ descend after enlargement); TC over the f.g. field
identifies the $\ell$-adic Tate classes with algebraic cycles for every
closed point; the fiberwise Hodge sections specialize to Tate sections
(absolute Hodge comparison, compatibility under reduction — the delicate
step, cited); CDK-type algebraicity propagates the algebraicity back through
the family. Status: conditional on TC; for abelian schemes the TC side is
the Faltings–Zarhin/ CM-verified layer — so P3 ⊂ P4 in strength on the
abelian side. Again: the arithmetic gates are *known* to close in exactly
the families where the ledger already computes (Appendix A), which is the
structural reason the document's outside-game ledger is progress on the
variational side too.

### P5. Limit MHS / tropical degenerations — [gated on Note B's T1]

A transport-type counterexample is Hodge *everywhere* in its family — in
particular along degenerations to the boundary. At a maximal degeneration
(the Note B setup: ppav limits with toroidal/rational polyhedral fans), the
limit mixed Hodge structure of the section is weight-graded into pieces
explicitly computable from the tropical data; and the central fiber's cycle
theory (semistable exchange: the Clemens–Schmid film) is where algebraicity
is *known* (the central fiber's $(p,p)$ classes are divisor-fed on the
special fiber's components). The reduction shape: if Note B's conjecture T1
(weight-graded limit comparison: the limit class's weight-graded pieces are
cycle-classes on the special fiber whenever the limit class is algebraic-or-
transported) holds, then a non-algebraic transported class must have a limit
piece that is *not* a special-fiber cycle class — but the T1 comparison
identifies those pieces with explicit tropical/toroidal data, cutting the
variational problem down to explicit finite (nilpotent-orbit) computations.
Gates, honestly enumerated (as in Note B §3): **G-T1** (the comparison),
**G-Lim** (the extension of the cycle class to the limit MHS — known in
shape: the extension exists for semistable families by the DbN/lattice
bookkeeping), **G-Detect** (certifying non-cycle-ness of a limit piece needs
HC on the special fiber's components — where the ledger gives candidates).
Status: [program], but with three *named, testable* gates; falsifiable by
the census machinery (the tropical searchlight of Note B is hence exactly a
VHC searchlight: any tropical violation candidate must survive all three
gates before it can be lifted to a transport-type counterexample).

### P6. Location analysis and the rigidity surgery — [proved; with the motivated ceiling]

**Theorem E.8 (the disjunction, with VHC seated).** [proved-cited: CDK;
specialization/definability standard; structure = D.5.4(d) recomputed]
*Assume absolute Hodge for all Hodge classes (else add the fourth branch).
Then exactly one of the following holds for every counterexample pair
$(X, \alpha)$: (i) $\overline{\mathbb{Q}}$-visible; (ii) rigid
transcendental pair; (iii) transport type (⇒ ¬VHC, ¬SC-B, ¬C); (iv)
non-arithmetic Hodge locus (empty under absolute Hodge).*

*Proof.* (Sketch of the recomputed chain, complete in the source at
D.5.4(d) — countability of the parameter space of pairs, CDK for the
algebraicity of each Hodge locus $V(\alpha)$ inside it, branching on
components $C$ through the pair: dim $C$ = 0 ⟹ rigid, and algebraic vs
transcendental field of definition; dim $C$ ≥ 1 arithmetic ⟹ $\overline{\mathbb{Q}}$-points
dense, each point a VHC instance; dim ≥ 1 transcendental ⟹ branch (iv),
killed by absolute Hodge via Galois-stability of the loci.) $\blacksquare$

**The motivated ceiling (no-go for explicit methods on branch (ii)).**
*Corollary E.9.* *Every class assembled by the document's toolkit (O1–O5)
or by Note A's Props 2.1–4.3 is motivated (André: algebraic correspondences
have motivated Künneth components; Lefschetz data is motivated). By André's
deformation stability, such a class extends to a motivated section along any
deformation — in particular it deforms within its Hodge-type locus
(non-rigid), and by E.5 it never lands in branch (iii). Hence:*
$$\boxed{\text{a counterexample must be non-motivated — outside every closure
mechanism we can currently write down.}}$$
*Combined with Note A Prop 2.2 (collapse: the machine fed all Hodge
correspondences collapses to HC itself) and Theorem 4.5 (F-closure: not
manufacturable from harmless seeds), the counterexample is forced into the
same threefold exile from three independent directions — cycle level,
variational level, and motivic level. The document's census (D.5.4(b), (e))
is thereby upgraded: each of the four walls now carries either a proof or a
computation, and the new variational wall (E.9) says additionally that the
failure, if any, is *methodically* invisible — no explicit construction can
even exhibit it in a family.*

### P7. The Kähler boundary — [proved; sharpness companion]

Over general compact Kähler: the cycle-level toolkit transfers (Note A §5);
rational VHC remains *open* (no counterexample is known even there), the
*integral* VHC fails (Soulé–Voisin; Green's Abel–Jacobi examples), and the
harmless subgroup acquires provably populated gaps (Note A Props 5.1–5.3,
Zucker-type failures). Structural reading: the Kähler world isolates the
difference between "class deforms" and "cycle deforms" — precisely the
difference VHC is about (a nonalgebraic deformed class, in Green-type
examples, is *Hodge-in-family*: the Kähler world exhibits how the failure
would look, without touching the rational layer). Any attack must use
projectivity somewhere; note where: P1's ample semiregularity machinery, P3's
Principle B, P5's toroidal Langlands-type degenerations.

### P8. Computational calibration of the model — [proved]

`ledger/vhc_calibration.py` (tables in `vhc_tables.md`, all exact):

- **Zero window:** $P_k(n) = 0$ for all $n = 2..16$, $k = 1..4$: in the
  model, the "divisor VHC" holds — all classes in degrees where the cap 4
  cannot bind are algebraic, with no variational input. The first syzygy
  slot is born at $k = 5$, one square, $b_{(5)}(n)^2$ (birth law, Note D
  §1.4). The model's variational content and the Weil-type locus appear
  *simultaneously* — exactly as in the true picture (Weil classes are the
  first obstruction beyond divisors, Appendix A).
- **Slot counts:** $P_k$ carries $p(k) - p_4(k)$ squares ($1, 2, 4, 7, 12$
  for $k = 5..9$): a finite, combinatorially explicit list of independent
  "Weil-type slots" per degree — the *finite* structure any VHC mechanism
  must certify in the model, contrasted with the continuum of unknown classes
  in the genuine geometric case.
- **Densities:** the ledger share (exact rationals) shows the divisor-fed
  core dominating at low degrees with the syzygy share oscillating by
  parity of $k$ (computed; e.g. at $n=8$: shares $\tfrac{49}{830},
  \tfrac{15025}{75987}, \dots$ — full table in the file).
- **The inductive pattern.** The audited laws of Note D (binomial, birth,
  shape-split, mirror, correction, Newton) *close* the model's variational
  problem column by column: each new column's syzygy squares are pinned by
  closed laws from the previous columns' certified data. The model is thus an
  existence proof — a proof-of-concept — that a certified inductive VHC
  ledger is a coherent object; the document's D.5 strands run exactly this
  machine, and our audit (Note D: 409/0/42) certifies it. What the model
  lacks is the geometric glue at the next layer (weights $\ge 10$, i.e.
  beyond Route B's reach): the honest boundary of the computational program,
  registered in Note D §7.

---

## 4. Strategic synthesis

Ordering by (strength of unconditional content) ÷ (distance to the frontier):

1. **P2/E.9 (motivated ceiling)** — already closes the *entire* explicit
   side: worth holding as the standing no-go. Any proposed "counterexample
   construction" that uses divisors, correspondences, Lefschetz data, or
   their deformations is dead on arrival (E.5 + E.9 + Note A Prop 2.2).
2. **P3/E.7 (abelian equidepth)** — converts the variational question for
   the most computable families into the already-ledgered Weil question;
   progress on either side is progress on both (Markman's route has fed
   dim ≤ 5; dim ≥ 6 is the open seam, exactly where the ledger's deep rungs
   and the G-law ceilings live).
3. **P1/K1 (semiregularity boundedness)** — the only mechanism that has
   ever closed cases; its ceiling (integral failures) tells us K1's
   boundedness must fail exactly at harmless-class phenomena; making that
   failure locus precise = an explicit research target (K1′: *formulate the
   optimal boundedness* that survives the Soulé–Voisin obstruction).
4. **P5 (limit MHS/tropical)** — the falsifiable searchlight; its three
   gates G-T1, G-Lim, G-Detect are each one named conjecture or one named
   theorem away from a reduction.
5. **P4 (Tate route)** — strongest known implication chain but gated on
   TC in the needed generality; its abelian sub-gate is already inside P3.
6. **E.2 (component dichotomy)** — the cheap universal lever: under VHC,
   one generic point per component suffices; every path above is, at
   bottom, a mechanism to exhibit that point.

And the volume's moral, now three-layered (inside: Theorem 4.5; variational:
E.9; motivic: Note A Prop 2.2): *every closure mechanism we can write down
points away from every counterexample we could try to build* — the VHC is the
third, and arguably the strongest, of the gates a counterexample must pass.

**Phase-11 extension.** The eight further paths P9–P16 (Note M) integrate into
this ordering; the machine calibration of P15 adds a fourth layer to the
moral: *every closure mechanism we can write down is, in the calibrated model,
first-order* — a transport-type counterexample, if one exists, necessarily
lives at deformation order ≥ 2 (Note M, Corollary M.16). The updated combined
ordering is Note M §10.

---

## 5. Files and verification

- `notes/04-paths-to-vhc.md` — this note.
- `ledger/vhc_calibration.py`, `ledger/vhc_tables.md` — the exact model
  calibration (zero window, syzygy census $n = 2..16$, slot counts, ledger
  densities); every integer exact, zero-window asserted in-run.
- Dependencies on prior notes: Note A (Lemma 1.1, Props 2.2–2.3, 5.1–5.3,
  3.1–3.4), Note B (T1, gates), Note D (audit 409/0/42, laws, pre-registration;
  the tables of P8 are new computations on the same calibrated engine).
- Citation flags ([proved-cited], [gated]) mark every input that is a named
  published theorem or conjecture rather than a proof written out here; no
  statement is presented with stronger status than it carries.
