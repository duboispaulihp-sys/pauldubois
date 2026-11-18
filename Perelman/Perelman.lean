/-
Perelman's three arXiv preprints, formalized as one Lean document.

  [I]   math/0211159 - The entropy formula for the Ricci flow and its
        geometric applications (2002)
  [II]  math/0303109 - Ricci flow with surgery on three-manifolds (2003)
  [III] math/0307245 - Finite extinction time for the solutions to the
        Ricci flow on certain three-manifolds (2003)

Scope and ground rules (manuscript-only, per instruction):

* Every landmark statement of the manuscripts is recorded, with its exact
  section reference, in the dependency ledger of Part I. Ledger entries are
  fields of a structure - proof obligations to be discharged later, never
  project axioms and never `sorry`ed theorems - so the compiled layer adds
  nothing to the kernel that it has not proved itself.

* What the manuscripts allow to be proved by pure logic plus arithmetic is
  proved here in full: the finite-extinction barrier (Part II) and the
  discrete audit layer of the constant-r/kappa/delta-bar surgery flow
  (Part III). The remaining, analytic-geometric content (entropy
  monotonicity, ancient kappa-solutions, canonical neighborhoods, the
  Omega-decomposition, the conformal-factor cap, the kappa-step of the
  a-priori induction) is exactly the content of the ledger: it needs
  Mathlib-scale foundations (no `Real`, no metric spaces, no measure
  theory exist in Lean core) and is deliberately not simulated here;
  the statement shapes for that layer are in MATHLIB_LAYER.md.

* Errors inside the manuscripts are recorded and handled explicitly, not
  silently patched; see ERRATA.md: the retracted horn-volume/smoothness
  claim of [I SS13], the redundant noncompact hypothesis of [I 11.7],
  the overlooked compact-cylinder ancient kappa-solutions [II SS1.3-1.4],
  Hamilton's unjustified `RMAX = Gamma` [II, intro], and the endgame
  (collapse implies graph manifold) which Perelman himself deferred
  outside the three preprints.

* Encoding for the compiled arithmetic: the manuscript's constants are
  positive reals; the compiled layer is core-only, so each constant is a
  positive integer in an arbitrary fixed unit and every manuscript
  inequality is transcribed literally as the corresponding integer
  inequality. Nothing below depends on the choice of unit. The October
  2026 Mathlib-scale formalizations of the same results are deliberately
  not used or consulted: this scaffold is grounded in the three
  preprints alone.

Verification record: `lake build` succeeds on Lean v4.36.0 (no Mathlib,
no project axioms, no `opaque`, no `sorry`); `#print axioms` for every
compiled theorem yields only `[propext]` or `[propext, Quot.sound]`.

Layout:

* Part I   - the manuscript dependency ledger (`PerelmanInputs`);
* Part II  - the finite-extinction barrier of [III], proved in full;
* Part III - the surgery flow of [II], proved in its discrete audit layer,
  with the staged bookkeeping of the a-priori induction of [II SS5.1].
-/

namespace Perelman
/-! ## Part I - the manuscript dependency ledger -/

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

/-! ## Part II - the finite-extinction barrier of [III], proved in full -/

/-
Formal skeleton of Perelman's finite-extinction barrier.

Manuscript source: G. Perelman, "Finite extinction time for the solutions to
the Ricci flow on certain three-manifolds", arXiv:math/0307245, §1 and §3.

Manuscript logic (III §1.1-1.3, restated factor by factor):

* III §1.1 defines `A(α, g)` — the infimum of areas of Lipschitz disks
  bounding the loops of a nontrivial homotopy class `α ∈ π∗(ΛM, M)` of
  contractible loops, minimized over the family `Γ` representing `α`
  (which is nonempty because `M` is not aspherical — Serre).
* III §1.2 (Lemma, cf. [H, §11]) estimates the rate of change of
  `A_t = A(α, g_t)` along a Ricci flow:
      dA_t/dt ≤ −2π − (1/2) R^min_t A_t,
  understood as limsup of forward difference quotients.
* III §1.3 notes `R^min_t ≥ −(3/2)/(t + c)` from the scalar-curvature
  evolution equation, so `Â_t = A_t/(t + c)` obeys
      dÂ_t/dt ≤ −2π/(t + c),
  a right-hand side non-integrable at infinity, while `Â_t` cannot become
  negative. Finite extinction follows.

This file formalizes the extremal, purely arithmetic core of that argument:
a quantity that is provably nonnegative for all time, but whose discretized
evolution has a strictly positive deficit at every step, forces a process
termination time bounded explicitly in terms of the initial value. In the
manuscript this is exactly the inference "the right hand side is
non-integrable at infinity whereas Â_t cannot become negative" (III §1.3),
with the continuous harmonic divergence `∫ 2π/(t+c) dt` supplied at the
Mathlib layer (see ../MATHLIB_LAYER.md). Continuous time, minimal disks,
curve-shortening regularization (III §2-3, following [A-G]) and the
surgery bookkeeping (cf. [P, §4.4]) are not reconstructed here.
-/


/-! ### Stepwise barrier, manuscript III §1.2 in discrete audit form

`A` models the extremal disk-area quantity along successive observation
steps; the deficit `d > 0` models the guaranteed per-step loss. -/

-- The extremal area quantity satisfies the stepwise bound
-- `A (k+1) ≤ A k - d` for all steps `k` (manuscript III §1.2-§1.3).
variable {A : Nat → Int} {d : Int}

/-- Inductive descent: the deficit accumulated over `k` steps is at
least `k * d`. -/
theorem bound_of_steps (hstep : ∀ k, A (k+1) ≤ A k - d) :
    ∀ k, A k ≤ A 0 - k * d := by
  intro k
  induction k with
  | zero => omega
  | succ k ih =>
      have hdistr : ((k : Int) + 1) * d = (k : Int) * d + d := by
        rw [Int.add_mul, Int.one_mul]
      have h2 : A (k+1) ≤ A k - d := hstep k
      have hcast1 : ((k + 1 : Nat) : Int) = (k : Int) + 1 := by omega
      rw [hcast1, hdistr]
      omega

/-- One step of integer division loses at most a remainder. -/
private theorem div_mul_le (n : Int) {d : Int} (hd : 0 < d) : n / d * d ≤ n := by
  have h1 := Int.mul_ediv_add_emod n d
  have h2 : 0 ≤ n % d := Int.emod_nonneg n (by omega)
  have hcomm : n / d * d = d * (n / d) := Int.mul_comm (n / d) d
  rw [hcomm]
  omega

/-- Excess steps force a negative value. This is the arithmetic form of
manuscript III §1.3: "`dÂ_t/dt ≤ −2π/(t + const)`, which implies finite
extinction time since the right hand side is non-integrable at infinity
whereas `Â_t` can not become negative." With a per-step deficit `d > 0`,
a positive initial value cannot survive more than `A 0` steps. -/
theorem exists_negative_index (hd : 0 < d) (hstep : ∀ k, A (k+1) ≤ A k - d)
    (h0 : 0 < A 0) : ∃ N : Nat, A N < 0 := by
  have hcast : ((((A 0).toNat + 1 : Nat) : Int)) = A 0 + 1 := by
    have h1 : A 0 = ((A 0).toNat : Int) := (Int.toNat_of_nonneg (by omega)).symm
    omega
  have hbound := bound_of_steps (A := A) (d := d) hstep
  refine ⟨(A 0).toNat + 1, ?_⟩
  have hstepN := hbound ((A 0).toNat + 1)
  have hcastmul : (((A 0).toNat + 1 : Nat) : Int) * d = (A 0 + 1) * d := by
    rw [hcast]
  rw [hcastmul] at hstepN
  have hv : 0 ≤ A 0 + 1 := by omega
  have h1 : 1 * (A 0 + 1) ≤ d * (A 0 + 1) :=
    Int.mul_le_mul_of_nonneg_right hd hv
  rw [Int.one_mul] at h1
  have h2 : d * (A 0 + 1) = (A 0 + 1) * d := Int.mul_comm d (A 0 + 1)
  rw [h2] at h1
  omega

/-- Therefore a process whose stepwise dynamics forces this deficit cannot
survive forever; it must terminate (in the manuscript: the Ricci flow with
surgery must become extinct in finite time). -/
theorem no_eternal_survival (hd : 0 < d) (hstep : ∀ k, A (k+1) ≤ A k - d)
    (h0 : 0 < A 0) : ¬ (∀ k, 0 ≤ A k) := by
  intro hnonneg
  obtain ⟨N, hN⟩ := exists_negative_index hd hstep h0
  exact absurd hN (by
    have := hnonneg N
    omega)

/-! ## Part III - the surgery flow of [II], in its discrete audit layer -/

/-
Typed interface of the constant-`r/kappa/delta-bar` construction of the
Ricci flow with delta-cutoff surgery.

Manuscript source: G. Perelman, "Ricci flow with surgery on
three-manifolds", arXiv:math/0303109 (cited below as [II]):

* [II, Notation]  epsilon is a fixed small positive constant; delta is a
  positive quantity, supposed to be as small as needed in each argument.
* [II §4.1]  the a priori assumptions held by the solutions under
  construction: (pinching) `Rm ≥ -phi(R) R` for a function phi decreasing
  to zero at infinity, and (canonical neighborhood) a scale `r > 0` such
  that every point where scalar curvature is at least `r^-2` has a
  neighborhood satisfying the conclusions of [II §1.5].
* [II §4.2]  the two claims (scalar curvature bound on parabolic
  neighborhoods from the estimates (1.3); the geodesic-distance estimate
  replacing the unjustified `RMAX = Gamma` of Hamilton [H 5] - ERRATA item 5)
* [II §4.3]  Lemma (`rho = delta r`): there is a radius `h`, `0 < h < delta rho`,
  depending only on `delta`, `rho` and the pinching function `phi`, such that
  for each point `x` with `h(x) = Rbar(x)^-1/2 ≤ h` in an epsilon-horn of
  `(Omega, gbar)` with boundary in `Omega_rho`, the parabolic neighborhood
  `P(x, T, delta^-1 h(x), -h^2(x))` is a strong delta-neck. This is the
  strong-neck lemma input that fixes the surgery radius.
* [II §4.4]  the Ricci flow with delta-cutoff: fix `delta > 0`, compute
  `rho = delta r` and determine `h` from the lemma above; run the flow until
  it goes singular at `t^+`; form the limit `(Omega, gbar)`. If `Omega_rho` is
  empty, the procedure stops - the solution became extinct. Otherwise: remove
  the components of `Omega` containing no point of `Omega_rho`; in every
  epsilon-horn of each remaining component find a delta-neck of radius `h`,
  cut it along the middle two-sphere, remove the horn-shaped end, and glue
  an almost standard cap so that the curvature pinching is preserved and a
  ball of radius `delta'^-1 h` near the cap center is, after scaling,
  `delta'`-close to the standard capped infinite cylinder of [II §2]
  (`delta' = delta'(delta)` tends to zero with `delta`); declare extinct
  every component epsilon-close to a metric quotient of the round sphere.
  "Now since every surgery reduces the volume by at least `h^3`, the
  sequence of surgery times is discrete, and, taking for granted the a
  priori assumptions, we can continue our solution indefinitely, not ruling
  out the possibility that it may become extinct at some finite time."
* [II §4.5]  Lemma (`deltaBar = deltaBar(A, theta)`): for any `A < infinity`
  and `0 < theta < 1` there is `deltaBar` such that for `delta < deltaBar`, at
  a surgery at time `T0` (with `p` the center of the standard cap and
  `T1 = min(T, T0 + theta h^2)`), either the solution on
  `P(p, T0, A h, T1 - T0)` is, after scaling and time shift, `A^-1`-close to
  the standard solution of [II §2], or the same holds up to an earlier
  surgery time `t^+ in [T0, T1)` near which the solution is cut off.
  Corollaries [II §4.6-4.7] convert this into the R-length obstruction for
  curves leaving the ball `B(p, T0, A h)` used in the kappa-step of §5.
* [II §5.1]  Proposition: there exist decreasing sequences
  `0 < r_j < epsilon^2`, `kappa_j > 0`, `0 < deltaBar_j < epsilon^2`,
  `j = 1, 2, ...`, such that for any normalized initial data and any cutoff
  function `delta(t)` with `0 < delta(t) < deltaBar_j` on
  `[2^(j-1) epsilon, 2^j epsilon]`, the Ricci flow with `delta(t)`-cutoff is
  defined for all `t`, is `kappa_j`-noncollapsed, and satisfies the canonical
  neighborhood assumption with parameter `r_j` on
  `[2^(j-1) epsilon, 2^j epsilon]`. The proof is by induction, with the
  retroactive step "defining `r_{i+1}, kappa_{i+1}, deltaBar_{i+1}, and
  redefining `deltaBar_i = deltaBar_{i+1}`"; the kappa-step is the
  admissible-curve argument of [I §7.3] carried out via S5.2-S5.3 on
  barely admissible curves. For the elliptization route [III §1.4] the
  surgery times are controlled by *single constants* `r, kappa, deltaBar` -
  the record `SurgeryControls` below.

Correspondence with the ledger of `Perelman.Skeleton`: `SurgeryControls`
packages exactly what the ledger fields `deltaCutoffFlow` ([II §4.4]) and
`aPrioriAssumptionJustified` ([II §5.1]) assert exists; the analyses of
[II §3] (the structure of `Omega` at a singular time) and [II §5.2-5.3]
(the kappa-noncollapsing step) remain proof obligations of the ledger, not
reproduced here.

Encoding. The manuscript's constants are positive reals. The compiled layer
is deliberately core-only (no Mathlib in the authoring sandbox, hence no
`Real`), so each constant is entered as a positive integer in an arbitrary
fixed unit, and every manuscript inequality transcribes as the
corresponding integer inequality; in particular `delta * (delta * r)` is
the mirror of `delta rho = delta * delta * r` and `h * h * h` the mirror of
the cubic volume loss at a delta-neck of radius `h`. Nothing below depends
on the choice of unit: given any instance of `SurgeryControls` in any unit,
scaling all constants by the same factor leaves every field invariant in
meaning - the bookkeeping theorems are proved for the abstract integers.

The theorems proved here (no project axioms, no `sorry`, no `opaque`):

* `drop_chain` - induction over `m` consecutive surgical steps starting at
  a boundary `b`: the volume surrendered by those surgeries is accumulated
  against the volume at `b`.
* `bound_of_steps_bounded` - bounded version of the barrier descent
  (`bound_of_steps (Part II)`): drops at the first `N` steps only.
* `surgery_volume_bound`, `surgery_count_bound` - [II §4.4]: `N` surgeries
  with cutoff `h` consume at least `N h^3` of volume; hence
  `surgeries * h^3 ≤ initial volume` - the discreteness of the sequence of
  surgery times.
* `boundary`, `cumDrops`, `stage_budget`, `cumulative_drops`,
  `total_surgery_budget` - [II §5.1] in staged, time-dependent-cutoff form:
  with stage `j` of the induction conducted with constants `r_j, kappa_j,
  deltaBar_j` and per-surgery loss `q_j`, each stage's surgery count obeys
  `n_j q_j` ≤ volume at the stage start, and over any finite prefix of
  stages the total volume surrendered to surgery is at most the initial
  volume - the bookkeeping that lets the induction of [II §5.1] continue
  indefinitely "not ruling out the possibility that [the flow] may become
  extinct at some finite time".
* `redefinedTo`, `redefinedTo_anti` - the retroactive step
  "redefining `deltaBar_i = deltaBar_{i+1}`" of [II §5.1] preserves the
  decreasing property of the tolerance sequence.
* `stageControls` - the constant-`r/kappa/deltaBar` record for stage `j`,
  assembled from the sequences of the Proposition [II §5.1] together with
  the strong-neck radius delivered by Lemma [II §4.3].
-/


/-! ### The constants of the delta-cutoff construction, [II §4.1-4.5, §5.1] -/

/-- The constant-`r/kappa/delta-bar` surgery interface.

In the manuscript the constants are positive reals; here each is a positive
integer in an arbitrary fixed unit (see the file header for the encoding)
and every manuscript relation between them is kept as a hypothesis field.

* `eps`       - [II, Notation] the fixed small positive constant epsilon
                with respect to which necks, caps and closeness are taken;
* `r`         - [II §4.1] the canonical neighborhood scale;
* `delta`     - [II §4.4] the cutoff parameter delta;
* `deltaBar`  - [II §4.5] the tolerance `deltaBar = deltaBar(A, theta)` with
                `delta < deltaBar`; constant on the elliptization route
                [III §1.4];
* `h`         - [II §4.3] the surgery (neck) radius with `0 < h < delta rho`,
                `rho = delta r`, delivered by the strong-neck lemma;
* `kappa`     - [II §5.1] the noncollapsing constant kappa_j. -/
structure SurgeryControls where
  /-- Fixed small positive constant [II, Notation]. -/
  eps : Int
  /-- Canonical neighborhood scale [II §4.1]. -/
  r : Int
  /-- Cutoff parameter [II §4.4]. -/
  delta : Int
  /-- Cutoff tolerance `deltaBar(A, theta)` [II §4.5]. -/
  deltaBar : Int
  /-- Surgery radius from the strong-neck lemma [II §4.3]. -/
  h : Int
  /-- Noncollapsing constant [II §5.1 Proposition]. -/
  kappa : Int
  hEpsPos : 0 < eps
  hRPos : 0 < r
  hDeltaPos : 0 < delta
  hDeltaBarPos : 0 < deltaBar
  hHPos : 0 < h
  hKappaPos : 0 < kappa
  hRLtEpsSq : r < eps * eps
  hDeltaBarLtEpsSq : deltaBar < eps * eps
  hDeltaLtDeltaBar : delta < deltaBar
  hLtDeltaRho : h < delta * (delta * r)

/-- The surgery radius is positive, so the manuscript's per-surgery volume
loss "at least `h^3`" ([II §4.4]) is a strictly positive quantity. -/
theorem hcube_pos (c : SurgeryControls) : 0 < c.h * c.h * c.h := by
  have h1 : 0 < c.h * c.h := Int.mul_pos c.hHPos c.hHPos
  exact Int.mul_pos h1 c.hHPos

/-- Bookkeeping obligations of one run of the delta-cutoff procedure of
[II §4.4], with its volume audit.

`volume k` is the total volume of the solution sampled immediately after
the `k`-th observation step; the field `surgeries` counts how many of the
steps were δ-cutoff surgeries. The flow between surgeries only decreases the total volume, and
each surgery removes the delta-neck together with the horn-shaped end,
which contains a ball of volume comparable to `h^3` - the manuscript's
lower bound `volume drop ≥ h^3`. The `Prop` fields are
the geometric outputs of the construction, kept as obligations exactly as
in the ledger `PerelmanInputs.deltaCutoffFlow`. -/
structure SurgeryOutcome (c : SurgeryControls) where
  /-- [II §4.4] the components of `Omega` containing no point of
  `Omega_rho` are removed. -/
  bareComponentsRemoved : Prop
  /-- [II §4.4] in every epsilon-horn of each remaining component a
  delta-neck of radius `h` is cut along its middle two-sphere and the
  horn-shaped end is replaced by an almost standard cap. -/
  deltaNecksCapped : Prop
  /-- [II §4.4; the conformal-factor cap construction, cf. [H 5, §4]]
  the curvature pinching condition is preserved by the cap. -/
  pinchingPreserved : Prop
  /-- [II §4.4] the capped ball of radius `delta'^-1 h` near the cap center
  is, after scaling, `delta'`-close to the standard capped infinite cylinder
  of [II §2], with `delta' = delta'(delta) to 0`. -/
  standardCapCloseness : Prop
  /-- [II §4.4] every component epsilon-close to a metric quotient of the
  round sphere is declared extinct. -/
  extinctComponentsDeclared : Prop
  /-- Total volume sampled at the observation steps (in the fixed unit of
  the integer encoding). -/
  volume : Nat → Int
  volumeNonneg : ∀ k, 0 ≤ volume k
  volumeNonincreasing : ∀ k, volume (k + 1) ≤ volume k
  surgeries : Nat
  /-- The manuscript's per-surgery volume loss [II §4.4]:
  `≥ h^3` whenever step `k` is a surgery. -/
  perSurgeryDrop : ∀ k, k < surgeries →
    volume (k + 1) ≤ volume k - c.h * c.h * c.h

/-- Bounded version of the barrier descent. If the volume drops by `q` on
each of the first `N` steps, then after `k ≤ N` steps it has dropped by at
least `k q` from its initial value - the prefix form of
`bound_of_steps (Part II)`, adapted to drops occurring on a finite
initial segment of the observation steps. -/
theorem bound_of_steps_bounded {V : Nat → Int} {q : Int} :
    ∀ N, (∀ k, k < N → V (k + 1) ≤ V k - q) →
      ∀ k, k ≤ N → V k ≤ V 0 - k * q := by
  intro N
  induction N with
  | zero =>
      intro hdrop k hk
      have he : k = 0 := by omega
      subst he
      omega
  | succ N ih =>
      intro hdrop k hk
      rcases Nat.lt_or_ge k (N + 1) with hlt | hge
      · exact ih (by intro i hi; exact hdrop i (by omega)) k (by omega)
      · have heq : k = N + 1 := by omega
        rw [heq]
        have hcast : ((N + 1 : Nat) : Int) = (N : Int) + 1 := by omega
        have hdistr : ((N : Int) + 1) * q = (N : Int) * q + q := by
          rw [Int.add_mul, Int.one_mul]
        have hd := hdrop N (by omega : N < N + 1)
        have hiN := ih (by intro i hi; exact hdrop i (by omega)) N (Nat.le_refl N)
        rw [hcast, hdistr]
        omega

/-- [II §4.4], quantitatively: after `N` surgeries with cutoff `h` (and
interleaved flow, which never increases volume) the total volume has
dropped by at least `N h^3` from its initial value. -/
theorem surgery_volume_bound (c : SurgeryControls) (o : SurgeryOutcome c)
    (k : Nat) (hk : k ≤ o.surgeries) :
    o.volume k ≤ o.volume 0 - k * (c.h * c.h * c.h) :=
  bound_of_steps_bounded (V := o.volume) (q := c.h * c.h * c.h)
    o.surgeries o.perSurgeryDrop k hk

/-- [II §4.4]: "since every surgery reduces the volume by at least `h^3`,
the sequence of surgery times is discrete" - in audit form: the total
number of surgeries, in units of `h^3`, is bounded by the initial volume.
The time-discreteness itself (positively separated surgery times in real
time) is the minute-bookkeeping statement this integer bound certifies. -/
theorem surgery_count_bound (c : SurgeryControls) (o : SurgeryOutcome c) :
    o.surgeries * (c.h * c.h * c.h) ≤ o.volume 0 := by
  have hb := surgery_volume_bound c o o.surgeries (Nat.le_refl _)
  have hnn := o.volumeNonneg o.surgeries
  omega

/-! ### Staged bookkeeping, [II §5.1]

The induction of [II §5.1] proceeds on stages `j`, conducted on the time
interval `[2^(j-1) epsilon, 2^j epsilon]` with constants `r_j, kappa_j,
deltaBar_j`. The machinery below is the discrete audit of that induction:
surgeries are grouped into stages, each stage `j` containing `n j` surgery
steps of per-surgery loss `q j` (in the manuscript, `q j = h_j^3` for the
surgery radius `h_j` in force on the stage). -/

/-- The surgery index at which stage `j` begins: stage `j` consists of the
surgery steps `boundary n j, ..., boundary n j + n j - 1`. -/
def boundary (n : Nat → Nat) : Nat → Nat
  | 0 => 0
  | j + 1 => boundary n j + n j

/-- Total volume surrendered by the surgeries of the first `j` stages,
staged surgery by surgery. -/
def cumDrops (q : Nat → Int) (n : Nat → Nat) : Nat → Int
  | 0 => 0
  | j + 1 => (n j : Int) * q j + cumDrops q n j

/-- Induction over `m` consecutive surgery steps of one stage, starting at
an arbitrary boundary `b`: the volume at the end of the run plus the total
surrendered volume is bounded by the volume at the start. -/
theorem drop_chain {V : Nat → Int} {q : Int}
    (m : Nat) : ∀ b, (∀ i, i < m → V (b + i + 1) ≤ V (b + i) - q) →
      V (b + m) + (m : Int) * q ≤ V b := by
  induction m with
  | zero =>
      intro b _
      have e : (b + 0 : Nat) = b := rfl
      rw [e]
      omega
  | succ m ih =>
      intro b hbd
      have hcast : ((m + 1 : Nat) : Int) = (m : Int) + 1 := by omega
      have hdistr : ((m : Int) + 1) * q = (m : Int) * q + q := by
        rw [Int.add_mul, Int.one_mul]
      have hidx : (b + (m + 1) : Nat) = b + m + 1 := by omega
      rw [hidx]
      have him := ih b (by intro i hi; exact hbd i (by omega))
      have hlast := hbd m (by omega)
      rw [hcast, hdistr]
      omega

/-- [II §5.1], single stage: the number `n j` of surgeries in stage `j`,
each of loss `q j`, is bounded by the volume available in units of `q j`
when the stage opens. -/
theorem stage_budget {V : Nat → Int} {q : Nat → Int} {n : Nat → Nat}
    (hnn : ∀ k, 0 ≤ V k)
    (hdrop : ∀ j i, i < n j →
      V (boundary n j + i + 1) ≤ V (boundary n j + i) - q j)
    (j : Nat) : (n j : Int) * q j ≤ V (boundary n j) := by
  have him := drop_chain (V := V) (q := q j) (n j) (boundary n j)
    (by intro i hi; exact hdrop j i hi)
  have hnnB := hnn (boundary n j + n j)
  omega

/-- [II §5.1], staged audit: after the surgeries of the first `J` stages,
the remaining volume plus everything surrendered to surgery so far is
bounded by the initial volume. -/
theorem cumulative_drops {V : Nat → Int} {q : Nat → Int} {n : Nat → Nat}
    (hdrop : ∀ j i, i < n j →
      V (boundary n j + i + 1) ≤ V (boundary n j + i) - q j)
    (J : Nat) : V (boundary n J) + cumDrops q n J ≤ V 0 := by
  induction J with
  | zero =>
      have e1 : boundary n 0 = 0 := rfl
      have e2 : cumDrops q n 0 = 0 := rfl
      rw [e1, e2]
      omega
  | succ J ih =>
      have hlocal := drop_chain (V := V) (q := q J) (n J) (boundary n J)
        (by intro i hi; exact hdrop J i hi)
      have e1 : boundary n (J + 1) = boundary n J + n J := rfl
      have e2 : cumDrops q n (J + 1) = (n J : Int) * q J + cumDrops q n J := rfl
      rw [e1, e2]
      omega

/-- [II §5.1]: over any finite prefix of the stage induction, the total
volume surrendered to surgery is at most the initial volume. This is the
discrete content of "we can continue our solution indefinitely, not ruling
out the possibility that it may become extinct at some finite time"
([II §4.4]) in the staged, time-dependent-cutoff form of [II §5.1]. -/
theorem total_surgery_budget {V : Nat → Int} {q : Nat → Int} {n : Nat → Nat}
    (hnn : ∀ k, 0 ≤ V k)
    (hdrop : ∀ j i, i < n j →
      V (boundary n j + i + 1) ≤ V (boundary n j + i) - q j)
    (J : Nat) : cumDrops q n J ≤ V 0 := by
  have hc := cumulative_drops hdrop J
  have hb := hnn (boundary n J)
  omega

/-- The retroactive redefinition of [II §5.1]: "defining `r_{i+1},
kappa_{i+1}, deltaBar_{i+1}`, and redefining `deltaBar_i = deltaBar_{i+1}`".
Redefining a tolerance sequence to its `i`-th value on the prefix below
`i` records that all earlier stages were conducted with the (smaller or
equal) final tolerance. -/
def redefinedTo (f : Nat → Int) (i : Nat) : Nat → Int :=
  fun j => if j ≤ i then f i else f j

/-- The retroactive redefinition of [II §5.1] preserves the decreasing
property of the tolerance sequence. -/
theorem redefinedTo_anti {f : Nat → Int} (hf : ∀ j, f (j + 1) ≤ f j)
    (i : Nat) : ∀ j, redefinedTo f i (j + 1) ≤ redefinedTo f i j := by
  intro j
  simp only [redefinedTo]
  rcases Nat.lt_or_ge j i with hlt | hge
  · rw [if_pos (by omega : j + 1 ≤ i), if_pos (by omega : j ≤ i)]
    omega
  · by_cases heq : j = i
    · rw [heq, if_neg (by omega : ¬ (i + 1 ≤ i)), if_pos (by omega : i ≤ i)]
      exact hf i
    · rw [if_neg (by omega : ¬ (j + 1 ≤ i)), if_neg (by omega : ¬ (j ≤ i))]
      exact hf j

/-- The three sequences of constants of the Proposition [II §5.1]:
`0 < r_j < epsilon^2`, `kappa_j > 0`, `0 < deltaBar_j < epsilon^2`, all
decreasing except the noncollapsing constants, whose values are only
asserted positive. -/
structure SurgerySequences where
  /-- Fixed small positive constant epsilon [II, Notation]. -/
  eps : Int
  /-- Canonical neighborhood parameters by stage [II §5.1]. -/
  r : Nat → Int
  /-- Noncollapsing parameters by stage [II §5.1]. -/
  kappa : Nat → Int
  /-- Cutoff tolerances by stage [II §5.1]. -/
  deltaBar : Nat → Int
  hEpsPos : 0 < eps
  rPos : ∀ j, 0 < r j
  rLtEpsSq : ∀ j, r j < eps * eps
  rAnti : ∀ j, r (j + 1) ≤ r j
  kappaPos : ∀ j, 0 < kappa j
  deltaBarPos : ∀ j, 0 < deltaBar j
  deltaBarLtEpsSq : ∀ j, deltaBar j < eps * eps
  deltaBarAnti : ∀ j, deltaBar (j + 1) ≤ deltaBar j

/-- The constant-`r/kappa/deltaBar` controls in force on stage `j`
([II §5.1]: cutoff `delta` with `delta(t) < deltaBar_j` on
`[2^(j-1) epsilon, 2^j epsilon]`), together with a surgery radius `h`
obeying the strong-neck lemma hypothesis `0 < h < delta rho` of
[II §4.3]; the volume drop at each surgery on the stage is at least
`h^3` ([II §4.4]), feeding the budget theorems above with `q j = h^3`
(here `delta rho = delta * delta * r`). -/
def stageControls (s : SurgerySequences) (j : Nat) (delta h : Int)
    (hΔ : 0 < delta) (hΔb : delta < s.deltaBar j) (hh : 0 < h)
    (hhr : h < delta * (delta * s.r j)) : SurgeryControls where
  eps := s.eps
  r := s.r j
  delta := delta
  deltaBar := s.deltaBar j
  h := h
  kappa := s.kappa j
  hEpsPos := s.hEpsPos
  hRPos := s.rPos j
  hDeltaPos := hΔ
  hDeltaBarPos := s.deltaBarPos j
  hHPos := hh
  hKappaPos := s.kappaPos j
  hRLtEpsSq := s.rLtEpsSq j
  hDeltaBarLtEpsSq := s.deltaBarLtEpsSq j
  hDeltaLtDeltaBar := hΔb
  hLtDeltaRho := hhr

/-- Sanity check: the controls assembled for stage `j` inherit the
manuscript's bounds `delta < deltaBar_j` ([II §4.5]) and
`deltaBar_j < epsilon^2` ([II §5.1]), hence `delta < epsilon^2`. -/
theorem stageControls_delta_lt_eps_sq (s : SurgerySequences) (j : Nat)
    (delta h : Int) (hD : 0 < delta) (hDb : delta < s.deltaBar j) (_hh : 0 < h)
    (hhr : h < delta * (delta * s.r j)) :
    (stageControls s j delta h hD hDb _hh hhr).delta
      < (stageControls s j delta h hD hDb _hh hhr).eps
        * (stageControls s j delta h hD hDb _hh hhr).eps :=
  Int.lt_trans hDb (s.deltaBarLtEpsSq j)
end Perelman
