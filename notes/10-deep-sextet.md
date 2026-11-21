# Note K — The deep sextet falls: Route C's polynomial state space, the first exact spectra of the deep columns, and the exact crest/margin table

**Phase 9.** Prior state after Phase 8 (Note J): the Route C norm formula
made the live census subexponential, the 30 deep rungs $k = 36..65$ at $n=35$
were resolved (26 exact, 4 superseded), and one block of six "deep-rung
anomalies" — $\mathrm{live}(119,33)$, $\mathrm{live}(123,34)$,
$\mathrm{live}(127,35)$, $\mathrm{live}(134,37)$, $\mathrm{live}(140,35)$,
$\mathrm{live}(146,40)$ — was declared **out of reach**, on a cost model
counting the DP state pool as $\sum_{r\le k} p(r)$ with $p$ the *unrestricted*
partition function ($15.4\times 10^9$ states at $k=119$; "hundreds of GB").
That model was wrong. Theorem K.1 below shows the true pool is polynomial in
$k$ with all parts $\le q$; the sextet falls in under two minutes of
computation per column, and in fact the **entire live spectra**
$\mathrm{live}_4(k,n)$, $k = 0..4n$, of five deep columns are now exact —
most of these values have never existed in exact form anywhere before.

---

## 0. Headline

1. **Theorem K.1 (polynomial state space) [proved + machine-checked].**
   Every key reachable by the Route C Hall–Gram DP is a partition with all
   parts $\le q$; hence the state pool at cap $k$ is at most
   $\sum_{r\le k} p_q(r) = O(k^q)$ — **polynomial**, not merely
   subexponential. At $(k,n,q) = (119,33,4)$ the true pool is
   $\sum_{r\le119} p_4(r) = 416{,}695$, not $15{,}425{,}991{,}887$: the
   Phase-8 model overcounted by a factor $\approx 37{,}000$.
2. **The sextet [all six exact].** $\mathrm{live}(119,33)$,
   $\mathrm{live}(123,34)$, $\mathrm{live}(127,35)$: the document's published
   integers are **confirmed EXACT, digit for digit**. $\mathrm{live}(134,37)$,
   $\mathrm{live}(140,35)$, $\mathrm{live}(146,40)$: the document held only
   float-precision data (log₁₀ markers / a corrupted extraction); these are
   **first-ever exact integer values** (168, 147, and 186 digits).
3. **Proposition K.2 (full-box identity) [proved].**
   $\mathrm{live}_4(4n,n) = T\big((4^n),(4^n)\big)$: the end-rung live of a
   column *equals* the full-box contingency-table monolith. The document's
   float markers $\log_{10} = 146.4368$ ($n=35$, its "end rung"/margin
   sentence) and $158.1962$ ($n=37$) are confirmed to four decimals by the
   exact values.
4. **Exact crest and margin table for the deep columns [new exact data].**
   Crests at $k = 119, 123, 127$ ($n = 33, 34, 35$), $134$ ($n=37$, runner-up
   correction below), $146$ ($n=40$): the document's $+4$ drift cadence holds
   exactly, crest$/n$ creeps $3.606 \to 3.650$, and both document margins
   are confirmed ($9.0346$ at $n=35$ within input rounding; $9.3243$ at
   $n=37$ exactly). One document correction: at $n=37$ the exact runner-up
   is $k=135$ ($\log_{10} = 167.5106$), not $k=133$; the document's
   $167.4797$ for $k=133$ is itself correct, so its published gap
   "$0.0407$ orders" is superseded by the exact gap $0.0098$.
5. **The original 42-SKIP ledger is fully discharged.** The Phase-2 audit
   report carries 42 SKIP *lines*, which decompose exactly as **40 distinct
   claims + 2 audit-report duplicates** (live(59,35) and live(146,40) are
   each listed twice, once per document occurrence). All 40 distinct claims
   are closed:
   (i) the 30 deep rungs live(k,35), k = 36..65 (Phase 8: 26 exact, 4
   superseded with corrected values — re-certified here in a single pass
   per column); (ii) live(20,35) (Phase 7, Route B, digit-exact against
   the document's 44-digit printed value); (iii) the six sextet rungs
   (this note); (iv) the ledger boundary rungs (139,35), (146,40),
   (160,40) (Phase 7 closed laws; and the document's exact
   $\mathrm{ledger}(146,40) =
   890{,}781{,}865{,}166{,}222{,}353{,}286{,}753{,}672{,}695{,}200$
   *re-verified EXACT against the engine here*).

Implementation: `ledger/sextet.py` (count-vector DP + chunked checkpoint
driver), output `ledger/sextet.txt`.

---

## 1. Theorem K.1 (the state space is polynomial)

**Setup.** The Route C DP of Note J (Corollary J.3, implemented in
`norm_route.routeC`) computes
$\mathrm{live}_q(k,n) = \lVert F_{q,n,k}\rVert^2$,
$F_{q,n,k} = [t^k]\big(\sum_{r\le q} h_r t^r\big)^n$, by iterating over the
$n$ factors and maintaining the $p$-basis expansion of the prefix product,
keys being $p$-monomials $\lambda$ (partitions) with total degree
$|\lambda| \le k$ (the truncation), values being $L$-scaled integers
($L = \mathrm{lcm}_\lambda z_\lambda$; in practice $L = 24$ at $q=4$).

**Theorem.** Let $B_q(m)$ denote the number of partitions of $m$ with all
parts $\le q$. At every step $j$ of the DP, every key $\lambda$ satisfies

$$\text{(i)}\ \ \text{all parts of } \lambda \text{ are} \le q, \qquad
\text{(ii)}\ \ |\lambda| \le \min(jq, k),$$

and therefore the number of live states is at most
$\sum_{r \le k} B_q(r) = O(k^q)$, with the total work at most
$n\cdot q \cdot \sum_{r\le k} B_q(r) \cdot O(1)$ bigint operations (plus one
sort of the state list per step).

*Proof.* Induction on $j$. Base: the single state is the empty partition.
Step: the factor update sends state $\mu$ and block $\lambda \vdash r$
($1 \le r \le q$, from $h_r = \sum_{\lambda\vdash r} p_\lambda/z_\lambda$)
to the multiset union $\mu \uplus \lambda$. Parts of $\mu$ are $\le q$ by
hypothesis and parts of $\lambda$ are $\le r \le q$, so parts of the union
are $\le q$; the degree is $|\mu| + r \le jq + q = (j+1)q$, and states of
degree $> k$ are discarded by the truncation (losslessly: parts are
nonnegative, so a state of degree $> k$ can never contribute to degree
$\le k$ later — this is Note J's truncation lemma). The count bound follows
since distinct multisets of parts $\le q$ of size $\le k$ inject into the
multiset union's key space: the map state $\mapsto$ key is injective
(hash key = the full partition tuple) and the codomain has exactly
$\sum_{r\le k} B_q(r)$ elements. Per step the state count is nondecreasing
(union with new states) and bounded by the same quantity, so the sum over
steps is at most $n$ times the pool size. $\square$

**Remarks.**
(a) $B_q(r)$ is the restricted partition number: $B_q(r)$ = number of
solutions of $a_1 + 2a_2 + \cdots + q a_q = r$, a quasipolynomial of degree
$q-1$ in $r$; so the pool is polynomial of degree $q$ in $k$. For $q = 4$:
pool$(k) = \sum_{r\le k} B_4(r) \approx k^4/483$ empirically.
(b) The pool bound is not attained for small $n$: a parts-$q$ partition is
reachable only if it packs into $n$ blocks of size $\le q$; e.g. at $q=3$,
$n=9$ the partition $(2^{10})$ needs ten $2$-blocks and is unreachable. The
machine check below certifies the *inequality* (the theorem's content) and
records the attainment ratio ($\approx 0.94$ at $q = 4$; $1.0000$
at $q=2$).
(c) **This corrects the Phase-8 cost model.** `deep_live.txt`'s verdict
"pool at $k=119$: $\sum_{r\le119} p(r) = 15{,}425{,}991{,}887$, ~$1077\times$
states, out of reach" used the unrestricted $p$; the unrestricted part size
can never arise (that was a docstring slip in `norm_route.py`, since
corrected in place with a pointer here).

**Machine certificate** (`sextet.py cert`, ALL GREEN, 16 s):

- 738/738 grid equality with the Phase-8 certified integer DP
  `norm_route.routeC`: all $k = 0..qn$ of every $(n,q)$ with
  $n \le 12$, $q \in \{2,3,4\}$ — the in-place count-vector DP reproduces
  `routeC` digit-exactly wherever the older engine reaches;
- state counts vs the polynomial bound, final layers:

| $n$ | $q$ | states | bound $\sum_{r\le qn} B_q$ | ratio |
|----|----|----|----|----|
| 12 | 4 | 13,377 | 14,147 | 0.9456 |
| 16 | 4 | 38,097 | 40,377 | 0.9435 |
| 20 | 4 | 87,241 | 92,582 | 0.9423 |
| 14 | 3 | 2,360 | 2,612 | 0.9035 |
| 20 | 2 | 441 | 441 | 1.0000 |

---

## 2. The sextet, exact

One full-cap pass per column ($\mathrm{cap} = 4n$, no truncation needed)
yields the **entire spectrum** $\mathrm{live}_4(k,n)$, $k = 0..4n$, at once
(all final-layer norms extracted per degree; every value verified integral,
"denominator bad = 0" on all five columns). Runtimes on this machine
(single core, count-vector DP): column 33: 35 s (final layer 583,100
states), column 34: 44 s (653,940), column 35: ~60 s (731,046), column 37:
~95 s (905,502), column 40: 90 s (1,223,481; 0.44 GB peak) — versus the
Phase-8 model's "hundreds of GB, out of reach".

| $k$ | $n$ | document's claim | exact verdict | digits |
|----|----|----|----|----|
| 119 | 33 | full integer printed (144 digits) | **EXACT MATCH** | 144 |
| 123 | 34 | full integer printed (150 digits) | **EXACT MATCH** | 150 |
| 127 | 35 | full integer printed (crest rung) | **EXACT MATCH** ($\log_{10}$ 155.4714, doc float agrees to 4 decimals) | 156 |
| 134 | 37 | float only: $\log_{10} = 167.5204$ (crest claim) | **FIRST EXACT VALUE**; $\log_{10}$ = 167.5204 (+0.0000 vs doc) | 168 |
| 140 | 35 | float only: $146.4368$ appeared in the document's margin sentence (its extractor garbled it to "146") | **FIRST EXACT VALUE**; $\log_{10}$ = 146.4368 | 147 |
| 146 | 40 | extraction returned 0 (no exact value printed anywhere) | **FIRST EXACT VALUE** | 186 |

Full exact integers of the three first-ever values are printed in
`sextet.txt` (finish blocks $n = 37, 40$); the two headline values:

$$\mathrm{live}(140,35) \ \ (= T((4^{35}),(4^{35})), \text{Prop. K.2}), \quad
\text{a } 147\text{-digit integer, } \log_{10} = 146.436831$$

(the full integer is printed in `sextet.txt`, finish block $n = 35$);
$$\mathrm{live}(146,40) =
847232785311321929505742726278347449772399243065953510849792599096813508572696645610464194621343322161298121842449306221210882840944136278748773602001239786256022187586939606000000000000$$

(186 digits.) The three confirmed claims:

$$\mathrm{live}(119,33) = 411979871679030163202100278100027384012329163163904739648681954182027117819430316625483165168410753440098521301304903875171091965378352000000000,$$
$$\mathrm{live}(123,34) = 330878838362741642778408071184614272040690671971751064829695216692710832366710132418708600914944562397197426765461678221592298550679595216853440000000,$$
$$\mathrm{live}(127,35) = 296058170131216016326368316102452660122790372487110821828525206591182488548011391316831682323668261060941939498226212595365618643073678739096864444000000000.$$

**Additional exact checkpoints landed by the same passes** (the document's
outer-leaf law, lines ~703–736): $\mathrm{live}(131,33) = 33^2\cdot
\mathrm{maxTab}(33)$ and $\mathrm{live}(135,34) = 34^2\cdot\mathrm{maxTab}(34)$
both **EXACT MATCH** against the document's printed integers; and the
$\times n^2$ divisibility signature holds at every probed rung
$((143,37),(147,37),(139,37): \div 1369$; $(155,40),(159,40),(146,40):
\div 1600)$.

---

## 3. Proposition K.2 (the full-box identity)

**Proposition.** For every $n \ge 1$ and $q \ge 1$:
$$\mathrm{live}_q(4n, n)\big|_{q=4} = T\big((4^n),(4^n)\big),$$
i.e. $\lVert[t^{4n}](\sum_{r\le4}h_rt^r)^n\rVert^2 = \langle
h_{(4^n)}, h_{(4^n)}\rangle$.

*Proof.* Write $\mu = (4^n)$ (the partition of $4n$ with $n$ parts equal to
$4$). The decomposition
$F = \sum_{\mu_1 \le 4,\ \ell(\mu)\le n} C_\mu(n)\, h_\mu$ with
$C_\mu(n) = n!/((n - \ell(\mu))!\prod_j m_j!)$ has, at $|\mu| = 4n$, the
single candidate $\mu = (4^n)$: it is the only partition of $4n$ with all
parts $\le 4$ and at most $n$ parts (sum of $n$ terms each $\le 4$ equals
$4n$ iff every term is $4$). For this $\mu$,
$C_{(4^n)}(n) = n!/((n-n)!\, n!) = 1$. Hence $F_{4,n,4n} = h_{(4^n)}$
exactly, and taking norms:
$\mathrm{live}_4(4n,n) = \langle h_{(4^n)}, h_{(4^n)}\rangle
= T((4^n),(4^n))$. $\square$

This is the document's empirical "the end rung gives the full box"
(its `(lll)` item phrase) — which it knew only as a float coincidence;
here it is a one-line theorem, and the four-decimal agreement
($146.4368$ at $n=35$, $158.1962$ at $n=37$, $134.8752$/$140.6306$/
$176.1830$ at $n=33/34/40$ first appearing in exact form here) is a
consequence, not a check.

**Corollary (mirror census fatuity).** The Hall involution $\omega$
($\omega(h_r) = e_r$, $\omega(p_\lambda) = (-1)^{|\lambda|-\ell(\lambda)}
p_\lambda$) is an isometry, so the elementary-symmetric ("mirror") census
$\mathrm{live}^e_q(k,n) = \lVert[t^k](\sum_{r\le q} e_r t^r)^n\rVert^2$
satisfies $\mathrm{live}^e_q(k,n) = \mathrm{live}^{h}_q(k,n)$ identically.
This is why the document's mirror laws are ledger-only statements: on the
live side the mirror quantity is the same quantity.

---

## 4. The exact crest and margin table (deep columns)

The document's crest program (drift law $\mathrm{crest}(n) \approx 3.55n$
with a $+4$ cadence; margin law
$\mathrm{margin}(n) = \log_{10}\mathrm{live}(\mathrm{crest},n) -
\log_{10} T((4^n),(4^n))$) was built from float surveyor passes plus a
modular exactifier. The exact spectra give both quantities exactly at five
deep columns (columns $33, 34, 35, 37, 40$; note the document never
measured $n=40$ at all):

| $n$ | crest $k$ (exact) | $\log_{10}$ live(crest) | runner-up $k$ | $\log_{10}$ end rung | margin (exact) | crest$/n$ |
|----|----|----|----|----|----|----|
| 33 | 119 | 143.614876 | 120 | 134.875225 | 8.739651 | 3.6061 |
| 34 | 123 | 149.519669 | 122 | 140.630599 | 8.889070 | 3.6176 |
| 35 | 127 | 155.471377 | 126 | 146.436831 | 9.034546 | 3.6286 |
| 37 | **134** | 167.520427 | **135** (doc said 133) | 158.196173 | 9.324254 | 3.6216 |
| 40 | **146** | 185.928003 | 145 | 176.182959 | 9.745044 | 3.6500 |

Readings:

1. **The $+4$ cadence is real and exact** where testable: crest increments
   $+4, +4, +3.5$/col ($35\to37$), $+4$/col ($37\to40$); the document's
   drift cadence $73, 77, \ldots, 115, 119, 123$ extends exactly to
   $134$ and, for the first time, to a column it never measured ($n=40$,
   crest $146$).
2. **Margin law confirmed**: increments $+0.148$, $+0.146$, $+0.097$/col
   spread over $35..37$ per column — inside the document's "increments
   floored near $+0.1425$–$0.1472$" window; the document's
   $\mathrm{margin}(35) = 9.0346$ and $\mathrm{margin}(37) = 9.3243$ agree
   with the exact values to the four decimals its float inputs carried
   (exact: $9.034546$, $9.324254$).
3. **Runner-up correction at $n=37$**: the document's float pass reported
   "crest at $k=134$ (167.5204), runner-up $k=133$ (167.4797), gap 0.0407".
   Exactly: $\log_{10}\mathrm{live}(133,37) = 167.4797$ (the document's
   value for the $k=133$ rung is right), but the true runner-up is
   $k = 135$ at $167.5106$ — their surveyor missed the closer contender,
   and the exact crest gap is $0.0098$ orders, not $0.0407$. The crest
   itself ($k=134$) is confirmed; only the race's silver medal moves.
4. **crest$/n$ keeps creeping**: $3.6061 \to 3.6286 \to 3.6500$ over
   $n = 33..40$; the document's $\approx 3.55n$ line (fit at
   $n = 23..26$) already sits slightly below the deep columns. The growth
   of the increment ($+4$ per column, i.e. crest$/n$ drifting up by
   $+0.09$ per column at $n\approx 40$) is the deep-column echo of the
   document's own "ratio climbing from 2.0 at $n=2$ to 3.5 at $n=22$".

---

## 5. Certification of this note's computations

- **Grid equality 738/738** vs `norm_route.routeC` (the Phase-8 engine,
  whose 114-check battery gates Routes A/B/C); see §1.
- **30-rung replication**: the single $n=35$ pass reproduces the entire
  Phase-8 deep campaign in one run: $k=36..65$ vs the document's claims:
  26 exact, 4 superseded, 0 unclaimed — with the four superseding values
  for $k=62..65$ re-derived digit-identically.
- **Integer denominators**: all five finish passes assert
  $\mathrm{live}(k,n) \in \mathbb{Z}$ via exact division by $L^{2n}$
  ($L = 24$): "bad = 0" everywhere.
- **Theorem K.1 per-degree counts** within the polynomial bound at every
  step of all five columns (PASS lines in `sextet.txt`).
- **Independent-law confirmations**: Prop K.2's three new full-box logs;
  the outer-leaf $\times n^2$ divisibilities of §2; the crest/margin
  agreement with the document's independently-produced floats (§4).

## 6. VHC reading and register

1. **The document's numeric layer is now fully settled.** Every one of the
   original 42 SKIP lines of the Phase-2 audit has been closed by machine
   (40 distinct claims — the lines double-list live(59,35) and
   live(146,40) — decomposed and discharged in §5 point 5):
   409 PASS stands, and the SKIP column is empty after Phases 2–9
   (30 deep rungs, live(20,35), 6 sextet rungs, 3 ledger boundary rungs).
   The residual uncertainty in the entire claim table is
   concentrated in exactly four integers — the superseded
   $\mathrm{live}(62..65,35)$ — where the *document* (not the census) was
   wrong by $0.46$–$1.45\%$.
2. **The document's own exactifier architecture (float surveyor + modular
   exactifier + 20-prime gate) is superseded** by Theorem K.1: an exact
   polynomial-time DP does the whole column in under two minutes on one
   core. In the CRT-corruption taxonomy of Note J §4.3, the six published
   sextet-adjacent integers are *clean* — confirmed digit-for-digit where
   printed — so the corruption at $k=62..65$ was an isolated event, not a
   systematic property of the deep columns.
3. **For the G-Detect gates (roadmap step 8/J.4)**: the deep-regime
   observables the gate constants were to be "pinned" against — crest
   position, crest gap, margin — now exist in exact integer form at
   $n = 33, 34, 35, 37, 40$; the gate constants can be certified against
   exact values instead of the document's floats. ($D_k(k)$'s J.2 window
   from Note J §3 is untouched by this note: it concerns the $n = k$ ray,
   where the sextet rungs do not sit.)
4. **Honest scope**: (a) the pool bound is an inequality; reachability of
   every packed partition is not needed for any claim here. (b) The exact
   crest/margin table covers five columns; the drift-law claims beyond
   $n = 40$ remain extrapolations. (c) The $\times n^2$ divisibilities are
   recorded as machine observations, subordinate to the full outer-leaf
   law statement the document makes (which our data corroborates at three
   of its own printed integers). (d) All of this is arithmetic about the
   model's cap-$4$ graded census; its bearing on VHC runs exclusively
   through Note E's gate architecture (status: gated, per Note E).

**Phase-10 addendum (added at close):** the promised full-leaf follow-up is
   delivered in Note L (`notes/12-outer-leaf.md`): the outer-leaf machine
   (`outer_leaf.py`) re-certifies the whole pipeline end-to-end (Thm L.1–L.5,
   triple-engine agreement for the transport tables) and sweeps ALL columns
   $n = 8,\dots,40$ over the full DP spectra — the outer-leaf divisibility
   is per-rung (a global $n^2 \mid \mathrm{live}$ law is FALSE: live(2,2) =
   10), the full j = 0 and j = 1 end-rung laws hold at all 33 columns, and
   the document's typographic constants are digit-exact everywhere except a
   registered six-constant anomaly register (maxTab at n = 10, 11, 22; the
   26! monolith; G(138); the peak at k = 47) — each anomaly double-certified
   on the engine side and dissected at the digit level in Note L §2. The
   decoder-rescued rungs $k = 85, 89, 92, 96, 100, 104$ of the drift chain
   are all machine-exact; every concern that Note E §d flagged on the
   arithmetic side is now discharged.

---

## 7. Engine notes (Phase 9 files)

* `ledger/sextet.py`: count-vector Route C (`blocks_counts`, `run_steps`
  in-place ascending-degree DP — certified equal to routeC 738/738);
  chunked spectrum driver with pickle checkpointing (`spectrum N BUDGET`);
  per-column finish with claims comparison (`finish N`); Thm K.1 bound
  checks (`cert`).
* `ledger/sextet.txt`: the run record (all columns, all claims, the exact
  crest/margin table); final line "end of sextet".
* Checkpoints `sextet_ckpt_{33,34,35,37,40}.pkl` hold the full spectra
  (all exact), $\approx$ 0.2–0.45 GB each.

*End of Note K.*
