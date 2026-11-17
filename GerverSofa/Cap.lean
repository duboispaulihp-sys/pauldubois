/-
Copyright (c) 2025. Formalization skeleton of Jineon Baek, *Optimality of Gerver's Sofa*
(arXiv:2411.19826).
-/
module

public import GerverSofa.StandardPosition

/-!
# Hallway systems, caps, and niches

This file formalizes the definitions of Section 1.2.2 and Chapter 2 of the paper:

* A `HallwaySystem` encodes the continuously moving supporting hallways `L_t` of a
  monotone sofa by their inner corners `x(t)` and outer corners `y(t)`
  (Definition 1.2.5).  Since `L_t = Q⁺_t \ Q⁻_t` (Theorem 2.4.2), the two corner
  functions determine everything.
* `outerCone y t` is the closed convex cone `Q⁺_t` with vertex `y(t)` bounded by the
  outer walls `a(t)`, `c(t)`; `innerCone x t` is the open convex cone `Q⁻_t` with
  vertex `x(t)` bounded by the inner walls `b(t)`, `d(t)`.
* `parallelogram ω` is `P_ω = H ∩ V^ω`, `fan ω` is `F_ω`.
* `capOf` is the cap `K = P_ω ∩ ⋂ Q⁺_t` (Equation (1.3)) and `nicheOf` is the niche
  `N(K) = F_ω ∩ ⋃ Q⁻_t` (Equation (1.4)).
* `sofaAreaFunctional` is the sofa area functional `A_ω(K) = |K| - |N(K)|`.

All elementary facts in this file are fully proved.
-/

@[expose] public section

open Real Set MeasureTheory

/-- The closed convex cone `Q⁺_t` with vertex `y` bounded from above by the outer walls
`a(t)`, `c(t)` of the hallway of angle `t`, spanned by the directions of the two outer
walls pointing away from the outer corner. -/
def outerCone (y : Point) (t : ℝ) : Set Point :=
  {p | ∃ u v : ℝ, 0 ≤ u ∧ 0 ≤ v ∧ p = y + (u • rotation t (-1, 0) + v • rotation t (0, -1))}

/-- The open convex cone `Q⁻_t` with vertex `x` bounded from above by the inner walls
`b(t)`, `d(t)` of the hallway of angle `t`. -/
def innerCone (x : Point) (t : ℝ) : Set Point :=
  {p | ∃ u v : ℝ, 0 < u ∧ 0 < v ∧ p = x + (u • rotation t (-1, 0) + v • rotation t (0, -1))}

lemma outerCone_unit_zero : outerCone (1, 1) 0 = {p : Point | p.1 ≤ 1 ∧ p.2 ≤ 1} := by
  ext p
  simp only [outerCone, Set.mem_ofPred_eq, rotation_zero]
  constructor
  · rintro ⟨u, v, hu, hv, rfl⟩
    refine ⟨?_, ?_⟩ <;>
      · simp only [Prod.add_def, Prod.smul_def, smul_eq_mul]
        linarith
  · rintro ⟨h1, h2⟩
    exact ⟨1 - p.1, 1 - p.2, by linarith, by linarith, by
      refine Prod.ext ?_ ?_ <;> simp only [Prod.add_def, Prod.smul_def, smul_eq_mul] <;> linarith⟩

lemma innerCone_zero_zero : innerCone (0 : Point) 0 = {p : Point | p.1 < 0 ∧ p.2 < 0} := by
  ext p
  simp only [innerCone, Set.mem_ofPred_eq, rotation_zero]
  constructor
  · rintro ⟨u, v, hu, hv, rfl⟩
    refine ⟨?_, ?_⟩ <;>
      · simp only [Prod.add_def, Prod.smul_def, smul_eq_mul, zero_add]
        linarith
  · rintro ⟨h1, h2⟩
    exact ⟨-p.1, -p.2, by linarith, by linarith, by
      refine Prod.ext ?_ ?_ <;> simp only [Prod.add_def, Prod.smul_def, smul_eq_mul, zero_add] <;> linarith⟩

/-- The hallway `L` itself is `Q⁺_0 \ Q⁻_0` (Theorem 2.4.2 at `t = 0`). -/
lemma hallway_eq_cones : hallway = outerCone (1, 1) 0 \ innerCone (0 : Point) 0 := by
  rw [outerCone_unit_zero, innerCone_zero_zero]
  ext p
  constructor
  · intro hp
    rcases (show p ∈ hallwayHorizontal ∨ p ∈ hallwayVertical from hp) with h | h
    · obtain ⟨h1, h2, h3⟩ := (show p.1 ≤ 1 ∧ 0 ≤ p.2 ∧ p.2 ≤ 1 from h)
      exact ⟨⟨h1, h3⟩, fun hn => by
        obtain ⟨hn1, hn2⟩ := (show p.1 < 0 ∧ p.2 < 0 from hn)
        linarith⟩
    · obtain ⟨h1, h2, h3⟩ := (show 0 ≤ p.1 ∧ p.1 ≤ 1 ∧ p.2 ≤ 1 from h)
      exact ⟨⟨h2, h3⟩, fun hn => by
        obtain ⟨hn1, hn2⟩ := (show p.1 < 0 ∧ p.2 < 0 from hn)
        linarith⟩
  · intro hp
    obtain ⟨hA, hB⟩ := (show (p.1 ≤ 1 ∧ p.2 ≤ 1) ∧ ¬(p.1 < 0 ∧ p.2 < 0) from hp)
    rcases Classical.em (p.2 < 0) with h4 | h4
    · refine Or.inr ⟨?_, hA.1, hA.2⟩
      by_contra h5
      exact hB (show p.1 < 0 ∧ p.2 < 0 from ⟨by linarith, h4⟩)
    · exact Or.inl ⟨hA.1, not_lt.mp h4, hA.2⟩

lemma convex_outerCone (y : Point) (t : ℝ) : Convex ℝ (outerCone y t) := by
  intro p hp q hq a b ha hb hab
  simp only [outerCone, Set.mem_ofPred_eq] at hp hq ⊢
  obtain ⟨u1, v1, hu1, hv1, rfl⟩ := hp
  obtain ⟨u2, v2, hu2, hv2, rfl⟩ := hq
  refine ⟨a * u1 + b * u2, a * v1 + b * v2, by positivity, by positivity, ?_⟩
  refine Prod.ext ?_ ?_
  · simp only [Prod.add_def, Prod.smul_def, smul_eq_mul, rotation_fst]
    linear_combination y.1 * hab
  · simp only [Prod.add_def, Prod.smul_def, smul_eq_mul, rotation_snd]
    linear_combination y.2 * hab

lemma pos_comb {a b u1 u2 : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : a + b = 1)
    (hu1 : 0 < u1) (hu2 : 0 < u2) : 0 < a * u1 + b * u2 := by
  rcases Classical.em (a = 0) with h0 | h0
  · rw [h0, zero_add] at hab
    rw [h0, hab]
    simpa using hu2
  · have hapos : 0 < a := lt_of_le_of_ne ha (Ne.symm h0)
    have h1 : 0 < a * u1 := mul_pos hapos hu1
    have h2 : 0 ≤ b * u2 := mul_nonneg hb hu2.le
    linarith

lemma convex_innerCone (x : Point) (t : ℝ) : Convex ℝ (innerCone x t) := by
  intro p hp q hq a b ha hb hab
  simp only [innerCone, Set.mem_ofPred_eq] at hp hq ⊢
  obtain ⟨u1, v1, hu1, hv1, rfl⟩ := hp
  obtain ⟨u2, v2, hu2, hv2, rfl⟩ := hq
  refine ⟨a * u1 + b * u2, a * v1 + b * v2, pos_comb ha hb hab hu1 hu2,
    pos_comb ha hb hab hv1 hv2, ?_⟩
  refine Prod.ext ?_ ?_
  · simp only [Prod.add_def, Prod.smul_def, smul_eq_mul, rotation_fst]
    linear_combination x.1 * hab
  · simp only [Prod.add_def, Prod.smul_def, smul_eq_mul, rotation_snd]
    linear_combination x.2 * hab

/-- Translating a set distributes over set difference (the translation maps are
bijections). -/
lemma translate_sdiff (v : Point) (s t : Set Point) :
    translate v (s \ t) = translate v s \ translate v t := by
  have hinj : Function.Injective (fun p : Point => p + v) := by
    intro p q h
    have h1 : p.1 + v.1 = q.1 + v.1 := congrArg Prod.fst h
    have h2 : p.2 + v.2 = q.2 + v.2 := congrArg Prod.snd h
    exact Prod.ext (by linarith) (by linarith)
  unfold translate
  exact Set.image_sdiff hinj s t

lemma image_sdiff_rotation (t : ℝ) (s u : Set Point) :
    rotation t '' (s \ u) = rotation t '' s \ rotation t '' u :=
  Set.image_sdiff (rotation_injective t) s u

lemma outerCone_eq_translate (x y : Point) (t : ℝ) (h : x + rotation t (1, 1) = y) :
    outerCone y t = translate x (rotation t '' outerCone (1, 1) 0) := by
  ext p
  simp only [outerCone, Set.mem_ofPred_eq, translate, Set.mem_image, rotation_zero]
  constructor
  · rintro ⟨u, v, hu, hv, rfl⟩
    exact ⟨rotation t ((1, 1) + (u • (-1, 0) + v • (0, -1))),
      ⟨(1, 1) + (u • (-1, 0) + v • (0, -1)), ⟨u, v, hu, hv, rfl⟩, rfl⟩,
      by rw [rotation_add_point, rotation_add_point, rotation_smul, rotation_smul, ← h]; abel⟩
  · rintro ⟨q, ⟨w, ⟨u, v, hu, hv, rfl⟩, rfl⟩, hqx⟩
    refine ⟨u, v, hu, hv, ?_⟩
    rw [← hqx, rotation_add_point, rotation_add_point, rotation_smul, rotation_smul, ← h]
    abel

lemma innerCone_eq_translate (t : ℝ) (x : Point) :
    innerCone x t = translate x (rotation t '' innerCone (0 : Point) 0) := by
  ext p
  simp only [innerCone, Set.mem_ofPred_eq, translate, Set.mem_image, rotation_zero]
  constructor
  · rintro ⟨u, v, hu, hv, rfl⟩
    refine ⟨u • rotation t (-1, 0) + v • rotation t (0, -1),
      ⟨u • (-1, 0) + v • (0, -1), ⟨u, v, hu, hv, by rw [zero_add]⟩,
        by rw [rotation_add_point, rotation_smul, rotation_smul]⟩, ?_⟩
    abel
  · rintro ⟨q, ⟨w, ⟨u, v, hu, hv, rfl⟩, rfl⟩, hqx⟩
    refine ⟨u, v, hu, hv, ?_⟩
    rw [← hqx, zero_add, rotation_add_point, rotation_smul, rotation_smul]
    abel

/-- A *hallway system* of rotation angle `ω`: continuously moving hallways `L_t` for
`t ∈ [0, ω]`, encoded by their inner corners `x(t)` and outer corners `y(t)`.  The
shape condition `y(t) - x(t) = R_t (1, 1)` says the hallway of angle `t` is a translate
of `R_t (L)`. -/
structure HallwaySystem (ω : ℝ) where
  /-- The inner corner `x(t)` of `L_t`. -/
  x : ℝ → Point
  /-- The outer corner `y(t)` of `L_t`. -/
  y : ℝ → Point
  /-- Inner and outer corner of the same hallway differ by `R_t (1, 1)`. -/
  shape : ∀ t, y t - x t = rotation t (1, 1)
  /-- At `t = 0` the hallway is `L` itself, whose inner corner is the origin. -/
  x0 : x 0 = 0
  /-- The hallways move continuously. -/
  contx : Continuous x
  /-- The hallways move continuously. -/
  conty : Continuous y

lemma HallwaySystem.y0 {ω : ℝ} (sys : HallwaySystem ω) : sys.y 0 = (1, 1) := by
  have h := sys.shape 0
  rw [sys.x0, sub_zero, rotation_zero] at h
  exact h

/-- The hallway `L_t` of a hallway system: `L_t = Q⁺_t \ Q⁻_t` (Theorem 2.4.2). -/
def HallwaySystem.L {ω : ℝ} (sys : HallwaySystem ω) (t : ℝ) : Set Point :=
  outerCone (sys.y t) t \ innerCone (sys.x t) t

/-- The hallway `L_t` of a hallway system is a translate of the rotated hallway
`R_t (L)`, i.e. a hallway of angle `t` in the sense of Proposition 1.2.2 (2). -/
lemma HallwaySystem.L_eq {ω : ℝ} (sys : HallwaySystem ω) (t : ℝ) :
    sys.L t = translate (sys.x t) (rotation t '' hallway) := by
  have hx : sys.x t + rotation t (1, 1) = sys.y t := by
    rw [← sys.shape t]
    abel
  have ho : outerCone (sys.y t) t = translate (sys.x t) (rotation t '' outerCone (1, 1) 0) :=
    outerCone_eq_translate (sys.x t) (sys.y t) t hx
  have hi : innerCone (sys.x t) t = translate (sys.x t) (rotation t '' innerCone (0 : Point) 0) :=
    innerCone_eq_translate t (sys.x t)
  unfold HallwaySystem.L
  rw [ho, hi, hallway_eq_cones, image_sdiff_rotation t, translate_sdiff]

/-- The parallelogram `P_ω = H ∩ V^ω` (Section 1.2.2). -/
noncomputable def parallelogram (ω : ℝ) : Set Point := horizontalStrip ∩ verticalStrip' ω

/-- The fan `F_ω = {y ≥ 0, x cos ω + y sin ω ≥ 0}` (Section 1.2.2). -/
noncomputable def fan (ω : ℝ) : Set Point := {p | 0 ≤ p.2 ∧ 0 ≤ dot p (cos ω, sin ω)}

/-- The cap `K = C(S)` of a monotone sofa: `P_ω` intersected with all outer cones
(Equation (1.3)). -/
noncomputable def capOf {ω : ℝ} (sys : HallwaySystem ω) : Set Point :=
  parallelogram ω ∩ ⋂ t ∈ Icc 0 ω, outerCone (sys.y t) t

/-- The niche `N(K)` of a cap: the fan intersected with the union of all inner cones
(Equation (1.4)). -/
noncomputable def nicheOf {ω : ℝ} (sys : HallwaySystem ω) : Set Point :=
  fan ω ∩ ⋃ t ∈ Icc 0 ω, innerCone (sys.x t) t

/-- The sofa area functional `A_ω(K) = |K| - |N(K)|` of Section 1.2.2. -/
noncomputable def sofaAreaFunctional {ω : ℝ} (sys : HallwaySystem ω) : ENNReal :=
  volume (capOf sys) - volume (nicheOf sys)

/-- The parallelogram `P_ω` is convex. -/
lemma convex_parallelogram (ω : ℝ) : Convex ℝ (parallelogram ω) := by
  unfold parallelogram
  refine Convex.inter convex_horizontalStrip ?_
  exact Convex.linear_image convex_verticalStrip (rotationLm ω)

/-- The cap of a hallway system is convex. -/
lemma convex_capOf {ω : ℝ} (sys : HallwaySystem ω) : Convex ℝ (capOf sys) := by
  unfold capOf
  exact Convex.inter (convex_parallelogram ω)
    (convex_iInter₂ fun t _ => convex_outerCone (sys.y t) t)

/-- The support condition of a wall: `S` is contained in the closed half-plane bounded
by the line through `y` with normal `n` and touches that line. -/
def SupportsOnLine (y n : Point) (S : Set Point) : Prop :=
  (∀ p ∈ S, dot (p - y) n ≤ 0) ∧ ∃ p ∈ S, dot (p - y) n = 0

/-- A monotone sofa realized by a specific hallway system (Chapter 2 of the paper):
`S` is the intersection of the horizontal strip with all hallways `L_t` of the system,
and the two outer walls of each hallway support `S`. -/
def IsMonotoneSofaWithSystem (ω : ℝ) (S : Set Point) (sys : HallwaySystem ω) : Prop :=
  S = horizontalStrip ∩ ⋂ t ∈ Icc 0 ω, sys.L t ∧
    ∀ t ∈ Icc 0 ω, SupportsOnLine (sys.y t) (rotation t (1, 0)) S ∧
      SupportsOnLine (sys.y t) (rotation t (0, 1)) S

/-- A *monotone sofa* of rotation angle `ω` (Section 1.2.1): the intersection of
continuously moving supporting hallways. -/
def IsMonotoneSofa (ω : ℝ) (S : Set Point) : Prop :=
  ∃ sys : HallwaySystem ω, IsMonotoneSofaWithSystem ω S sys

lemma isMonotoneSofa_of_isMonotoneSofaWithSystem {ω : ℝ} {S : Set Point} {sys : HallwaySystem ω}
    (h : IsMonotoneSofaWithSystem ω S sys) : IsMonotoneSofa ω S :=
  ⟨sys, h⟩
