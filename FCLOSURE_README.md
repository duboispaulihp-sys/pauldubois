# The Harmless Subgroup and the F-Closure Lemma — Working Materials

This directory develops new techniques around Paul Dubois's working-session
notes on the Hodge conjecture: the harmless subgroup $B$, the F-subgroup
$F^p(X)$, the F-closure lemma (Theorem 4.5), and the Weil-slot census. All
content was developed from the uploaded 153-page PDF.

## Contents

| Path | What it is | Status |
|---|---|---|
| [`notes/01-f-closure-extensions.md`](notes/01-f-closure-extensions.md) | **Note A** — full-proof extensions of the F-closure toolkit: collapse of the machine when fed full Hodge correspondences (bound is sharp), B-preservation by rationally algebraic correspondences, Künneth components under hypothesis C, primitive detection, descent along finite covers and isogenies, Kähler transfer, census calculus | complete; conditional results labeled |
| [`notes/02-tropical-program.md`](notes/02-tropical-program.md) | **Note B** — tropical program, honestly framed as a *searchlight*: explicit conjectures T1 (weight-graded limit comparison) and VHC gating; Weil-type/CM ledger targets; AHK/matroid anchor; primitivity + F-generacy gates | complete; no invented fan conventions |
| [`roadmap/00-roadmap.md`](roadmap/00-roadmap.md) | **Roadmap** — technique catalogue (T1–T11), two-pillar program, prioritized steps with risk register, census engine extension plan | complete |
| `census/harmless_census.py` | **Note C engine** — exact-arithmetic graded-ring machine: degree-capped Buchberger + saturation, seed closure, Weil-slot tables, external products, AHK matroid Chow rings, PD certificates | complete, 9/9 tests pass |
| `census/test_census.py` | unit tests (run `python3 test_census.py`) | 9/9 pass |
| `census/results.md` | validated outputs with hand checks and honest limitations | complete |
| `census/results_demo.txt` | full captured demo output | complete |
| [`notes/04-paths-to-vhc.md`](notes/04-paths-to-vhc.md) | **Note E** — the complete map of paths to the variational Hodge conjecture: F-transport ⟺ VHC, component dichotomy, primitive reduction and its exact SC-B boundary, the motivated-class ceiling (no-go for explicit methods), abelian equidepth theorem, Tate/limit-MHS/Kähler routes, model calibration | complete; every claim status-labeled |
| [`notes/03-ledger-verification.md`](notes/03-ledger-verification.md) | **Note D** — digit-exact audit of the document's Appendix D.5 iterative ledger (markdown version), deep power-chain verifications, pre-registration for columns n = 36..40, Newton forms of the syzygy polynomials | complete; **409 PASS / 0 FAIL / 42 SKIP** |
| `ledger/ledger_engine.py` | **Ledger engine** — exact arithmetic: Route A (T-matrix DP), Route B (Kostka b-law), hook-square ledger, brute-force arbiter, all laws | complete; all routes arbitrated |
| `ledger/calibrate.py` | engine self-calibration battery (GT vs SSYT 345/345, brute-force arbitration, law checks) | all PASS |
| `ledger/extract_claims.py` + `claims.json` | claim extraction from the uploaded markdown (282+ claims) | complete |
| `ledger/verify_claims.py` + `verification_report.txt` | the audit: every printed claim within engine reach | **409 PASS / 0 FAIL / 42 SKIP** |
| `ledger/audit_powers.py` + `powers_audit.txt` | deep power-chain audits: P_9(24), P_10(25), P_11(26), **P_20(35) — 519 squares**, column total_35 | all digit-exact |
| `ledger/pre_register.py` + `pre_register.txt` | pre-registered columns n = 36..40 (live all k≤9, birth squares, P_6–P_8, ledger k≤9, mirrors) | complete, self-asserting |
| `ledger/newton_fit.py` + `newton_fit.txt` | exact Newton forms of P_6, P_7, P_8, certified on ~25 fresh points each | complete |
| [`notes/05-closed-laws-and-asymptotics.md`](notes/05-closed-laws-and-asymptotics.md) | **Note F** — closed laws and exact asymptotics of the ledger: polynomiality in n with exact degree 2k (Thm F.1), exact leading constants via RSK with Σf² = k! (Thm F.2), zero/closure law with constructive positivity witness (Thm F.3), certified closed-law atlas extended to rungs k = 9, 10 (Thm F.4), pre-registration P₉–P₁₁ at n = 36..40 | complete; proofs full, flags per claim |
| [`notes/06-frozen-profiles.md`](notes/06-frozen-profiles.md) | **Note G** — the second asymptotic direction (k → ∞): the frozen constants are classical — Σ_(μ₁≤4) f_² = N_k(4) = # perms with LIS ≤ 4 (Gessel), Gessel's Bessel-determinant identity verified digit-exactly k = 0..30, Regev share law (harmless share dies at root rate 16e/k), frozen shape profile with participation numbers and dominant-shape fingerprints | complete; C₄ itself registered, not evaluated |
| `ledger/closed_laws.py` + `closed_laws.txt` | Phase-4 engine: RSK constant table (k = 5..10), zero-law checks, full Newton forms of ledger(5..8,·), live(5..9,·), P(6..10,·), each certified on 2k fresh points | all green |
| `ledger/pre_register2.py` + `pre_register2.txt` | pre-registered rungs P₉/P₁₀/P₁₁ (12/19/29 squares) at columns n = 36..40 + one-row maturation law b_(k), k = 5..9 | complete, all assertions pass |
| `ledger/vhc_calibration.py` + `vhc_tables.md` | VHC calibration of the model: zero window k≤4, syzygy census n=2..16, slot counts, ledger densities | complete, self-asserting |
| [`notes/07-cap-q-and-joint-regime.md`](notes/07-cap-q-and-joint-regime.md) | **Note H** — the cap-q family of ledger models (q = 1..4): complete proofs that every cap-4 law (Kostka–contingency identity, b-law, mirror law, zero law, birth, maturation, exact top coefficients) holds at every cap q; split identity = square-count law certified k ≤ 10 for all q ≤ 4 (proved at q = 1); new closed laws P¹ = C(n,k)²(k!−1) and P¹ₙ(n) = n!−1; Gessel/Regev parameter identification (cap ↔ LIS); joint (k,n) census table | complete; **172-check battery H.0–H.8 all PASS / 0 FAIL (191 s)** |
| `ledger/capq_engine.py` + `capq.txt` | Phase-6 engine: parameterized cap-q family (b_q, T_q, live_A_q/live_B_q, ledger_q, P_q, brute_live_q, N_k_q, Newton interpolator), H.0–H.8 arbitration battery (T-identity, three-route arbitration, split/square-count polynomial identities, zero law + witnesses + mirror, birth, maturation vs IE & GF, top coefficients, Gessel family k ≤ 30, joint census k = 5..12) | **172 PASS / 0 FAIL**; reuse conventions documented in-file (partitions is a generator; Kostka type convention pinned; `dom_padded` for q-family witnesses; brute-force entry cap is q, not n) |
| [`notes/08-closed-forms-boundary-law-and-regev-constants.md`](notes/08-closed-forms-boundary-law-and-regev-constants.md) | **Note I** — Phase 7, the targeted completion pass: J.3 at q = 2 closed (margins-2 cycle-decomposition closed form, full proof, three-route + engine-identity certificates); the cap-boundary law (rectangle identity, forced-columns proof of ledger_4(4n,n) = 1 and ledger_4(4n−1,n) = n²); Regev constants C_q identified in closed form (C_2 = 1/√π digit-exact, C_3 two-route 9-digit agreement, C_4 census-tail cert, C_5/C_6 predictions); J.2 census to k = 19 (liminf window tightened to ≤ 1.420); SKIP re-audit with measured cost ceilings | complete; every claim status-labeled [proved]/[proved-cited]/[cert]/[program] |
| `ledger/margins2.py` + `margins2.txt` | Phase-7 application: margins-2 closed form M(n,2) = (n!)²·Σ richness with c_j = j!(j−1)!/2, three-route arbitration (formula/DFS/EGF) + engine identity P²(2n,n) = M(n,2) − 1 (n = 1..12 ALL PASS) + A001499 prepaid n = 0..40 | all green |
| `ledger/boundary_law.py` + `boundary_law.txt` | Phase-7 application: rectangle identity + headline boundary values at n = 10/20/35/40, complement-shape-count law, mirror-law consistency (62/62 OK) | all green |
| `ledger/regev_constants.py` + `regev_constants.txt` | Phase-7 constants: Regev closed form to 40+ digits (C_1..C_6) + independent all-integer W_k extrapolation ladders with exact-Fraction 5-window fits and q = 2 method self-check | complete; q = 2 digit-exact | 
| `ledger/joint_ext.py` + `joint_ext.txt` | Phase-7 application: joint-diagonal census rows k = 13..19 (D_k(k), cos_k(k), n·maxErr) in Note-H §6 format; ends at k = 19 (k = 20 rung deferred to sped-up engine) | complete to k = 19 |
| `ledger/skip_reach.py` + `skip_reach.txt` | Phase-7 appendix to the sealed Phase-2 audit: 3 ledger SKIPs REACHED with structural explanations, live(20,35) dedicated engine attempt, remaining SKIPs with measured cost ceilings (T_q: 5.4 ms/pair at k = 12 → 111 s at k = 24); **4/4 upgrades verified digit-exactly against the document's printed values, incl. live(20,35) = 27277245818749123471218465200909528830189120 (Route B, 1780 s)** | complete |
| [`notes/09-live-norm-formula.md`](notes/09-live-norm-formula.md) | **Note J** — Phase 8, the norm formula: full proofs that the engine's contingency count is the Hall Gram matrix ($T(\mu,\nu) = \langle h_\mu, h_\nu\rangle$ via Jacobi–Kostka + Schur orthonormality), that $\sum_\mu C_\mu(n) h_\mu = [t^k](\sum_{r\le q} h_r t^r)^n$ (Route C, Theorem J.2), hence $\mathrm{live}_q(k,n) = \lVert[t^k]P_q(t)^n\rVert^2 = \sum_{\lambda\vdash k} z_\lambda f_\lambda^2$ with a subexponential DP; $q=1$ closed law; leading law $\cdot k!/n^{2k}\to 1$; the deep campaign (**26/30 deep rungs digit-exact** vs the document, and 4 rungs superseded — the document's CRT-reconstructed live(62..65,35) fail against exact arithmetic, corrected values recorded); J.2 diagonal to k = 40 with the liminf window tightened | complete; every claim status-labeled |
| `ledger/norm_route.py` + `norm_route.txt` | Phase-8 engine: Route C (integer Hall–Gram DP in the p-basis, scale $L=\mathrm{lcm}\,z_\lambda$), certification batteries vs `live_A_q` (72 + 30 checks), vs `live_B_q` (12 checks incl. (12,12,4)), $q=1$ closed law (152 checks), leading-law window, timings ((20,35,4) in 0.12 s vs 1780 s Route B in Phase 7) | all green |
| `ledger/j2_diagonal.py` + `j2_diagonal.txt` | Phase-8 application: J.2 joint-diagonal census rows k = 13..40 (Route C live; hook ledger; batched Schur coefficients by iterated Pieri — the whole $b$-vector at once, replacing the per-shape bottleneck that cost 923 s at k = 19); regression rows k = 13..19 reproduced digit-exactly from `joint_ext.txt`; per-k certifications (Route-B identity $\sum b^2 = $ live, spot `b_q`, RSK frozen denominator $k! - N_k(4)$, fast hooks vs `f_syt`) | all green |
| `ledger/deep_live.py` + `deep_live.txt` | Phase-8 application: the 30 deep-rung document claims live(k,35), k = 36..65, recomputed exactly by Route C: **26 EXACT**, 4 superseded (k = 62..65, corrected values printed); k ≥ 119 sextet resolved exactly in Phase 9 — see Note K / `sextet.py` | complete |
| [`notes/10-deep-sextet.md`](notes/10-deep-sextet.md) | **Note K** — Phase 9, the deep sextet: **Theorem K.1 proved** (Route C's reachable keys have parts ≤ q, so the state pool is Σ_{r≤k} p_q(r) = O(k^q) — the Phase-8 "hundreds of GB" cost model was a ~37,000× p(r)-vs-p_q(r) overcount, its verdict void); all six deep-anomaly rungs resolved exactly in one full-spectrum pass per column (~90 s each), three confirmed digit-for-digit ((119,33), (123,34), (127,35)) and three first-ever exact values ((134,37), 168 digits; (140,35), 147 digits; (146,40), 186 digits, integer printed in full); **Prop K.2** (live₄(4n,n) = T((4ⁿ),(4ⁿ)), the end-rung "full box" explained); mirror-census isometry corollary; exact crest/margin table for five deep columns — drift cadence +4 confirmed to crest/n = 3.650, both margin floats confirmed, one runner-up correction (n = 37: k = 135, exact gap 0.0098, not 0.0407); the 42-SKIP audit ledger fully discharged | complete; 738/738 grid certification vs the Phase-8 engine; 30-rung replication 26/4/0 |
| `ledger/sextet.py` + `sextet.txt` | Phase-9 engine: full-cap count-vector DP (Route C with in-place ascending-degree scheme — the Thm-K.1 key space), cert mode (738/738 grid equality + pool-bound checks), spectrum/finish modes (chunked with pickle checkpoints; per-degree Thm-K.1 key-space assertion, crest/runner-up/margin extraction, claim comparison, outer-leaf divisibility spot checks) | all green; runs certified |
| [`notes/12-outer-leaf.md`](notes/12-outer-leaf.md) | **Note L** — Phase 10, the outer-leaf column machine: the certification battery (Thm L.1 closed supports == brute 90/90 + C_μ grid 8,473/8,473; the T-runner's TRIPLE-engine agreement — contingency DP 23,716/23,716 and Sum-K-K 3,720/3,720 digit-exact; Prop L.3 n! = T((1ⁿ)) machine-proof n ≤ 27; Prop L.4 banded Gram == routeC DP 66/66; Prop L.5 master identity three-way 48/48; honesty note: live(2,2) = 10 not ≡ 0 mod 4 — divisibility is per-rung, no global n²-law); eight live document grammars parsing the uploaded markdown (no hand transcription) with the six-constant anomaly register (maxTab n = 10, 11, 22; the 26! monolith; G(138)'s dropped tail; the peak k = 47 43-vs-44-digit typeset) — each anomaly double-certified on the engine side (Gram runner + routeC DP agree) and the doc's own series shown non-smooth at exactly those points; the FULL column sweep n = 8..40: 33/33 columns with complete DP spectra (cap = 4n, up to 160 rungs), Thm L.2 live(4n−1,n) = n²·T((4ⁿ⁻¹,3)) PASS in all, the j = 0 full-box law PASS in all, bands j = 2..5 4/4 in all, Runge-D spots all pass, 25 doc-printed peak integers EXACT (including the 93-digit k = 85, 99-digit k = 89, 104-digit k = 92, 110-digit k = 96, 115-digit k = 100 decoder-pinned rungs), per-rung n²-divisibility scans recorded; the five deeps n = 33..40 re-run from the phase-9 checkpoints, all PASS | complete; transcript 1,289 lines, 158 PASS, session FAILS = 7 (all six registered anomalies, faithfully reproduced) |
| `ledger/outer_leaf.py` + `outer_leaf.txt` | Phase-10 engine: the certification / docgram / column / deep / close mode suite over the certified runner + norm_route DP + sextet pools; parses the document LIVE and appends every battery to `outer_leaf.txt`; ends with the "end of outer_leaf" close marker | all PASS except the six registered doc-constant anomalies |
| [`notes/13-further-paths-to-vhc.md`](notes/13-further-paths-to-vhc.md) | **Note M** — Phase 11, "where else can VHC be reached?": eight NEW paths P9–P16 beyond Note E's map, each with a proved reduction, a named gate, and a falsifiable target — P9 CM islands (Deligne landing [proved-cited] + island-spreading reduction [proved]); P10 o-minimal/definable (locus descent [proved] + the no-period-only-route boundary theorem [proved]); P11 function fields (p = 1 vacuous [proved] + one-fiber Chebotarev criterion [proved]); P12 smoothability (flat-cycle transport half [proved], gate G-SMOOTH incomparable with P1); P13 Mumford–Tate/motive gate (sub-PVHS reduction [proved]); P14 family frozen constants [program: FAM-1/2/3]; P15 the first-order family gate — laws [proved] (Props M.11/M.12) and machine-tested (see `family_gate_results.txt`); P16 Kuga–Satake variational lifting [proved-cited] with the calibrated alignment of the model's zero window k ≤ 4 against the document's closed dim ≤ 5 record (Remark M.16) | complete; every claim status-labeled [proved]/[proved-cited]/[gated]/[program] |
| `census/family_gate.py` + `family_gate_results.txt` | Phase-11 engine: the model-family gate — first-order families as ε-ring external products on the full demo roster (P⁴, P², Weil-slot ring, slot⊗P², matroids U_{2,3}, U_{2,4}, U_{3,5}, F₇, K₄); slot law w_fam(p) = w_A(p) + fw·w_A(p−1), B-law, Z-law, VHC invariance, engine-vs-teacher transport certificates, hand anchors (P², slot ring), two-parameter (ε,δ) variants, and Tate-dropped negative controls — all checks PASS, exact `fractions` arithmetic | complete; transcript in `family_gate_results.txt` |

## Headlines

- **Collapse theorem (Note A, Props 2.2′/2.3):** feeding the F-machine all
  Hodge correspondences collapses it to HC itself — the cycle-level hypothesis
  of Theorem 4.5 is *exactly* sharp. Every future extension must stay at cycle
  level or be honestly conditional.
- **Primitive reduction (Note A, Prop 3.3 / Cor 3.4′):** HC failure reduces to
  primitive failure, one direction unconditionally — every candidate
  counterexample must be primitive and not F-generated from $B$.
- **Descent (Note A, Props 4.1/4.2):** counterexamples and F-membership both
  transfer along finite covers; Weil scalars $[m]^* = m^{2k}$ give infinitely
  many representatives of any gap.
- **Kähler transfer (Note A, Props 5.1–5.3):** the whole dictionary works for
  compact Kähler with analytic cycles; Zucker-type failures populate the gap
  provably.
- **Validated census (Note C):** $\mathbb{P}^4$ all slots 0; Weil-slot ring
  $w = (0,0,1)$; slot$\otimes\mathbb{P}^2$ $w = (0,0,1,1,1)$ (hand-checked);
  AHK Chow rings of $U_{2,3}, U_{2,4}, U_{3,5}, F_7, K_4$ satisfy Poincaré
  duality in the engine; known computational ceilings documented.
- **The ledger is sound (Note D):** the document's Appendix D.5 iterative
  ledger verifies digit-exactly against an independently built engine
  everywhere the engine reaches — including the fully spelled 519-square
  $P_{20}(35)$ descent, the printed live(20,35) and ledger(20,35), the 69-rung
  35th column, and the 74-digit column total. 42 claims lie beyond the
  pure-Python reach and are enumerated as honest SKIPs; no mismatch found.
- **Paths to VHC (Note E):** the variational problem is calibrated three ways
  — F-transport ⟺ VHC (proved, both directions); the motivated-class ceiling
  (no class assembled from divisor-fed equipment can ever fault VHC — the
  third, and strongest, mutual exile of any counterexample, alongside
  Theorem 4.5 and the collapse Prop 2.2); and the abelian equidepth theorem
  (VHC for abelian families ⟺ HC(AV) at each relative dimension, via
  Principle B). The ledger model's own inductive VHC-pattern is computed
  exactly: zero window k ≤ 4, first Weil-type slot born at k = 5.
- **The next columns, in advance (Note D §4–5):** complete pre-registration
  for n = 36..40 (all rungs k ≤ 9, birth squares, syzygy decompositions,
  ledger), plus exact Newton-form polynomial laws for P_6 (deg 12), P_7
  (deg 14), P_8 (deg 16) certified on ~25 fresh points each — run-by-run
  prints are upgraded to closed forms.
- **Closed form, with exact constants (Note F, Phase 4):** the ledger's
  variational pattern is now proved polynomial of exact degree 2k; its
  n → ∞ shares freeze into exact RSK constants — live(k,n) ~ n^{2k}/k!,
  P_k(n) ~ (Σ_{σ₁≥5} f_σ²)·n^{2k}/(k!)² with Σ_σ f_σ² = k! (RSK), so
  P₅/live → 1/120; zero law P_k(n) = 0 ⟺ k ≤ 4 or k ≥ 4n+1 with explicit
  interior witnesses; the closed-law atlas (ledger k = 5..8, live k = 5..9,
  P k = 6..10) is certified on 2k fresh points with top coefficients
  matching the RSK constants exactly; pre-registration extended to rungs
  P₉/P₁₀/P₁₁ at n = 36..40 (12/19/29 squares) and the maturation law to
  b_(5..9) at n = 36..40.
- **The constants are classical (Note G, Phase 5):** the harmless share of
  rung k is exactly N_k(4)/k! — permutations with LIS ≤ 4 (RSK); Gessel's
  Bessel-determinant identity reproduces these constants digit-exactly for
  k = 0..30 through a wholly independent route; by Regev, the harmless share
  dies at root rate 16e/k (by k = 30 it is 7×10⁻⁶, from 119/120 at birth),
  and each rung's square census freezes into the SYT-weighted shape profile
  (dominant shapes at n = 40 already match the ∞-frozen ones at k = 9, 10;
  participation ρ₂₀ = 95.6 vs the document's 519 finite-n squares).
- **The cap-4 framework is one instance of a rigid per-cap structure (Note
  H, Phase 6):** every law the document uses at cap 4 survives at caps q =
  1, 2, 3, 4 — the Kostka–contingency identity and generalized b-law are
  cap-free (Lemma H.1 + Theorem H.2, both proved), the mirror law (Prop
  H.4), zero law (Prop H.6), birth P^q_{q+1} = (C(n+q,q+1) − n)² (Prop
  H.8) and maturation law (Prop H.9) hold at all q; the split identity =
  square-count law is certified k ≤ 10 for all q ≤ 4 and proved at q = 1
  (Theorem H.5, new closed law P¹ = C(n,k)²(k!−1)); exact top coefficients
  [n^{2k}] derived for all q (Theorem H.11); and the cap is identified as
  the LIS parameter: N_k(q) = # permutations with LIS ≤ q (Gessel family,
  Theorem H.12), Regev exponent (q²−1)/2, v⁴(30) = 161.3249 matching Note
  G digit-exactly. Top-corner law P^q_{qn}(n) + 1 = # all-margins-q
  matrices (Observation H.10; proved at q = 1 as n! − 1). Battery H.0–H.8:
  **172 checks, all PASS**, runtime 191 s. Open items J.1–J.4 registered in
  the roadmap.
- **Closed forms at the margins, exact boundary degeneracies, and universal
  constants (Note I, Phase 7):** the top corner at q = 2 is now EXACT:
  P²(2n,n) = M(n,2) − 1 with M(n,2) = # 2-regular bipartite multigraphs =
  A001499 given by the cycle-decomposition closed form (c_j = j!(j−1)!/2
  Hamiltonian cycles; proved; three routes agree + engine identity n ≤ 12) —
  the first non-birth closed law for P; the cap-boundary law proves
  ledger_4(4n,n) = 1 and ledger_4(4n−1,n) = n² (forced columns), re-deriving
  audit SKIPs ledger(139,35) = 35² and ledger(160,40) = 1 structurally (plus
  ledger(146,40) via the rectangle form); the Gessel/Regev constants are
  identified in closed form C_q = (2π)^−(q−1)/2·2^−(q²−1)/2·q^(q²/2)·∏_{j<q} j!
  (C_2 = 1/√π digit-exact to 16 digits; C_3 = 3^{9/2}/(16π) agrees with this
  session's fully independent exact-rational extrapolation ladder to 11 digits;
  C_4 = 275.845814… vs extrapolated 275.845518 — 0.0001 %, with the window
  spread converging monotonically; C_5 = 972294.5631…, C_6 = 1.91349947×10¹¹
  registered as predictions); the joint census tightens the liminf window to
  1 ≤ liminf D_k(k) ≤ 1.420 (k = 19) with the frozen-profile cosine sinking —
  the diagonal regime stays genuinely joint; the SKIP ledger is now accountable and
  closed at this pass: 4 claim lines upgraded and cross-verified digit-for-digit
  against the document's printed values — ledger(139,35) = 1225 = 35²,
  ledger(146,40) = 890…520, ledger(160,40) = 1, and live(20,35) = 27…920, the
  document's 44-digit printed value matched exactly by the Route-B engine —
  leaving 38 honest SKIPs, each with a measured engine ceiling and a named
  algorithmic unlock (fast contingency DP; f_syt suffix counts).
- **The norm formula unlocks the exponential wall (Note J, Phase 8):** the
  engine's contingency count is exactly the Hall Gram matrix,
  $T(\mu,\nu) = \langle h_\mu, h_\nu\rangle$, so the live census is the
  norm of a coefficient: $\mathrm{live}_q(k,n) = \lVert[t^k](1+h_1t+\cdots+h_qt^q)^n\rVert^2$.
  The resulting integer DP (Route C) computes deep rungs that cost hours on
  the contingency DP in seconds (live(20,35): 0.12 s vs 1780 s), certifies
  26/30 deep document rungs digit-exactly, and SUPERSEDES four of them — the
  document's CRT-reconstructed live(62..65,35) are off by 0.5–1.5 %, caught
  by exact arithmetic, with corrected values recorded; the document's own
  digit-count parabola survives. The J.2 diagonal reaches k = 40 (engine
  window), tightening the registered liminf window on $D_k(k)$.
- **The deep sextet falls (Note K, Phase 9):** Theorem K.1 shows the Route C
  key space is polynomial in $k$ (parts $\le q$), voiding the Phase-8
  "hundreds of GB" verdict (a ~37,000× state-pool overcount) and delivering
  all six deep-anomaly rungs exactly in ~90 s per column — three confirmed
  digit-for-digit, three first-ever exact values, the end rungs identified
  with the full-box norm $T((4^n),(4^n))$ (Prop K.2), the crest/margin
  structure of the deep columns pinned exactly, and the audit's 42-SKIP
  ledger fully discharged. No documented census claim remains beyond the
  engine's exact reach.
- **The outer leaf closes (Note L, Phase 10):** the whole verification stack
  is re-certified end-to-end in one machine (Thm L.1–L.5; the transport
  tables agree across THREE independent engines — p-basis runner,
  contingency DP, Sum-K-K — 27,436 digit-exact equalities), the document's
  typographic constants are parsed live and matched digit-for-digit at
  ~99% of the 200+ constant claims, and the six mismatches are registered
  as document-side corruptions (digit-drops and a ×10), each diagnosed at
  digit level with the engine value double-certified. The full column
  sweep n = 8..40 delivers every rung of every column exactly — the cap-4
  census is, from this phase on, completely machine data at every
  documented rung.
- **The map grows to sixteen paths (Note M, Phase 11):** eight new,
  independently-gated routes to the variational Hodge conjecture (CM
  islands, definable control, function-field one-fiber arithmetic,
  smoothability, Mumford–Tate/motive, family frozen constants, the
  machine-tested first-order family gate, Kuga–Satake lifting), each with
  its unconditionally provable half proved in full and its gate named.
  The P15 model battery (66 checks, all PASS) proves the model's family
  laws (Z/B/slot) and yields the phase's calibrated moral: in the model,
  first-order families transport the inductive VHC pattern without
  exception, while a Tate-dropped direction manifests as an exact
  full-band slot phenomenon — so in the model, any transport failure
  must be of deformation order ≥ 2 (Cor M.14).
