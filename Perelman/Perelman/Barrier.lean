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

namespace Perelman

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

end Perelman
