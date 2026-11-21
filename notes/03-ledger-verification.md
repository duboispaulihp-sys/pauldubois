# Note D — Digit-Exact Audit of the Iterative Ledger (Appendix D.5) and Pre-Registration for the Next Columns

*Working note, phase 2. Companion to Note A (F-closure extensions) and Note B
(tropical program). All numbers in this note are exact integers produced by
the independently built engine in `ledger/ledger_engine.py` under pure-Python
arithmetic (`int`, `fractions.Fraction`); no floating point is used anywhere,
and every displayed identity below was re-asserted programmatically.*

---

## 0. What was audited, and the headline result

The uploaded document ("The Harmless Subgroup and the F-Closure Lemma", Paul
Dubois, working session) carries an iterative numerical program in Appendix
D.5: four self-continuing "strands" that maintain a *certified ledger* for the
motive powers $h(A)^{\boxtimes n}$ of an abelian variety $A$, organized column
by column ($n = $ power, $k = $ cohomological degree half). Each strand pass
prints exact integers and claims laws connecting them.

We rebuilt the combinatorial scaffold from the document's definitions, built an
independent exact engine with **three internally arbitrated routes**, and
audited **every printed claim the engine can reach**.

**Headline: 409 PASS, 0 FAIL, 42 SKIP.** Every claim of the document that lies
within the engine's provable reach — binomial phases, birth laws, first and
higher syzygy decompositions through the *tenth power*, the deep $n = 35$
ledger sweep $k = 5..70$, the middle rung, the column total, and the mirror
seatings — agrees **digit-exactly** with the independent engine. The 42 SKIPs
are enumerated honestly in §7 (claims whose verification would require
machinery beyond the pure-Python reach, not disagreements). No digit slip, no
broken identity, no overstated law was found inside the audited window — the
only irregularities located are three extraction artifacts on our side (§6)
and two slips the document itself already found and corrected on its own pages
(so our audit confirms the *corrected* values).

---

## 1. The framework, reconstructed

### 1.1 The three quantities

For $n, k \ge 1$ the document tracks:

- **live**$(k,n)$ = the number of $n \times n$ matrices of nonnegative
  integers of total sum $k$ with every row sum and column sum $\le 4$.
- **ledger**$(k,n)$ = the "diagonal" part, computed by the hook-square closed
  form below.
- $P_k(n)$ = live$(k,n)$ − ledger$(k,n)$, the "syzygy" count: the *new*
  classes born at degree $k$ beyond the ledger's accounting.

For $h(A)^{\boxtimes n}$, $n$ is the external power, $2k$ the cohomological
degree, and the cap 4 is $\dim A = 4$ (so $4n$ is the top degree and column
$k$ runs $k = 1, \dots, 4n-1$ with mirror $k \leftrightarrow 4n-k$).

### 1.2 The hook-square (ledger) closed form — Proposition

$$\mathrm{ledger}(k,n) \;=\; \sum_{\mu \vdash k,\ \mu_1 \le 4} s_\mu(1^n)^2,$$

with $s_\mu(1^n)$ computed by the hook–content formula
$\prod_{(i,j)\in\mu} (n - i + j)/h(i,j)$ (exact rationals; every such value is
an integer, and the product is checked integral).

*Scaffold (RSK).* Weight-graded Cauchy:
$\sum_{\mu} s_\mu(x)\,$$\,s_\mu(y)\,t^{|\mu|} = \prod_{i,j}(1 - t x_i y_j)^{-1}$.
At $x = y = (1,\dots,1)$ ($n$ each) with the restriction $\mu_1 \le 4$
(dual word: rows/cols $\le 4$ is the same cap on both sides of the RSK pair),
the diagonal contribution is exactly the sum above; in particular

$$\sum_{\mu \vdash k,\ \text{unrestricted}} s_\mu(1^n)^2 \;=\; \binom{n^2 - 1 + k}{k},$$

which is the **binomial phase**: for $k \le 4$ the caps $\le 4$ cannot bind
(any matrix entry is $\le k \le 4$), so

$$\mathrm{live}(k,n) = \binom{n^2-1+k}{k}, \qquad k \le 4.$$

*Proof status: proved (closed form + triviality of the cap at $k\le4$), and
confirmed by the engine independently at all calibrated points.* The engine
recomputes ledger$(k,n)$ directly from the sum — no reference to the
document's own arithmetic.

### 1.3 The $b$-law (Route B) — Proposition

For each partition $\sigma \vdash k$ define

$$b_{k,\sigma}(n) \;=\; \sum_{\mu \vdash k,\ \mu_1 \le 4} C_\mu(n)\, K_{\sigma\mu},
\qquad C_\mu(n) = \frac{n!}{(n - \ell(\mu))! \prod_j m_j!},$$

where $K_{\sigma\mu}$ is the Kostka number (SSYT of shape $\sigma$, content
$\mu$) and $m_j$ counts the parts of size $j$. Then

$$\mathrm{live}(k,n) = \sum_{\sigma \vdash k} b_{k,\sigma}(n)^2, \qquad
P_k(n) = \sum_{\sigma_1 \ge 5} b_{k,\sigma}(n)^2 .$$

*Scaffold.* Semistandard tableaux of shape $\sigma$ on the letter content
$\mu$: choose *which* of the $n$ letters realize the multiset $\mu$
($C_\mu(n)$ ways), then fill ($K_{\sigma\mu}$ ways); summing over contents and
squaring via the column-strict Cauchy identity gives the two formulas. The
**square-count law** is then immediate: $P_k$ is a sum of exactly

$$p(k) - p_4(k)$$

squares, one per partition $\sigma \vdash k$ with $\sigma_1 \ge 5$ (the shapes
whose *letter spectrum* leaves the 4-box — these are precisely where the
ledger's diagonal accounting ends). Note the pleasing self-consistency: the
ledger side is recovered as $\sum_{\sigma_1 \le 4} b_{k,\sigma}(n)^2$ =
ledger$(k,n)$, which is the hook-square identity in its $b$-form; the engine
verifies this equality directly (it is the shape-split test in
`verify_claims.py`, all green).

*Proof status: proved; engine Route B computes live by the $\sum b^2$ law.*
Route A computes live independently as

$$\mathrm{live}(k,n) = \sum_{\mu,\nu \vdash k,\ \mu_1,\nu_1 \le 4}
C_\mu(n)\, C_\nu(n)\, T(\mu,\nu),$$

where $T(\mu,\nu)$ is a row-by-row transfer-matrix count of $n \times n$
matrices with prescribed row margins $\nu_i$ and column-usage margins $\mu_j$
(a memoized DP on remaining column margins; entries are automatically $\le 4$
when margins are). This is the document's $T$-matrix identity; the engine
confirms Route A ≡ Route B for all $k \le 9$, $n \le 40$, and both against
**direct brute-force enumeration** (row-composition pools, exact) for
$n = 2, 3, 4$ — that brute-force arbitration is what licenses every later
digit.

### 1.4 The birth law at $k = 5$ — Proposition (complete proof)

$$b_{k,(5)}(n) = \binom{n+4}{5} - n \quad\text{for all } k \ge 5 \text{ with } k=5; \qquad
P_5(n) = \Big(\binom{n+4}{5} - n\Big)^2 .$$

*Proof.* Partitions of $5$ with $\mu_1 \le 4$ are
$(4,1), (3,2), (3,1,1), (2,2,1), (2,1,1,1), (1^5)$ — every multiset of size $5$
*except* $(5)$ (a part $5$ would leave the 4-cap). Since $K_{(5),\mu} = 1$ for
every content $\mu$ (a single weakly increasing row is forced by its
content), and starring: every multiset $\mu$ of size $5$ from $n$ letter types
can be chosen in $\binom{n+5-1}{5} = \binom{n+4}{5}$ ways (stars and bars),
while $\mu = (5)$ contributes $C_{(5)}(n) = n$,
$$b_{(5)}(n) = \binom{n+4}{5} - n. \qquad\blacksquare$$

The document's one-row generalization (the "hockey-stick" inclusion–exclusion,
letters born at $k = 5j$),

$$b_{(k)}(n) = \sum_{j \ge 0} (-1)^j \binom{n}{j}\binom{n + k - 5j - 1}{k - 5j},$$

and its $k = 9, 10, 11$ refinements with the pair term
$\binom{n}{2}$ (resp. $n\binom{n}{2}$) were **independently re-verified
digit-exactly by the engine** for the printed ranges ($n = 4..24$, $4..25$,
$4..26$) — recorded in the report; the engine's `b_one_row` implements the
IE form and `calibrate.py` checks it against Route B for $n \in \{6, 17, 35\}$
and all $k \le 25$, all PASS.

### 1.5 The mirror (box-duality) law — verified at depth

ledger$(k,n) = $ ledger$(4n-k, n)$. The engine confirms this identity
digit-exactly at every small $n$ tested, across the full lower half
$k = 1..20 \leftrightarrow 139..120$ at $n = 35$, and in the new columns
$n \in \{36, 38, 40\}$ ($k = 5, 6, 7$). The document seats the upper half
$k = 71..139$ of the 35th column by this law; our audit confirms the seating
is consistent (the middle rung ledger$(70,35)$ — 73 digits — is reproduced by
the engine independently, and is verified to be the column's largest rung,
as claimed).

---

## 2. The deep power-chain audits (headline verifications)

The document's most impressive printed artifacts are the fully expanded
syzygy powers — hundreds of squares spelled out digit by digit. The engine
reaches all of them via Route B ($b_\sigma$ for all shapes of $k$, size-20
Kostka DPs included) and verifies each at the level of **individual squares**:

| Claim (md line) | Squares printed | Square-count law | Base multiset = $\{b_\sigma\}$ | $\sum$ squares $= P_k(n)$ | Printed total $= P_k(n)$ |
|---|---|---|---|---|---|
| $P_9(24)$, L1266 | 12 | $30-18=12$ | IDENTICAL | PASS | PASS ($9{,}163{,}574{,}786{,}161{,}952{,}640$) |
| $P_{10}(25)$, L1278 | 19 | $42-23=19$ | IDENTICAL | PASS | PASS ($1{,}572{,}793{,}486{,}090{,}905{,}341{,}100$) |
| $P_{11}(26)$, L1290 | 29 | $56-27=29$ | IDENTICAL | PASS | PASS ($257{,}337{,}843{,}029{,}527{,}585{,}613{,}600$) |
| $P_{20}(35)$, L1414 | 519 | $627-108=519$ | IDENTICAL | PASS | PASS (via $=$ live − ledger, below) |

(The line-1290 entry also prints $P_6(26)$ and $P_7(26)$ beside $P_{11}$; the
auditor chunk-parses each claim, and those two were verified separately —
both PASS.)

**The $P_{20}(35)$ descent.** Line 1414 closes with the identity
$P_{20}(35) = \mathrm{live}(20,35) - \mathrm{ledger}(20,35)$ spelled out as a
~63-digit minus a 44-digit number. The engine verifies *both* operands
digit-exactly — the ledger side by the hook-square closed form directly, and
the live side by Route B as $\sum_{\sigma \vdash 20} b_\sigma(35)^2$ over all
$627$ shapes (an independent derivation of a number the document itself
presents as out of the hand-checks' reach):

- live$(20,35) = 27{,}277{,}245{,}818{,}749{,}123{,}471{,}218{,}465{,}200{,}909{,}528{,}830{,}189{,}120$ — **engine = printed**;
- ledger$(20,35) = 42{,}185{,}191{,}927{,}758{,}873{,}531{,}355{,}693{,}813{,}215{,}446{,}041{,}104$ — **engine = printed**;
- and live − ledger $= \sum_{\sigma_1 \ge 5} b_\sigma(35)^2 = $ the full 519-square printed chain, to the digit.

**The column total.** Line 2517 prints
$\mathrm{total}_{35} = 2\sum_{k=1}^{69} \mathrm{ledger}(k,35) + \mathrm{ledger}(70,35) = 43{,}703{,}277{,}415{,}946{,}102{,}027{,}762{,}262{,}336{,}352{,}020{,}449{,}841{,}884{,}468{,}763{,}234{,}069{,}294{,}147{,}723{,}281{,}069{,}374$
(74 digits). The engine sums the 69 hook-square rungs itself and **confirms
the total digit-exactly** (`total_35` PASS), which transitively re-verifies
every rung $k = 1..69$ of the 35th column in one stroke, on top of the
run-by-run misc-claim checks.

---

## 3. Audit census (the full battery)

Per-category results from `ledger/verification_report.txt`
(`409 PASS, 0 FAIL, 42 SKIP`):

| Block | Checks | Result |
|---|---|---|
| Binomial phase: printed quads $=\binom{n^2-1+k}{k}$, dedup to ~27 columns, $n = 10..36$ | printed $=$ closed form $=$ engine | **PASS (all)** |
| Birth law: $P_5 = (\binom{n+4}{5}-n)^2$ + live/ledger sides | 9 claims, $n = 12..40$ | **PASS (all)** |
| $P_6$ (27 claims, $n = 10..35$, incl. 2-square forms) | totals, squares, shape split | **PASS (all)** |
| $P_7$ (17 claims, four-square forms from $n = 17$) | totals, squares, shape split | **PASS (all)** |
| Misc live/ledger printed rungs | $k \le 9$ live, $k \le 90$ ledger, $n \le 40$ | **PASS (all in reach)** |
| Subtraction identities live − ledger $= A - B$ ($k=5,20$ at $n=35$) | both sides | **PASS** |
| Column total$_{35}$ | 69 rungs + middle | **PASS** |
| Mirror law | small $n$; $n=35$, $k = 1..20 \leftrightarrow 139..120$ | **PASS (all)** |
| Correction law (the document's IE formula) vs engine Route A | grid $n \in \{2..35\}$, $k = 5..8$ | **PASS (44/44)** |
| Calibration of the engine itself (`calibrate.py`) | Kostka GT vs direct SSYT 345/345; Routes A/B vs brute force; binomial/birth/split/one-row/T-identity | **PASS (all)** |
| Deep power chains ($P_9$–$P_{11}$, $P_{20}$) | §2 table | **PASS (all)** |
| SKIP register | live $k > 9$ upper part of strands (e.g. the deep "$G$-law" ceiling constants, crest $\approx 10^{155.47}$), columns $n \ge 41$, density certifications | 42, enumerated |

---

## 4. Pre-registration: the columns $n = 36..40$

The document certifies through $n = 35$ (with one advance print of the $n=36$
binomial row). The engine produces the complete next columns in advance. All
values below are engine-computed, with every asserted identity checked inside
the run (`pre_register.py`; full text `pre_register.txt`).

**Discharge note (Phase 10):** the registered $n = 36..40$ columns are now
fully swept — complete DP spectra for all five columns (every rung $k =
0..4n$, exact), Thm L.2, the $j=0$ full-box law, bands, Runge-D spots and
peak battery all PASS (`outer_leaf.py`, transcript lines "== end of column
n=36..40 =="); see Note L §3. Nothing conditional remains from this
registration.

**Binomial phase** (confirmed live by Route A as well):

| $n$ | live(1) | live(2) | live(3) | live(4) |
|---|---|---|---|---|
| 36 | 1,296 | 840,456 | 363,637,296 | 118,091,211,876 |
| 37 | 1,369 | 937,765 | 428,558,605 | 146,995,601,515 |
| 38 | 1,444 | 1,043,290 | 502,865,780 | 181,911,695,915 |
| 39 | 1,521 | 1,157,481 | 587,614,521 | 223,881,132,501 |
| 40 | 1,600 | 1,280,800 | 683,947,200 | 274,091,840,400 |

(The $n = 36$ row matches the document's stray advance print exactly:
$1296, 840{,}456, 363{,}637{,}296, 118{,}091{,}211{,}876 = \binom{1295+k}{k}$.)

**Birth squares** $P_5(n) = (\binom{n+4}{5} - n)^2$: $b_{(5)}(n) =$
657,972 / 749,361 / 850,630 / 962,559 / 1,085,968 for $n = 36..40$; squares
$432{,}927{,}152{,}784$, $561{,}541{,}908{,}321$, $723{,}571{,}396{,}900$,
$926{,}519{,}828{,}481$, $1{,}179{,}326{,}497{,}024$.

**Syzygy squares** (square-count law; shape-split identity asserted for each):

- $P_6(36) = 4{,}495{,}092^2 + 19{,}190{,}640^2 = 388{,}486{,}515{,}698{,}064$
- $P_6(40) = 8{,}143{,}460^2 + 35{,}293{,}700^2 = 1{,}311{,}961{,}200{,}461{,}600$
- $P_7(36) = 26{,}954{,}352^2 + 134{,}846{,}280^2 + 276{,}340{,}680^2 + 279{,}631{,}980^2 = 173{,}468{,}271{,}983{,}161{,}104$
- $P_8(40) = 313{,}998{,}295^2 + 1{,}825{,}250{,}505^2 + 4{,}536{,}714{,}000^2 + 4{,}525{,}431{,}495^2 + 5{,}787{,}996{,}240^2 + 12{,}261{,}791{,}360^2 + 6{,}202{,}776{,}385^2 = 266{,}818{,}301{,}181{,}738{,}052{,}500$

(both four- and seven-square forms for $P_7(37..40)$, $P_8(37..39)$ are in the
pre-register file, each asserted equal to live − ledger and to Route A).

**Ledger rungs** ledger$(k,n)$, $k = 5..9$ (hook-square, asserted mirror-checked):

| $n$ | ledger(5) | ledger(6) | ledger(9) |
|---|---|---|---|
| 36 | 30,270,740,559,696 | 6,269,042,357,539,416 | 17,825,932,959,029,067,139,696 |
| 40 | 86,749,249,024,256 | 22,208,819,811,214,400 | 120,387,356,251,662,997,411,200 |

(full $k = 5..9$ table incl. $n = 37..39$ in `pre_register.txt`.) Mirror
seatings ledger$(k,n) =$ ledger$(4n-k,n)$ spot-checked at $n \in \{36,38,40\}$,
$k = 5,6,7$: ALL PASS.

**Falsifiability.** These are genuine pre-registrations: if the document's
next strand pass prints anything else in these cells, the discrepancy is now
decidable by two independent code paths plus brute force — the same arbitration
standard that validated this audit.

---

## 5. Newton forms of the syzygy polynomials

Because $C_\mu(n)$ is (up to the constant Kostka factor) a falling factorial
of degree $\ell(\mu)$, $b_{k,\sigma}(n)$ is a polynomial in $n$ of degree
$\le k$ and $P_k(n)$ a polynomial of degree $\le 2k$. `newton_fit.py` derives
the **exact Newton forward forms** (coefficients = $\Delta^j P(1)/j!$, exact
rationals) and certifies them by evaluation at ~25 fresh points each
(agreement of two degree-$d$ polynomials at $d+1$ fresh points is equality):

- $P_6$: degree 12; coefficients from $18$ (i.e. $P_6'(1)$-slot) through
  $\tfrac{13}{259200}$ at $j = 12$; certified on $n = 14..40$; e.g.
  $P_6(17) = 78{,}991{,}075{,}280$ — **exactly the value the document prints**
  for its seventeenth column.
- $P_7$: degree 14; certified on $n = 16..40$; $P_7(35) = 118{,}377{,}571{,}195{,}388{,}825$.
- $P_8$: degree 16; certified on $n = 18..40$; $P_8(35) = 33{,}128{,}194{,}427{,}374{,}451{,}475$.

This upgrades the document's run-by-run prints to *closed laws* for the first
three syzygy columns: any future printed value in these cells must be the
Newton polynomial's value, no iteration required.

---

## 6. Irregularities found (both sides)

1. **Three extraction artifacts (our side, fixed).** The extractor's greedy
   number capture, applied to lines of the form
   "$\mathrm{live}(k,n) - \mathrm{ledger}(k,n) = A - B$" and to the
   "$\mathrm{total}_{35} = 2\sum \dots + \mathrm{ledger}(70,35) = T$" line,
   initially attributed the wrong operand ($A$, resp. $T$) to the ledger
   label. After context-aware parsing, the document's actual operands match
   the engine. No document error is involved.
2. **Document self-corrections, confirmed.** The document notes two of its own
   earlier slips (a pre-registered $n = 25$ ledger print "corrected this round
   by three independent routes"; a fifth-rung figure that "mixed the birth
   law's syzygy value into the fifth rung"). Our audit confirms the
   *corrected* values are right (e.g. the final ledger$(5,35) =
   22{,}844{,}591{,}558{,}446$, and the birth subtraction
   $23{,}176{,}047{,}379{,}730 - 22{,}844{,}591{,}558{,}446 = 575{,}722^2$,
   both engine-exact).
3. **A "live(5,15) ≈ 5.022e9" floating claim** — engine: exactly
   $5{,}021{,}988{,}930$; consistent.

*No substantive mismatch between document and engine was found anywhere in
reach.*

---

## 7. Out-of-scope register (honest non-coverage, 42 SKIPs)

- **live$(k,n)$ for $k > 9$ in general position**: Route A's $T$-matrix DP
  (needed for an *independent* second route) becomes prohibitive beyond size
  ~10; Route B (used for $P_{20}(35)$) covers the specific audited instances,
  but the strand-3 "G-law ceiling" constants —
  $G(129) = T((4^{32},1),(4^{32},1)) - 1$-type objects, crest $\approx
  10^{155.47}$ — and the histogram-style density certifications were not
  reproduced.
- **Columns $n \ge 41$**: reachable per cell but not swept in bulk.
- **The census $v_n$ strand** and the intermediate Hodge-theoretic
  interpretation (which numbers are actual $\mathrm{CH}$-group dimensions vs
  upper-bookkeeping) — framework reconstruction only; see Note A §6 for the
  census calculus that such a ledger would feed into.
- **Beyond-rung obligations**: the document's strands 2–4 (density march,
  ceiling constants) are tracked but not recomputed; their claims rest on the
  same Kostka/hook-square scaffold verified here, but each printed constant
  remains un-audited unless it falls within the table of §3.

## 8. Files

- `ledger/ledger_engine.py` — the exact engine (Route A $T$-matrix, Route B
  Kostka/$b$-law, brute force, hook-square ledger, laws).
- `ledger/calibrate.py` — the internal arbitration battery (all PASS).
- `ledger/extract_claims.py` — claim extraction from the uploaded md (63
  binomial, 9 birth, 27 $P_6$, 17 $P_7$, 114 misc, subtraction and total
  claims).
- `ledger/verify_claims.py` + `verification_report.txt` — the 409/0/42 audit.
- `ledger/audit_powers.py` + `powers_audit.txt` — the deep power-chain audits
  (§2), square by square.
- `ledger/pre_register.py` + `pre_register.txt` — the $n = 36..40$
  pre-registration (§4).
- `ledger/newton_fit.py` + `newton_fit.txt` — the Newton-form laws (§5).
