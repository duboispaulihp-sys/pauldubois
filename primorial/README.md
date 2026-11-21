# Primorial Transport Program

Formal and machine-certified analysis of the primorial-ratio framework
(`α_k = log N_{k+1} / log N_k`) and its connection to the Riemann hypothesis via
J.-L. Nicolas' criterion (1983).

## Contents

- [`proof/LEAN.tex`](proof/LEAN.tex) — the canonical LaTeX manuscript of the program (single
  source; the former plain printouts `primorial-transport.tex/.md/.pdf` were
  removed at the author's request). Build with `pdflatex LEAN.tex` twice (note:
  authored without a TeX toolchain in the sandbox; treat as reviewed source).
  Contents: step identities, exact solutions of all three identity families
  (origin-phase, modified single-level, mixed-level), the chained
  constant-offset two-form analysis (§3.4: an ε-scale approximation that does
  **not** close — phantom chain over-estimates $H$; refuted at line 1 for
  seed 0, by certified anchor data), the memoir recurrence
  theory (closed form, monotonicity, trichotomy, linear confinement), the error
  decomposition, the y-sign theorems, and the bridges to RH:
  - **Theorem 7 (MAIN BRIDGE):** original-system `y > 0` for all sufficiently
    large `k` ⟹ RH;
  - **Theorem 8 (anchored dichotomy):** chain seeded at `H ≥ H_K` stays positive;
    seeded at `H < H_K` it turns negative eventually;
  - **§9, anchor evaluation:** exact first step at `K = 10^8`,
    `H_1 = (1+r_K)H + s_K/u_K` (certified by `verification/h1_at_1e8.py`), every
    `H_i` an explicit affine function of the seed `H`;
  - **Theorem 9 (§9.5, all-step chain positivity `H_i > 0`):** under seed
    dominance `H_K ≤ H` (certified at the anchor, `H_K = 4132.288212`) and
    Nicolas' criterion `f(p_{K+i}) < 1` at every step, `H_i ≥ ε_{K+i}/u_K > 0`
    for every `i`; with the normalized iff criterion
    `H_i > 0 ∀i ⟺ π_i > H_K − H ∀i` (`π_i` = normalized physical chain). At
    `i = 1` positivity is certified unconditionally (`f(p_{K+1}) < 1`); the
    all-step statement is exactly the RH-hard half (Theorem 7 bridge).
  - **Corollary `cor:superpos` (§9, unconditional):** for every seed
    `H > H_K` the chain is *eventually* positive (Mertens: `H_i/P_i →
    H − H_K > 0`), so all possible failures of `H_i > 0` are confined to a
    finite initial window — which, at the critical seed `H = H_K`, becomes
    the whole tail and is exactly the RH-hard brick.
  - **Proposition `prop:hiposwin` (§9, certified window, unconditional):**
    `H_i > 0` for every `0 ≤ i ≤ 2×10⁸` at the physical seed (0 flips; min
    margin ε = 2.44e-5 vs float drift ≤ 3e-12, safety ≥ 8.1e6; cross-checked
    vs the deep pass at 7 checkpoints, rel. 3.3e-11) — equivalently Nicolas'
    criterion `f(p) < 1` certified for the 2×10⁸ consecutive primes in
    `[2 038 074 751, 6 461 335 109]` (`verification/hipos_window.py`). The
    tail `i > 2×10⁸` remains the RH-hard brick.
  - Appendix A: honest limitations; Appendix B: the complete ASCII-
    transliterated Lean listing.
- Lean 4 + Mathlib formalization: merged into `proof/LEAN.tex` — the full
  401-line listing is Appendix B there (chain `chain`, exact step law, closed
  forms, anchored invariant, dichotomy (`chain_pos`, `chain_neg_eventually`),
  the first-step block (`H1`–`H1_pos_of_ge`), the Theorem-9 package
  (`chain_all_pos_imp_ge`, `chain_all_pos_iff`) and the sieve-verified anchor
  checkpoint at `K = 10^8`); uncompiled (no toolchain in the authoring
  environment).
- [`verification/`](verification/README.md) — pure-Python sieve certificates with recorded results
  (see `verification/README.md`); `h1_at_1e8.py` computes the exact anchor
  evaluation at `K = 10^8` (sieve to 2.05e9): `θ(p_{10^8}) = 2 038 030 124.415365`,
  `H_{10^8} = 4132.288212` (inside the Theorem-C band), and the first chain step
  `H₁ = (1+r_K)H + s_K/u_K` as an explicit affine function of the seed `H`.

## Honest status

Every identity system constructed here re-encodes the exact transport recursion
`ε_{k+1} = (1 + r_k) ε_k + s_k`; the positivity prefix (`y > 0` eventually /
`H ≥ H_K`) is as hard as RH itself. What is *new* is Theorem 7: a one-directional
bridge from a thin positivity band to RH. Details and limitations in Appendix A
of [`proof/LEAN.tex`](proof/LEAN.tex).
