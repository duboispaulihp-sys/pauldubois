# Roadmap — Two-Pillar Program Around the F-Closure Lemma

**Synthesis of the parent document ("The Harmless Subgroup and the F-Closure Lemma",
P. Dubois), Note A (extensions with full proofs), Note B (tropical program), Note
C (computational census: `census/harmless_census.py`, `census/results.md`), Note D
(ledger audit), Notes E–G (paths to VHC, closed laws, frozen profiles), Note H
(the cap-q family and joint (k, n) regime: `ledger/capq_engine.py`, `capq.txt`),
and Note I (Phase 7 completion pass: margins-2 closed form, cap-boundary law,
Regev constants, SKIP re-audit).**

---

## 1. Technique catalogue (what is now proved or built)

| # | Technique | Source | Status |
|---|---|---|---|
| T1 | F-closure lemma at cycle level (operations O1–O5), Theorem 4.5 | parent §4 | proved in parent |
| T2 | Dictionary cycles ↔ cohomology operations | parent Prop 2.3 | proved in parent |
| T3 | Collapse: the machinery fed full Hodge correspondences is *exactly* as strong as HC; sharpness of the cycle-level hypothesis | Note A Props 2.2′, 2.3 | proved (Note A) |
| T4 | B preserved by rationally algebraic correspondence action (Fulton–MacPherson on cycles) | Note A Lem 1.1, Lem 3.2 | proved, unconditional |
| T5 | Künneth components of correspondences land in B — under hypothesis C | Note A Prop 3.1 | proved, conditional on C |
| T6 | Primitive detection: HC failure reduces to primitive failure; one direction unconditional | Note A Props 3.3, Cor 3.4′ | proved, one direction unconditional |
| T7 | Descent/transfer of F-membership and HC counterexamples along finite covers and isogenies; Weil scalars give infinite representatives per gap | Note A Props 4.1, 4.2, Rk 4.3 | proved, unconditional |
| T8 | Kähler transfer of the whole dictionary, $B_{\mathrm{an}}$, F-closure; Zucker-type failures populate the gap provably | Note A Props 5.1–5.3 | proved |
| T9 | Census calculus: Weil slots $w_X(p) = \dim\mathrm{Hdg}^{2p} - \dim B^p$; unconditional-in-model rows with per-row flags | Note C §6 of Note A, `results.md` | built, 9/9 tests pass |
| T10 | Matroid pillar: AHK Chow rings, PD certificates, slot tables for $U_{2,3}, U_{2,4}, U_{3,5}, F_7, K_4$ | Note C (`matroid_chow`, `pd_check`) | built, validated |
| T11 | Tropical searchlight (T1-conjecture + VHC gate), Weil/CM ledger targets, primitivity+F-generacy gates | Note B | formulated, explicit conjectures |
| T12 | Ledger closed laws: polynomiality (deg exactly 2k), exact RSK leading constants (Σf² = k!), zero/closure law with constructive witnesses, certified Newton atlas k = 5..10 | Note F (`closed_laws.py`) | proved + machine-certified |
| T13 | Second asymptotic direction: rung constants = classical LIS counts N_k(4) (Gessel determinant, verified k = 0..30), Regev decay of the harmless share (root rate 16e/k), frozen SYT-weighted shape profile + participation numbers | Note G (`frozen_profiles.py`) | proved-cited + machine-certified |
| T14 | Cap-q family: parameterized ledger framework for caps q = 1..4; Kostka–contingency identity + generalized b-law proved cap-free; mirror/zero/birth/maturation laws at all q; split = square-count law certified k ≤ 10 all q ≤ 4, proved at q = 1; exact top coefficients all q; cap identified with the LIS parameter (Gessel/Regev) | Note H (`capq_engine.py`, 172 checks all PASS) | proved (most laws) + certified (split, k ≤ 10) |
| T15 | Phase-7 completion: margins-2 cycle-decomposition closed form (P²(2n,n) = A001499 − 1, proved, three-route + engine-identity certificates); cap-boundary laws ledger_4(4n,n) = 1, ledger_4(4n−1,n) = n² (forced columns; re-derive audit SKIPs (139,35) = 35², (160,40) = 1, plus (146,40)); Regev constants C_q closed form [proved-cited; two-route agreement C_2 16-digit, C_3 11-digit, C_4 0.0001 %]; SKIP ledger 42 → 38 unresolved, 4 upgrades verified digit-exactly vs the document (incl. the 44-digit live(20,35)) | Note I (`margins2.py`, `boundary_law.py`, `regev_constants.py`, `skip_reach.py`) | proved + proved-cited + cert |
| T16 | Phase 8, the norm formula (Route C): Hall–Gram identity T(μ,ν) = ⟨h_μ, h_ν⟩ and the norm formula Σ_μ C_μ(n) h_μ = [t^k](Σ_{r≤q} h_r t^r)^n, live = Σ z_λ f_λ² [proved; 114-check battery vs Routes A/B]; integer Hall–Gram DP, timings (live(20,35): 0.12 s vs 1780 s); deep campaign k = 36..65 at n = 35: 26/30 document claims digit-exact, 4 superseded (k = 62..65: document's CRT-reconstruction values disagree with exact arithmetic — corrected values recorded; document's own digit-count parabola confirmed); J.2 diagonal to k = 40 with liminf window tightened; batched Pieri Schur coefficients (whole b-vector at once) | Note J (`norm_route.py`, `j2_diagonal.py`, `deep_live.py`) | proved + cert + superseded-claims |

## 2. The two-pillar program

**Pillar I — the inside game (make $F$ sharp and computable).**
Theorem 4.5 + Note A's collapse theorem pin the boundary: the F-machine is
exactly as strong as its cycle-level hypotheses. Research thrusts:
- (I.a) Enumerate which cycle-level correspondences provably preserve $B$
  (so far: divisors, diagonals, Lefschetz, pushforwards — Note A Lem 1.1).
  Each addition is a theorem of the form "B-stable under —".
- (I.b) Prove or refute C (Künneth components of diagonals rationally
  algebraic) for special classes: curves (trivial), surfaces with $h^{2,0}=0$,
  abelian varieties. Under C, Note A Props 3.1/3.3 give the primitive-gap
  equivalence that Pillar II needs.
- (I.c) Extend the unconditional side of T6: refine exactly how much of the
  hard-Lefschetz bookkeeping can be made unconditional without C.

**Pillar II — the outside game (populate a Weil slot with a theorem).**
Target: some $X, p$ with $w_X(p) > 0$ proven (both dimensions is theorems),
i.e. an unconditional HC disproof in one degree. Thrusts:
- (II.a) **Kähler first** (Note A Prop 5.3): Zucker-type classes on compact
  non-projective Kähler manifolds are the cheapest hunting ground; the
  dictionary transfers verbatim. Deliverable: one worked example computing
  $\dim\mathrm{Hdg}^{2p}$ vs $\dim B^p_{\mathrm{an}}$ for a specific non-projective
  Kähler threefold.
- (II.b) **Weil-type / CM ledger** (parent App. A + Coda, Note B §3): tensor
  powers $\tau^m$ of Weil classes, gated through primitivity (Note A Cor 3.4′)
  and F-generacy checks run mechanically in Note C.
- (II.c) **Tropical searchlight** (Note B): conditional locator under
  (T1 ∧ VHC); its AHK/matroid anchor is already validated (T10). Only worth
  funding effort after (II.a) produces its first worked example.

## 3. Prioritized steps, with deliverable and risk

| Priority | Step | Deliverable | Risk of failure | Value if it works |
|---|---|---|---|---|
| 1 | Worked Kähler example (II.a) | written computation, populating a gap provably | low (Zucker's template exists) | first unconditional nonempty F-gap in the program |
| 2 | C for abelian varieties (I.b) | theorem or disproof of C for ppav of low dimension | medium: the question is genuinely open | unlocks T5/T6 converse; census slots become conditional-only |
| 3 | Census at larger scope: rank-4 matroids, $K_5$, degree-3 slots | faster GB (numerator/lex order, F4-style), or sage backend when available | computational only | bigger validated anchor set for Note B |
| 4 | Prove easy half of T1 (Note B §5.1) | unconditional specialization lemma | low-medium | makes the tropical pillar half-honest without conjectures |
| 5 | VHC resolution (parent App. B status) | unconditional proof of VHC for the cycle-level toolkit subset | high | either unlocks the searchlight, or produces shape-(iii) counterexamples — both are wins |
| 6 | Weil/CM ledger classification ($\tau^m$ powers, App. A scalars) | table of which powers are forced algebraic | medium | direct falsifiable targets for Steps 3–5 |
| 7 | ~~General cap q ≠ 4 engine~~ — DONE (Phase 6, Note H: cap-q family, 172 checks all PASS). Successor: **J.1** — bijective proof of the split identity for general (q,k): certified k ≤ 10 for all q ≤ 4, proved at q = 1; a bijective proof would close the one open structural piece of the per-cap framework | bijection between syzygy squares and big-shape/RSK data at all (q,k) | medium-high (combinatorial ingenuity) | upgrades Note H's model robustness reading from certified to proved |
| 8 | **J.2** — joint (k, n) regime: limit of D_k(k) (certified 1 ≤ liminf ≤ D_40 = 1.2049 at k = 40 via Route C — see Note J §3 for the k = 13..40 table (28 certified rungs, four certifications each, k = 13..19 digit-exact regression vs Phase 7) and the tightened window; cosine holding ~0.64–0.65 through the extended window, n·maxErr fallen to ≈ 0.17, D falling ≈ 0.009/rung (locally linear); the diagonal regime stays genuinely joint); the Phase-7 engineering unlock is DELIVERED (Route C, norm formula) and the census is no longer engine-bound inside k ≤ 40 | phase-diagram theorem or certified census at further rungs (k = 40 now costs minutes, k = 60 minutes-to-hours; the deep columns n = 33..40 are exact end-to-end via Note K) | low (engineering, resolved), with an open analytic core | pins Note E's G-Detect gate constants |
| 9 | **J.3** — ~~closed form at q = 2~~ **LARGELY DONE (Phase 7, Note I Prop I.1):** M(n,2) = (n!)²·Σ richness with c_j = j!(j−1)!/2, proved; engine identity P²(2n,n) = M(n,2) − 1 certified n ≤ 12 (proved at q = 1). **Successor:** closed form for all-margins-q matrix counts at q ≥ 3 (component classification no longer one-parameter; product/Skachkov-type IE in the literature) | closed form at q = 3, certified against Obs H.10 q = 3 data | medium-high | the second non-birth closed law; completes the margins ladder |
| 10 | **J.4** — joint-regime gate for the VHC hand-off: convert the certified census into a statement of the form "slot ranks grow at most like the degree" (the regime where the document's diagonal accounting is applied) | gate statement interfacing with Note E's G-T1/G-Lim/G-Detect | medium (geometric side) | connects the census program to the VHC boundary |
| 11 | **T17 (Phase 9, Note K) — DONE.** **Theorem K.1 proved**: every reachable Route C key has parts $\le q$, so the (k, q = 4) state pool is $\sum_{r\le k} p_4(r)$ — polynomial $O(k^q)$ in $k$ (~416{,}695 at $k = 119$, vs the 15.4e9 unrestricted-p(r) figure that produced the Phase-8 "hundreds of GB" void verdict — a ~37,000× overcount). All six deep-anomaly rungs resolved exactly in one full-spectrum pass per column (~90 s each): live(119,33), live(123,34), live(127,35) confirmed digit-for-digit; live(134,37) (168 digits), live(140,35), live(146,40) first-ever exact values; **Prop K.2** proved (live₄(4n,n) = T((4ⁿ),(4ⁿ))); exact crest/margin table for five deep columns confirming the document's +4 drift cadence (3.606 → 3.650) and both margin floats, one correction (runner-up at n = 37 is k = 135, exact gap 0.0098 not 0.0407); 738/738 grid certification vs the Phase-8 engine; 30-rung deep-campaign replication 26/4/0; outer-leaf divisibility spot checks all pass | — (delivered) | — | the census is no longer engine-bound at ANY documented rung; the deep columns n = 33..40 are exact data |

| 12 | **Phase 10 (Note L, `outer_leaf.py`) — DONE.** (a) **Certification battery** — Thm L.1 (closed supports == brute n ≤ 6, 90/90; C_μ spot grid 8,473/8,473), triple-engine T agreement (contingency DP 23,716/23,716; Sum-K-K 3,720/3,720; pinned values), Prop L.3 (n! = T((1ⁿ)) machine-proof n ≤ 27), Prop L.4 (banded Gram == routeC DP, 66/66 incl. n = 10..12), Prop L.5 (master identity three-way, 48/48), honesty note live(2,2) = 10 not ≡ 0 mod 4 — divisibility per-rung; (b) **document grammars** — eight live-parse grammars, ~200 constants digit-exact (21/24 maxTab, 24/25 monoliths, 7/7 six-box under the new half-margin convention, 41/42 gap ceilings, 10/10 mid-box, 17/17 maxInv, 25 peaks EXACT incl. the decoder-rescued k = 85, 89, 92, 96, 100, 104) with a **six-constant anomaly register** (maxTab n = 10/11/22, 26!, G(138), peak k = 47) — each double-certified engine-side (Gram + routeC DP agree) and diagnosed at digit level (typesetting digit-drops class + a ×10 + two broken doc series); (c) **full column sweep n = 8..40**: 33/33 columns, complete exact DP spectra (cap = 4n up to 160 rungs), Thm L.2 PASS in all, j = 0 full-box law PASS in all, bands 4/4, Runge-D spots pass, per-rung n²-divisibility scans recorded; the five deeps n = 33..40 re-run from the phase-9 checkpoints, all PASS. Next: mid-column anatomy parse (battery J parked: (34,17)…(60,30)), digit-restoration pass over the anomaly constants | Note L | — | the engine is certified end-to-end; every documented rung is now machine data |
| 13 | **Phase 11 (Note M, `family_gate.py`) -- DONE.** "Where else can VHC be reached?" -- eight NEW paths P9--P16 beyond Note E's map, each with a proved reduction, a named gate, and a falsifiable target: P9 CM islands (Deligne CM landing [proved-cited] + island-spreading reduction [proved, Prop M.2]; gates G-CM/G-SPREAD); P10 o-minimal/definable (locus descent [proved]; no-period-only-route boundary [proved, Prop M.6]; gate G-BR); P11 function fields (p=1 vacuous [proved]; one-fiber Chebotarev criterion [proved, Prop M.8]; gate TC-FF -- distinct mechanics from P4); P12 smoothability (flat-cycle transport half [proved, Prop M.9]; gate G-SMOOTH; incomparable with P1); P13 Mumford-Tate/motive (sub-PVHS reduction [proved, Prop M.10]; gate G-MLAB); P14 family frozen constants [program; FAM-1/2/3]; P15 first-order family gate -- MACHINE-TESTED: model laws Z/B/slot/invariance all [proved] (Props M.11/M.12), battery all PASS (see Note M Sec 8 / family_gate_results.txt), Tate-dropped band isolated; P16 Kuga-Satake variational lifting (lifting [proved-cited]; gate G-KS2 = P3's own seam; calibrated alignment of the model's zero window k<=4 with the doc's closed dim<=5 record -- Remark M.16, no exact mapping claimed). New tracks T19 (island arithmetic generation -- shape-constrained to order>=2 by Cor M.14), T20 (second-order model experiment FAM-2), T21 (one-fiber Chebotarev instances) | Note M | -- | the path map now has 16 entries; first-order transport is calibrated safe in the model, all explicit-construction doors stay closed by E.5/E.9 |

Sequencing rule: Steps that produce *rational-side theorems unconditionally*
(1, 2, 4, 5) dominate steps that only sharpen conditionals (3, 6) — but 3 runs
in the background since the engine exists and scales by engineering, not ideas.
The dependency graph is: 5 → (4, 6) → 2; 1 is independent; 3 supports everything.

**Engineering unlocks registered in Phase 7** (move the deep-rung ceiling,
not the mathematics):

1. **Fast contingency DP — DELIVERED in Phase 8, from the other side.
   The contingency DP itself is unchanged; instead Note J proves the norm
   formula live_q(k,n) = ‖[t^k](Σ h_r t^r)^n‖², whose integer DP in the
   p-basis costs ~ n·Σ_{r≤k} p(r) block-multiplications — subexponential
   in k (Hardy–Ramanujan) instead of exponential. Measured: live(20,35)
   0.12 s (Route B: 1780 s), live(65,35) 10 s. Delivered: the 30 deep
   rungs k = 36..65 at n = 35 (26 document claims digit-exact, 4
   superseded) and the J.2 diagonal to k = 40. ~~Remaining: the k ≥ 119
   sextet needs Σ_{r≤119} p(r) ~ 10^8 states — a further ~1000× state-space
   reduction, or a closed form for [t^k] P_4(t)^n at n ~ k/4.~~
   **SUPERSEDED in Phase 9 (Note K, Theorem K.1):** the quoted pool was an
   unrestricted-p(r) overcount — the true key space is Σ_{r≤k} p_q(r) =
   O(k^q), and the sextet was resolved exactly (row 11 above). Optionally
   still open: a closed form for [t^k] P_4(t)^n at n ~ k/4 (Prop K.2 gives
   the end rung live₄(4n,n) = T((4ⁿ),(4ⁿ)); the interior rungs are the
   remaining honest target).
2. **f_syt suffix counts.** The inner `down`-hook sum of `f_syt` costs
   O(k·rows) per shape; suffix counts give O(rows + k). Ladder rungs k
   ≥ 243 (current q = 4 ceiling) then coast into the extrapolation
   regime, and the J.2 census passes k = 22.
3. **N_k_q is already validated against Gessel's Bessel determinant at
   k = 30, 31, 32, 35, 38, 40 (digit-exact, this session)** — the
   constants ladder can be trusted wherever f_syt reaches.

## 4. How the census engine extends

Current state (`census/harmless_census.py`, ~600 lines, pure Python,
exact `fractions.Fraction` arithmetic, 9/9 unit tests):
- `GradedRing`: full-length exponent tuples, degree-capped Buchberger with
  saturation (all monomial multiples of GB elements per degree), exact rref/rank.
- `HarmlessCensus`: seed-closure (`algebra_B`), per-degree slot table
  $\dim_Z, \dim_B, w(p)$; external products with both-side zero-padding of
  relations; validated examples: $\mathbb{P}^4$ (all slots 0), Weil-slot ring
  $w = (0,0,1)$, slot$\otimes\mathbb{P}^2$ ($w = (0,0,1,1,1)$, hand-checked).
- Matroid pillar: circuits → flats lattice → AHK Chow presentation → PD
  certificates; $U_{3,5}, F_7, K_4$ all pass PD.

Planned extensions, in engineering order:
1. **Speed**: monomial order → graded lex for degree-capped GB; fraction-free
   rref; memoize S-pairs. Cap currently ~10 vars top≤3 or ~15–20 vars top≤2.
2. **Scope**: rank-4 matroids (16 flats → 16-variable rings, borderline),
   $K_5$ graphic, Weil rings at higher $g$.
3. **Semantics**: add the Hodge-correspondence-collapse simulation only as a
   *report* (three-line proof in Note A Prop 2.3: deliberately not simulated in
   the engine — the collapse is a theorem, not a computation).
4. **Interface**: emit per-row provenance flags (model vs theorem) exactly as
   Note A's Lemma 6.2 demands, so no row is ever read as more than it is.

## 5. Risk register (program level)

| Risk | Pillar | Severity | Response |
|---|---|---|---|
| C stays unproven in all useful cases | I | high | census rows carry conditional flags; T6 keeps one direction unconditional |
| VHC fails | II | ends inside game as designed | shape-(iii) transport counterexamples become the deliverable (Note B §2) |
| T1 (limit comparison) false | II (tropical) | fatal to tropical pillar | gates in Note B §3 discard false positives; AHK anchor survives independently |
| Pure-Python GB too slow for the next scope | computational | medium | engine swaps algorithms, not math; results.md records verified ceilings |
| A "candidate counterexample" is F-generated after all | II | fatal to that candidate | mechanical gate (Note B §3): seed-closure check + primitivity, both automated |

## 6. File index

- `notes/01-f-closure-extensions.md` — Note A: proofs T3–T8 above.
- `notes/02-tropical-program.md` — Note B: T11, conjectures T1/VHC gated.
- `census/harmless_census.py`, `census/test_census.py` — engine + tests (T9, T10).
- `census/results.md`, `census/results_demo.txt` — validated outputs and demo log.
- `notes/03-ledger-verification.md` — Note D: digit-exact audit of the document's
  Appendix D.5 ledger (409 PASS / 0 FAIL / 42 SKIP), deep power-chain audits
  (P_9–P_11, the 519-square P_20(35), column total_35), pre-registration of the
  columns n = 36..40, exact Newton forms of P_6/P_7/P_8.
- `notes/04-paths-to-vhc.md` — Note E: the complete map of paths to the
  variational Hodge conjecture (F-transport ⟺ VHC; motivated-class ceiling
  E.9, the variational no-go; abelian equidepth E.7; Tate, limit-MHS/tropical
  and Kähler routes; model calibration), with every claim status-labeled
  (proved / proved-cited / gated / program).
- `ledger/vhc_calibration.py`, `ledger/vhc_tables.md` — exact VHC calibration
  of the ledger model (zero window k ≤ 4, syzygy census n = 2..16, slot counts,
  densities).
- `notes/05-closed-laws-and-asymptotics.md` — Note F: closed laws and exact
  asymptotics (Thm F.1 polynomiality, F.2 RSK constants with Σf² = k!, F.3
  zero/closure law, F.4 certified atlas k = 5..10); VHC reading: any candidate
  detection functional must carry a frozen RSK-type leading constant.
- `notes/06-frozen-profiles.md` — Note G: the second asymptotic direction —
  rung constants are the classical bounded-LIS permutation counts N_k(4)
  (Gessel's Bessel determinant, digit-exact cross-check k = 0..30); Regev
  share law (harmless share dies at 16e/k root rate); frozen shape profile
  (dominant shapes, participation numbers); two-parameter VHC detection
  fingerprint (frozen share + Regev decay + SYT profile).
- `ledger/closed_laws.py` + `closed_laws.txt` — Phase-4 run: RSK constants,
  zero-law checks, full Newton forms with 2k-point certifications.
- `ledger/pre_register2.py` + `pre_register2.txt` — pre-registered rungs
  P₉/P₁₀/P₁₁ at n = 36..40 (12/19/29 squares) + maturation law b_(5..9).
- `ledger/` — engine (`ledger_engine.py`), calibration (`calibrate.py`), claim
  extractor (`extract_claims.py`), auditor (`verify_claims.py`), power audits
  (`audit_powers.py`), pre-registration (`pre_register.py`), Newton forms
  (`newton_fit.py`), each with its captured output/report file.
- `notes/07-cap-q-and-joint-regime.md` — Note H: the cap-q family (T14). §1
  definitions, §2 the cap-free Kostka–contingency identity (Lemma H.1) and
  generalized b-law (Theorem H.2) with the uncapped Cauchy limit (Remark H.3),
  §3 mirror law (Prop H.4, all q, with the honesty note that per-shape
  s_{μ†}(1ⁿ) = s_μ(1ⁿ) is false) and split = square-count theorem (H.5;
  certified k ≤ 10 all q ≤ 4, proved at q = 1 with closed law
  P¹ = C(n,k)²(k!−1)), §4 zero law + witnesses (Prop H.6 / Thm H.7, all q,
  `dom_padded`), birth (H.8), maturation (H.9), top-corner law (Obs H.10:
  P¹ₙ(n) = n!−1; q = 2 row = OEIS A001499 − 1), §5 exact top coefficients
  (Thm H.11) and Gessel family anchors (Thm H.12, Regev exponent (q²−1)/2,
  v⁴(30) = 161.3249 ≡ Note G), §6 joint (k,n) census (k = 5..12 at n = k/2k/3k),
  §7 VHC reading, §8 out-of-scope register.
- `ledger/capq_engine.py` + `capq.txt` — Phase-6 engine and H.0–H.8 battery
  transcript (**172 checks, all PASS, 191 s**). Reuse conventions (in-file):
  `partitions` is a generator; Kostka in the pinned type convention; witnesses
  need zero-padded dominance (`dom_padded`); brute-force row-pool entry cap is
  q, not n (a first-draft bug the three-route arbitration caught — evidence
  the arbitration protocol works).
- `notes/08-closed-forms-boundary-law-and-regev-constants.md` — Note I: Phase 7
  completion pass (T15): §1 margins-2 closed form (Conjecture → Prop I.1 with
  full cycle-decomposition proof; certificates C.1–C.3; Obs H.10 q = 2
  triangulated n ≤ 12), §2 cap-boundary law (Lemma I.2 rectangle identity,
  Lemma I.3 forced columns, Prop I.4 top-boundary laws, Prop I.5 boundary
  shape counts; 62/62 certificate; the three audit SKIPs re-derived), §3
  Regev constants closed form (Thm I.6; C_1..C_6 values; the √(2π) and j!
  transcription traps recorded), §4 J.2 census to k = 19 (D_k(k) → 1.420;
  cosine sinking), §5 SKIP re-audit (measured T_q cost model), §6 VHC reading
  (three exactly-solved strata; four-way consistency demand), §7 out-of-scope
  register.
- `ledger/margins2.py` + `margins2.txt`, `ledger/boundary_law.py` +
  `boundary_law.txt`, `ledger/regev_constants.py` + `regev_constants.txt`,
  `ledger/joint_ext.py` + `joint_ext.txt`, `ledger/skip_reach.py` +
  `skip_reach.txt` — Phase-7 applications and transcripts, as indexed in
  Note I's closing engine note.
- §3 of this file: items 7–10 are the post-Phase-6 queue (J.1–J.4 of Note H
  §§7–8) with their Phase-7 statuses; C_q for q ≤ 4 is now closed
  [proved-cited] (q ≥ 5 needs no census route); the SKIP ledger is 42 → 38
  unresolved with measured ceilings and named unlocks (above); the four
  upgrades (3 ledger + live(20,35)) are verified digit-exactly against the
  document's printed values.

**File-index addendum for Phases 8–10:**

- `notes/09-live-norm-formula.md` — Note J: the norm formula (Hall–Gram
  identity), integer DP, deep campaign, J.2 diagonal.
- `ledger/norm_route.py` + `norm_route.txt`, `ledger/j2_diagonal.py` +
  `j2_diagonal.txt`, `ledger/deep_live.py` + `deep_live.txt` — Phase-8
  engines and transcripts.
- `notes/10-deep-sextet.md` — Note K: Theorem K.1 (pool bound, parts ≤ q),
  the six deep-anomaly resolutions, Prop K.2, crest/margin table; engines
  `ledger/sextet.py`, `ledger/j2_parent*.py`, `ledger/j2_worker.py`,
  `ledger/j2_resume.py`, checkpoints `sextet_ckpt_*.pkl`, transcript
  `ledger/sextet.txt`.
- `notes/12-outer-leaf.md` — **Note L**: Phase 10 — the outer-leaf column
  machine (`ledger/outer_leaf.py`, transcript `ledger/outer_leaf.txt`,
  1,289 lines): certification battery (Thm L.1–L.5, triple-engine T
  agreement), eight live document grammars with the six-constant anomaly
  register, the full column sweep n = 8..40 and the five deeps n =
  33..40 — all PASS.
- `notes/13-further-paths-to-vhc.md` — **Note M**: Phase 11 — eight NEW
  paths to VHC (P9–P16): CM islands, definable route, function-field
  arithmetic, smoothability, Mumford–Tate gate, family frozen constants,
  the machine-tested first-order family gate, and Kuga–Satake
  variational lifting; each with proved reductions, named gates, and
  falsifiable targets (T19–T21).
- `census/family_gate.py` + `family_gate_results.txt` — Phase-11 engine:
  the model-family gate (ε-ring external products on the full demo
  roster), model laws proved (Props M.11/M.12), battery all PASS, and
  the Tate-dropped negative controls.
