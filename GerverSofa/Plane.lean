/-
Copyright (c) 2025. Formalization skeleton of Jineon Baek, *Optimality of Gerver's Sofa*
(arXiv:2411.19826).
-/
module
public import Mathlib.Topology.Order.IntermediateValue
public import Mathlib.Analysis.Convex.Basic
public import Mathlib.Topology.Connected.Basic
public import Mathlib.Basic.Real.Basic
public import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# The plane, rotations, strips, and the hallway

This file sets up the planar geometry of the moving sofa problem, following
Sections 1.1 and 1.2 of the paper:

* `Point` is a point of the plane `ℝ × ℝ`.
* `rotation t` is the counterclockwise rotation `R_t` around the origin by angle `t`
  (Definition 1.2.2 uses the same convention).
* `horizontalStrip`, `verticalStrip` and `verticalStrip'` are the unit strips
  `H`, `V` and `V^ω`.
* `hallwayHorizontal`, `hallwayVertical` and `hallway` are the two sides `HL`, `VL`
  and the L-shaped hallway `L` (Definition 1.1.1).

All elementary facts in this file are fully proved.
-/

@[expose] public section

open Real Set

/-- A point of the plane. -/
abbrev Point := ℝ × ℝ

/-- The counterclockwise rotation `R_t` of the plane around the origin by the angle `t`
(Definition 1.2.2 of the paper). -/
noncomputable def rotation (t : ℝ) (p : Point) : Point :=
  (p.1 * cos t - p.2 * sin t, p.1 * sin t + p.2 * cos t)

lemma rotation_apply (t : ℝ) (x y : ℝ) :
    rotation t (x, y) = (x * cos t - y * sin t, x * sin t + y * cos t) := rfl

lemma rotation_fst (t : ℝ) (p : Point) : (rotation t p).1 = p.1 * cos t - p.2 * sin t := rfl

lemma rotation_snd (t : ℝ) (p : Point) : (rotation t p).2 = p.1 * sin t + p.2 * cos t := rfl

@[simp] lemma rotation_zero (p : Point) : rotation 0 p = p := by
  simp [rotation]

lemma rotation_smul (t : ℝ) (c : ℝ) (p : Point) :
    rotation t (c • p) = c • rotation t p := by
  obtain ⟨x, y⟩ := p
  simp only [rotation_apply, Prod.smul_def, smul_eq_mul]
  refine Prod.ext ?_ ?_ <;> ring

lemma rotation_add_point (t : ℝ) (p q : Point) :
    rotation t (p + q) = rotation t p + rotation t q := by
  obtain ⟨x1, y1⟩ := p
  obtain ⟨x2, y2⟩ := q
  simp only [rotation_apply, Prod.add_def]
  refine Prod.ext ?_ ?_ <;> ring

lemma rotation_add (s t : ℝ) (p : Point) :
    rotation (s + t) p = rotation s (rotation t p) := by
  obtain ⟨x, y⟩ := p
  simp only [rotation_apply, Real.cos_add, Real.sin_add]
  refine Prod.ext ?_ ?_ <;> ring

lemma rotation_neg (t : ℝ) (p : Point) : rotation (-t) (rotation t p) = p := by
  obtain ⟨x, y⟩ := p
  simp only [rotation_apply, Real.cos_neg, Real.sin_neg]
  refine Prod.ext ?_ ?_
  · linear_combination x * Real.sin_sq_add_cos_sq t
  · linear_combination y * Real.sin_sq_add_cos_sq t

lemma rotation_neg' (t : ℝ) (p : Point) : rotation t (rotation (-t) p) = p := by
  have h := rotation_neg (-t) p
  rwa [neg_neg] at h

lemma rotation_surjective (t : ℝ) : Function.Surjective (rotation t) := by
  intro p
  exact ⟨rotation (-t) p, rotation_neg' t p⟩

lemma rotation_injective (t : ℝ) : Function.Injective (rotation t) := by
  intro a b hab
  have : rotation (-t) (rotation t a) = rotation (-t) (rotation t b) := by rw [hab]
  simpa [rotation_neg] using this

lemma rotation_bijective (t : ℝ) : Function.Bijective (rotation t) :=
  ⟨rotation_injective t, rotation_surjective t⟩

lemma continuous_rotation (t : ℝ) : Continuous (rotation t) := by
  refine Continuous.prodMk ?_ ?_
  · exact (continuous_fst.mul continuous_const).sub (continuous_snd.mul continuous_const)
  · exact (continuous_fst.mul continuous_const).add (continuous_snd.mul continuous_const)

/-- `rotation t` as a linear map. -/
noncomputable def rotationLm (t : ℝ) : Point →ₗ[ℝ] Point where
  toFun := rotation t
  map_add' := rotation_add_point t
  map_smul' := rotation_smul t

lemma rotationLm_apply (t : ℝ) (p : Point) : rotationLm t p = rotation t p := rfl

/-- The unit-width horizontal strip `H = ℝ × [0, 1]` (Definition 1.2.3). -/
def horizontalStrip : Set Point := {p | 0 ≤ p.2 ∧ p.2 ≤ 1}

/-- The unit-width vertical strip `V = [0, 1] × ℝ` (Definition 1.2.3). -/
def verticalStrip : Set Point := {p | 0 ≤ p.1 ∧ p.1 ≤ 1}

/-- The vertical strip `V^ω` rotated counterclockwise by `ω` (Definition 1.2.3). -/
noncomputable def verticalStrip' (ω : ℝ) : Set Point := rotation ω '' verticalStrip

/-- The horizontal side `HL = (-∞, 1] × [0, 1]` of the hallway (Definition 1.1.1). -/
def hallwayHorizontal : Set Point := {p | p.1 ≤ 1 ∧ 0 ≤ p.2 ∧ p.2 ≤ 1}

/-- The vertical side `VL = [0, 1] × (-∞, 1]` of the hallway (Definition 1.1.1). -/
def hallwayVertical : Set Point := {p | 0 ≤ p.1 ∧ p.1 ≤ 1 ∧ p.2 ≤ 1}

/-- The L-shaped hallway `L = HL ∪ VL` of unit width (Definition 1.1.1). -/
def hallway : Set Point := hallwayHorizontal ∪ hallwayVertical

lemma horizontalStrip_eq : horizontalStrip = univ ×ˢ Icc 0 1 := by
  ext p
  simp [horizontalStrip]

lemma verticalStrip_eq : verticalStrip = Icc 0 1 ×ˢ univ := by
  ext p
  simp [verticalStrip]

lemma hallwayHorizontal_eq :
    hallwayHorizontal = Iic 1 ×ˢ Icc 0 1 := by
  ext p
  simp [hallwayHorizontal]

lemma hallwayVertical_eq :
    hallwayVertical = Icc 0 1 ×ˢ Iic 1 := by
  ext p
  simp [hallwayVertical, and_assoc]

lemma convex_horizontalStrip : Convex ℝ horizontalStrip := by
  rw [horizontalStrip_eq]
  exact Convex.prod convex_univ (convex_Icc 0 1)

lemma convex_verticalStrip : Convex ℝ verticalStrip := by
  rw [verticalStrip_eq]
  exact Convex.prod (convex_Icc 0 1) convex_univ

lemma convex_hallwayHorizontal : Convex ℝ hallwayHorizontal := by
  rw [hallwayHorizontal_eq]
  exact Convex.prod (convex_Iic 1) (convex_Icc 0 1)

lemma convex_hallwayVertical : Convex ℝ hallwayVertical := by
  rw [hallwayVertical_eq]
  exact Convex.prod (convex_Icc 0 1) (convex_Iic 1)

lemma closed_horizontalStrip : IsClosed horizontalStrip := by
  rw [horizontalStrip_eq]
  exact isClosed_univ.prod isClosed_Icc

lemma closed_verticalStrip : IsClosed verticalStrip := by
  rw [verticalStrip_eq]
  exact isClosed_Icc.prod isClosed_univ

lemma closed_hallwayHorizontal : IsClosed hallwayHorizontal := by
  rw [hallwayHorizontal_eq]
  exact isClosed_Iic.prod isClosed_Icc

lemma closed_hallwayVertical : IsClosed hallwayVertical := by
  rw [hallwayVertical_eq]
  exact isClosed_Icc.prod isClosed_Iic

lemma closed_hallway : IsClosed hallway :=
  closed_hallwayHorizontal.union closed_hallwayVertical

lemma isConnected_hallwayHorizontal : IsConnected hallwayHorizontal :=
  convex_hallwayHorizontal.isConnected ⟨(0, 0), by simp [hallwayHorizontal]⟩

lemma isConnected_hallwayVertical : IsConnected hallwayVertical :=
  convex_hallwayVertical.isConnected ⟨(0, 0), by simp [hallwayVertical]⟩

/-- The hallway `L` is connected. (Used implicitly in the paper, e.g. in
Proposition 1.2.2.) -/
lemma isConnected_hallway : IsConnected hallway :=
  IsConnected.union ⟨(1 / 2, 1 / 2), by
      simp only [hallwayHorizontal, Set.mem_ofPred]
      constructor <;> norm_num, by
      simp only [hallwayVertical, Set.mem_ofPred]
      constructor <;> norm_num⟩
    isConnected_hallwayHorizontal isConnected_hallwayVertical
