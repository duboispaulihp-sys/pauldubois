/-
Copyright (c) 2025. Formalization skeleton of Jineon Baek, *Optimality of Gerver's Sofa*
(arXiv:2411.19826).
-/
module

public import GerverSofa.Main

/-!
# Formalization of *Optimality of Gerver's Sofa* (arXiv:2411.19826)

This library formalizes Jineon Baek's resolution of the moving sofa problem.

* `GerverSofa.Plane` — the hallway, strips, and rotations (Section 1.1–1.2).
* `GerverSofa.Motion` — rigid motions, moving sofas, `αmax` (Definition 1.1.2).
* `GerverSofa.StandardPosition` — standard position, Propositions 1.2.1, 1.2.2.
* `GerverSofa.Cap` — hallway systems, caps, niches, the area functional (Section 1.2.2,
  Chapter 2).
* `GerverSofa.Deep` — the deep theorems of Chapters 3, 4, 6, 7, 8 (stated, proofs
  open) and the proved abstract optimization step `Q_global_max`.
* `GerverSofa.Gerver` — the data of Gerver's sofa (Chapter 8).
* `GerverSofa.Main` — the main Theorem 1.1.1.
-/

@[expose] public section
