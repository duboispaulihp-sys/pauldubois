# Mathlib layer — end statements and analytic obligations (NOT compiled in this sandbox)

The statements below use Mathlib surface syntax that was independently
compile-verified in a third-party check build (Lean v4.33.1 era Mathlib
`0df444a`); they are reproduced here as the target shapes for this project's
Mathlib layer. Because the authoring sandbox cannot build Mathlib (GitHub-only
network; Mathlib no longer publishes olean caches as GitHub release assets;
5 CPU cores), this file is a specification, not a build artifact. Build with
`lake exe cache get && lake build` in a Mathlib environment before relying on
any of it. **None of it should be trusted as compile-verified until then.**

```lean
import Mathlib

/-- The standard unit three-sphere in ℝ⁴. -/
abbrev ThreeSphere : Set (EuclideanSpace ℝ (Fin 4)) :=
  Metric.sphere (0 : EuclideanSpace ℝ (Fin 4)) 1

/-- Smooth Poincaré conjecture (Morgan–Tian Corollary 0.2, smooth form). -/
def SmoothPoincare : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [SecondCountableTopology M]
    [ChartedSpace (EuclideanSpace ℝ (Fin 3)) M] [IsManifold (𝓡 3) ∞ M]
    [CompactSpace M] [SimplyConnectedSpace M],
    Nonempty (Diffeomorph (𝓡 3) (𝓡 3) M ThreeSphere ∞)

/-- Topological Poincaré conjecture (Morgan–Tian Corollary 0.2, topological
form). -/
def TopologicalPoincare : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [SecondCountableTopology M]
    [ChartedSpace (EuclideanSpace ℝ (Fin 3)) M]
    [CompactSpace M] [SimplyConnectedSpace M], Nonempty (M ≃ₜ ThreeSphere)

/-- Finite extinction, the end statement of manuscript [III §1.1]: every
Ricci-flow-with-surgery solution on a manifold without aspherical prime
factors becomes extinct in finite time, for every initial metric. To be
instantiated against the surgery-flow structure of [II §4, §6.1]. -/
def FiniteTimeExtinction (ManuscriptManifoldShape : Type → Type) : Prop :=
  ∀ (M : Type) (_ : ManuscriptManifoldShape M),
    Nonempty (T : ℕ → Type) -- placeholder: to be typed by the surgery-flow
                            -- interface; see the ledger (Part I) of Perelman.lean.

/-- Analytic obligations to be discharged (manuscript references in
`Perelman.lean`, Part I):
- [I §3.4]      W-entropy monotonicity — needs weighted Gaussian log-Sobolev
                (Gross) on the conjugate heat equation; missing from Mathlib.
- [I §4.1]      no local collapsing I — test function `f = −log φ(d/r) + c`.
- [I §7]        L-length, L-geodesic equations, reduced-volume monotonicity.
- [I §8]        no local collapsing II (via reduced volume).
- [I §11+II§1]  ancient κ-solutions: compactness modulo scaling,
                classification (incl. the [II §1.4] capped-cylinder example).
- [I §12.1]     canonical neighborhoods at high scalar curvature.
- [II §4.4-5]   δ-cutoff surgery; a priori assumptions by induction.
- [III §2-3]    curve shortening in `M × S¹_λ` (Altschuler–Grayson);
                minimal-disk area barrier `dA/dt ≤ −2π − ½ R^min A`.
Of these, only the arithmetic skeleton of the last item's conclusion is
proved in this repo (`Perelman.lean`, Part II).
-/
```
