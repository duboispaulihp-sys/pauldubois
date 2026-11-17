/-
Copyright (c) 2025. Formalization skeleton of Jineon Baek, *Optimality of Gerver's Sofa*
(arXiv:2411.19826).
-/
module

public import GerverSofa.Gerver

/-!
# Optimality of Gerver's sofa: the main theorem

This file assembles Theorem 1.1.1 of the paper:

`αmax = |G|`,

i.e. Gerver's sofa `G` attains the maximum area `αmax` of a moving sofa.

The proof follows Section 1.8.3 of the paper verbatim:

* `≥`: `G` is a moving sofa, so `|G| ≤ αmax`.
* `≤`: by `exists_balanced_maximum_sofa` (Chapters 1–3) there is a maximum-area
  monotone sofa `S*`; by `rotationAngle_eq_pi_half` (Chapter 4) its rotation angle is
  `π/2`; by `injectivity_condition` (Chapter 6) its rotation path satisfies the
  injectivity condition; by `exists_qDomain` (Section 8.1) it determines a point `q*`
  of the domain of `Q`; by `Q_upper_bound` (Section 8.2) `|S*| ≤ Q(q*)`; and by
  `Q_global_max` (the abstract optimization step, proved here) together with the
  optimality of `Q` at Gerver's triple (Section 8.5) and `Q(K_G,B_G,D_G) = |G|`
  (Theorem 8.4.6), `Q(q*) ≤ |G|`.
-/

@[expose] public section

open Real Set MeasureTheory

/-- The upper bound `Q` is maximized at Gerver's triple, so every maximum-area moving
sofa has area at most the area of Gerver's sofa (Section 1.8.3 of the paper). -/
theorem volume_le_volume_gerverSofa (G : GerverSofaData) (S : Set Point)
    (hS : IsMovingSofa S) : volume S ≤ volume G.sofa := by
  obtain ⟨S₁, hS₁sofa, hS₁max, ω, hω, hS₁mono⟩ := exists_balanced_maximum_sofa
  have h1 : volume S ≤ volume S₁ := hS₁max S hS
  obtain ⟨sys, hMS⟩ := hS₁mono
  have h2 : ω = π / 2 :=
    rotationAngle_eq_pi_half hS₁max (isMonotoneSofa_of_isMonotoneSofaWithSystem hMS)
  subst h2
  obtain ⟨hdiff, hsign⟩ := injectivity_condition hS₁max hMS
  obtain ⟨q, hqK⟩ := exists_qDomain hMS ⟨hdiff, hsign⟩
  have h3 : volume S₁ ≤ ENNReal.ofReal (Q q) :=
    Q_upper_bound hMS ⟨hdiff, hsign⟩ q hqK
  have h4 : Q q ≤ Q G.hdom := Q_global_max (G.hoptim q)
  calc volume S
      ≤ volume S₁ := h1
    _ ≤ ENNReal.ofReal (Q q) := h3
    _ ≤ ENNReal.ofReal (Q G.hdom) := ENNReal.ofReal_le_ofReal h4
    _ = volume G.sofa := G.hQeq

/-- **Theorem 1.1.1 of the paper**: Gerver's sofa attains the maximum area `αmax` of a
moving sofa. -/
theorem optimality_of_gerver_sofa (G : GerverSofaData) : αmax = volume G.sofa := by
  apply le_antisymm
  · rw [αmax, sSup_le_iff]
    rintro a ⟨S, hS, rfl⟩
    exact volume_le_volume_gerverSofa G S hS
  · exact le_sSup ⟨G.sofa, G.hsofa, rfl⟩
