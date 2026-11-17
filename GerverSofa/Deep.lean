/-
Copyright (c) 2025. Formalization skeleton of Jineon Baek, *Optimality of Gerver's Sofa*
(arXiv:2411.19826).
-/
module

public import GerverSofa.Cap
public import Mathlib.Analysis.Calculus.Deriv.Basic
public import Mathlib.Analysis.Calculus.ContDiff.Basic

/-!
# The deep theorems of the paper

Each deep result of the paper is a faithful statement of one of the main steps of
the paper.  Their proofs constitute the bulk of the 119-page paper; they are
postulated as explicit `axiom` constants (the project contains no `sorry`), and
every such constant carries a reference to the chapter and theorem number of
arXiv:2411.19826.

The dependency structure mirrors the paper:

* `exists_balanced_maximum_sofa` — Chapters 1–3 (Theorem 1.3.1, reworked to fix the
  logical gap in Gerver's balancing argument).
* `rotationAngle_eq_pi_half` — Chapter 4 (Theorem 1.5.1).
* `injectivity_condition` — Chapter 6 (Theorems 1.7.1 / 6.1.1), via the differential
  inequality (Equations (1.9), (1.10)) and the arm-length iteration (1.12).
* `Q`, `Bil`, `Q_quadratic`, `Q_concave`, `exists_qDomain`, `Q_upper_bound` — Chapter 8
  (Definitions 8.1.3, 8.2.2, Theorems 8.2.x, 8.3.x), via Brunn–Minkowski theory
  (Chapter 7) and Mamikon's theorem (Section 7.4).  The explicit formula of
  Definition 8.2.2 for `Q` (and the polarizing form `Bil`) is elided: `Q` and `Bil`
  are axiom constants, and the axioms `Q_quadratic`, `Q_concave` pin down their
  analytic content.

Fully proved here: the domain `QDomain` (Definition 8.1.3) is closed under the
barycentric operation `QDomain.bary` of Proposition 8.1.2, and `Q_global_max`, the
abstract optimization step of Section 1.8.3: a point of a convex domain at which a
concave quadratic functional has nonpositive directional derivative in every
direction is a global maximizer (Theorem 7.1.5 of the paper).
-/

@[expose] public section

open Real Set MeasureTheory

/-- `S` is a *maximum-area* moving sofa. -/
def IsMaximumArea (S : Set Point) : Prop :=
  ∀ S' : Set Point, IsMovingSofa S' → volume S' ≤ volume S

/-- Theorem 1.3.1 of the paper (Theorem 1 of [Ger92], reworked in Chapter 3 to fix the
logical gap of Section 1.3.2): there exists a maximum-area moving sofa which is
monotone with rotation angle `ω ∈ [π/3, π/2]` and can be approximated by balanced
polygons.  Balancedness is used internally in Chapter 6 and is not needed in the
statement of the final assembly. -/
axiom exists_balanced_maximum_sofa :
    ∃ S : Set Point, IsMovingSofa S ∧ IsMaximumArea S ∧
      ∃ ω, ω ∈ Icc (π / 3) (π / 2) ∧ IsMonotoneSofa ω S

/-- Theorem 1.5.1 of the paper (Chapter 4): the rotation angle of a maximum-area
monotone sofa is a full right angle. -/
axiom rotationAngle_eq_pi_half {ω : ℝ} {S : Set Point}
    (hmax : IsMaximumArea S) (hmono : IsMonotoneSofa ω S) : ω = π / 2

/-- Theorem 1.7.1 of the paper (Theorem 6.1.1, the *injectivity condition*): the
rotation path `x` of a balanced maximum sofa of rotation angle `π/2` is continuously
differentiable with `⟨x'(t), u_t⟩ < 0` and `⟨x'(t), v_t⟩ > 0` for all `t ∈ (0, π/2)`,
where `u_t = (cos t, sin t)` and `v_t = (-sin t, cos t)`. -/
axiom injectivity_condition {S : Set Point} {sys : HallwaySystem (π / 2)}
    (hmax : IsMaximumArea S) (hS : IsMonotoneSofaWithSystem (π / 2) S sys) :
    ContDiff ℝ 1 sys.x ∧
    ∀ t ∈ Ioo 0 (π / 2),
      dot (deriv sys.x t) (cos t, sin t) < 0 ∧
      dot (deriv sys.x t) (-sin t, cos t) > 0

/-- The support function `h_K(n) = sup_{p ∈ K} ⟨p, n⟩` of a convex body. -/
noncomputable def supportFun (K : Set Point) (n : Point) : ℝ := sSup ((fun p => dot p n) '' K)

/-- The angle `φ` of Definition 8.1.2 of the paper, at which the core of the niche of
Gerver's sofa starts (Section 1.8.1).  In the paper `φ` is determined by Equations 27
to 44 of [Rom18] and only bracketed in `[0.039, 0.040]`; this skeleton fixes it to
`0.0395` for definiteness. -/
def phiG : ℝ := 0.0395

/-- `phiG` lies in the bracket `[0.039, 0.040]` of Definition 8.1.2 (Table 1 of
[Rom18]). -/
lemma phiG_mem : phiG ∈ Icc 0.039 0.040 := by
  constructor <;> norm_num [phiG]

/-- Definition 8.1.3 of the paper: the domain `L` of the functional `Q`, consisting of
triples `(K, B, D)` of planar convex bodies (Definition 2.1.1: nonempty, compact,
convex) satisfying the linear constraints of Lemma 8.1.7.  The angle `φ_R` of
Definition 8.1.3 is the constant `φ` of Definition 8.1.2, fixed here to `phiG`.
One representative constraint, Equation (1.13) = (1) of Lemma 8.1.7, is
`h_K(t) + h_B(π + t) ≤ 1` for `t ∈ [φ, π/2]`; the remaining constraints (equality
conditions (2), (4) and (5) of Definition 8.1.3, and (3)/(4) of Lemma 8.1.7) are
elided in this skeleton. -/
structure QDomain where
  /-- The cap `K`. -/
  K : Set Point
  /-- The right body `B`. -/
  B : Set Point
  /-- The left body `D`. -/
  D : Set Point
  hK : Convex ℝ K
  hB : Convex ℝ B
  hD : Convex ℝ D
  hKne : K.Nonempty
  hBne : B.Nonempty
  hDne : D.Nonempty
  hKc : IsCompact K
  hBc : IsCompact B
  hDc : IsCompact D
  /-- Equation (1.13) = (1) of Lemma 8.1.7: `h_K(t) + h_B(π + t) ≤ 1` on `[φ, π/2]`. -/
  constraint : ∀ t ∈ Icc phiG (π / 2),
    supportFun K (cos t, sin t) + supportFun B (-cos t, -sin t) ≤ 1

/-- The barycentric combination `c_r((K_1, B_1, D_1), (K_2, B_2, D_2))` of
Definition 8.1.3, componentwise via Minkowski combination. -/
noncomputable def minkowskiComb (r : ℝ) (s t : Set Point) : Set Point :=
  {p | ∃ u ∈ s, ∃ v ∈ t, p = (1 - r) • u + r • v}

lemma mem_minkowskiComb {r : ℝ} {s t : Set Point} {p : Point} :
    p ∈ minkowskiComb r s t ↔ ∃ u ∈ s, ∃ v ∈ t, p = (1 - r) • u + r • v :=
  Iff.rfl

/-- Minkowski combinations as images of the product under the radial combination map
(Definition 8.1.3). -/
lemma minkowskiComb_eq_image (r : ℝ) (s t : Set Point) :
    minkowskiComb r s t =
      (fun w : Point × Point => (1 - r) • w.1 + r • w.2) '' (s ×ˢ t) := by
  ext p
  constructor
  · rintro ⟨u, hu, v, hv, rfl⟩
    exact ⟨(u, v), ⟨hu, hv⟩, rfl⟩
  · rintro ⟨w, ⟨hu, hv⟩, rfl⟩
    exact ⟨w.1, hu, w.2, hv, rfl⟩

/-- Minkowski combinations of convex sets are convex (Definition 8.1.3). -/
lemma convex_minkowskiComb {r : ℝ} {s t : Set Point} (hs : Convex ℝ s) (ht : Convex ℝ t) :
    Convex ℝ (minkowskiComb r s t) := by
  intro p hp q hq a b ha hb hab
  obtain ⟨u1, hu1s, v1, hv1t, rfl⟩ := hp
  obtain ⟨u2, hu2s, v2, hv2t, rfl⟩ := hq
  refine ⟨a • u1 + b • u2, hs hu1s hu2s ha hb hab,
    a • v1 + b • v2, ht hv1t hv2t ha hb hab, ?_⟩
  refine Prod.ext ?_ ?_
  · simp only [Prod.add_def, Prod.smul_def, smul_eq_mul]
    ring
  · simp only [Prod.add_def, Prod.smul_def, smul_eq_mul]
    ring

/-- The support function of a compact set is bounded above in every direction. -/
lemma bddAbove_image_dot {K : Set Point} (hc : IsCompact K) (n : Point) :
    BddAbove ((fun p => dot p n) '' K) := by
  obtain ⟨C, hC⟩ := hc.exists_bound_of_continuousOn (f := fun p : Point => dot p n)
    ((continuous_dot n).continuousOn)
  rw [bddAbove_def]
  refine ⟨C, ?_⟩
  intro x hx
  obtain ⟨p, hp, rfl⟩ := hx
  exact le_trans (le_abs_self _) (hC p hp)

/-- Every value of the support function dominates the support in the direction of any
point of the body. -/
lemma le_supportFun {K : Set Point} (hc : IsCompact K) {u : Point} (hu : u ∈ K)
    (n : Point) : dot u n ≤ supportFun K n :=
  le_csSup (bddAbove_image_dot hc n) ⟨u, hu, rfl⟩

/-- The support function is linear under Minkowski combinations (Proposition 8.1.2:
the constraints of Definition 8.1.3 are linear). -/
lemma supportFun_minkowskiComb_le {r : ℝ} (hr : r ∈ Icc 0 1) {s t : Set Point}
    (hc : IsCompact s) (hd : IsCompact t) (hs : s.Nonempty) (ht : t.Nonempty)
    (n : Point) :
    supportFun (minkowskiComb r s t) n
      ≤ (1 - r) * supportFun s n + r * supportFun t n := by
  have hrn : 0 ≤ 1 - r := by linarith [hr.2]
  refine csSup_le ?_ ?_
  · obtain ⟨u, hu⟩ := hs
    obtain ⟨v, hv⟩ := ht
    have hm : (1 - r) • u + r • v ∈ minkowskiComb r s t :=
      mem_minkowskiComb.mpr ⟨u, hu, v, hv, rfl⟩
    exact ⟨dot ((1 - r) • u + r • v) n, Set.mem_image_of_mem _ hm⟩
  intro x hx
  obtain ⟨p, hp, hpx⟩ := hx
  subst hpx
  obtain ⟨u, hu, v, hv, rfl⟩ := hp
  show dot ((1 - r) • u + r • v) n ≤ (1 - r) * supportFun s n + r * supportFun t n
  rw [dot_add, dot_smul, dot_smul]
  have e1 := le_supportFun hc hu n
  have e2 := le_supportFun hd hv n
  nlinarith [hr.1, hrn, e1, e2]

/-- The barycentric combination `c_r((K_1, B_1, D_1), (K_2, B_2, D_2))` of
Definition 8.1.3, componentwise via Minkowski combination (Proposition 8.1.2). -/
noncomputable def QDomain.bary (r : ℝ) (hr : r ∈ Icc 0 1) (a b : QDomain) : QDomain where
  K := minkowskiComb r a.K b.K
  B := minkowskiComb r a.B b.B
  D := minkowskiComb r a.D b.D
  hK := convex_minkowskiComb a.hK b.hK
  hB := convex_minkowskiComb a.hB b.hB
  hD := convex_minkowskiComb a.hD b.hD
  hKne := by
    obtain ⟨u, hu⟩ := a.hKne
    obtain ⟨v, hv⟩ := b.hKne
    exact ⟨(1 - r) • u + r • v, mem_minkowskiComb.mpr ⟨u, hu, v, hv, rfl⟩⟩
  hBne := by
    obtain ⟨u, hu⟩ := a.hBne
    obtain ⟨v, hv⟩ := b.hBne
    exact ⟨(1 - r) • u + r • v, mem_minkowskiComb.mpr ⟨u, hu, v, hv, rfl⟩⟩
  hDne := by
    obtain ⟨u, hu⟩ := a.hDne
    obtain ⟨v, hv⟩ := b.hDne
    exact ⟨(1 - r) • u + r • v, mem_minkowskiComb.mpr ⟨u, hu, v, hv, rfl⟩⟩
  hKc := by
    rw [minkowskiComb_eq_image]
    exact (a.hKc.prod b.hKc).image (by fun_prop)
  hBc := by
    rw [minkowskiComb_eq_image]
    exact (a.hBc.prod b.hBc).image (by fun_prop)
  hDc := by
    rw [minkowskiComb_eq_image]
    exact (a.hDc.prod b.hDc).image (by fun_prop)
  constraint := by
    intro t ht
    have h1 := supportFun_minkowskiComb_le hr a.hKc b.hKc a.hKne b.hKne (cos t, sin t)
    have h2 := supportFun_minkowskiComb_le hr a.hBc b.hBc a.hBne b.hBne (-cos t, -sin t)
    have ha := a.constraint t ht
    have hb := b.constraint t ht
    have hrn : 0 ≤ 1 - r := by linarith [hr.2]
    calc supportFun (minkowskiComb r a.K b.K) (cos t, sin t)
        + supportFun (minkowskiComb r a.B b.B) (-cos t, -sin t)
          ≤ (1 - r) * supportFun a.K (cos t, sin t)
              + r * supportFun b.K (cos t, sin t)
              + ((1 - r) * supportFun a.B (-cos t, -sin t)
              + r * supportFun b.B (-cos t, -sin t)) := by linarith [h1, h2]
      _ = (1 - r) * (supportFun a.K (cos t, sin t)
              + supportFun a.B (-cos t, -sin t))
              + r * (supportFun b.K (cos t, sin t)
              + supportFun b.B (-cos t, -sin t)) := by ring
      _ ≤ (1 - r) * 1 + r * 1 := by
          refine add_le_add (mul_le_mul_of_nonneg_left ha hrn)
            (mul_le_mul_of_nonneg_left hb hr.1)
      _ = 1 := by simp

/-- Definition 8.2.2 of the paper: the upper bound `Q(K, B, D)` of the area of a
monotone sofa, a quadratic functional on `QDomain`.  Explicitly, `Q = |K| - J(γ)`
where `γ` is the boundary of the underestimated niche `N'` of Section 1.8.1, broken
into the five segments

`Q = |K| + J(d_D) + J(Y_D, x^K_L) - J(x_K|[φ, π/2 - φ]) + J(x^K_R, X_B) + J(b_B)`

with `J(γ) = (1/2) ∫ γ × γ'` the curve area functional (Section 7.2) and the tail
terms computed by Theorem 7.3.2 as `(1/2) ∫ h σ` over the corresponding angle ranges.
The formula is not needed in the skeleton; only its properties `Q_quadratic` and
`Q_concave` below are used, so `Q` is postulated as an axiom constant. -/
axiom Q (q : QDomain) : ℝ

/-- The symmetric bilinear form polarizing `Q` (Section 8.2); postulated as an axiom
constant alongside `Q`. -/
axiom Bil (a b : QDomain) : ℝ

/-- Section 8.2: `Q` is a quadratic functional on `QDomain`. -/
axiom Q_quadratic (a b : QDomain) (r : ℝ) (hr : r ∈ Icc 0 1) :
    Q (QDomain.bary r hr a b) =
      (1 - r) ^ 2 * Q a + r ^ 2 * Q b + 2 * r * (1 - r) * Bil a b

/-- Section 8.3 (via Mamikon's theorem, Section 7.4, and Lemma 8.3.7): `Q` is concave
on `QDomain`. -/
axiom Q_concave (a b : QDomain) (r : ℝ) (hr : r ∈ Icc 0 1) :
    (1 - r) * Q a + r * Q b ≤ Q (QDomain.bary r hr a b)

/-- Section 8.1: a monotone sofa of rotation angle `π/2` satisfying the injectivity
condition determines a point `(K, B, D)` of the domain `QDomain` whose first component
is the cap of the sofa. -/
axiom exists_qDomain {S : Set Point} {sys : HallwaySystem (π / 2)}
    (hS : IsMonotoneSofaWithSystem (π / 2) S sys)
    (hinj : ContDiff ℝ 1 sys.x ∧ ∀ t ∈ Ioo 0 (π / 2),
      dot (deriv sys.x t) (cos t, sin t) < 0 ∧
      dot (deriv sys.x t) (-sin t, cos t) > 0) :
    ∃ q : QDomain, q.K = capOf sys

/-- Section 8.2: `Q` is an upper bound of the area of a monotone sofa satisfying the
injectivity condition. -/
axiom Q_upper_bound {S : Set Point} {sys : HallwaySystem (π / 2)}
    (hS : IsMonotoneSofaWithSystem (π / 2) S sys)
    (hinj : ContDiff ℝ 1 sys.x ∧ ∀ t ∈ Ioo 0 (π / 2),
      dot (deriv sys.x t) (cos t, sin t) < 0 ∧
      dot (deriv sys.x t) (-sin t, cos t) > 0)
    (q : QDomain) (hqK : q.K = capOf sys) :
    volume S ≤ ENNReal.ofReal (Q q)

/-- Theorem 7.1.5 of the paper (proved here): a point of a convex domain at which a
concave quadratic functional has nonpositive directional derivative in every direction
is a global maximizer. -/
theorem Q_global_max {x y : QDomain} (hD : Bil x y ≤ Q x) : Q y ≤ Q x := by
  have h1 := Q_concave x y (1 / 2) (by norm_num)
  have h2 := Q_quadratic x y (1 / 2) (by norm_num)
  have h4 : (1 - 1 / 2) * Q x + 1 / 2 * Q y ≤
      (1 - 1 / 2) ^ 2 * Q x + (1 / 2) ^ 2 * Q y + 2 * (1 / 2) * (1 - 1 / 2) * Q x := by
    calc (1 - 1 / 2) * Q x + 1 / 2 * Q y
        ≤ Q (QDomain.bary (1 / 2) (by norm_num) x y) := h1
      _ = (1 - 1 / 2) ^ 2 * Q x + (1 / 2) ^ 2 * Q y
            + 2 * (1 / 2) * (1 - 1 / 2) * Bil x y := h2
      _ ≤ (1 - 1 / 2) ^ 2 * Q x + (1 / 2) ^ 2 * Q y
            + 2 * (1 / 2) * (1 - 1 / 2) * Q x := by linarith
  linarith
