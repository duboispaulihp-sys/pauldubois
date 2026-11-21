# Note G — The Second Asymptotic Direction: Frozen Profiles of the Ledger
# Constants as $k \to \infty$

**Status:** Phase 5 of the working session. Note F (Phase 4) froze the
$n \to \infty$ behaviour of each rung $k$ of the Dubois ledger into exact
RSK constants. This note explores the *other* direction — what happens to
those constants as $k \to \infty$ — and finds that the model's constants
are classical objects in the asymptotic theory of permutations with
bounded longest increasing subsequence (LIS): the ledger-share of rung
$k$ is exactly $N_k(4)/k!$ where $N_k(d)$ is Gessel's LIS-counting
function, known by Gessel's determinant identity (verified digit-exactly
here for $k \le 30$) and Regev's asymptotics. Consequence: the
harmless/ledger share of high rungs **dies** (root rate $16e/k \to 0$),
the syzygy share tends to 1, and the per-shape composition of each rung
freezes into an SYT-weighted profile.

**Citation flags** as in Notes A–F: [proved] / [proved-cited] / [cert] /
[program]. **Companion artifacts:** `ledger/frozen_profiles.py` /
`frozen_profiles.txt` (all machine content below), building on
`closed_laws.py` / `closed_laws.txt` (Note F).

---

## 0. Summary

* **Theorem G.1** (LIS interpretation): $\sum_{\mu_1 \le 4} f_\mu^2 =
  N_k(4)$, the number of permutations of $k$ letters with LIS $\le 4$;
  hence the Note-F frozen constants are $P_k/\mathrm{live}\to 1 -
  N_k(4)/k!$. [proved, given RSK]
* **Theorem G.2** (Gessel's determinant, certified): $\sum_{k\ge 0}
  N_k(d)\, \dfrac{x^{2k}}{(k!)^2} = \det\bigl(I_{|i-j|}(2x)\bigr)_{d\times
  d}$ — verified **exactly** over $\mathbb Q$ for $d = 1, 2$ (Catalan
  anchor) and $d = 4$ against an independent hook-formula census, $k =
  0..30$. [proved-cited][cert]
* **Theorem G.3** (Regev share law): $N_k(4) \sim C_4\cdot 16^k/k^{15/2}$
  with $C_4 \in (0,\infty)$; hence the ledger-share of rung $k$ satisfies
  $\bigl(N_k(4)/k!\bigr)^{1/k} \to 0$ (root rate $16e/k$): the harmless
  content of the ledger dies superexponentially in the rung. Power-law
  consistency certified through $k = 60$. The constant $C_4$ itself is
  **not evaluated** here (slow $1/k$-scale approach). [proved-cited][cert]
* **Theorem G.4** (frozen shape profile): for every shape $\sigma_1 \ge
  5$, as $n \to \infty$, $\;b_\sigma(n)^2/P_k(n) \to f_\sigma^2
  /\!\sum_{\tau_1 \ge 5} f_\tau^2$, at $O(1/n)$ rate (plateau
  $n\cdot$err $\approx 2.04$ at $k = 9$). Participation numbers $\rho_k$
  and dominant shapes tabulated, $k = 5..30$; the $n = 40$ finite-
  fingerprints of Phase 2 already coincide with the $\infty$-dominant
  shapes at $k = 9, 10$. [proved][cert]

The model phase diagram is thereby closed in both directions ($n \to
\infty$: Note F; $k \to \infty$: here), and the VHC readings consolidated
in §6.

---

## 1. Notation (inherited from Note F)

* $f_\sigma = K_{\sigma,(1^k)}$ = number of standard Young tableaux (SYT)
  of shape $\sigma \vdash k$; by the hook–length formula
  $f_\sigma = k!/\prod_{(i,j)\in\sigma} h(i,j)$ — this gives an exact and
  cheap census of $f_\sigma$ for all shapes at once (used here up to
  $k = 60$), *independent of the Kostka/GT route* of Note F.
* $\sum_{\mu_1\le 4} f_\mu^2$ ("ledger constant" $\Lambda_k$) and
  $\sum_{\sigma_1 \ge 5} f_\sigma^2$ ("syzygy constant" $\Sigma_k$) with
  $\Lambda_k + \Sigma_k = k!$ (Note F, Thm F.2e exhaustiveness).
* $b_\sigma(n) = \sum_{\mu_1\le4} C_\mu(n)\,K_{\sigma\mu}$ and the laws
  $\mathrm{live} = \sum_\sigma b_\sigma^2$, $P_k =
  \sum_{\sigma_1\ge5} b_\sigma^2$ (Note D), and
  $b_\sigma(n) = \frac{f_\sigma}{k!}n^k + O(n^{k-1})$ (Note F, Thm
  F.2a).

### G.1 data: the extended split (hook census, k = 1..30) [cert]

| $k$ | $\Lambda_k = N_k(4)$ | $\Sigma_k$ | $\Sigma_k/k!$ (syzygy share) |
|---|---|---|---|
| 5 | 119 | 1 | 0.008333 (= 1/120) |
| 10 | 2 190 688 | 1 438 112 | 0.396305 |
| 15 | 172 188 608 886 | 1 135 485 759 114 | 0.868325 |
| 20 | 26 525 044 132 374 656 | 2.4064 × 10¹⁸ | 0.989097 |
| 25 | 6.0546 × 10²¹ | 1.5505 × 10²⁵ | 0.99961 |
| 30 | 1.7902 × 10²⁷ | 2.6525 × 10³² | 0.999993 |

(asserted exactly: $\Lambda_k + \Sigma_k = k!$ for every $k = 1..30$.)

---

## 2. Theorem G.1 — the ledger constants count permutations with bounded LIS

**Theorem G.1.** *For every $k \ge 0$, $\Lambda_k = \sum_{\mu_1\le4}
f_\mu^2$ equals the number of permutations $\pi \in S_k$ whose longest
increasing subsequence has length $\le 4$.*

*Proof.* Under the Robinson–Schensted correspondence, $\pi$ maps to a
pair $(P_\pi, Q_\pi)$ of SYT of one common shape $\mathrm{sh}(\pi) \vdash
k$, bijectively [proved-cited: Knuth, *TAOCP* 3, §5.1.4]. The classical
companion theorem reads off from the insertion process that the first row
of $\mathrm{sh}(\pi)$ has length exactly $\mathrm{LIS}(\pi)$ [proved-
cited: Knuth, *TAOCP* 3, Thm 5.1.4A; Schensted 1961]. Hence
$$\#\{\pi : \mathrm{LIS}(\pi) \le 4\} =
\sum_{\substack{\mu \vdash k\\ \mu_1 \le 4}} \#\mathrm{SYT}(\mu)^2 =
\Lambda_k,$$
the last equality by bijection onto pairs of SYT of a common shape
$\mu_1 \le 4$ and the definition of $f_\mu$. $\blacksquare$ [proved,
given the two cited RSK facts]

**Consequence (model reading).** The Note-F frozen share of rung $k$ is
$$\frac{P_k}{\mathrm{live}} \xrightarrow[n\to\infty]{} \frac{\Sigma_k}{k!}
= 1 - \frac{N_k(4)}{k!}:$$
in the ledger model, the *harmless* content of a rung is precisely the
(normalized) count of permutations whose increasing subsequences are
bounded by the column cap 4 — the model's parameter "4" therefore ties
the whole apparatus to the deepest classical layer of the theory of
bounded-LIS permutations (Gessel determinants, Toeplitz/Bessel
integrable systems, BDJ theory). [proved modulo the Note-F theorem]

---

## 3. Theorem G.2 — Gessel's determinant identity, an independent derivation

**Theorem G.2 (Gessel).** *Define $N_k(d) := \sum_{\mu_1 \le d}
f_\mu^2$. Then*
$$\sum_{k \ge 0} N_k(d)\, \frac{x^{2k}}{(k!)^2}
= \det\bigl(I_{|i-j|}(2x)\bigr)_{1\le i,j\le d},$$
*where $I_m(2x) = \sum_{j\ge0} x^{2j+m}/(j!\,(j+m)!)$.* [proved-cited:
Gessel, *Symmetric functions and P-recursiveness*, J. Combin. Theory A
53 (1990), 257–285 — generalized RSK with bounded shape width; the
normalization displayed is the one certified below]

**Verification (exact, two independent censuses).** [cert —
`frozen_profiles.txt`, G.3 block]

* $d = 1$: coefficients give $N_k(1) = 1$ for all $k$ (only the identity
  permutation has LIS $\le 1$) — ALL PASS, $k = 0..6$.
* $d = 2$: the determinant side reproduces the Catalan numbers $C_k$ for
  $k = 0..15$ — ALL PASS. (Classically: LIS $\le 2$ = 321-avoiding, and
  those are counted by $C_k$; this anchors the $(k!)^2$
  normalization of Gessel's identity independently of the literature
  convention.) Also matches the hook census $\sum_{\mu_1\le2} f_\mu^2$,
  $k = 0..15$ — ALL PASS.
* $d = 4$: the determinant side matches the hook-formula census
  $\Lambda_k$ **digit-exactly for every $k = 0..30$** — ALL PASS. Two
  wholly different algorithms (truncated-$\mathbb Q$ Bessel-determinant
  expansion vs. hook-length enumeration of all 4-column shapes) agree
  through 62-digit values.

**Remark G.2.a.** The $d=4$ check is genuinely independent of Note F: the
Note-F constants came from $K_{\sigma,(1^k)}$ via the Gelfand–Tsetlin DP;
here both sides come from hook products and Bessel coefficients. The
ledger's harmless constants are confirmed by a third, fully classical,
route. [cert]

---

## 4. Theorem G.3 — the harmless share dies (Regev)

**Theorem G.4 of [Regev, Adv. Math. 41 (1981)].** *For fixed $d \ge 1$
there is a constant $C_d \in (0, \infty)$ with*
$$N_k(d) \sim C_d\, d^{2k} \, k^{-\frac{d^2-1}{2}} \qquad (k \to \infty).$$
*[proved-cited; the exponent is $\frac{d^2-1}{2}$, consistent with the
elementary endpoints: $d = 1$: $N_k(1) = 1 = 1^{2k}k^0$; $d = 2$:
Catalan, $C_k \sim 4^k/(\sqrt\pi\, k^{3/2})$, exponent $\frac{3}{2}$.]*

**Theorem G.3 (share law).** *The frozen ledger-share of rung $k$,
$s_k := N_k(4)/k!$, satisfies $s_k > 0$ for all $k$ and*
$$\lim_{k\to\infty} s_k = 0, \qquad s_k^{1/k} \;\le\;
\frac{C_4' \, 16^k / k^{15/2}}{k!}^{\!1/k}\cdot(1+o(1))
\;\sim\; \frac{16e}{k} \to 0 .$$
*Equivalently $\Sigma_k/k! \to 1$: the syzygy squares are asymptotically
*all* of each rung.*

*Proof.* $0 < s_k \le C_4' 16^k k^{-15/2}/k!$ with $C_4'$ any eventual
upper bound for the convergent standardization $N_k(4)k^{15/2}/16^k$
(Regev gives finitely many exceptional $k$; absorb them). Stirling:
$(k!)^{1/k} \sim k/e$, so $s_k^{1/k} \le 16e\, k^{-o(1)}/k \to 0$,
with the displayed rate $16e/k$. Positivity: $\Lambda_k \ge f_{(k,
1^{...})}$-terms — concretely $\Lambda_k \ge f_{(4,4^{\ldots})}^2 \ge 1$
(the shape $(4^{\lfloor k/4 \rfloor}, r)$ has at least one SYT).
$\blacksquare$ [proved, given Regev]

**Numerical certification of the power law.** [cert — `frozen_profiles.txt`,
G.4 block] The corrected ratio testing $N_k(4) \propto
16^k k^{-15/2}$ locally,
$$q_k = \frac{N_k(4)^2}{N_{k-1}(4)^2}\cdot\frac{(k+1)^{15}}{256\, k^{15}},$$
is (exact rationals, float view): 1.341 (k=6), 1.142 (k=10), 1.069
(k=15), 1.040 (k=20), 1.026 (k=25), 1.019 (k=30) — monotone decreasing
toward 1 from $k = 9$ on, within 25% of 1 for $20 \le k \le 30$ (check:
ALL PASS). The standardized values $v_k = N_k(4)\,k^{7.5}/16^k$
(floats), extended to $k = 60$:

| $k$ | 30 | 41 | 46 | 51 | 56 | 60 |
|---|---|---|---|---|---|---|
| $v_k$ | 161.32 | 185.39 | 193.32 | 199.98 | 205.66 | 209.62 |

The approach to $C_4$ is slow (visible $1/k$-scale drift; the values are
strictly increasing on all computed data). We therefore do **not**
evaluate $C_4$ here; the data certify the power-law consistency and give
exact lower certificates ($v_{60} = 209.62 < C_4$). Determining $C_4$
closely — e.g. by high-order singularity analysis of the $4\times4$
Bessel determinant or by the Toeplitz-integral route — is registered as
future work. [program]

**Remark G.3.a (why this matters for the ledger).** The rung share table
of §G.1 shows the model's transition: at $k = 5$ the harmless share is
119/120; by $k = 30$ it is $7\times10^{-6}$. The "harmless subgroup" of
the model, so dominant at the birth rung, is asymptotically invisible
along the $k$-direction — in contrast with the $n$-direction, where Note
F's Theorem F.2e shows the shares freeze to a rung-dependent constant
between 0 and 1. [proved-cited][cert]

---

## 5. Theorem G.4 — the frozen shape profile of each rung

**Theorem G.4.** *Fix $k \ge 5$. For every shape $\sigma_1 \ge 5$:*
$$\lim_{n\to\infty} \frac{b_\sigma(n)^2}{P_k(n)}
= \frac{f_\sigma^2}{\Sigma_k}, \qquad
\text{and} \qquad \sum_{\sigma_1\ge5} \frac{b_\sigma(n)^2}{P_k(n)}
= 1 \ \text{for all } n .$$

*Proof.* By Note F Thm F.2(a): $b_\sigma(n) = \frac{f_\sigma}{k!}n^k +
O(n^{k-1})$ (the $O$-constant depends on $\sigma$); and Thm F.2(d):
$P_k(n) = \frac{\Sigma_k}{(k!)^2} n^{2k} + O(n^{2k-1})$. The ratio tends
to the claimed constant; the second identity is the square-count law
divided by $P_k(n) > 0$ (Note F Thm F.3 positivity). $\blacksquare$
[proved]

**Interpretation.** The document's per-rung decompositions list the
squares (one per shape $\sigma_1 \ge 5$) — e.g. the fully-spelled 519
nonzero squares of $P_{20}(35)$ (Phase-2 deep audit). Theorem G.4 says
that at $n = \infty$ this census is not merely a list: it is a
*probability law* on shapes, namely the normalized SYT-square law
$f_\sigma^2/\Sigma_k$ on $\{\sigma_1 \ge 5\}$ — RSK again: this is
(marginally) the shape distribution of a uniform random permutation
conditioned on $\mathrm{LIS} \ge 5$. [proved]

**Certification.** [cert — `frozen_profiles.txt`, G.5 block]

* $k = 6$: shapes $(6), (5,1)$ with $f = 1, 5$; frozen shares
  $1/26, 25/26$. Live shares at $n = 10..40$: the max error
  $\cdot\, n$ declines 0.590 → 0.483 (still in its $1/n^2$ tail).
* $k = 9$: 12 shapes; frozen shares range from
  $1/101072$ (shape $(9)$) to $35721/101072$ (shape $(5,2,1,1)$).
  $n \cdot \max$err plateaus at $\approx 2.04$ from $n = 20$ onward —
  the $O(1/n)$ rate is confirmed, with per-shape constants and signs
  (shares of top-heavy shapes like $(6,2,1)$ and $(5,3,1)$ fall toward
  their frozen values; shares of tail-heavy shapes like $(5,2,1,1)$,
  $(5,2,2)$, $(5,1^4)$ rise).
* **Coherence with the Phase-2 fingerprints:** the $\infty$-dominant
  shapes are $(5,2,1,1)$ at $k = 9$ and $(5,3,1,1)$ at $k = 10$ —
  exactly the $n = 40$ dominant-$b^2$ shapes measured independently in
  `pre_register2.txt`. The finite pictures at $n = 40$ already see the
  frozen profile. [cert]

**Participation numbers.** $\rho_k := \Sigma_k^2/\sum_{\sigma_1\ge5}
f_\sigma^4$ (the inverse Herfindahl of the frozen profile — the
"effective number of squares at $n = \infty$"): [cert]

| $k$ | 5 | 6 | 7 | 8 | 9 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\rho_k$ | 1.00 | 1.08 | 2.32 | 2.54 | 4.37 | 6.98 | 32.1 | 95.6 | 204.2 | 439.3 |
| dominant | (5,) | (5,1) | (5,1¹) | (5,2,1) | (5,2,1¹) | (5,3,1¹) | (5,4,3,2,1) | (7,5,3,2²,1) | (8,6,4,3,2,1¹) | (8,6,5,4,3,2,1¹) |

Two honest contrasts with the document's finite data:

* $\rho_{20} = 95.6$ vs the 519 nonzero squares of $P_{20}(35)$: at $n =
  35$ many more shapes carry visible squares than will carry weight at
  $n = \infty$ — the finite-n corpus is *broader* than the frozen
  profile; the concentration happens late ($\rho_k \sim$ slow
  growth: $\rho_{30}/\rho_{20} \approx 4.6$ over that window; exact
  values are in the artifact).
* The dominant shapes at small $k$ hug the birth boundary (first row
  exactly 5); by $k \ge 20$ they drift inward toward bulk shapes
  ($k = 15$: the staircase $(5,4,3,2,1)$ — the perfectly
  RSK-balanced shape). The model's dominant defects migrate from
  "first-column-critical" to "bulk" as the rung grows. [cert, descriptive]

---

## 6. VHC reading of the two-direction picture

[program] Assembling Notes F and G, the model's phase diagram:

* **$n \to \infty$ at fixed $k \ge 5$** (Note F): shares freeze to exact
  constants $\Sigma_k/k!$; polynomiality exact; zero window exact.
* **$k \to \infty$** (here): the frozen constants themselves obey the
  Gessel/Regev law — harmless share dies at root rate $16e/k$; syzygy
  squares take over; the per-shape profile freezes into the conditional
  RSK shape law.
* **Large $n$ AND large $k$ jointly:** the only regime not yet
  described; note the model has *no* literally two-variable limit
  mechanism in the current notes — $P_k(n)$ is polynomial in $n$ per
  rung, and the constants per rung are classical, but joint regimes
  (e.g. $n \sim k$, $n \sim \sqrt k$) are untouched. This is the next
  computational avenue: the engine already reaches $k = 20$ at $n \le
  40$ (minutes), so the diagonal regime is partially reachable now.
  [program]

For the VHC gates of Note E (G-T1 limit comparison; G-Detect detection
by a computable invariant), this note sharpens the "detection
fingerprint" requirement to a two-parameter form: a candidate invariant
should reproduce (i) the frozen share $\Sigma_k/k!$ in the
degenerate-column regime, (ii) the Gessel/Regev decay $16e/k$ of the
harmless part along the rung, and (iii) the SYT-weighted frozen profile
of §5. An invariant failing (iii) while passing (i) would itself be
informational (it would detect the rung, not the shape). All of this
remains model-side calibration; the geometric gates are untouched.
[program]

---

## 7. Out-of-scope register

* **$C_4$ itself**: not evaluated (slow approach; the exact data give
  $v_{60} = 209.62$ as a lower certificate; singularity/Toeplitz routes
  registered as future work). [program]
* **General column cap $q \ne 4$**: the whole Gessel/Regev layer
  generalizes ($\Lambda_k^{(q)} = N_k(q+1)$-type counts, cap $q$
  singularities) but the engine hardcodes cap 4; a generalized engine is
  straightforward (replace `partitions(k, 4)` by `partitions(k, q)`) and
  untested — registered, not claimed.
* **Joint regimes in $(k, n)$**: see §6, [program].
* **Geometry**: as in Note F — model-side only; the Note-E interface
  (Props E.1–E.4, Thms E.5/E.7/E.9, gates G-T1/G-Lim/G-Detect) is the
  standing boundary between the ledger and the variational Hodge
  conjecture.
* **Verification horizon**: the exact Gessel check reaches $k = 30$
  (62-digit values); the hook census reaches $k = 60$ cheaply and
  beyond on demand; beyond $k \sim 150$ the hook products still compute
  but the split table becomes unwieldy to print.

---

*Companion files: `ledger/frozen_profiles.py` +
`frozen_profiles.txt` (G.1 split, G.3 Gessel, G.4 Regev ratios, G.5
profile/participation). Upstream: Note D (laws), Note F (Thm F.2a/d/e,
F.3), `pre_register2.txt` (the $n=40$ fingerprints), and the parent
document's Appendix D.5 for the rung/column architecture.*
