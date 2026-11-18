/-
The manuscript dependency ledger of Perelman's argument, transcribed
from his three arXiv preprints only:

  [I]   math/0211159 - The entropy formula for the Ricci flow and its
        geometric applications (2002)
  [II]  math/0303109 - Ricci flow with surgery on three-manifolds (2003)
  [III] math/0307245 - Finite extinction time for the solutions to the
        Ricci flow on certain three-manifolds (2003)

`PerelmanInputs` below is the ledger: one field per landmark statement
of the manuscripts, each kept as an opaque *field of a structure* - i.e.
a proof obligation to be discharged by construction at the Mathlib
layer (see ../MATHLIB_LAYER.md) - never as a project axiom and never as
a `sorry`ed bare theorem. This deliberately avoids two traps:

* using `opaque X : Prop` would silently add `X` to the kernel axiom
  closure of every theorem below (check with `#print axioms`);
* using the retracted horn-volume claim (see ERRATA.md item 1) would
  make the record unprovable-in-principle - Perelman showed it to be
  unnecessary.

Fields appear in the order in which the route consumes them. The one
constituent that needs no geometry - the finite-extinction barrier of
[III §1.2-§1.3] in discrete audit form - is fully proved with no
project axioms in `Perelman.Barrier`.
-/

namespace Perelman

/-! ### [I] math/0211159 - the entropy formulas (all dimensions,
no curvature assumptions; consumed for the analysis of singularities). -/

/-- The manuscript ledger.

* `noLocalCollapsingI`  - [I §4.1, Theorem] a smooth Ricci flow on a
  closed manifold (`T < ∞`) is not locally collapsing at `T`: no sequence
  of balls `B(p_k, r_k)` with `r_k²/t_k` bounded, `|Rm| ≤ r_k^{-2}` on
  `B_k`, and `r_k^{-n} Vol(B_k) → 0`.

* `noncollapsingCorollary` - [I §4.2] definition of κ-noncollapsing on
  the scale ρ and its consequence: given `g_0` and `T < ∞` there is
  `κ = κ(g_0, T) > 0` with the flow κ-noncollapsed on scale `√T`;
  hence blow-up limits (Hamilton convergence) are ancient
  κ-noncollapsed solutions ([I §4.2, Corollary]).

* `entropyWMonotone` - [I §3.4, formula (3.4)] monotonicity of the
  scale-invariant entropy `W(g, f, τ) = ∫[τ(R + |∇f|²) + f - n]
  (4πτ)^{-n/2} e^{-f} dV`, via the Gaussian logarithmic Sobolev
  inequality of L. Gross; with the gradient-flow reduction of [I §1-2]
  (the F-functional, `λ(g)` = lowest eigenvalue of `-4Δ + R`, and the
  no-steady-or-expanding-breather corollaries [I §2.4]).

* `reducedVolumeMonotone` - [I §7] the reduced volume `∇̄V(τ̄)` obtained
  from the L-function's comparison-geometric analysis on the backward
  Ricci flow is nonincreasing in `τ` along the flow; supplies the
  second (local) noncollapsing mechanism used in [I §8, §10] and in the
  κ-noncollapsing step of the surgery scheme ([II §5.2]). This is the
  "Bishop-Gromov relative volume comparison theorem" for the
  potentially infinite-dimensional formalism of [I §6].

* `ancientKSolutionsCompact` - [I §11.7, as corrected by II §1.1-1.5]
  compactness modulo scaling of the space of ancient κ-solutions, and
  their classification: each is a κ₀-solution or a metric quotient of
  the round sphere; the derivative estimates `|∇R| < ηR^{3/2}`,
  `|R_t| < ηR²` ([II §1.5, (1.3)]). Observe the two corrections of the
  first paragraph of [I §11.7]: the "noncompact" hypothesis was
  redundant (per [II §1.1]), and the possibility of compact ancient
  solutions with cylindrical asymptotic soliton was overlooked - see
  ERRATA.md items 2-3, [II §1.3-1.4].

* `canonicalNeighborhoods` - [I §12.1 / II §1.5] every point of
  sufficiently high scalar curvature has a neighborhood which is a
  strong ε-neck, an ε-cap, a closed manifold ≃ S³ or ℝP³, or a closed
  manifold of constant positive sectional curvature, with the stated
  bounds on scalar curvature (between C₁⁻¹/₂ R and C₂ R), volume
  (≥ C₂⁻¹/₂ R^{-3/2} in cases (a),(b),(c)), and sectional curvature
  (≥ C₁⁻¹/₂ R in case (c)).

* `deltaCutoffFlow` - [II §4.4] the Ricci flow with δ-cutoff: at each
  singular time, in every δ-neck of radius `h(ρ = δr, lemma [II §4.3])`,
  cut along the middle two-sphere, discard the horn end, glue an almost
  standard cap preserving the pinching condition (the conformal-factor
  cap construction adapting [H5 §4]; Hamilton's original argument had
  the unjustified step `RMAX = Γ` - ERRATA.md item 5). Volume decreases
  by ≥ h³ per surgery, so surgery times are discrete.

* `aPrioriAssumptionJustified` - [II §5.1, Proposition] existence of
  decreasing sequences `0 < r_j < ε², κ_j > 0, 0 < δ̄_j < ε²` such that
  for every normalized initial metric and cutoff function
  `δ(t) < δ̄_j` on `[2^{j-1}ε, 2^jε]`, the Ricci flow with δ(t)-cutoff
  is defined on `[0, +∞)`, satisfies κ_j-noncollapsing, and satisfies
  the canonical neighborhood assumption with parameter `r_j` on
  `[2^{j-1}ε, 2^jε]`; justification is by induction, the κ-step being
  the admissible-curve argument of [I §7.3] carried out on
  barely-admissible curves ([II §6]). For the elliptization route
  [III §1.4] constant values `r, κ, δ̄` suffice.

* `minimalDiskBarrier` - [III §1.2, Lemma; proof in III §3] for a
  smooth Ricci flow on a closed three-manifold and any nontrivial
  relative homotopy class `α ∈ π∗(ΛM, M)` (nonempty by Serre's
  classical result when `M` is not aspherical), `A_t = A(α, g_t)`
  satisfies `dA_t/dt ≤ -2π - (1/2) R^min_t A_t` in the limsup of
  forward difference quotients; the analytic proof uses
  Altschuler-Grayson regularization of curve shortening in
  `M × S¹_λ` ([III §2-3]). The scalar-curvature estimate
  `R^min_t ≥ -3/2/(t + const)` then gives (III §1.3)
  `dÂ_t/dt ≤ -2π/(t + c)` for `Â_t = A_t/(t + c)` - the interval
  arithmetic form of which is proved unconditionally in
  `Perelman.Barrier` (see `bound_of_steps`, `extinct_below_zero`,
  `no_eternal_survival`).

* `finiteTimeExtinction` - [III §1.1, Theorem] for a closed oriented
  three-manifold whose prime decomposition contains no aspherical
  factors, and any initial metric, the solution to the Ricci flow with
  surgery ([II §6.1]) becomes extinct in finite time. Irreducible case
  [III §1.1-1.3]; general case via Kneser + Milnor-uniqueness and the
  (1+ξ)-Lipschitz trivial-surgery property [III §1.3, §1.5]. The
  purely arithmetic skeleton of the extinction inference is
  `Perelman.Barrier.no_eternal_survival`.

* `elliptization` - [III §1.4, Remark] the extinction theorem together
  with [I §1-5] and Kneser proves: a closed manifold with finite
  π₁ is homeomorphic to a spherical space form; surgery times are
  controlled by single constants `r, κ, δ̄`, and Kneser itself can be
  avoided by tracking π₁ through distance-nonincreasing homotopy
  equivalences at surgeries ([III §1.4, end]).

* `poincareConjecture` - every closed simply-connected topological
  three-manifold is homeomorphic to `S³` (equivalently for smooth
  structures: diffeomorphic to the round `S³`). Route from the
  manuscripts: [II §8] + extinguishing surgery solutions. Does NOT
  require the collapse-to-graph-manifold material.

* `geometrizationConjecture` - [I §13, sketch] every closed oriented
  three-manifold admits a prime decomposition (Kneser-Milnor) each of
  whose factors is geometrized. The endgame is NOT contained in the
  three preprints: [II] defers "collapse with local lower sectional
  curvature bound ⟹ graph manifold" to a separate paper, and the
  long-time analysis of [I §13] is a sketch only - see ERRATA.md
  item 6. Alternatives: after [I §12.1] and [II], the surviving
  component at a late time admits either (i) complete finite-volume
  hyperbolic pieces with cusp tori, or (ii) locally collapsed pieces,
  or (iii) closed pieces of nonnegative sectional curvature - the
  dichotomy used at [I §13]. Formalizing (ii) requires the external
  collapse theory; a manuscript-only formalization therefore records
  this field as an obligation discharged by an explicitly separated
  external input (Kleiner-Lott 2014, Shioya-Yamaguchi 2005), not by
  content of the three preprints.
-/
structure PerelmanInputs where
  /-- [I §4.1] -/
  noLocalCollapsingI : Prop
  /-- [I §4.2] κ-noncollapsing along the flow and for blow-up limits. -/
  noncollapsingCorollary : Prop
  /-- [I §3.4] W-entropy monotonicity (with [I §1-2] as gradient flow). -/
  entropyWMonotone : Prop
  /-- [I §7] reduced-volume monotonicity on the backward flow. -/
  reducedVolumeMonotone : Prop
  /-- [I §11.7 + II §1.1-1.5] corrected compactness and classification
  of ancient κ-solutions. -/
  ancientKSolutionsCompact : Prop
  /-- [I §12.1 / II §1.5] -/
  canonicalNeighborhoods : Prop
  /-- [II §4.4] -/
  deltaCutoffFlow : Prop
  /-- [II §5.1] -/
  aPrioriAssumptionJustified : Prop
  /-- [III §1.2; III §3] -/
  minimalDiskBarrier : Prop
  /-- [III §1.1] -/
  finiteTimeExtinction : Prop
  /-- [III §1.4] -/
  elliptization : Prop
  /-- every closed simply-connected topological 3-manifold ≃ S³. -/
  poincareConjecture : Prop
  /-- [I §13], with the deferred collapse analysis of
  ERRATA.md item 6 as a separated external input. -/
  geometrizationConjecture : Prop

end Perelman
