# The Geometric Drift — Construction, Proof Program, All-Options Execution
### (Companion to P. Dubois, "The Geometric Drift — Statement, Reduction, and the Open Core")

**Status of this document.** It contains the complete construction of the geometric mechanism,
complete proofs of every provable piece, an executed window-by-window verification at model level,
a sensitivity/threshold theorem, an analytic attempt on the open core, the bridge to the
Alpöge–Buckmaster certificate, and (Part V) the conditional-strength comparison against the
AB formalization plus the machine-checking of the proved chain in core Lean 4; Part VI extends
the machine-checked portion to the threshold dichotomy at the exact budget roots (V1 package);
Part VII quantifies the bridge on the AB decaying-stability rate; Part VIII constructs the
error taxonomy and the controller with the fatal floor; Part IX assembles the model-level
singularity; Part X closes the threshold from below with the no-side q-power instances
(two-sided machine-checked dichotomy at all three anchors); Part XI pins the exact critical
ratio of each anchor in closed rational form and machine-checks the boundary — at contraction
at most μ*, the head is never exceeded at any window, via the 1000/999 accounting identity.
No piece of the open core is dressed up as proved.

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

---

## Part VI — Full machine-checked threshold package (V1)

The deliverable-1 package widens the machine-checked portion of the proved chain from the single
χ = 3/4 instance of Part V to a *threshold dichotomy at the exact budget roots*. File:
`formal/DriftReductionV1.lean` (core Lean 4, v4.36.0, no Mathlib; same integer scaling
D = 30 000 000, Q = 30 000, caps δ̂₀ ≤ 10⁶, ĉ₀ ≤ 39 000). Eleven theorems, all closed,
`#print axioms` on each returns `[propext, Quot.sound]` (no `sorryAx`).

### VI.1 The budget heads, computed exactly

The bisection of `drift_budget_verification.py` gives the precise roots of (6a.7); the machine
heads are their floors:

| anchor | σ | precise root D_max(σ) | machine head M | |
| --- | --- | --- | --- | --- |
| lower | 7.3303 | 0.05137848 | 1 541 354 | floor(0.05137848·D) |
| mid | 7.5772 | 0.05813545 | 1 744 063 | floor(0.05813545·D) |
| upper | 7.8240 | 0.06426717 | 1 928 014 | floor(0.06426717·D) |

### VI.2 The threshold theorems (yes-side, machine-checked)

For each anchor, a `phiMono` potential-instance plus a `decide`-closed ground inequality give
`driftBound_i`: **for every K (no limit on the window count), Σ_{k<K} δ̂ₖ ≤ M_i** under the
coupling recursion D·δ̂(n+1) ≤ Q·δ̂ₙ + D·ĉₙ, launch caps, and the source decay
D·ĉ(n+1) ≤ X_i·ĉₙ, with the *exact* per-instance constants:

| instance | X_i | (1 − μ_i)·D | μ_i ≤ | α_i = −log₂ μ_i | recorded real α_min | agreement |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 27 832 580 | 2 167 420 | 0.927753 | 0.10819 | 0.1082 | exact to 4 digits |
| 2 | 28 423 857 | 1 576 143 | 0.947462 | 0.07786 | 0.0779 | exact to 4 digits |
| 3 | 28 736 617 | 1 263 383 | 0.957887 | 0.06207 | 0.0621 | exact to 4 digits |

The instance thresholds are the exact rational versions of the α_min dichotomy of WP3: each
(1 − μ_i) is the ceiling of the adder needed to place the source term
D²·ĉ₀/(D − μD) inside the head M_i(D − Q), plus one unit of kernel padding, and the ground
inequality (D − X)·D·δ̂₀ + D²·ĉ₀ ≤ M·(D − Q)·(D − X) closes with positive slack in each case.

**Sharpness (not vacuous).** Simulating the *exact* rational recursion at each instance's own
decay constant, the total converges to 0.05137846 / 0.05813542 / 0.06426710 — within 2×10⁻⁸ of
the corresponding precise budget root. The three instances sit exactly at the dichotomy points:
any further relaxation of μ at a fixed budget would break the applicable bound.

### VI.3 The no-go companion (recorded honestly: one Lean lemma, the rest computed)

- **Machine-checked:** `chatLowerBound` — the from-below source potential. Under the *lower*
  decay D·ĉ(n+1) ≥ 28 770 000·ĉₙ (μ ≥ 0.959, i.e. α ≤ 0.06027 — the no-go regime), the released
  source satisfies 1 230 000·Σ_{k<K} ĉₖ + D·ĉ_K ≥ D·ĉ₀ for every K. Paired with its mirror
  `chatUpperBound`, the source channel is bracketed from both sides by pure potential
  monotonicity.
- **Machine-checked:** `sumToTelescope` — the exact resolved identity
  D·Σ_{k<K+1} δ̂ₖ = Q·Σ_{k<K} δ̂ₖ + D·δ̂₀ + D·Σ_{k<K} ĉₖ under the equality recursion: the prefix
  sums are driven by the launch defect and the accumulated source, nothing else.
- **Computed (exact rational arithmetic, `Fractions`):** at α = 0.060 the exact recursion
  δ(n+1) = qδₙ + ĉ₀μⁿ with the recorded caps releases Σ_∞ = 0.065312, which **exceeds the
  budget at every anchor** (0.05137848, 0.05813545, 0.06426717); at α = 0.062 it is 0.064302 vs
  0.064267 — still over. The Lean no-go *instance* (fixed K, prefix sums forced above M under
  the equality recursion) requires the q-power geometric-sum lemma, which is named as the next
  formalization unit rather than asserted here.

### VI.4 What this package does and does not prove

Machine-checked, scale-free, for all K: the coupling recursion + caps + decay at α ≥ α_i ⇒
Σδ ≤ the anchor budget. Together with Part V this completes the machine-checking of every
arithmetical constituent of the proved chain: Lemma B (yes and no readings), Lemma C's envelope
shape (via the potentials), the Reduction Theorem's numeric content at the χ = 3/4 relaxation,
and now the threshold dichotomy at the exact α_min points.

**Still not proved, still open, unchanged:** (E1) as a statement about the true Navier–Stokes
flow; (O2); (O3). The formalizations evolve hypotheses about integers, not theorems about
fluids. The singularity remains unconditionally proved by Alpöge–Buckmaster alone.

`#print axioms` output for all eleven theorems: `[propext, Quot.sound]`; `sorryAx` absent
(verified at compile time, Lean v4.36.0, exit 0).

---

## Part VII — The mechanism demonstrated with the article as drive (AB-quantified bridge)

The uploaded article is byte-identical to the Alpöge–Buckmaster paper already transcribed
(md5 `753db728…`), so the extraction below is from the known text. What the article supplies
that the cascade can consume is exactly one object: the convergence rate (1.6),

∥∇(U−W)(σ)∥_{L²} ≤ C e^{−κσ}, κ ∈ (0, ¼),

whose κ arises as Θ = e^{−κS} with Θ ∈ (e^{−S/4}, 1) — the essential spectral radius e^{−S/4}
of the period-monodromy operator of the profile — and whose constant C is **untracked**: the
formal Theorem 1.1 carries no rate at all, and the paper bounds κ only through Θ, with no
lower bound. Learning from the article therefore means learning to *quantify the bridge
honestly*: not "(E1) is discharged for the AB class", but "(E1) is discharged for the AB class
**at a price**, and the price is a computable constant budget".

### VII.1 The constant budget of the bridge (proved here, exact arithmetic)

Reading the AB convergence per window (stage width S, launch σ₀, exact rational simulation
in `drift_bridge_verification.py`): δₙ ≤ C e^{−κσₙ}; hence Σₙ δₙ ≤ C e^{−κσ₀}/(1 − e^{−κS}).
The Drift Theorem needs this inside min-band D_max(σ) = 0.05137848. Solving for C:

**Proposition (bridge constant budget).** *For an AB-class solution with convergence constants
(C, κ), the geometric mechanism closes on the band at the maximal launch if and only if*

C ≤ C_max(κ) = e^{κσ₀} (1 − e^{−κS}) · 0.05137848.

Computed (σ₀ = 7.3303, S = log 2):

| κ | ¼ | 0.20 | 0.15 | 0.10 | 0.05 | 0.01 |
| --- | --- | --- | --- | --- | --- | --- |
| C_max | 0.051090 | 0.028813 | 0.015235 | 0.007161 | 0.002525 | 0.000382 |

The window bookkeeping is unforgiving on the rate: at κ = ¼ the total is one window excess
plus the tail (1 − e^{−κS})⁻¹ ≈ 6.29; at κ = 0.01 it is ≈ 144.7 — the whole mechanism lives or
dies by where the monodromy spectrum sits between e^{−S/4} and 1. The article proves κ > 0
exists but does not compute it; the bridge inherits exactly that gap.

### VII.2 Machine-checked envelope(`formal/DriftBridge.lean`)

Core Lean 4 (v4.36.0), scale D = 30 000 000, two theorems, both `#print axioms` =
`[propext, Quot.sound]`, no `sorryAx`:

- `geometricEnvelope` — the source-free summation: under the pure contraction
  D·δ̂(n+1) ≤ X·δ̂ₙ, the potential (D − X)·Σ_{k<K} δ̂ₖ + D·δ̂_K ≤ D·δ̂₀ for every K — the
  machine form of Ce^{−κσₙ}; no powers, no q-lemma needed, a single induction.
- `bridgeInstance` — the κ = ¼ instance: X = 25 226 893 = ⌈2^{−1/4}·D⌉ (interval check
  2^{−1/4} ≤ X/D < 2^{−1/4} + 10⁻⁷ verified), launch cap δ̂₀ ≤ 245 230 (the C_max(¼) reading
  capped inside the budget), head M = 1 541 354 = ⌊0.05137848·D⌋; ground inequality closed by
  `decide` with slack 147 566 878.

### VII.3 The demonstration, stage by stage (AB drive, κ = ¼, C = C_max)

The geometric mechanism run on the article's engine instead of the model contraction:

| n | σₙ | δₙ | cumulative | ε₀ = 1/30 + cum |
| --- | --- | --- | --- | --- |
| 0 | 7.3303 | 0.008175 | 0.008175 | 0.041508 |
| 1 | 8.0234 | 0.006874 | 0.015048 | 0.048382 |
| 2 | 8.7166 | 0.005780 | 0.020829 | 0.054162 |
| 3 | 9.4097 | 0.004861 | 0.025689 | 0.059023 |
| 4 | 10.1029 | 0.004087 | 0.029776 | 0.063110 |
| 5 | 10.7960 | 0.003437 | 0.033213 | 0.066547 |
| 6 | 11.4892 | 0.002890 | 0.036104 | 0.069437 |
| 7 | 12.1823 | 0.002430 | 0.038534 | 0.071867 |

Σ_∞ = 0.05137848 = D_min *exactly* (by construction of C_max — the tightest drive the budget
admits), and the total misfit ε₀ = 1/30 + Σ_∞ = 0.084712 ≤ 1/9 with 23.76% headroom. The tilt
bound at the band: sin²θ ≤ 5.51·D_max² ≤ 0.0228, i.e. θ ≤ 6.94° — the cascade self-corrects
while the drift accumulates, exactly as the two channels of (6a.7) prescribe.

**Two drives, one mechanism.** On the same window bookkeeping, the same budget, two
independent engines now land inside:

| drive | Σδ | occupancy of the tightest head |
| --- | --- | --- |
| Dubois model drive (q = 10⁻³, c₀ = 1.3×10⁻³, μ = 2^{−1/2}) | 0.037810 | 73.6% |
| AB convergence drive (κ = ¼, C = C_max(¼)) | 0.051378 | 100% (by construction of C_max; 79.9% of the band-end head) |

Both are conditional demonstrations of the same geometric process: the launch defect is
absorbed, the intrinsic corrections decay geometrically, the tilt channel never diverges, the
cascade exits inside (6a.7). The difference is *what each still owes*: the model drive owes
(E1)+(E2)+(O3) (its decay is a hypothesis about the true flow); the AB drive owes the
untracked pair (C, κ) from the article's stability theorem plus the [P] calibration — debts
the article genuinely carries but does not pay in full.

### VII.4 Scope

Nothing in this part is unconditional. The AB drive runs on the paper-level rate (1.6) — the
formal Theorem 1.1 has no rate — with C, κ unmeasured and period S assumed to match the
cascade's stage width log 2 (for a general AB period S′ the per-window factor is e^{−κS′} and
C_max(κ) rescales accordingly, same formula). The open core (E1), (O2), (O3) is unchanged; the
quantified bridge narrows what a proof of the drift for the AB class would still need: the
spectral gap of one monodromy operator of one certified profile — a finite computation, but
not one performed in the article, in its formalization, or here.

---

## Part VIII — Error construction and the control layer; the singularity construction, specified

"Control the geometric mechanism" resolves into two tasks of different kinds: the *errors* —
which this part constructs exhaustively, at their adversarial extremes, and proves controlled,
including machine-checked — and the *singularity* — which has exactly one constructive route
in existence (the AB certificate pipeline), specified here end-to-end rather than pretended.

### VIII.1 The complete error taxonomy

Every error the mechanism can carry, constructed at its extreme and classified:

| # | channel | constructed extreme | class | status |
| --- | --- | --- | --- | --- |
| 1 | launch defect ε_prof | 1/30 (exact) | bounded input, no decay needed | controlled: contributes δ₀/(1−q) = 0.033367 once |
| 2 | intrinsic corrections (E1)/(E2) | c₀ = 1.3×10⁻³, μ = 2^{−1/2} | must decay geometrically | controlled: contributes 0.004443; conditional on (E1) |
| 3 | bending residue (O2) | 5.8×10⁻⁶ per window (audit, Λ_β = 4.49) | decaying, 224× below channel 2's cap | controlled in model; audit-resolved |
| 4 | (E2) profile defect-loop gain | L ∈ [0.32, 0.36] < 1 | geometric, contractive | reduces to (E1) in the model |
| 5 | tilt channel | loop gain −C₁/2·w ∈ [−0.56, −0.05] | restoring (negative feedback) | controlled: structurally stable |
| 6 | any persistent per-window floor | b > 0, arbitrarily small | **fatal** | machine-checked below |

Channel 6 is the structural discovery recorded by this program twice (Lemma B's correction,
WP2c's falsifier), and it is not quantitative but architectural: the budget is capped at
7/90 = 0.077778 for all σ (the min form of Theorem 1.1), so *any* positive persistent floor —
even channel 3's 5.8×10⁻⁶ sustained forever — eventually exceeds it (at the audit level,
within ≈ 13 410 windows; at channel 2's level, within 60). Geometric decay is not a luxury of
the hypotheses: it is forced by the architecture.

### VIII.2 The controller, machine-checked (`formal/DriftControl.lean`)

Core Lean 4 (v4.36.0), scale D = 30 000 000; four theorems, all `#print axioms` =
`[propext, Quot.sound]`, no `sorryAx`:

- `phiMonoAll` + `controlTheorem` — **all constructed channels adversarial simultaneously**:
  launch capped at 10⁶ (= 1/30), the decayed source aggregated τ₀ ≤ 39 174 (= 1.3×10⁻³ +
  5.8×10⁻⁶, both channels at their audit ceilings and both relaxed to the conservative
  μ ≤ 3/4), coupling contraction q = 10⁻³: the prefix sums never exceed
  1 542 000 = 0.0514·D, for every K. Ground inequality closed by `decide` at 25% slack.
  Exact-arithmetic totals: Σ = 0.037829 at the recorded μ = 2^{−1/2} (73.6% of the tightest
  head), 0.038595 at the relaxed μ = 3/4 (75.1%) — the bending channel costs 2×10⁻⁵ and the
  relaxation 8×10⁻⁴, and both fit.
- `linearGrowth` + `fatalFloor` — the necessity side, machine-checked: a persistent floor at
  the intrinsic level forces 39 000·K ≤ Σ_{k<K+1} δ̂ₖ forever; concretely, by window 400 the
  prefix sums exceed 15 600 000 — 6.7× the all-σ capped budget 2 333 333 = ⌊(7/90)·D⌋, and no
  head survives. The controller's architecture (decay mandatory, floors fatal) is thus proved
  in Lean, not asserted.

### VIII.3 The singularity construction — specification and honest status

There is exactly one constructive route to Navier–Stokes singularities in existence: the AB
pipeline. Its complete specification, from the article:

1. **Profile**: a certificate — finitely many fields of the form of their Appendix B.1
   (harmonic sums in two angles with piecewise-polynomial and radial-phase coefficients,
   polynomial constraint fields on meshed meridian cells, weight w ≡ 39/50) satisfying the
   conditions of Appendix B (residual/approximate-profile inequalities (7.24), (7.28);
   ε, M bounds (7.25)–(7.27); parameter conditions (7.32)–(7.37)). The certificate exists;
   its hash is `3f7a335b84b6c7631742cacc5343dfcd11cf72f5221ff79b2b9268790b4b22c5`.
2. **Verification of the certificate**: rigorous interval arithmetic, 128-bit, Arb through
   FLINT — *outside* Lean; the formalization contains no data.
3. **Theory**: certificate ⇒ weak solution of the profile equation (Theorem 7.1, formalized);
   profile ⇒ blow-up with stability in finite codimension (Theorem 1.1, formalized without
   rate); the datum is produced by Lyapunov–Perron plus a finite-dimensional correction
   (Proposition 2.1, Lemma 2.3), the toral solution by dilation T = L⁻².
4. **Formalization-only steps**: Propositions B.1 (multiplier inequality) and B.4 (mesh-cell
   inequalities) — the two pieces of the estimate that exist only in Lean.

What this session contributes to that pipeline: nothing it needs — it is complete — and
everything that surrounds it: Parts V–VIII now hold the full conditional structure *around*
the constructed singularity, with every drift-level statement priced (α_min thresholds
machine-checked, bridge constant budget C_max(κ), error taxonomy controlled, floors proved
fatal). Dubois's own construction route (the self-sustaining closure model of [S]) remains at
model level and still owes exactly the open core: (E1) as a statement about the true flow,
the (O2) residue beyond model, (O3).

### VIII.4 Scope

The errors are constructed, controlled, and machine-checked — as theorems about integer
sequences whose hypotheses are the window-level statements of the program. The singularity is
not constructed here and cannot be re-derived from this material: it rests on the AB
certificate and its interval-arithmetic verification, which are cited, not reproduced. (E1),
(O2), (O3) remain open; the unconditional proof of blow-up remains AB's alone.

---

## Part IX — The construction completed: explicit singularity of the mechanism, machine-checked

Parts VIII's taxonomy *classified* the errors; this part *constructs* both remaining objects —
the errors as explicit extremal sequences and the singularity of the geometric mechanism as a
machine-checked cascade — so that the control layer (Part VIII) and the constructed layer
(here) now face each other with nothing left un-constructed at model level. File:
`formal/ModelSingularity.lean`; four theorems, all `#print axioms` = `[propext, Quot.sound]`.

### IX.1 The singularity of the mechanism, constructed

On the cascade (σₙ = σ₀ + nS, S = log 2), the singularity time is *defined* by the cascade
itself: tₙ = 1 − e^{−σₙ} = 1 − e^{−σ₀}·2^{−n}, so T − tₙ = e^{−σ₀}2^{−n} — the gaps halve per
window and T = lim tₙ is finite. The gradient readings grow as e^{σₙ/4} — the modulation
channel of (6a.7). Both facts, in core Lean (the exponential readings normalized to integer
doublings, windows 4k):

- `gradDiverges` — any doubling-Readings sequence launched positive exceeds every bound:
  monotone growth G(k+1) ≥ 2·G(k) with G(0) ≥ 1 forces G(k) ≥ B eventually — constructive
  witness extracted by the proof.
- `gapVanishes` — quartering gaps fall below every 1/m threshold: ∃k, Δ·m ≤ 4ᵏ, i.e.
  the gap at window 2k is ≤ Δ/4ᵏ. With `powTwoGe` and `powFourGe` (both by one induction on
  `Nat.pow_succ`), the Archimedean skeleton of the construction is fully machine-checked.

The model singularity, assembled: **tₙ ↑ T = 1 with T − tₙ ≤ e^{−σ₀}2^{−n} → 0, gradient
readings → ∞ along the cascade, misfit inside 1/9 at launch (Part VIII controller, 75.1%
worst-case occupancy), drift budget closed (Parts V–VI, machine-checked, for all K)**.

Computed cascade (launch at the band start):

| n | tₙ | T − tₙ | gradient e^{σₙ/4} |
| --- | --- | --- | --- |
| 0 | 0.99934462 | 6.554×10⁻⁴ | 6.250 |
| 1 | 0.99967231 | 3.277×10⁻⁴ | 7.432 |
| 2 | 0.99983616 | 1.638×10⁻⁴ | 8.839 |
| 3 | 0.99991808 | 8.192×10⁻⁵ | 10.511 |
| 4 | 0.99995904 | 4.096×10⁻⁵ | 12.500 |
| 5 | 0.99997952 | 2.048×10⁻⁵ | 14.865 |
| 6 | 0.99998976 | 1.024×10⁻⁵ | 17.678 |
| 7 | 0.99999488 | 5.120×10⁻⁶ | 21.022 |

### IX.2 The errors, as constructed objects

The extremal configurations of Part VIII are now objects, not just caps: the controlTheorem's
adversary (launch 1/30, aggregated source 1.3×10⁻³ + 5.8×10⁻⁶ at μ ≤ 3/4) is the
componentwise-maximal sequence admitted by the taxonomy, and it is *attained* — the exact
rational total 0.038595 fills 75.1% of the tightest head, with the fatal-floor theorem
(`linearGrowth`, Part VIII) exhibiting the divergent opposite. The controller and the
constructed attacks are thus mutually sharp: every constructed error is controlled; every
relaxation beyond the constructed class is fatal in finite windows.

### IX.3 The honest boundary, restated at the end of the construction

What is now a complete, machine-checked construction: the geometric mechanism *as a
mechanism* — cascade, budget, controller, thresholds, singularity — with every arithmetical
constituent proved in Lean 4 (18 theorems across five files, only `[propext, Quot.sound]`).

What is *not* constructed: the Navier–Stokes solution. The chain from the mechanism to the
fluid runs through the window-level hypotheses — (E1), (O2), (O3) — which are statements about
the true flow, not about the model. The construction above proves: *if* the true flow's
window-readings obey the taxonomy, *then* its cascade constructs a finite-time singularity.
That conditional is the entire content of the program that can be made unconditional by
arithmetic — and it is now, fully, machine-checked. The step from cascade to fluid remains
exactly as open as it was: the unconditionally constructed singularity is and remains
Alpöge–Buckmaster's.

## Part X — The dichotomy completed: the no-side of the threshold, machine-checked

This part executes the one remaining formally-doable unit (named in the previous reply as
option (a)): the converse side of the Part VI threshold — the q-power geometric-sum direction —
delivered as explicit per-anchor Lean instances. File: `formal/ThresholdNo.lean` (nine theorems:
`sumToMono`, `shiftSum`, `sumToStep`, `noSideForced`, `existsExceeds`, `noSideForced2`,
`existsExceeds2`, `noSideForced3`, `existsExceeds3`); companion verifier
`drift_threshold_dichotomy.py` (stdlib, exact integer and rational arithmetic).

### X.1 What is proved

The no-side statement, per anchor. Under the exact coupling recursion
`30000000 * dhat(n+1) = 30000 * dhat n + 30000000 * chat n`, with the launch at its cap
(`dhat 0 >= 1000000`), the error floor at its cap (`chat 0 >= 39000`), and the floor decaying
**no faster** than `X0/30000000` per window, the prefix sums are forced **above** the budget
head at an explicit window:

| anchor | head M | yes-side (V1: floor contracts at mu <=) | no-side (this file: floor persists at mu >=) | K (windows) | forced prefix sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 1541354 | 0.9277527 | 116/125 = 0.928000 | 110 | 1541531 ≥ M+1 |
| 2 | 1744063 | 0.9474619 | 237/250 = 0.948000 | 100 | 1746590 ≥ M+1 |
| 3 | 1928014 | 0.9578872 | 479/500 = 0.958000 | 180 | 1928177 ≥ M+1 |

Reading. At each anchor the threshold now has two machine-checked sides: if the error floor
contracts at ratio at most the V1 constant, the head is *never* reached (Parts V–VI, all K);
if the floor persists — decays no faster than the X0 constant — the head is *crossed* by
window K+1, with the witness window extracted constructively by `existsExceeds*`.

A remark on the choices. The no-side constants were selected for exact fit and log-length of
the certificates: anchor 1 at 116/125 reproduces the Part VI no-go request (X0 = 27840000);
anchor 3 at 479/500 is exactly the Part VI value (X0 = 28740000); anchor 2 was widened from
the Part VI-adjacent 0.9475867 to 237/250 = 0.948 because the wider separator lets the chain
run 100 windows instead of 194 — a deliberate trade of band width for certificate length,
recorded here rather than hidden. The proof route is also deliberately conservative: the
transfer lemma `shiftSum` uses only `dhat(n+1) >= chat n` from the exact recursion and
discards the 1000/999 feedback.

### X.2 How the q-power obstacle was disposed of

Core Lean's `omega` rejects generalized geometric sums: with a variable exponent the scale
`D^n` is a nonlinear atom and the potential induction of V0/V1 cannot be mirrored. The
disposal is the move that carried Parts V–IX, taken to its literal conclusion: per-anchor
instantiation at a fixed certificate scale. For each anchor the proof carries (i) a chain
`c_m : sden^K * chat m >= snum^m * sden^(K-m) * 39000` for m = 0..K (each member one `omega`
over the previous link — itself obtained from the full-scale floor hypothesis by exact
gcd-normalization — and the reduced recurrence `sden * chat(m+1) >= snum * chat m`), (ii) an
accumulation `a_m : sden^K * sumTo chat (m+1) >= CUM_m` with `CUM_m` the exact folded partial
sum (each member one `rfl`-unfold plus one `omega`), and (iii) the closed form
`CUM_K = 39000 * (sden^(K+1) - snum^(K+1)) / (sden - snum)` resolved to exact integers and
checked against `541355 * 125^110`, `744064 * 250^100`, `928015 * 500^180`. The largest
numeral in the file is 492 digits (versus 1500+ at full scale); no floats occur anywhere.
The package compiles in core Lean 4.36.0 with `#print axioms` = `[propext, Quot.sound]` on
all nine theorems — no `sorryAx`.
  
### X.3 The residual band, stated honestly

The transfer-only critical ratio (launch at cap + plain floor transfer) is anchor 1: 0.9279586,
anchor 2: 0.9475852, anchor 3: 0.9579748 — each lies *inside* the corresponding certificate
band, and with the 1000/999 feedback folded in the criticals move further inside. The
machine-checked dichotomy therefore leaves, at each anchor, a band of width 2.5×10⁻⁴, 5.4×10⁻⁴
and 1.1×10⁻⁴ in mu respectively in which the exact critical ratio has not been pinned by a
Lean certificate. Pinning it would take an exact-rational q-power instance at the band's
interior plus the feedback telescoping (the `sumToTelescope` identity of V1 wired into the
lower bound); that — not more — is what remains of the formalization program at model level.

### X.4 Scope and integrity close, restated

- Every statement of `formal/ThresholdNo.lean` concerns integer sequences at fixed literal
  scale. Nothing in it is a Navier–Stokes statement.
- The dichotomy is machine-checked *as a band-pair* per anchor; the exact critical ratio
  inside each band is not claimed.
- (E1), (O2), (O3) remain open; the model singularity of Part IX remains model-level; the
  bridge imports Alpöge–Buckmaster and cannot outrank it; the unconditionally constructed
  singularity is and remains Alpöge–Buckmaster's. No deliverable of this program claims an
  unconditional blow-up proof for the Navier–Stokes equations.

With Part X the construction ledger stands at 33 theorems across six Lean files (V0, V1,
Bridge, Control, ModelSingularity, ThresholdNo), each closed with printed axiom dependencies,
plus three independent stdlib verifiers (`drift_budget_verification.py`,
`drift_bridge_verification.py`, `drift_threshold_dichotomy.py`).

## Part XI — The exact critical point: the 1000/999 accounting identity and the boundary of the dichotomy, machine-checked

Part X left, per anchor, a machine-checked band-pair: yes-side at contraction ratio
at most the V1 constant, no-side at persistence ratio at least the X0 constant, with the
exact critical ratio inside the band *not claimed*. This part pins the boundary of the
yes region **exactly**, in closed rational form, and machine-checks it: at contraction
ratio at most the exact critical μ*, the budget head is **never exceeded at any window**
— not merely at the witness windows of V1, but for all K. File: `formal/DriftCritical.lean`
(seven theorems: `telescope`, `chatBound1–3`, `criticalNever1–3`); companion verifier
`drift_critical_point.py` (stdlib, exact rationals).

### XI.1 The exact accounting identity (the 1000/999 feedback telescoping, general K)

Under the exact coupling recursion `30000000 * dhat(n+1) = 30000 * dhat n + 30000000 * chat n`,
the prefix sums satisfy, **exactly**, at every window K:

  `29970000 * sumTo dhat K + 30000000 * dhat K = 30000000 * (dhat 0 + sumTo chat K)`.

Splitting the left side, this is `(1000/999) * (dhat 0 + sumTo chat K)` minus the boundary
correction `dhat K / 999`: the response prefix is exactly 1000/999 times (launch + released
source), and the finite-window correction is always positive — the accounting never
overstates. This closes the item left open in Part X, where the transfer route deliberately
used only `dhat(n+1) ≥ chat n` and discarded the feedback.

### XI.2 The exact critical ratios, in closed form

With the caps at their adversarial values (launch d̂₀ = 10⁶, floor ĉ₀ = 39000), the exact
critical total released source is T = (999/1000)·M − d̂₀, and the exact critical contraction
ratio is μ* = 1 − ĉ₀/T in lowest terms:

| anchor | head M | exact critical μ* (closed form) | decimal |
| --- | --- | --- | --- |
| 1 | 1541354 | **250406323/269906323** | 0.927753 |
| 2 | 1744063 | **703318937/742318937** | 0.947462 |
| 3 | 1928014 | **443542993/463042993** | 0.957887 |

The boundary identity validating these, exact at all three anchors:

  `(999·M − 10⁹)·(d − c) = ĉ₀·1000·d`,  verified: 19500000·539812646 = 39000·1000·269906323 (anchor 1),
  39000000·742318937 = 39000·1000·742318937 (anchor 2), 19500000·926085986 = 39000·1000·463042993 (anchor 3);

equivalently the saturating limit is exact: (1000/999)·(10⁶ + ĉ₀·d/(d−c)) = M, i.e. a
trajectory contracting at exactly μ* saturates the head with deficit 0 in the limit —
and the Lean theorems show it never *breaches* the head at any finite window.

### XI.3 Machine-checked content

- `telescope`: the 1000/999 accounting identity above, proved for all K by omega induction
  with definitional step equations. This is the feedback telescoping named in Part X as the
  second half of the remaining unit.
- `chatBound1–3`: the source potential at each exact critical ratio — if
  `d·chat(n+1) ≤ c·chat n` with μ* = c/d, then `(d−c)·sumTo chat K + d·chat K ≤ d·chat 0`
  at every K: the released source is at most `d·chat0/(d−c)`.
- `criticalNever1–3`: the boundary theorems. Under the exact coupling, launch at cap
  d̂₀ ≤ 10⁶, floor at cap ĉ₀ ≤ 39000, and contraction at ratio **at most the exact critical
  μ\*\**, the prefix sums satisfy `sumTo dhat K ≤ M` for **every** window K. Printed axiom
  dependencies, all seven: `[propext, Quot.sound]`.

### XI.4 What this changes in the ledger

The yes region of the dichotomy is now machine-checked on the closed interval
[…, μ*ᵢ] at all three anchors (Part VI covered only […, νᵢ] at the witness windows, with
νᵢ < μ\*ᵢ by gaps of 4.5×10⁻⁸, 3.6×10⁻⁸, 4.6×10⁻⁸ — the V1 bisected anchors land within
5×10⁻⁸ of the exact criticals, now explained rather than coincidental). The no-side stands
as in Part X at ρᵢ ∈ {116/125, 237/250, 479/500}. The single remaining unresolved interval
per anchor is the open band (μ\*ᵢ, ρ\*ᵢ) of widths 2.47×10⁻⁴, 5.38×10⁻⁴, 1.13×10⁻⁴, inside
which the exact critical ratio has now been pinned from below by the exact closed form and
from above by the Part X no-side certificates. Disposing of it would require formalizing
monotonicity of the response in the source channel (the response prefix sums are nondecreasing
in each chat n) to convert the lower-bound persistence of Part X into a squeeze against the
exact boundary; that is the one remaining named formal unit.

### XI.5 Scope and integrity close

- Every statement of `formal/DriftCritical.lean` concerns integer sequences at fixed literal
  scale. Nothing in it is a Navier–Stokes statement.
- The boundary theorems are saturation-exact, not divergence claims: at μ* the head is
  approached and never breached; no no-side is claimed inside (μ*, ρ).
- (E1), (O2), (O3) remain open; the model singularity of Part IX remains model-level; the
  bridge imports Alpöge–Buckmaster and cannot outrank it; the unconditionally constructed
  singularity is and remains Alpöge–Buckmaster's. No deliverable of this program claims an
  unconditional blow-up proof for the Navier–Stokes equations.

With Part XI the construction ledger stands at 40 theorems across seven Lean files (V0, V1,
Bridge, Control, ModelSingularity, ThresholdNo, DriftCritical), each closed with printed
axiom dependencies, plus four independent stdlib verifiers (`drift_budget_verification.py`,
`drift_bridge_verification.py`, `drift_threshold_dichotomy.py`, `drift_critical_point.py`).
