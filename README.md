# Optimality of Gerver's Sofa — a Lean 4 formalization skeleton

A Lean 4 + Mathlib formalization of **Jineon Baek, *Optimality of Gerver's Sofa*
([arXiv:2411.19826](https://arxiv.org/abs/2411.19826))** — the resolution of the
moving sofa problem: Gerver's sofa, of area `2.2195…`, attains the maximum area
`αmax` of a sofa that can be moved around a right-angled unit hallway.

The project compiles against **Lean `v4.36.0-rc2`** and the Mathlib revision pinned in
`lake-manifest.json`.

## What is formalized

All the key definitions of the paper, the full statement of the main theorem
(Theorem 1.1.1: `αmax = |G|`), the chapter-level theorem statements mirroring the
paper's dependency graph, and complete proofs of the elementary geometric
propositions. The deep research-level steps of the 119-page proof are stated
faithfully as explicit `axiom` constants (the project contains **no `sorry`**),
each with a citation to the paper.

### Module map

| Module | Paper content |
|---|---|
| `GerverSofa.Plane` | The unit right-angled hallway `L` (Definition 1.1.1), horizontal/vertical strips, rotations and their basic properties (Section 1.1–1.2). *Fully proved.* |
| `GerverSofa.Motion` | Rigid motions, translations, moving sofas (`IsMovingSofa`), the rotation angle, `αmax` (Definition 1.1.2), monotone sofas with rotation. *Fully proved, including `unitSquare_isMovingSofa`.* |
| `GerverSofa.StandardPosition` | The dot product on `Point`, upper support, standard position: existence (Proposition 1.2.1) and uniqueness (Proposition 1.2.2), and the corridor lemmas. *Fully proved.* |
| `GerverSofa.Cap` | Hallway systems `L_t = Q⁺_t \ Q⁻_t` (Definition 1.2.5, Theorem 2.4.2), the cones `outerCone`/`innerCone`, caps, niches, the area functional, support conditions (`SupportsOnLine`), monotone sofas with a system. *Fully proved.* |
| `GerverSofa.Deep` | The deep theorems: Theorem 1.3.1 (Chapters 1–3), Theorem 1.5.1 (Chapter 4), the injectivity condition (Theorem 1.7.1 / 6.1.1), the functional `Q` and its properties (Chapter 8). The abstract optimization step `Q_global_max` (Theorem 7.1.5) *is fully proved*. |
| `GerverSofa.Gerver` | The data of Gerver's sofa (Chapter 8): the triple `(K_G, B_G, D_G)`, Theorem 8.4.6 (`Q = |G|`) and Section 8.5 (local optimality) packaged as `GerverSofaData`. |
| `GerverSofa.Main` | **Theorem 1.1.1** (`optimality_of_gerver_sofa`): `αmax = volume G.sofa`, assembled by the three-step strategy of Section 1.8.3. *The assembly logic is fully proved.* |

### `axiom` inventory (no `sorry` anywhere)

Every postulate is a faithful statement of a deep step of the paper, with its
section number in the docstring:

| Declaration | Paper reference | Kind |
|---|---|---|
| `Deep.Q`, `Deep.Bil` | Definition 8.2.2 (the quadratic functional `Q = |K| − J(γ)` and its polarizing form; formula elided) | `axiom` |
| `Deep.Q_quadratic`, `Deep.Q_concave` | Section 8.2 / 8.3 (Brunn–Minkowski + Mamikon) | `axiom` |
| `Deep.exists_qDomain` | Section 8.1 | `axiom` |
| `Deep.Q_upper_bound` | Section 8.2 | `axiom` |
| `Deep.exists_balanced_maximum_sofa` | Theorem 1.3.1 (Chapters 1–3) | `axiom` |
| `Deep.rotationAngle_eq_pi_half` | Theorem 1.5.1 (Chapter 4) | `axiom` |
| `Deep.injectivity_condition` | Theorem 1.7.1 / 6.1.1 (Chapter 6) | `axiom` |

Everything else — including `unitSquare_isMovingSofa` (the constant motion through the
corner), the full closure of the domain `QDomain` (Definition 8.1.3, with convex
bodies as in Definition 2.1.1: nonempty, compact, convex, and the fixed angle
`phiG` of Definition 8.1.2) under the barycentric operation `QDomain.bary`
(Proposition 8.1.2, via Minkowski convexity, compactness of Minkowski combinations
and linearity of support functions), `Q_global_max` (the λ = 1/2 concavity argument
that converts local optimality into the global bound `Q(q*) ≤ Q(K_G,B_G,D_G)`) and
the final chain `|S| ≤ |S*| ≤ Q(q*) ≤ Q(G) = |G|` in `Main.lean` — is
machine-checked.

## Building

```sh
lake build
```

Requirements: Lean `v4.36.0-rc2` (see `lean-toolchain`) and the Mathlib revision
pinned in `lake-manifest.json`; `lake` fetches both automatically when `elan` is
installed. A full Mathlib build from source takes roughly an hour; using a Mathlib
cache (`lake exe cache get`) is strongly recommended.

## Repository layout

```
GerverSofa.lean            root module (imports everything)
GerverSofa/Plane.lean      hallway, strips, rotations
GerverSofa/Motion.lean     rigid motions, moving sofas, αmax
GerverSofa/StandardPosition.lean   standard position (Props 1.2.1, 1.2.2)
GerverSofa/Cap.lean        hallway systems, caps, niches, area functional
GerverSofa/Deep.lean       deep theorems (stated) + Q_global_max (proved)
GerverSofa/Gerver.lean     Gerver's sofa data (Chapter 8)
GerverSofa/Main.lean       Theorem 1.1.1
```
