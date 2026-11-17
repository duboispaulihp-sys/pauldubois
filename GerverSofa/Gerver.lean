/-
Copyright (c) 2025. Formalization skeleton of Jineon Baek, *Optimality of Gerver's Sofa*
(arXiv:2411.19826).
-/
module

public import GerverSofa.Deep

/-!
# Gerver's sofa

Section 8.4 of the paper constructs Gerver's sofa `G` from the 18 analytic curve
sections of [Rom18] and proves (Theorem 8.4.6) that the overestimated region `R`
coincides with `G`, so that `Q` at the triple `(K_G, B_G, D_G)` equals the area of `G`,
and (Section 8.5, using the local optimality ODEs of Romik) that the directional
derivative of `Q` at `(K_G, B_G, D_G)` is nonpositive in every direction.

In this skeleton, `GerverSofaData` packages these two deep facts as fields; the
existence of such data is the content of Chapter 8 and is not proved here.
-/

@[expose] public section

open Real Set MeasureTheory

/-- The data of Gerver's sofa (Chapter 8 of the paper). -/
structure GerverSofaData where
  /-- The cap `K_G` of Gerver's sofa. -/
  K : Set Point
  /-- The right convex body `B_G`. -/
  B : Set Point
  /-- The left convex body `D_G`. -/
  D : Set Point
  /-- The sofa `G = K_G \ N'(K_G)` itself. -/
  sofa : Set Point
  /-- The triple `(K_G, B_G, D_G)` lies in the domain of `Q`. -/
  hdom : QDomain
  hK : hdom.K = K
  hB : hdom.B = B
  hD : hdom.D = D
  /-- `G` is a moving sofa. -/
  hsofa : IsMovingSofa sofa
  /-- `G` is a monotone sofa of rotation angle `π/2`. -/
  hmono : ∃ sys : HallwaySystem (π / 2), IsMonotoneSofaWithSystem (π / 2) sofa sys
  /-- Section 8.5: the directional derivative of `Q` at `(K_G, B_G, D_G)` towards any
  point of the domain is nonpositive (Equation (1.14) ≤ 0), i.e.
  `Bil((K_G, B_G, D_G), q) ≤ Q(K_G, B_G, D_G)` for all `q`. -/
  hoptim : ∀ q : QDomain, Bil hdom q ≤ Q hdom
  /-- Theorem 8.4.6: the overestimated region `R` coincides with `G`, so `Q` at
  `(K_G, B_G, D_G)` equals the area of `G`. -/
  hQeq : ENNReal.ofReal (Q hdom) = volume sofa
