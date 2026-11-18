# Error log — errors inside Perelman's three preprints and their handling

Compile-verified files in this repo contain **none** of the statements below
that are marked RETRACTED / UNFIXED.

## 1. RETRACTED — horn-volume lower bound and eventual smoothness
Announced in [I §13]; retracted in the abstract and §0 of [II math/0303109]:

> "... and (2) the claim about the lower bound for the volumes of the maximal
> horns and the smoothness of the solution from some time on, which turned out
> to be unjustified, and, on the other hand, irrelevant for the other
> conclusions."

Handling: this claim never appears in `PerelmanInputs`; the ledger's details
(par. de `aPrioriAssumptionJustified`, `deltaCutoffFlow`) mirror [II §4-5] as
written, which do not use it. Any Lean formalization that reproduces the
[I §13] sketch verbatim would encode a false lemma.

## 2. CORRECTED — redundant hypothesis in the κ-solution compactness theorem
[I §11.7] assumed the ancient κ-solutions `M_α` **noncompact**. [II §1.1]:

> "(The assumption in I.11.7. that M_α be noncompact was clearly redundant, as
> it was not used in the proof. Note also that M need not have the same
> topology as M_α.)"

Handling: the ledger field `ancientKSolutionsCompact` states the corrected
(compact and noncompact) form.

## 3. CORRECTED — overlooked case in the classification of ancient κ-solutions
The first paragraph of [I §11.7] missed compact ancient κ-solutions whose
asymptotic soliton is the round infinite cylinder:

> "This latter possibility, which was overlooked in the first paragraph of
> [I.11.7], is illustrated by the example below..." ([II §1.3])

Example [II §1.4]: long round cylinders `S² × I` with caps on `S³`, whose
normalized flows converge to an ancient κ-solution on `S³` (also giving the
negative answer to the question at the end of [I §5.1] — tracked here as part
of the same item). Handling: the ledger references [II §1.3–1.5] as the
authoritative classification.

## 4. Noted — Hamilton's surgery argument is broken as written
[II, Introduction, p.1]:

> "The Ricci flow with surgery was considered by Hamilton [H5, §4,5];
> unfortunately, his argument, as written, contains an unjustified statement
> (RMAX = Γ on page 62, lines 7-10 from the bottom), which I was unable to fix."

Handling: Perelman's own fix (two scale bounds `h ≪ r`, [II §4.4] δ-cutoff)
is what the ledger's `deltaCutoffFlow` field reflects. A formalization
following [H5] directly would formalize an unjustified step.

## 5. DEFERRED OUT OF SCOPE — collapse ⟹ graph manifold
[II, abstract/§0]:

> "...(1) the statement that a 3-manifold which collapses with local lower
> bound for sectional curvature is a graph manifold - this is deferred to a
> separate paper, as the proof has nothing to do with the Ricci flow..."

It was never published as a preprint by Perelman; the geometry was supplied
by Shioya–Yamaguchi (2005; with a closed-case gap fixed by Kleiner–Lott,
Astérisque 365 (2014)). Handling: `geometrizationConjecture` is recorded as
an obligation whose late-piece alternative (ii) requires this **external**
input; the manuscript-only proof route covers Poincaré/elliptization, which
do not need it ([III §1], [II §8.2-type classification]).

## 6. Editorial — [II] header and [I §13] sketch status
- [I §13] is a *sketch*: the surgery assertions there are a program, not
  theorems; [II] verifies "most" of them (exceptions in item 1 and item 5
  above).
- The geometrization route of [I §13] also relies on Perelman's unpublished
  "[Alexandrov's spaces with curvatures bounded from below, II]" (1991) for
  collapsing with local lower curvature bound — additional evidence for
  item 5.

## Verification boundary of this repo
- `Perelman.lean` (the unified document; formerly split as
  `Perelman/Barrier.lean` + `Perelman/Skeleton.lean` +
  `Perelman/SurgeryFlow.lean`): kernel-checked in Lean
  v4.36.0 during authoring; `#print axioms` on the public theorems lists
  `[propext, Quot.sound]` only.
- `MATHLIB_LAYER.md`: mathematical shapes verified against Mathlib usage in
  an independent check repository, but **not compiled here** (no Mathlib
  build available in the sandbox) — treat as pseudocode until built.
