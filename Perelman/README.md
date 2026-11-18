# Perelman in Lean — manuscript-faithful scaffold

Source restriction (user instruction): **Perelman's three preprints only**.

  [I]   arXiv:math/0211159 (2002) — The entropy formula for the Ricci flow and its geometric applications
  [II]  arXiv:math/0303109 (2003) — Ricci flow with surgery on three-manifolds
  [III] arXiv:math/0307245 (2003) — Finite extinction time for the solutions to the Ricci flow on certain three-manifolds

No content from the 2026 team formalizations (frenzymath, Chow–Liao–Qin, qinz1yang)
is used. See `ERRATA.md` for the errors found inside the manuscripts themselves
and how this scaffold handles them.

## What is here

| File | Status | Content |
| --- | --- | --- |
| `Perelman.lean` | **compiled & kernel-checked** (Lean v4.36.0, no Mathlib, no project axioms) | The unified whole, in three parts. **Part I** — the manuscript dependency ledger `PerelmanInputs`: one `Prop` field per landmark theorem, with exact section references, incl. the two corrections Perelman made to his own [I §11.7] in [II §1]. **Part II** — the arithmetic core of the finite-extinction barrier [III §1.2–1.3], proved in full: `bound_of_steps`, `exists_negative_index`, `no_eternal_survival`. **Part III** — the constant-`r/κ/δ̄` surgery-flow interface [II §4.1–4.7, §5.1–5.3]: `SurgeryControls`, `SurgeryOutcome`, `redefinedTo`/`redefinedTo_anti` (the retroactive "redefining δ̄ᵢ = δ̄ᵢ₊₁" step), `SurgerySequences`/`stageControls`, and the surgery-volume audit theorems `surgery_volume_bound`, `surgery_count_bound` ("every surgery reduces the volume by at least h³, hence the sequence of surgery times is discrete"), `drop_chain`, `stage_budget`, `cumulative_drops`, `total_surgery_budget` |
| `MATHLIB_LAYER.md` | reference only (not compiled here) | The Mathlib-level end statements (smooth/topological Poincaré, geometrization) and the analytic obligations, in verified Mathlib statement shapes |
| `ERRATA.md` | — | Error log of the manuscripts |

`#print axioms` for every compiled theorem of `Perelman.lean` shows only
`[propext, Quot.sound]` or `[propext]` (verified during authoring: no
`sorryAx`, no `Classical.choice`, no project axioms; `Perelman.div_mul_le`
is `private` and appears only inside the closure of
`exists_negative_index`). The file header documents the integer-unit
encoding used for the (real-valued) manuscript constants `ε, r, δ, δ̄, h, κ`.

## Build

```bash
cd Perelman
lake build
```

Requires only the Lean toolchain (`leanprover/lean4:v4.36.0`); the compiled
layer deliberately needs no Mathlib, because a full Mathlib build was not
reproducible in the authoring sandbox (5 cores, GitHub-only network — Mathlib
no longer ships its olean cache as GitHub release assets).

## What is deliberately NOT claimed

- This is **not** a proof of the Poincaré or geometrization conjecture.
- `PerelmanInputs`' fields are proof obligations, not results. Discharging
  them is the multi-person-year-scale work that two teams (arXiv:2610.08329
  and arXiv:2610.13897) completed in October 2026 with millions of lines of
  Lean; that machinery is outside the "manuscripts only" scope of this task.
- The geometrization endgame (collapse with local lower curvature bound ⟹
  graph manifold) is genuinely **outside** the three preprints: Perelman
  deferred it to a separate paper. That fact is recorded in the ledger and
  in `ERRATA.md` item 6 rather than papered over.

## Roadmap to a full manuscript-only formalization

1. **[I §1–3]** F/λ/W functionals on Mathlib's `RiemannianMetric` layer:
   first-variation formula, λ-monotonicity, W-monotonicity via log-Sobolev
   — largest missing Mathlib prerequisite is the Gaussian log-Sobolev
   inequality with weights.
2. **[I §4]** No-local-collapsing I (test function `f = −log φ(dist/r) + c`).
3. **[I §7–8]** L-function, reduced volume (Bishop–Gromov on `M × Sᴺ × ℝ₊`),
   no-local-collapsing II.
4. **[I §10]** Almost-Euclidean regions from the log-Sobolev inequality.
5. **[I §11 + II §1]** Ancient κ-solutions: compactness, classification —
   including the compact-capped-cylinder example of [II §1.4] that corrects
   [I §11.7].
6. **[II §3–4]** Structure at the first singular time; δ-cutoff surgery —
   the constant-`r/κ/δ̄` interface and the surgery-volume audit
   (Part III of `Perelman.lean`) are done above; the geometric content
   (Ω-decomposition, the conformal-factor cap) is ledger work.
7. **[II §5–7]** A priori assumptions by induction (constants suffice for
   the extinction route, per [III §1.4]) — the staged audit theorems
   (`stage_budget`, `cumulative_drops`, `total_surgery_budget`, and the
   δ̄ᵢ := δ̄ᵢ₊₁ redefinition) are the discrete backbone of that induction.
8. **[III]** Minimal-disk barrier; Altschuler–Grayson regularization;
   discrete extinction (arithmetic core already proved above); Kneser ≤
   Milnor bookkeeping → elliptization [III §1.4] and the smooth/topological
   Poincaré corollaries.
9. *(external input, not in the manuscripts)* Kleiner–Lott / Shioya–Yamaguchi
   collapse theorem → geometrization.
