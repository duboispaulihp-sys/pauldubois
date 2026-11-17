/-
Copyright (c) 2025. Formalization skeleton of Jineon Baek, *Optimality of Gerver's Sofa*
(arXiv:2411.19826).
-/
module

public import GerverSofa.Motion
public import Mathlib.Topology.MetricSpace.Bounded

/-!
# Standard position

This file formalizes Definition 1.2.4 (standard position), Proposition 1.2.1 and
Proposition 1.2.2 of the paper.

A moving sofa `S` of rotation angle `ω ∈ (0, π/2]` is in *standard position* if the
upper sides `y = 1` of `H` and `x cos ω + y sin ω = 1` of `V^ω` support `S` from above.
For closed bounded `S` this is equivalent to `S` being contained in the two closed
half-planes below the lines and touching both lines.

All results of this file are fully proved.
-/

@[expose] public section

open Real Set

/-- The dot product of two points, `⟨p, n⟩`. -/
def dot (p n : Point) : ℝ := p.1 * n.1 + p.2 * n.2

lemma dot_add (p q n : Point) : dot (p + q) n = dot p n + dot q n := by
  simp only [dot, Prod.add_def, add_mul]
  ring

lemma dot_sub (p q n : Point) : dot (p - q) n = dot p n - dot q n := by
  simp only [dot, Prod.sub_def, sub_mul]
  ring

lemma dot_smul (c : ℝ) (p n : Point) : dot (c • p) n = c * dot p n := by
  simp only [dot, Prod.smul_def, smul_eq_mul]
  ring

lemma continuous_dot (n : Point) : Continuous (fun p : Point => dot p n) := by
  simp only [dot]
  exact ((continuous_fst).mul continuous_const).add
    ((continuous_snd).mul continuous_const)

lemma dot_rotation (p n : Point) (t : ℝ) : dot (rotation t p) (rotation t n) = dot p n := by
  obtain ⟨px, py⟩ := p
  obtain ⟨nx, ny⟩ := n
  simp only [dot, rotation_apply]
  linear_combination ((px * nx + py * ny) * Real.sin_sq_add_cos_sq t)

lemma dot_rotation' (p n : Point) (t : ℝ) : dot (rotation t p) n = dot p (rotation (-t) n) := by
  have h : rotation t (rotation (-t) n) = n := rotation_neg' t n
  have h2 := dot_rotation p (rotation (-t) n) t
  rw [h] at h2
  exact h2

lemma dot_unit_vertical (p : Point) : dot p (0, 1) = p.2 := by
  simp [dot]

lemma dot_unit_horizontal (p : Point) : dot p (1, 0) = p.1 := by
  simp [dot]

lemma dot_pair_add (x y c s : ℝ) : dot (x, y) (c, s) = x * c + y * s := by
  simp [dot]

lemma fst_rotation_neg (p : Point) (ω : ℝ) :
    (rotation (-ω) p).1 = dot p (cos ω, sin ω) := by
  simp only [rotation_fst, dot, Real.cos_neg, Real.sin_neg]
  ring

/-- A unit vector `n` *supports `S` from above* (with respect to the line `⟨p, n⟩ = 1`)
if `S` is contained in the half-plane `⟨p, n⟩ ≤ 1` and touches the line `⟨p, n⟩ = 1`.
For closed sets this is equivalent to the supporting-line condition of the paper. -/
def SupportsFromAbove (n : Point) (S : Set Point) : Prop :=
  (∀ p ∈ S, dot p n ≤ 1) ∧ ∃ p ∈ S, dot p n = 1

/-- Definition 1.2.4 of the paper: `S` is in *standard position* for rotation angle `ω`. -/
def InStandardPosition (ω : ℝ) (S : Set Point) : Prop :=
  SupportsFromAbove (0, 1) S ∧ SupportsFromAbove (cos ω, sin ω) S

/-- Proposition 1.2.1 of the paper (existence part): every moving sofa with rotation
angle `ω ∈ (0, π/2)` has a translation in standard position. -/
theorem exists_inStandardPosition {ω : ℝ} {S : Set Point} (hω : ω ∈ Ioo 0 (π / 2))
    (h : IsMovingSofaWithRotation ω S) :
    ∃ v : Point, InStandardPosition ω (translate v S) := by
  obtain ⟨Φ, hΦc, hangle, hne, hc, hconn, hb, -, -, -, -⟩ := h
  have hcomp : IsCompact S := Metric.isCompact_of_isClosed_isBounded hc hb
  have hf1 : Continuous (fun p : Point => p.2) := continuous_snd
  obtain ⟨x1, hx1S, hmax1⟩ := hcomp.exists_isMaxOn hne hf1.continuousOn
  have hf2 : Continuous (fun p : Point => dot p (cos ω, sin ω)) := by
    simp only [dot]
    fun_prop
  obtain ⟨x2, hx2S, hmax2⟩ := hcomp.exists_isMaxOn hne hf2.continuousOn
  have hcos : 0 < cos ω :=
    Real.cos_pos_of_mem_Ioo (by constructor <;> linarith [hω.1, hω.2, Real.pi_pos])
  have hcosne : cos ω ≠ 0 := hcos.ne'
  obtain ⟨b, hbdef⟩ : ∃ b : ℝ, b = 1 - x1.2 := ⟨1 - x1.2, rfl⟩
  obtain ⟨a, hac⟩ : ∃ a : ℝ, a * cos ω = 1 - dot x2 (cos ω, sin ω) - b * sin ω :=
    ⟨(1 - dot x2 (cos ω, sin ω) - b * sin ω) / cos ω, by field_simp⟩
  refine ⟨(a, b), ?_, ?_⟩
  · constructor
    · intro p hp
      obtain ⟨z, hz, rfl⟩ := hp
      have h1 : dot (z + (a, b)) (0, 1) = z.2 + b := by
        rw [dot_add, dot_unit_vertical, dot_pair_add]
        ring
      have h2 : z.2 ≤ x1.2 := hmax1 hz
      rw [h1, hbdef]
      linarith
    · refine ⟨x1 + (a, b), ⟨x1, hx1S, rfl⟩, ?_⟩
      have h1 : dot (x1 + (a, b)) (0, 1) = x1.2 + b := by
        rw [dot_add, dot_unit_vertical, dot_pair_add]
        ring
      rw [h1, hbdef]
      ring
  · constructor
    · intro p hp
      obtain ⟨z, hz, rfl⟩ := hp
      have h1 : dot (z + (a, b)) (cos ω, sin ω)
          = dot z (cos ω, sin ω) + a * cos ω + b * sin ω := by
        simp only [dot, Prod.add_def]
        ring
      have h2 : dot z (cos ω, sin ω) ≤ dot x2 (cos ω, sin ω) := hmax2 hz
      rw [h1, hac]
      linarith
    · refine ⟨x2 + (a, b), ⟨x2, hx2S, rfl⟩, ?_⟩
      have h1 : dot (x2 + (a, b)) (cos ω, sin ω)
          = dot x2 (cos ω, sin ω) + a * cos ω + b * sin ω := by
        simp only [dot, Prod.add_def]
        ring
      rw [h1, hac]
      ring

/-- Proposition 1.2.1 of the paper (uniqueness part): for `ω ∈ (0, π/2)` the translation
into standard position is unique. -/
theorem inStandardPosition_unique {ω : ℝ} {S : Set Point} (hω : ω ∈ Ioo 0 (π / 2))
    {v w : Point} (hv : InStandardPosition ω (translate v S))
    (hw : InStandardPosition ω (translate w S)) : v = w := by
  have hcos : 0 < cos ω :=
    Real.cos_pos_of_mem_Ioo (by constructor <;> linarith [hω.1, hω.2, Real.pi_pos])
  have hcosne : cos ω ≠ 0 := hcos.ne'
  obtain ⟨hv1, p1, hp1S, hp1⟩ := hv.1
  obtain ⟨hw1, q1, hq1S, hq1⟩ := hw.1
  obtain ⟨hv2, p2, hp2S, hp2⟩ := hv.2
  obtain ⟨hw2, q2, hq2S, hq2⟩ := hw.2
  obtain ⟨z1, hz1S, hz1e⟩ := hp1S
  obtain ⟨z2, hz2S, hz2e⟩ := hq1S
  obtain ⟨z3, hz3S, hz3e⟩ := hp2S
  obtain ⟨z4, hz4S, hz4e⟩ := hq2S
  have hz1v : z1 + v = p1 := hz1e
  have hz2v : z2 + w = q1 := hz2e
  have hz3v : z3 + v = p2 := hz3e
  have hz4v : z4 + w = q2 := hz4e
  have e1 : ∀ p ∈ S, p.2 + v.2 ≤ 1 := by
    intro p hp
    have h2 := hv1 (p + v) ⟨p, hp, rfl⟩
    simp only [dot_unit_vertical, Prod.add_def] at h2
    linarith
  have e2 : ∀ p ∈ S, p.2 + w.2 ≤ 1 := by
    intro p hp
    have h2 := hw1 (p + w) ⟨p, hp, rfl⟩
    simp only [dot_unit_vertical, Prod.add_def] at h2
    linarith
  have e3 : z1.2 + v.2 = 1 := by
    rw [← hz1v] at hp1
    simp only [dot_unit_vertical, Prod.add_def] at hp1
    exact hp1
  have e4 : z2.2 + w.2 = 1 := by
    rw [← hz2v] at hq1
    simp only [dot_unit_vertical, Prod.add_def] at hq1
    exact hq1
  have hvy : v.2 = w.2 := by
    have h5 : z1.2 + w.2 ≤ 1 := e2 z1 hz1S
    have h6 : z2.2 + v.2 ≤ 1 := e1 z2 hz2S
    linarith
  have f1 : ∀ p ∈ S, dot p (cos ω, sin ω) + dot v (cos ω, sin ω) ≤ 1 := by
    intro p hp
    have h2 := hv2 (p + v) ⟨p, hp, rfl⟩
    simp only [dot_add] at h2
    linarith
  have f2 : ∀ p ∈ S, dot p (cos ω, sin ω) + dot w (cos ω, sin ω) ≤ 1 := by
    intro p hp
    have h2 := hw2 (p + w) ⟨p, hp, rfl⟩
    simp only [dot_add] at h2
    linarith
  have f5 : dot z3 (cos ω, sin ω) + dot v (cos ω, sin ω) = 1 := by
    rw [← hz3v] at hp2
    simp only [dot_add] at hp2
    exact hp2
  have f6 : dot z4 (cos ω, sin ω) + dot w (cos ω, sin ω) = 1 := by
    rw [← hz4v] at hq2
    simp only [dot_add] at hq2
    exact hq2
  have f7 : dot z3 (cos ω, sin ω) + dot w (cos ω, sin ω) ≤ 1 := f2 z3 hz3S
  have f8 : dot z4 (cos ω, sin ω) + dot v (cos ω, sin ω) ≤ 1 := f1 z4 hz4S
  have hdot : dot v (cos ω, sin ω) = dot w (cos ω, sin ω) := by linarith
  have hdiff : dot (v - w) (cos ω, sin ω) = 0 := by
    rw [dot_sub]
    linarith
  have hcomp : (v.1 - w.1) * cos ω + (v.2 - w.2) * sin ω = 0 := by
    have h : dot (v - w) (cos ω, sin ω) = (v.1 - w.1) * cos ω + (v.2 - w.2) * sin ω := by
      simp only [dot, Prod.sub_def]
    rw [← h]
    exact hdiff
  have h2 : v.2 = w.2 := hvy
  have h1 : v.1 = w.1 := by
    have hzero : (v.1 - w.1) * cos ω = 0 := by rw [← hcomp, h2]; ring
    rcases mul_eq_zero.mp hzero with h | h
    · linarith
    · exact absurd h hcosne
  exact Prod.ext h1 h2

/-- Proposition 1.2.2 (1) of the paper: a moving sofa in standard position is contained
in the horizontal strip `H`. -/
theorem subset_horizontalStrip_of_standardPosition {ω : ℝ} {S : Set Point}
    (hstd : InStandardPosition ω S) (hmov : IsMovingSofaWithRotation ω S) :
    S ⊆ horizontalStrip := by
  intro p hp
  obtain ⟨Φ, hΦc, hangle, hne, hc, hconn, hb, h0tr, h0, h1, h2⟩ := hmov
  obtain ⟨hup1, p1, hp1S, hp1⟩ := hstd.1
  have hv0 : (Φ 0).apply p = p + (Φ 0).2 :=
    RigidMotion.apply_eq_of_isTranslation h0tr p
  have hv0p1 : (Φ 0).apply p1 = p1 + (Φ 0).2 :=
    RigidMotion.apply_eq_of_isTranslation h0tr p1
  have hm1 := h0 ⟨p, hp, rfl⟩
  have hm2 := h0 ⟨p1, hp1S, rfl⟩
  rw [hv0] at hm1
  rw [hv0p1] at hm2
  simp only [hallwayHorizontal, Set.mem_ofPred_eq, Prod.add_def] at hm1 hm2
  have e1 : p.2 + (Φ 0).2.2 ≤ 1 ∧ 0 ≤ p.2 + (Φ 0).2.2 := ⟨hm1.2.2, hm1.2.1⟩
  have e2 : p1.2 + (Φ 0).2.2 ≤ 1 := hm2.2.2
  have hp1'' : p1.2 = 1 := by rw [← dot_unit_vertical]; exact hp1
  have hupp : p.2 ≤ 1 := by
    have h3 := hup1 p hp
    rwa [dot_unit_vertical] at h3
  constructor
  · linarith
  · exact hupp

/-- Proposition 1.2.2 (2) of the paper: for every `t ∈ [0, ω]` the sofa `S` is contained
in a hallway `L_t` which is a translation of `R_t (L)`. -/
theorem exists_hallway_of_standardPosition {ω : ℝ} {S : Set Point}
    (_hstd : InStandardPosition ω S) (hmov : IsMovingSofaWithRotation ω S)
    (t : ℝ) (ht : t ∈ Icc 0 ω) :
    ∃ v : Point, S ⊆ translate v (rotation t '' hallway) := by
  obtain ⟨Φ, hΦc, hangle, hne, hc, hconn, hb, h0tr, h0, h1, h2⟩ := hmov
  have hΦ0 : (Φ 0).1 = 0 := h0tr
  have hΦ1 : (Φ 1).1 = -ω := by
    have h3 : (Φ 0).1 - (Φ 1).1 = ω := hangle
    rw [hΦ0] at h3
    linarith
  have hΦc' : Continuous (fun s => (Φ (1 - s)).1) := by
    fun_prop
  have hgI : ContinuousOn (fun s => (Φ (1 - s)).1) (Icc 0 1) := hΦc'.continuousOn
  have hmem : -t ∈ Icc ((Φ (1 - (0:ℝ))).1) ((Φ (1 - 1)).1) := by
    rw [show (1 - (0:ℝ)) = 1 from by norm_num, show (1 - (1:ℝ)) = 0 from by norm_num,
      hΦ0, hΦ1]
    have ht' : 0 ≤ t ∧ t ≤ ω := ht
    constructor <;> linarith
  obtain ⟨s, hs, hgs⟩ := intermediate_value_Icc (by norm_num : (0:ℝ) ≤ 1) hgI hmem
  have hgs' : (Φ (1 - s)).1 = -t := hgs
  have hsI : 1 - s ∈ Icc 0 1 := by
    constructor <;> linarith [hs.1, hs.2]
  have hsub : S ⊆ (Φ (1 - s)).apply ⁻¹' hallway :=
    fun p hp => h1 (1 - s) hsI ⟨p, hp, rfl⟩
  rw [preimage_hallway, hgs', neg_neg] at hsub
  exact ⟨rotation t (-(Φ (1 - s)).2), hsub⟩

/-- Proposition 1.2.2 (3) of the paper: a moving sofa in standard position is contained
in the rotated vertical strip `V^ω`. -/
theorem subset_verticalStrip'_of_standardPosition {ω : ℝ} {S : Set Point}
    (hstd : InStandardPosition ω S) (hmov : IsMovingSofaWithRotation ω S) :
    S ⊆ verticalStrip' ω := by
  intro p hp
  obtain ⟨Φ, hΦc, hangle, hne, hc, hconn, hb, h0tr, h0, h1, h2⟩ := hmov
  obtain ⟨hup1, -, -, -⟩ := hstd.1
  obtain ⟨hup2, p2, hp2S, hp2⟩ := hstd.2
  have hΦ0 : (Φ 0).1 = 0 := h0tr
  have hΦ1 : (Φ 1).1 = -ω := by
    have h3 : (Φ 0).1 - (Φ 1).1 = ω := hangle
    rw [hΦ0] at h3
    linarith
  have hv1 : ∀ q ∈ S, 0 ≤ dot q (cos ω, sin ω) + (Φ 1).2.1 ∧
      dot q (cos ω, sin ω) + (Φ 1).2.1 ≤ 1 := by
    intro q hq
    have hm := h2 ⟨q, hq, rfl⟩
    simp only [hallwayVertical, Set.mem_ofPred_eq] at hm
    have hcoord : ((Φ 1).apply q).1 = dot q (cos ω, sin ω) + (Φ 1).2.1 := by
      show (rotation (Φ 1).1 q + (Φ 1).2).1 = _
      rw [hΦ1, Prod.add_def]
      simp only [fst_rotation_neg]
    rw [hcoord] at hm
    exact ⟨hm.1, hm.2.1⟩
  have e1 : dot p2 (cos ω, sin ω) + (Φ 1).2.1 ≤ 1 := (hv1 p2 hp2S).2
  have e2 : dot p2 (cos ω, sin ω) = 1 := hp2
  have hv1' : (Φ 1).2.1 ≤ 0 := by linarith
  have hlow : 0 ≤ dot p (cos ω, sin ω) := by linarith [(hv1 p hp).1]
  have hupp : dot p (cos ω, sin ω) ≤ 1 := hup2 p hp
  have hmemV : rotation (-ω) p ∈ verticalStrip := by
    simp only [verticalStrip, Set.mem_ofPred_eq]
    rw [fst_rotation_neg]
    exact ⟨hlow, hupp⟩
  exact ⟨rotation (-ω) p, hmemV, rotation_neg' ω p⟩
