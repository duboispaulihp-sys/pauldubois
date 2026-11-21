# Note B — A Tropical Program for the F-Gap (Searchlight Formulation)

**Working-session notes, companion to "The Harmless Subgroup and the F-Closure Lemma" (P. Dubois), Note A, and Note C.**

**Honest framing, up front.** This note does *not* prove anything tropical about
Hodge classes. It formulates a *searchlight program*: a disciplined way to use
tropical/calabi–Yau-degeneration geometry to *locate* candidate non-algebraic
Hodge classes (Weil-slot populations), with every implication from the tropical
side to the rational side stated as an explicit named conjecture, no unvalidated
fan conventions asserted, and the one fully validated tropical-adjacent fact —
the Adiprasito–Huh–Katz (p,p)-theorem for matroids, implemented and tested in
Note C's engine — kept as the program's anchor. The point of the note is that
even *conditional* and *one-directional* implications have value: they tell
the outside game (see the roadmap) where to aim the census.

---

## §0. Orientation: what the two games are

The parent document splits the HC effort around the F-closure lemma (Theorem 4.5):

- **Inside game** (F-closure): characterise $F^p(X) = \mathrm{Hdg}^{2p}(X)$
  internally, at cycle level. Note A proves the boundary theorem here: feeding
  arbitrary Hodge correspondences into the machine collapses it to HC itself
  (Props 2.2′, 2.3 of Note A), so the machine is exactly as strong as its
  hypotheses — no more.
- **Outside game** (the frontier): find $\tau \in \mathrm{Hdg}^{2p}(X)
  \setminus B^p(X)$ for a *specific* $X$ and $p$, i.e. populate a Weil slot
  $w_X(p) > 0$ with a proven equality of dimensions. Note A's Cor 3.4′ (and
  Prop 3.3) show this may be taken **primitive** — a constraint every
  candidate must respect, by Theorem 4.5's consistency requirements.

The tropical program is a proposed engine for the outside game.

## §1. The tropicalization strategy, described honestly

**Setup (standard, no conventions invented).** Let $A$ be a principally
polarized abelian variety of dimension $g$ over $\mathbb{C}(\!(t)\!)$, with a
maximal (rank-$g$) toric degeneration to a semiabelian variety $A_0 =
(\mathbb{G}_m)^g$ with dual complex (dual intersection complex) — the cone
complex $\Sigma(A)$ attached to the degeneration. No invented claims here: the
existence and construction of such degenerations is classical for abelian
varieties, via semiabelian degenerations à la Mumford/Faltings–Chai. The
relevant structure: the limit mixed Hodge structure (MHS) on $H^k(A_t)$ has a
weight-graded decomposition whose graded pieces are built from
$H^1(A_0) \cong \mathbb{Q}^g$ placements — specifically
$\mathrm{Gr}^W_{2\bullet}\, H^k(A_t) \cong \wedge^{\bullet} H^1(A_0)$ in the
abelian case.

**What we would want (and do not have):** a statement of the form

$$(\star)\quad \tau \in \mathrm{Hdg}^{2p}(A) \;\Rightarrow\;
\mathrm{Gr}^W_{2p}\bigl(\lim_t \tau\bigr) \text{ is tropical-algebraic on } A_0,$$

where "tropical-algebraic" means: a tropical cycle class in the Chow cohomology
$A^{\bullet}(A_0)$ of the tropical torus — a combinatorial object ring, of the
same formal type as the matroid Chow rings of the AHK theorem. We state $(\star)$
as a conjecture and name it:

**Conjecture T1 (weight-graded limit comparison).** *For a maximally
degenerating family of ppav's $A \to \mathbb{A}^1_t$, the specialization map on
Hodge classes followed by the weight-graded quotient identifies*
$\mathrm{Hdg}^{2p}(A_t)_{\mathbb{Q}}$ *with a subspace of the
$(p,p)$-Chow-cohomology of the tropical skeleton, compatibly with correspondence
transport. In particular, if the limit class is NOT tropical-algebraic, then
some $t$-nearby class on $A$ is not algebraic.*

**Status: conjecture, do not assume.** No proof is claimed or sketched here.
The correct statement would need a careful comparison between the limit MHS
(Steenbrink), the tropical homology of Itenberg–Katzarkov–Mikhalkin–Zharkov,
and the Chow cohomology of the dual complex — three objects whose exact
dictionary is precisely the missing input. Note A's discipline (Prop 2.3:
anything unconditional here proves HC, hence nothing is unconditional) applies
with full force: **any** unconditional version of $(\star)$ in the direction
"tropical counterexample ⟹ rational counterexample" would be a major theorem.
So the program treats $(\star)$ as a target, not a tool.

## §2. The VHC dependency

Even granting T1, transferring a tropical violation to a rational one on $A$
passes through the parent document's Appendix B: the equivalence between
F-transport and VHC (very-Hodge-compatible correspondences). Precisely:

- If VHC holds: correspondences that preserve $B$ are exactly the transport
  operators the F-machine absorbs, and the tropical searchlight's outputs are
  interpretable inside the census's slot table (Note C, `results.md`).
- If VHC fails: the parent document's transport-type counterexample of shape
  (iii) already gives a *rational-side* failure, and the game is over — no
  tropical input is needed.

So the program's logical position is: **tropical falsification of a slot is
useful only under (T1 ∧ VHC)**, and its contrapositive flight paths are the
falsifiable targets of §3.

## §3. Falsifiable targets: the Weil-type / CM ledger

The honest, history-linked targets are the classes the parent document's
Coda already ledgers:

- **Weil-type classes** (Appendix A of the parent): on a Weil-type abelian
  variety $A$ of signature $(r,s)$, the Weil classes $\tau \in
  \bigwedge$-subalgebras attached to the symplectic argument are Hodge iff the
  dominance condition holds; their non-algebraicity (generic Weil HC failure)
  is the classical open case. Concretely the tensor powers
  $\tau^m \in \mathrm{Hdg}^{2m}$ for suitable $m$ are the falsifiable targets:
  if tropical analysis of a maximal degeneration of $A$ shows the limit of
  $\tau^m$ leaves tropical-algebraicity, and T1+VHC hold, then $\tau^m
  \notin B^{mr}$ and the slot $w_A(mr) > 0$ is **provable** — conditional only
  on T1 and VHC, both stated.
- **CM ledger classes**: on CM points of the Shimura variety (the
  compactification locus in the degeneration), the parent document's ledger
  tracks which power combinations $(\tau, \bar\tau)$-monomials are forced
  algebraic by the CM action. The tropical side mirrors this: CM degenerations
  are maximally degenerate, so their skeletons are the cleanest.

**Consistency check with Theorem 4.5 (must-pass gate).** Any candidate
$\tau$ produced this way must be *primitive* (Note A, Cor 3.4′) and must not be
F-generated from $B$ (Theorem 4.5 + Note A Prop 2.3: if $\tau$ were
F-generated from $B$ by cycle-level correspondences, it would be in $B$, and
no counterexample exists). Both checks are mechanical in Note C's engine:
primitive-ness is a hard-Lefschetz check on the model ring; F-generacy is the
seed-closure computation itself. A candidate that passes neither is discarded —
this is the "several falsifiable gates" the program offers.

## §4. The validated anchor: AHK and the matroid pillar

The one tropical-adjacent body of facts that is *fully rigorous and implemented*
(Note C: `matroid_from_circuits`, `chow_presentation`, `pd_check`, `hr_spot_check`)
is the Adiprasito–Huh–Katz theorem: the Chow ring
$A^{*}(M) = \mathbb{Q}[x_S : \text{proper nonempty flats}] / (\text{incomparability} + \text{rank reset})$
of a matroid $M$ satisfies Poincaré duality, the hard Lefschetz theorem, and
HR-type quotient isomorphisms. In the engine (validated, 9/9 tests):
- $A^1(M) = \#\{\text{proper flats}\} - \dim M$ (test `test_uniform_dims`),
- PD certificate on $U_{2,3}, U_{2,4}, U_{3,5}, F_7, K_4$
  (tests `test_fano_pd`, `test_k4_pd_and_dims`),
- the SLOT table $w(p)$ per degree for each matroid ring (`print_census`).

**Why this is the anchor.** Matroid Chow rings are the cleanest setting
where "Hodge-theoretic theorems hold for combinatorial objects" is a theorem
(AHK 2015, Huh–Wang for HR). The tropical program's ambition is *exactly* to
place the limit cohomology of maximal degenerations into a comparable combinatorial
Chow-type ring, for which AHK-style positivity would then be available. The
engine's matroid pillar is the working model of what that end-state looks like
computationally: graded ring, relations from combinatorial data, PD/Lefschetz
certificates, and slot table.

## §5. What would make the program honest mathematics, in steps

1. **State and prove the easy half of T1** (the one-direction we control):
   tropical-algebraic limit classes on maximal degenerations of ppav's come
   from algebraic cycles on the central fiber, via the standard
   specialization/LC-injection. This direction uses only known compatible
   specializations and should be unconditional. (Not done here.)
2. **Formulate T1's hard direction** as above; identify precisely which MHS
   comparison theorem(s) it would follow from. (Partial: Steenbrink +
   IKMZ tropical homology dictionary, program level only.)
3. **Gate every output through Note A**: primitivity (Cor 3.4′), non-F-generacy
   (§3 above), VHC-consistency (§2 above). All three are mechanically checkable
   in Note C.
4. **Run the census on the degeneration family**: slot tables as functions of
   the toric data, using `external_product` for the ring-theoretic gluing. The
   engine supports this today for models up to ~10–15 variables (see the
   limitations in `results.md`).

## §6. Risk register (tropical pillar)

| Risk | Severity | Mitigation |
|---|---|---|
| T1 may be false as stated (MHS vs tropical cycle dictionary is subtle) | fatal to the program | treat T1 as falsifiable; run gate 3 on every candidate |
| VHC may fail, collapsing the game to shape-(iii) counterexamples | ends the game, not the math | VHC failure is itself a win — it produces rational violations; ledger both |
| Tropical-algebraic on $A_0$ may be *strictly weaker* than algebraic on $A$, so tropical violations occur where rational ones cannot | produces false positives | gate 3 must be applied; the census slot $w>0$ is *necessary*, never *sufficient* |
| GB engine caps: rank-4 matroids, $K_5$, high-degree slots out of reach of pure-Python | computational | documented in `results.md`; engine is a prototype, not a ceiling for the math |

**Bottom line.** The tropical program, honestly framed, is a *location* device:
under two explicitly stated conjectures (T1, VHC), tropical degeneration
calculations convert Weil-type and CM ledger candidates into provable slot
falsifications; under no conjectures, its AHK/matroid anchor is already fully
validated and computed in Note C, and its targets are exactly the
primitive-shaped gaps the census knows how to expose.
