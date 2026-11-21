# The Geometric Drift — Construction, Proof Program, All-Options Execution
### (Companion to P. Dubois, "The Geometric Drift — Statement, Reduction, and the Open Core")

**Status of this document.** It contains the complete construction of the geometric mechanism,
complete proofs of every provable piece, an executed window-by-window verification at model level,
a sensitivity/threshold theorem, an analytic attempt on the open core, the bridge to the
Alpöge–Buckmaster certificate, and (Part V) the conditional-strength comparison against the
AB formalization plus the machine-checking of the proved chain in core Lean 4. No piece of the open core is dressed up as proved.

---

## Part I — Construction

### 1. Variables and the profile equation
Self-similar variables with blow-up time 1:
σ = log(1/(1−t)),  y = x/√(1−t),  u(t,x) = (1−t)^{−1/2} U(σ,y),
satisfying (∂σ + ½ + ½ y·∇ − Δ)U + (U·∇)U = −∇p, div U = 0.

### 2. The cascade
Windows of width S = log 2 (scale ratio λ = ½ per stage). Window-n reference packet W_n reproduces
under the discrete symmetry W_{n+1}(σ,y) = R W_n(σ−S, R^{−1}y). Per-window excess:
δ_n = (closure ratio in window n) − ε_prof, ε_prof = 1/30; ε_drift = Σ_{n≥n0} δ_n;
total misfit ε₀ = ε_prof + ε_drift. Certificate tilt constant: sin²θ ≤ 5.51 D².

### 3. The budget
On the band σ ∈ (7.3303, 7.8240) = (4 log(25/4), 4((5/2)log2 + log(5/4))), the drift must satisfy
Σ δ_n ≤ D_max(σ), the root of (¼ − 5.51 D²)σ = log 4 + 2 log((1+ε_prof+D)/(1−ε_prof−D)).

---

## Part II — Proved chain (complete proofs in the reply of this session; restated)

- **Lemma A (budget).** f_σ(D) := (¼−5.51D²)σ − log4 − 2log((1+ε+D)/(1−ε−D)) is strictly
  decreasing on [0, 7/90] (f' = −11.04σD − 2[(1+ε+D)^{−1} + (1−ε−D)^{−1}] < 0);
  f_σ(0) ≥ 0.31291 > 0; f_σ(7/90) ≤ 0.216668·7.82405 = 1.69513 < 1.83258 = log(25/4) (the right
  side at 7/90 is EXACTLY log(25/4), since ε + 7/90 = 1/9). Unique root D_max(σ) ∈ (0, 7/90);
  ε_prof + D_max < 1/9.
  Roots: 0.0514 / 0.0581 / 0.0643 at σ = 7.3303 / 7.5771 / 7.8240.
- **Lemma B (decaying-source summation).** δ_{n+1} ≤ qδ_n + cμ^{n−n0} ⟹ Σδ_n ≤
  δ0/(1−q) + c/((1−q)(1−μ)). Proof: unroll, exchange absolutely convergent double sum.
  Calibration: a CONSTANT source equilibrates at c/(1−q) and the sum necessarily diverges —
  the geometric decay is the exact dividing line (the pre-correction summation was unprovable).
- **Lemma C (envelope).** δ_{n0+k} ≤ ε_prof e^{−βk}, β ∈ (log 5, (5/2)log2) ⟹ Σδ_n ≤ ε_prof ρ,
  ρ ∈ (1.2147, 5/4); ε_prof ρ ∈ (0.04049, 0.04167).
- **Reduction Theorem.** (i) δ_{n0} ≤ 1/30; (ii') δ_{n+1} ≤ 10⁻³δ_n + 1.3·10⁻³·2^{−(n−n0)/2}
  ⟹ Σδ_n ≤ 0.033367 + 0.004443 = 0.037810 < D_max(σ) ∈ [0.0514, 0.0643]: headroom 26.4%–41.2%.

---

## Part III — All-options execution (this session)

### WP2: Model-level verification (Exit 1, executed)
Stage-by-stage recursion with the recorded constants; adversarial ceilings applied at every stage.

| anchor σ | D_max | proved Σδ_n | occupancy |
|---|---|---|---|
| 7.3303 | 0.0514 | 0.037810 | 73.6% |
| 7.5771 | 0.0581 | 0.037810 | 65.1% |
| 7.8240 | 0.0643 | 0.037810 | 58.8% |

Feasible region at the binding point (σ = 7.3303), recorded q = 10⁻³, μ = 2^{−1/2}:
- c₀ may grow to 5.27×10⁻³ (**4.1×** the recorded seed) before binding.
- q may grow to **0.2648** (265× recorded) before binding.
- Falsification control (constant source, the pre-correction lemma): sum after 10³ windows =
  **1.3347** (equilibrium c/(1−q) = 0.0013) against a budget of ~0.05 — reproduces the program's
  simulated 1.33 divergence; confirms the necessity of decay.

### WP3: Threshold theorem (new, analytic)
For a stage halving λ = ½, write the intrinsic relative level as λ^α per stage
(source c_n ≤ c₀ 2^{−α(n−n0)}). The Drift closes iff α ≥ α_min(σ):
- α_min = 0.1082 / 0.0779 / 0.0621 at σ = 7.3303 / 7.5771 / 7.8240.

This analytically reproduces the program's measured (E1) slack "½ → 0.108–0.062" [S-XVII]
(hardened stack [S-XX]: 0.103–0.060). Interpretation: the budget is insensitive to every constant
(c₀: ×4, q: ×265) but razor-sensitive to exactly one exponent — and (E1) grants ½, i.e. a factor
2^{(1/2−0.108)(n−n0)} of slack: comfortable but the load-bearing wall.

### Honest correction to the session record (WP2c output)
Contrary to a claim made earlier in this session, the *free* self-similar dissipation does NOT
close the budget: per log-2 window the free contraction is e^{−S/4} = 0.841 (not 0.16 — that
figure treated the whole band as one window). At q = 0.841 the fixed-point bound is 0.0333/0.159 =
0.2098 ≫ 0.0514 and fails. The ≤10⁻³ per-window contraction is genuinely conditional content of
(E1)+(E2); the e^{−S/4} floor only bounds the ESSENTIAL spectrum and provides the stage
dissipation, not the closure.

### WP1: The bridge (Exit 2 attempt, constructive form)
Proposition (bridge, modulo the closure-ratio calibration of [P]). Let u be an Alpöge–Buckmaster
blow-up solution: smooth, finite energy, ‖∇(U−W)(σ)‖_{L²} ≤ C e^{−κσ}, κ ∈ (0, ¼), W a certified
profile of period S. Reading the window excess against the stage copies of W gives directly
δ_n ≲ C e^{−κσ_n}, i.e. the GEOMETRIC envelope (Lemma C) with source ZERO: the entire intrinsic
source c_n ≡ 0, and Σδ_n ≤ Ce^{−κσ0}/(1−e^{−κS}). For the AB-class solutions the decaying-source
hypothesis (E1) is therefore discharged by the AB convergence theorem — the Geometric Drift holds
for that class, conditional only on the [P] closure-ratio calibration and (O3)'s pulse→window
transition. This is not an independent proof (it cross-wires two programs), but it converts
Dubois's axiom closure_implies_singularity into a theorem for a nonempty, unconditionally
constructed class of solutions.

### WP3 (analytic attempt, recorded no-go)
Leray's unconditional bound ‖∇u‖ ≤ C(T−t)^{−1/2} gives the window reading M_n ≤ Cλ_n^{−1/2},
against (E1)'s need M_n ≤ M*λ_n^{1/2}: the gap is λ_n^{−1} = 2^{n−n0}, exponentially widening.
No a priori technique known closes it; E1 is a rigidity statement about the true flow along the
cascade. Within the window model, Drift ⟺ E1-type decay (Lemma B calibration above) — no
relaxation of the hypothesis is available.

---

## Part IV — Ledger

- **Proved here (arithmetic verified independently):** Lemmas A, B, C; Reduction Theorem; all
  recorded digits of the drift document; the divergence calibration; the threshold theorem
  (α_min = 0.1082/0.0779/0.0621); the feasible region.
- **Corrected here:** the free-dissipation misconception (q_floor per log-2 window = 0.841, budget
  does not close on it); recorded candidly in Part III.
- **Model-verified here:** stage-by-stage pass at recorded constants with adversarial ceilings;
  constant-source falsification control (1.3347 divergence).
- **Discharged conditionally (bridge):** (E1) for AB-class solutions.
- **Still open:** (E1) for a solution not known to converge; (O3) pulse→window transition;
  the (E2) loop gain off-model. Unconditional statements: none.

Assembled conditional conclusion, unchanged and now verified twice:
Σδ_n ≤ 0.0378 < D_max(σ) ∈ [0.0514, 0.0643], headroom ≥ 26.4% on the band.

---

## Part V — Conditional-strength comparison and machine-checked status

This part compares, strength by strength, what each result in play actually proves, and records
the machine-checking of the proved chain executed in this session. Nothing below adds an
unconditional statement; the opening rule of the document is restated: **no piece of the open core
is discharged here, and the singularity is not proved by any configuration in this comparison.**

### V.1 Side-by-side

| | Alpöge–Buckmaster (Theorem 1.1 + 7.1) | Dubois (Drift Theorem 1.1) | This session (Reduction chain) |
| --- | --- | --- | --- |
| Conclusion | Blow-up exists unconditionally, from a certified profile | Drift along the true solution: Σδₙ ≤ D_max(σ) on the band | (i)+(ii') ⇒ Drift, with Σδₙ ≤ 0.0378 < D_max |
| Status | Proved | **Open** (axiom `closure_implies_singularity(_D)`) | Proved, as a conditional theorem |
| Hypotheses | Only the NS equations (data from the certificate) | Window-level bounds on the true flow: (i), (ii'), i.e. (E1), (O2), (O3) | The same window-level bounds, taken as hypotheses |
| Machine-checked | Yes: Theorems 1.1 and 7.1 formalized in Lean 4 + Mathlib (§1.5); formal Theorem 1.1 stated **without rate**; two steps (Props. B.1, B.4) exist only in the formalization | The drift field is an axiom, not a theorem, in the Lean Segments 1–2 | Yes, this session, core Lean 4 only (V.4): `phiMono`, `driftBound`, `constantSourceDiverges` |
| Outside the formalization | The certificate itself: 128-bit interval arithmetic (Arb/FLINT), verified rigorously but not machine-checked; the formalization **contains no data** | The entire open core | The NS reading of the hypotheses; all real analysis; the certificate arithmetic |
| Relation to the truth of blow-up | Establishes it | Feeds the proved chain [P]; yields blow-up only conditionally | Raises nothing unconditionally: its hypotheses are precisely the open core |

The decisive row is the last one. The conditional chain of Dubois, even with every provable piece
proved and machine-checked, cannot outrank the AB result: a conditional theorem whose hypotheses
are unproved statements about the true flow is strictly weaker than an unconditional existence
theorem. The correct reading is complementarity: AB proves that the singularity exists;
Dubois's program proposes an independent, window-level mechanism whose open core is a rigidity
statement about the true flow along the cascade — the two are different mathematics arriving at
the same conclusion, and only one of them currently closes.

### V.2 What the bridge imports, precisely

The bridge (Part III, WP1) converts Dubois's axiom `closure_implies_singularity` into a theorem
for the AB-class solutions. Its imports, itemized:

1. **Profile existence** — imported from AB: Theorem 7.1 (certificate ⇒ weak solution of the
   profile equation) applied to their certificate (hash
   `3f7a335b84b6c7631742cacc5343dfcd11cf72f5221ff79b2b9268790b4b22c5`). This import is
   unconditionally established, but its verification lives in the interval arithmetic, not in Lean.
2. **The convergence rate** — the second bound of (1.6): ‖∇(U−W)(σ)‖_{L²} ≤ C e^{−κσ},
   κ ∈ (0, ¼). This is **paper-level only**: the formal Theorem 1.1 is deliberately stated
   without a rate. The bridge's hypothesis (E1)-for-AB-class therefore runs on an input that is
   not machine-checked anywhere.
3. **The closure-ratio calibration** A = ρΩ of [P] — model-level, part of the conditional side,
   not imported from AB.
4. **(O3)**, the pulse→window transition — still open; the bridge does not touch it.

Consequence: the bridge's only genuinely new input over the AB paper is the *transcription*
δₙ ≲ Ce^{−κσₙ} with cₙ ≡ 0, which is Lemma C's envelope with a better constant. It cannot prove
more than AB already proved: for a solution already known (by AB) to converge to a blow-up
profile, the drift follows. **Removing AB from the picture removes the bridge's own hypothesis**:
for a solution not known to converge, (E1) is exactly as open as it was in §3 of the Dubois
document. The bridge is a consistency upgrade of the AB class inside the drift framework, not an
independent route to the singularity.

### V.3 Strength ordering

1. **AB (paper + formalization)** — unconditional; the only configuration that proves the
   singularity.
2. **Dubois + bridge on the AB class** — conditional, and its hypotheses are true there; adds
   framework, adds no existence content.
3. **Dubois + proved chain, unbridged** — conditional on (E1)+(O2)+(O3); the open core is
   untouched by everything in this document.
4. **Machine-checked reduction (this session's Lean file)** — verifies the arithmetic of level 3
   only; says nothing about Navier–Stokes beyond: *if* the window recursion holds, *then*
   Σδₙ ≤ 0.0514·D scale-free.

### V.4 Machine-checking of the proved chain (core Lean 4, no Mathlib)

File: `formal/DriftReduction.lean` (Lean 4, v4.36.0, core only — no external library, matching
what this environment could obtain; AB's own formalization is Mathlib-based and considerably
deeper). The proved chain is verified over integers with explicit scaling, so that every rational
constant of the Reduction Theorem is exact:

| Lean constant | value | mathematical meaning |
| --- | --- | --- |
| D | 30 000 000 | scale (10⁷); all quantities below are D-multiples |
| Q | 30 000 | q = 10⁻³ per-window contraction of (ii') |
| X | 22 500 000 | χ = 3/4, a valid relaxation of μ ≤ 2^{−1/2}: 2^{−1/2} = 0.7071… ≤ 0.75 (⇔ √2 ≥ 4/3 ⇔ 2 ≥ 16/9) |
| δ̂₀ cap | 1 000 000 | launch excess δ₀ ≤ 1/30 |
| ĉ₀ cap | 39 000 | source c₀ ≤ 1.3×10⁻³ |
| M | 1 542 000 | budget head D_max = 0.0514 at the lower band end |
| D − Q | 29 970 000 | (1 − q)·D |
| D − X | 7 500 000 | (1 − χ)·D = D/4 |

The χ = 3/4 relaxation costs the fixed-point bound 0.0378 → 0.0386, still 25.1% inside the
0.0514 head — this is deliberately not tight, so the `decide`-closed ground inequality is robust.

Three theorems, all closed without any unproved step:

- `phiMono` — the monotone two-channel potential used in the summation: for every K,
  sumTo d̂ K·(D−Q)(D−X) + (D−X)·D·d̂ K + D²·ĉ K ≤ (D−X)·D·δ̂₀ + D²·ĉ₀, by induction on K from
  the recursion hstep: D·d̂(n+1) ≤ Q·d̂ n + D·ĉ n and decay hdec: D·ĉ(n+1) ≤ X·ĉ n.
- `driftBound` — the headline: `sumTo dhat K ≤ 1542000` for every K, i.e. **Σ_{k<K} δ̂ₖ ≤
  0.0514·D scale-free, for all K**, with no a priori limit on the number of windows. Closed by
  `phiMono` plus the ground inequality (D−X)·D·δ̂₀ + D²·ĉ₀ ≤ M·(D−Q)·(D−X), discharged by
  `decide` on exact integers.
- `constantSourceDiverges` — the machine-checked form of the divergence calibration (Lemma B's
  correction, Part II): under the *constant-source* recursion D·d̂(n+1) = Q·d̂ n + D·ĉ₀ exactly,
  the window excesses never drop below their source level, ĉ₀·K ≤ Σ_{k<K+1} d̂ₖ — the prefix
  sums grow linearly forever, so no constant of the form 1/(1−q)² can bound them. This is the
  counter-lemma that justifies why (ii') needs its geometric μ < 1: it is the machine-level
  certificate of the 1.3347 divergence of WP2c.

Machine output of `#print axioms` (the certificate that no step was left unproved):

```
'DriftReduction.phiMono' depends on axioms: [propext, Quot.sound]
'DriftReduction.driftBound' depends on axioms: [propext, Quot.sound]
'DriftReduction.constantSourceDiverges' depends on axioms: [propext, Quot.sound]
```

`propext` and `Quot.sound` are Lean's standard logical axioms; `sorryAx` is absent. What is NOT
machine-checked, by design and in exact parallel with AB's own division of labor: the reading of
the hypotheses on the true Navier–Stokes flow ((E1), (O2), (O3) — untouched), the real-analysis
content of the profile equation, and the interval arithmetic of any certificate. The Lean file
formalizes exactly level 4 of V.3 and nothing more — which is precisely its honest value: the
arithmetic of the reduction is now as certain as the rest of the program's proved chain, and the
open core remains exactly as open as it was.
