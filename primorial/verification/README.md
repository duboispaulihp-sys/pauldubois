# Verification certificates

Pure Python 3 (no numpy), float64. All scripts sieve primes to `LIMIT = 35,000,000`
with a bytearray sieve and keep running accumulators

- `X[k+1] = log θ(p_k)` (1-indexed: `X[k] = θ(p_k) = log N_k`),
- `Pv[k+1] = ∏_{p ≤ p_k} p/(p−1)`.

Precision pitfalls handled: use `math.log1p(u)` (never `math.log(1.0 + u)`);
avoid float cancellation `Q·A − A₁` (compare via the 4-term series instead).

| Script | Purpose | Recorded result |
|---|---|---|
| `identsolve3.py` | QuoPODkm system: `y = s/u` pinned; transport closure | errors ~1e-16; `s < 0` in 2146773/2146773 cases |
| `identsolve3b.py` | transport residual census | max 7.98e-15; ε<0 count 0; leg-1 all-true |
| `census_s.py` | `s`-sign census | sign(s) = sign(D) 100% |
| `errxy.py` | error-term audit | err_s/(u²/2) → 1.0006; err_y identical ratio; dominance of (1+log p)\|D\|/(p log p) |
| `ypos.py` | pinned y vs original y census | orig y min margin 3.398e-4 (>0 everywhere) |
| `signcert.py` | two-sided alternating s-bounds | UB 0 violations; LB ≤ 3.7e-22 (float noise) |
| `dbg2.py` | sharp s-asymptotics check | rel. dev 3.4e-5 at k = 2e6 |
| `chain3.py` | 3-step chain H1, H2, x | all > 0 on range; residual ≤ 3.5e-13 |
| `anchortest.py` | anchored chain dichotomy, K = 5e5 | invariant 4.2e-14; crossing ρ 3.407 vs 3.44 predicted |
| `leg2cert.py` | Leg-2: u_{k+1} > u_{2k} ∀ k ≥ 2 | 0 violations; min rel margin 0.21617 (k=2) |
| `approachA.py` | memoir trichotomy at k = 1e8 | Θ_k = 2.965083464; regime table |
| `hpos.py` | h_j positivity thresholds | boundary h_j ~ 1 − ℓ_j → −∞; flip j = 35,181,418 for h_0 = −0.5 |
| `confin.py` | affine sandwich checks | 20/20 pass, k = 1e8, j ∈ {1e6 … 4e7} |
| `chainform.py` | chained constant-offset two-form census (LEANT §3.4) | residuals β = −2s + c₁r (scaled), −(1+1/u_K)s + c₁r (bare): all > 0 in the K = 1e8 window (W = 5e6), measured–predicted ≤ 3.0e-12; per-line β negative from j = 2; phantom seed-0 stays > 0 while the true chain flips at j = 1 — the family does not close |
| `hipos_window.py` | certified positivity window at K = 1e8, physical seed, W = 2e8 (stream starts at the certified anchor, own segmented sieve to 7e9) | all gates PASS: 0 sign flips; min ε = 2.44e-5, min H = 2320.69 (both at j = 2e8) vs worst-case float drift ≤ 3e-12 (safety ≥ 8.1e6); cross-checked vs `chainform.py` deep pass at 7 checkpoints (rel. 3.3e-11) — H_i > 0 ⟺ f(p) < 1 (Nicolas) for all 2e8 consecutive primes [2 038 074 751, 6 461 335 109] |
| `h1_at_1e8.py` | exact anchor eval. at K = 1e8 (own segmented sieve to 2.05e9, fsum partials) | π(p_K) = 10⁸ verified; θ(p_K) = 2 038 030 124.415365; H_K = 4132.288212 (in Theorem-C band [4115.3, 4309.1]); f(p_{K+1}) < 1; H₁ = (1+r_K)H + s_K/u_K table; fixed point H_c = 46 696.77; consistency 1.5e-10 (rel.) |
| `sresp.py` | residual sign law + 2nd-order identity at K = 1e8, strip of consecutive primes [2 038 074 761, 2 070 000 000] (N = 1 488 557) | s < 0 in 1488557/1488557 (s ∈ [−2.92e-13, −1.95e-13]); identity p²s = 2a − e′(1+a) + a²/2 to 4.4e-5 rel.; sign law s>0 ⟺ e′ < τ (= 11.1953): 0 counterexamples; e′/√p ∈ [0.80, 1.23]; x_k = s_k/u_k < 0 at every strip prime — Littlewood Ω⁺ refutes "x < 0 eventually" (prop:soscil) |
| `sqrtlaw.py` | census of the proposed law p_{k+1} = log N_k + c (log N_k)^½ at K = 1e8, strip of 1 488 557 primes to 2.07e9 | ratio c_k = e′/√X ∈ [0.806, 1.218], mean 1.027, rms 0.087 (at the anchor: c_K = 0.9885 — c = 1 to 1.2%); law residual up to ±10⁴ (5×10³ gaps); best-fit c plugged into the 2nd-order law reproduces s to 27% rel.; as an eventual law refutable by Littlewood — c_k is Ω±(log log log X), no fixed c exists (rem:sqrtlaw) |
| `seedsign.py` | seed–sign dichotomy through the certified window W = 2e8 (same anchor-started walk as hipos_window.py, 280 s): H_i(H) = H^phys_i + (H−H_K)·P_i, sign(H_i) = sign(ρ_i − (H_K−H)), ρ = H^phys/P | all gates PASS: closed form vs 3 direct recursions (seeds 1000, 1, −100) to abs 1.0e-16; critical seed c_W = 1930.140054 (min ρ = 2202.148158 at i = 2e8, P_W = 1.05382793); d_W = 0 — every seed H < 0 stays negative on [0, W]; certified flips for subcritical seeds (H=1: i=42 993; 100: 4 373 363; 1000: 61 006 410; 1900: 191 615 334; 0 re-crossings); every seed H ≥ H_K: H_i ≥ 2320.68524 on [0, W] — same sign as the seed (cor:sgnsame) |
| `stepdiff.py` | increment convergence Δ_j = H_j − H_(j−1) at K = 1e8, physical seed, window W = 2e7 steps (sieve to 2.6e9, 31 s): Δ_j = r·H_(j−1) + s_(K+j−1)/u_K, unconditional Δ_j → 0 (Mertens + PNT only; prop:stepdiff) | all gates PASS: exact identity resid. 1.96e−12 H-units; s-shape dev. ≤ 4.70e−5 (2nd-order law of sresp.py); Δ_j < 0 at 2e7/2e7 steps, min margin e′/(εp/(1+a)) = 6.42; η = e′/√p ∈ [0.557, 1.454] (drift beyond the strip band [0.806, 1.218]); r·H-part 2.028e−6 → 1.515e−6 tracks ε/p; non-implication: ΣΔ telescopes — supercritical seeds diverge like P (log P ~ log log p), physical-seed telescope ⟺ open Mertens limit of ε = brick (rem:stepdiffnum) |
| `steporder.py` | the « 1/i error law » Δ_k = H_k − H_(k−1), K = 1e8, window W = 2e7 (sieve to 2.6e9, 29 s): exact decomposition Δ_k = (H−H_K)(P_j − P_(j−1)) + Δphys_k, P_j = anchored Mertens product | all gates PASS: seed decomposition (H_K+1000, −100) vs direct recursions ≤ 2.4e−12; drift telescope Σ = (H−H_K)(P_J−1) rel 6.4e−11; anchored ratio c_M = A_K P_W/log p_W = 0.9999986 (e^γ cancels); drift 1/i-constant (H−H_K)·c_M/A_K = 0.046652·(H−H_K), in-window k·rP ∈ [0.04904, 0.04907] (5.1% = k log p/p excess); physical seed on both sides: |Δphys|·k ∈ [1022, 3027] in-window (above 1/i at 19 952 477 of 2e7 steps), Δphys = o(1/k) asymptotically (rate e′/p → 0) — a 1/i law sums to harmonic divergence; brick untouched (cor:invlaw) |

`h1_at_1e8.py` and `chainform.py` (deep pass) are the exceptions to the 3.5e7
limit: `h1_at_1e8.py` runs its own segmented sieve to 2.05e9 (~40 s) and
verifies π(2 038 074 743) = 10⁸ independently, and `chainform.py`'s deep pass
segments to 2.2e9 (~160 s), re-certifying the same anchor to rel. 3.3e-11.
`hipos_window.py` is also an exception (sieve to 7e9, ~150 s) — it skips
primes below the certified anchor p_K entirely, cross-checks at every
deep-pass checkpoint, and extends the certified Nicolas range to 2.47e9.
The anchor results are in `h1_at_1e8_results.txt` (and
`chainform_results.txt` for the chained two-form experiment,
`sresp_results.txt` for the residual sign law / strip certificate,
`sqrtlaw_results.txt` for the constant-c gap-law census,
`seedsign_results.txt` for the seed–sign dichotomy,
`stepdiff_results.txt` for the increment-convergence certificate,
`steporder_results.txt` for the 1/i error-law dichotomy) and quoted in
the canonical manuscript `proof/LEAN.tex` — §9 there, including Theorem 9:
all-step chain positivity `H_i > 0`, and §3.4: the chained constant-offset
two-form is an ε-scale approximation that does not close (its phantom chain
over-estimates H and contradicts the certified seed-0 flip).

Run any of them with `python3 <script>.py`; each prints its census table.
