/-
Copyright (c) 2025. Formalization skeleton of Jineon Baek, *Optimality of Gerver's Sofa*
(arXiv:2411.19826).
-/
module

public import GerverSofa.Plane

/-!
# Rigid motions, moving sofas, and the maximum area

This file formalizes Definition 1.1.2 (moving sofa) and the quantity `αmax`
of Section 1.1 of the paper.

Following footnote 3 of the paper, a rigid motion is encoded by a rotation angle
and a translation vector, and the movability of `S` is the existence of a continuous
curve `Φ : ℝ → RigidMotion` of rigid motions with

* `Φ 0` a translation with `Φ 0 '' S ⊆ HL`,
* `Φ t '' S ⊆ L` for all `t ∈ [0, 1]`,
* `Φ 1 '' S ⊆ VL`.

Boundedness of `S` is additionally required: it is automatic for maximum-area sofas
(since the hallway intersection of Section 1.2 is bounded) and is needed to make sense
of widths in Section 1.2.
-/

@[expose] public section

open Set MeasureTheory

/-- A rigid motion of the plane: rotation by `rot` around the origin, followed by
translation by `shift`.  The underlying type is `ℝ × Point` so that continuity of a
curve of rigid motions is ordinary componentwise continuity. -/
abbrev RigidMotion := ℝ × Point

/-- The action of a rigid motion on a point. -/
noncomputable def RigidMotion.apply (m : RigidMotion) (p : Point) : Point :=
  rotation m.1 p + m.2

lemma RigidMotion.apply_inv (m : RigidMotion) (p : Point) :
    rotation (-m.1) (m.apply p - m.2) = p := by
  have h : m.apply p - m.2 = rotation m.1 p := by
    show rotation m.1 p + m.2 - m.2 = rotation m.1 p
    abel
  rw [h, rotation_neg]

lemma RigidMotion.apply_injective (m : RigidMotion) :
    Function.Injective m.apply := by
  intro a b hab
  have h : rotation (-m.1) (m.apply a - m.2) = rotation (-m.1) (m.apply b - m.2) := by
    rw [hab]
  rw [RigidMotion.apply_inv, RigidMotion.apply_inv] at h
  exact h

lemma RigidMotion.apply_surjective (m : RigidMotion) :
    Function.Surjective m.apply := by
  intro p
  refine ⟨rotation (-m.1) (p - m.2), ?_⟩
  show rotation m.1 (rotation (-m.1) (p - m.2)) + m.2 = p
  rw [rotation_neg']
  abel

lemma RigidMotion.continuous_apply (m : RigidMotion) : Continuous m.apply := by
  show Continuous (fun p => rotation m.1 p + m.2)
  exact (continuous_rotation m.1).add continuous_const

/-- Translation of a set by a vector. -/
def translate (v : Point) (s : Set Point) : Set Point := (fun p => p + v) '' s

/-- A rigid motion is a *translation* when its rotation angle is zero. -/
def RigidMotion.IsTranslation (m : RigidMotion) : Prop := m.1 = 0

lemma RigidMotion.apply_eq_of_isTranslation {m : RigidMotion} (h : m.IsTranslation) (p : Point) :
    m.apply p = p + m.2 := by
  show rotation m.1 p + m.2 = p + m.2
  rw [h, rotation_zero]

/-- The preimage of the hallway under a rigid motion is a translate of the rotated
hallway.  This is the geometric fact behind "S is contained in a hallway `L_t` which
is a translation of `R_t (L)`" (Proposition 1.2.2 (2) of the paper). -/
lemma preimage_hallway (m : RigidMotion) :
    m.apply ⁻¹' hallway =
      translate (rotation (-m.1) (-m.2)) (rotation (-m.1) '' hallway) := by
  ext p
  constructor
  · intro hp
    refine ⟨rotation (-m.1) (m.apply p), ⟨m.apply p, hp, rfl⟩, ?_⟩
    show rotation (-m.1) (m.apply p) + rotation (-m.1) (-m.2) = p
    rw [← rotation_add_point]
    have h2 : m.apply p + -m.2 = rotation m.1 p := by
      show rotation m.1 p + m.2 + -m.2 = rotation m.1 p
      abel
    rw [h2, rotation_neg]
  · rintro ⟨z, ⟨w, hw, rfl⟩, hp⟩
    have hp' : rotation (-m.1) w + rotation (-m.1) (-m.2) = p := hp
    have h1 : rotation m.1 p = w - m.2 := by
      rw [← hp', rotation_add_point]
      simp only [rotation_neg']
      abel
    show rotation m.1 p + m.2 ∈ hallway
    rw [h1]
    have h2 : w - m.2 + m.2 = w := by abel
    rwa [h2]

/-- Definition 1.1.2 of the paper: `S` is a *moving sofa*. -/
def IsMovingSofa (S : Set Point) : Prop :=
  S.Nonempty ∧ IsClosed S ∧ IsConnected S ∧ Bornology.IsBounded S ∧
  ∃ Φ : ℝ → RigidMotion, Continuous Φ ∧
    (Φ 0).IsTranslation ∧ (Φ 0).apply '' S ⊆ hallwayHorizontal ∧
    (∀ t ∈ Icc (0:ℝ) 1, (Φ t).apply '' S ⊆ hallway) ∧
    (Φ 1).apply '' S ⊆ hallwayVertical

/-- The (clockwise) rotation angle of a motion, i.e. the amount `S` rotates as it moves
from `HL` to `VL` (Definition 1.2.1).  A clockwise rotation of `ω` means the rotation
component decreases by `ω`. -/
def rotationAngle (Φ : ℝ → RigidMotion) : ℝ := (Φ 0).1 - (Φ 1).1

/-- A moving sofa together with a motion of rotation angle `ω`. -/
def IsMovingSofaWithRotation (ω : ℝ) (S : Set Point) : Prop :=
  ∃ Φ : ℝ → RigidMotion, Continuous Φ ∧ rotationAngle Φ = ω ∧
    S.Nonempty ∧ IsClosed S ∧ IsConnected S ∧ Bornology.IsBounded S ∧
    (Φ 0).IsTranslation ∧ (Φ 0).apply '' S ⊆ hallwayHorizontal ∧
    (∀ t ∈ Icc (0:ℝ) 1, (Φ t).apply '' S ⊆ hallway) ∧
    (Φ 1).apply '' S ⊆ hallwayVertical

lemma isMovingSofa_of_isMovingSofaWithRotation {ω : ℝ} {S : Set Point}
    (h : IsMovingSofaWithRotation ω S) : IsMovingSofa S := by
  obtain ⟨Φ, hΦ, -, hne, hc, hconn, hb, h0, h1, h2, h3⟩ := h
  exact ⟨hne, hc, hconn, hb, ⟨Φ, hΦ, h0, h1, h2, h3⟩⟩

/-- The set of areas of moving sofas (Section 1.1 of the paper). -/
noncomputable def sofaAreas : Set ENNReal :=
  {a : ENNReal | ∃ S : Set Point, IsMovingSofa S ∧ volume S = a}

/-- The maximum area `αmax` of a moving sofa (Section 1.1 of the paper). -/
noncomputable def αmax : ENNReal := sSup sofaAreas

/-- A `1 × 1` square is a moving sofa: placed at the corner `[0,1] × [0,1]` it is
already contained in both `HL` and `VL`, so the constant identity motion moves it
from `HL` to `VL`.  This shows `sofaAreas` is nonempty. -/
theorem unitSquare_isMovingSofa :
    IsMovingSofa (Icc 0 1 ×ˢ (Icc 0 1 : Set ℝ)) := by
  have hsq : ∀ p : Point, p ∈ Icc 0 1 ×ˢ (Icc 0 1 : Set ℝ) →
      p ∈ hallwayHorizontal ∧ p ∈ hallway ∧ p ∈ hallwayVertical := by
    intro p hp
    obtain ⟨h1, h2⟩ := hp
    obtain ⟨h1a, h1b⟩ := h1
    obtain ⟨h2a, h2b⟩ := h2
    exact ⟨⟨h1b, h2a, h2b⟩, Or.inl ⟨h1b, h2a, h2b⟩, ⟨h1a, h1b, h2b⟩⟩
  have hI : IsConnected (Icc (0:ℝ) 1) := isConnected_Icc (by norm_num)
  have hconn : IsConnected (Icc (0:ℝ) 1 ×ˢ (Icc (0:ℝ) 1 : Set ℝ)) := hI.prod hI
  have hbdd : Bornology.IsBounded (Icc (0:ℝ) 1 ×ˢ (Icc (0:ℝ) 1 : Set ℝ)) :=
    (isCompact_Icc.prod isCompact_Icc).isBounded
  have hApp : ∀ q : Point, RigidMotion.apply ((0:ℝ), (0, 0)) q = q := by
    intro q
    refine Prod.ext ?_ ?_ <;> simp [RigidMotion.apply, rotation_zero, Prod.add_def]
  refine ⟨⟨(0, 0), by norm_num⟩, isClosed_Icc.prod isClosed_Icc, hconn, hbdd,
    ⟨fun _ => (0, (0, 0)), continuous_const, rfl, ?_, ?_, ?_⟩⟩
  · intro p hpimg
    obtain ⟨q, hq, hpq⟩ := hpimg
    subst hpq
    rw [hApp q]
    exact (hsq q hq).1
  · intro t _ p hpimg
    obtain ⟨q, hq, hpq⟩ := hpimg
    subst hpq
    rw [hApp q]
    exact (hsq q hq).2.1
  · intro p hpimg
    obtain ⟨q, hq, hpq⟩ := hpimg
    subst hpq
    rw [hApp q]
    exact (hsq q hq).2.2
