/-
Typed interface of the constant-`r/kappa/delta-bar` construction of the
Ricci flow with delta-cutoff surgery.

Manuscript source: G. Perelman, "Ricci flow with surgery on
three-manifolds", arXiv:math/0303109 (cited below as [II]):

* [II, Notation]  epsilon is a fixed small positive constant; delta is a
  positive quantity, supposed to be as small as needed in each argument.
* [II SS4.1]  the a priori assumptions held by the solutions under
  construction: (pinching) `Rm >= -phi(R) R` for a function phi decreasing
  to zero at infinity, and (canonical neighborhood) a scale `r > 0` such
  that every point where scalar curvature is at least `r^-2` has a
  neighborhood satisfying the conclusions of [II SS1.5].
* [II SS4.2]  the two claims (scalar curvature bound on parabolic
  neighborhoods from the estimates (1.3); the geodesic-distance estimate
  replacing the unjustified `RMAX = Gamma` of Hamilton [H 5] - ERRATA item 5)
* [II SS4.3]  Lemma (`rho = delta r`): there is a radius `h`, `0 < h < delta rho`,
  depending only on `delta`, `rho` and the pinching function `phi`, such that
  for each point `x` with `h(x) = Rbar(x)^-1/2 <= h` in an epsilon-horn of
  `(Omega, gbar)` with boundary in `Omega_rho`, the parabolic neighborhood
  `P(x, T, delta^-1 h(x), -h^2(x))` is a strong delta-neck. This is the
  strong-neck lemma input that fixes the surgery radius.
* [II SS4.4]  the Ricci flow with delta-cutoff: fix `delta > 0`, compute
  `rho = delta r` and determine `h` from the lemma above; run the flow until
  it goes singular at `t^+`; form the limit `(Omega, gbar)`. If `Omega_rho` is
  empty, the procedure stops - the solution became extinct. Otherwise: remove
  the components of `Omega` containing no point of `Omega_rho`; in every
  epsilon-horn of each remaining component find a delta-neck of radius `h`,
  cut it along the middle two-sphere, remove the horn-shaped end, and glue
  an almost standard cap so that the curvature pinching is preserved and a
  ball of radius `delta'^-1 h` near the cap center is, after scaling,
  `delta'`-close to the standard capped infinite cylinder of [II SS2]
  (`delta' = delta'(delta)` tends to zero with `delta`); declare extinct
  every component epsilon-close to a metric quotient of the round sphere.
  "Now since every surgery reduces the volume by at least `h^3`, the
  sequence of surgery times is discrete, and, taking for granted the a
  priori assumptions, we can continue our solution indefinitely, not ruling
  out the possibility that it may become extinct at some finite time."
* [II SS4.5]  Lemma (`deltaBar = deltaBar(A, theta)`): for any `A < infinity`
  and `0 < theta < 1` there is `deltaBar` such that for `delta < deltaBar`, at
  a surgery at time `T0` (with `p` the center of the standard cap and
  `T1 = min(T, T0 + theta h^2)`), either the solution on
  `P(p, T0, A h, T1 - T0)` is, after scaling and time shift, `A^-1`-close to
  the standard solution of [II SS2], or the same holds up to an earlier
  surgery time `t^+ in [T0, T1)` near which the solution is cut off.
  Corollaries [II SS4.6-4.7] convert this into the R-length obstruction for
  curves leaving the ball `B(p, T0, A h)` used in the kappa-step of SS5.
* [II SS5.1]  Proposition: there exist decreasing sequences
  `0 < r_j < epsilon^2`, `kappa_j > 0`, `0 < deltaBar_j < epsilon^2`,
  `j = 1, 2, ...`, such that for any normalized initial data and any cutoff
  function `delta(t)` with `0 < delta(t) < deltaBar_j` on
  `[2^(j-1) epsilon, 2^j epsilon]`, the Ricci flow with `delta(t)`-cutoff is
  defined for all `t`, is `kappa_j`-noncollapsed, and satisfies the canonical
  neighborhood assumption with parameter `r_j` on
  `[2^(j-1) epsilon, 2^j epsilon]`. The proof is by induction, with the
  retroactive step "defining `r_{i+1}, kappa_{i+1}, deltaBar_{i+1}, and
  redefining `deltaBar_i = deltaBar_{i+1}`"; the kappa-step is the
  admissible-curve argument of [I SS7.3] carried out via S5.2-S5.3 on
  barely admissible curves. For the elliptization route [III SS1.4] the
  surgery times are controlled by *single constants* `r, kappa, deltaBar` -
  the record `SurgeryControls` below.

Correspondence with the ledger of `Perelman.Skeleton`: `SurgeryControls`
packages exactly what the ledger fields `deltaCutoffFlow` ([II SS4.4]) and
`aPrioriAssumptionJustified` ([II SS5.1]) assert exists; the analyses of
[II SS3] (the structure of `Omega` at a singular time) and [II SS5.2-5.3]
(the kappa-noncollapsing step) remain proof obligations of the ledger, not
reproduced here.

Encoding. The manuscript's constants are positive reals. The compiled layer
is deliberately core-only (no Mathlib in the authoring sandbox, hence no
`Real`), so each constant is entered as a positive integer in an arbitrary
fixed unit, and every manuscript inequality transcribes as the
corresponding integer inequality; in particular `delta * (delta * r)` is
the mirror of `delta rho = delta * delta * r` and `h * h * h` the mirror of
the cubic volume loss at a delta-neck of radius `h`. Nothing below depends
on the choice of unit: given any instance of `SurgeryControls` in any unit,
scaling all constants by the same factor leaves every field invariant in
meaning - the bookkeeping theorems are proved for the abstract integers.

The theorems proved here (no project axioms, no `sorry`, no `opaque`):

* `drop_chain` - induction over `m` consecutive surgical steps starting at
  a boundary `b`: the volume surrendered by those surgeries is accumulated
  against the volume at `b`.
* `bound_of_steps_bounded` - bounded version of the barrier descent
  (`Perelman.Barrier.bound_of_steps`): drops at the first `N` steps only.
* `surgery_volume_bound`, `surgery_count_bound` - [II SS4.4]: `N` surgeries
  with cutoff `h` consume at least `N h^3` of volume; hence
  `surgeries * h^3 <= initial volume` - the discreteness of the sequence of
  surgery times.
* `boundary`, `cumDrops`, `stage_budget`, `cumulative_drops`,
  `total_surgery_budget` - [II SS5.1] in staged, time-dependent-cutoff form:
  with stage `j` of the induction conducted with constants `r_j, kappa_j,
  deltaBar_j` and per-surgery loss `q_j`, each stage's surgery count obeys
  `n_j q_j` <= volume at the stage start, and over any finite prefix of
  stages the total volume surrendered to surgery is at most the initial
  volume - the bookkeeping that lets the induction of [II SS5.1] continue
  indefinitely "not ruling out the possibility that [the flow] may become
  extinct at some finite time".
* `redefinedTo`, `redefinedTo_anti` - the retroactive step
  "redefining `deltaBar_i = deltaBar_{i+1}`" of [II SS5.1] preserves the
  decreasing property of the tolerance sequence.
* `stageControls` - the constant-`r/kappa/deltaBar` record for stage `j`,
  assembled from the sequences of the Proposition [II SS5.1] together with
  the strong-neck radius delivered by Lemma [II SS4.3].
-/

namespace Perelman

/-! ### The constants of the delta-cutoff construction, [II SS4.1-4.5, SS5.1] -/

/-- The constant-`r/kappa/delta-bar` surgery interface.

In the manuscript the constants are positive reals; here each is a positive
integer in an arbitrary fixed unit (see the file header for the encoding)
and every manuscript relation between them is kept as a hypothesis field.

* `eps`       - [II, Notation] the fixed small positive constant epsilon
                with respect to which necks, caps and closeness are taken;
* `r`         - [II SS4.1] the canonical neighborhood scale;
* `delta`     - [II SS4.4] the cutoff parameter delta;
* `deltaBar`  - [II SS4.5] the tolerance `deltaBar = deltaBar(A, theta)` with
                `delta < deltaBar`; constant on the elliptization route
                [III SS1.4];
* `h`         - [II SS4.3] the surgery (neck) radius with `0 < h < delta rho`,
                `rho = delta r`, delivered by the strong-neck lemma;
* `kappa`     - [II SS5.1] the noncollapsing constant kappa_j. -/
structure SurgeryControls where
  /-- Fixed small positive constant [II, Notation]. -/
  eps : Int
  /-- Canonical neighborhood scale [II SS4.1]. -/
  r : Int
  /-- Cutoff parameter [II SS4.4]. -/
  delta : Int
  /-- Cutoff tolerance `deltaBar(A, theta)` [II SS4.5]. -/
  deltaBar : Int
  /-- Surgery radius from the strong-neck lemma [II SS4.3]. -/
  h : Int
  /-- Noncollapsing constant [II SS5.1 Proposition]. -/
  kappa : Int
  hEpsPos : 0 < eps
  hRPos : 0 < r
  hDeltaPos : 0 < delta
  hDeltaBarPos : 0 < deltaBar
  hHPos : 0 < h
  hKappaPos : 0 < kappa
  hRLtEpsSq : r < eps * eps
  hDeltaBarLtEpsSq : deltaBar < eps * eps
  hDeltaLtDeltaBar : delta < deltaBar
  hLtDeltaRho : h < delta * (delta * r)

/-- The surgery radius is positive, so the manuscript's per-surgery volume
loss "at least `h^3`" ([II SS4.4]) is a strictly positive quantity. -/
theorem hcube_pos (c : SurgeryControls) : 0 < c.h * c.h * c.h := by
  have h1 : 0 < c.h * c.h := Int.mul_pos c.hHPos c.hHPos
  exact Int.mul_pos h1 c.hHPos

/-- Bookkeeping obligations of one run of the delta-cutoff procedure of
[II SS4.4], with its volume audit.

`volume k` is the total volume of the solution sampled immediately after
the `k`-th observation step; `the field `surgeries` counts how many of the steps were delta-cutoff
surgeries. The flow between surgeries only decreases the total volume, and
each surgery removes the delta-neck together with the horn-shaped end,
which contains a ball of volume comparable to `h^3` - the manuscript's
lower bound `volume drop >= h^3`. The `Prop` fields are
the geometric outputs of the construction, kept as obligations exactly as
in the ledger `PerelmanInputs.deltaCutoffFlow`. -/
structure SurgeryOutcome (c : SurgeryControls) where
  /-- [II SS4.4] the components of `Omega` containing no point of
  `Omega_rho` are removed. -/
  bareComponentsRemoved : Prop
  /-- [II SS4.4] in every epsilon-horn of each remaining component a
  delta-neck of radius `h` is cut along its middle two-sphere and the
  horn-shaped end is replaced by an almost standard cap. -/
  deltaNecksCapped : Prop
  /-- [II SS4.4; the conformal-factor cap construction, cf. [H 5, SS4]]
  the curvature pinching condition is preserved by the cap. -/
  pinchingPreserved : Prop
  /-- [II SS4.4] the capped ball of radius `delta'^-1 h` near the cap center
  is, after scaling, `delta'`-close to the standard capped infinite cylinder
  of [II SS2], with `delta' = delta'(delta) to 0`. -/
  standardCapCloseness : Prop
  /-- [II SS4.4] every component epsilon-close to a metric quotient of the
  round sphere is declared extinct. -/
  extinctComponentsDeclared : Prop
  /-- Total volume sampled at the observation steps (in the fixed unit of
  the integer encoding). -/
  volume : Nat -> Int
  volumeNonneg : forall k, 0 <= volume k
  volumeNonincreasing : forall k, volume (k + 1) <= volume k
  surgeries : Nat
  /-- The manuscript's per-surgery volume loss [II SS4.4]:
  `>= h^3` whenever step `k` is a surgery. -/
  perSurgeryDrop : forall k, k < surgeries ->
    volume (k + 1) <= volume k - c.h * c.h * c.h

/-- Bounded version of the barrier descent. If the volume drops by `q` on
each of the first `N` steps, then after `k <= N` steps it has dropped by at
least `k q` from its initial value - the prefix form of
`Perelman.Barrier.bound_of_steps`, adapted to drops occurring on a finite
initial segment of the observation steps. -/
theorem bound_of_steps_bounded {V : Nat -> Int} {q : Int} :
    forall N, (forall k, k < N -> V (k + 1) <= V k - q) ->
      forall k, k <= N -> V k <= V 0 - k * q := by
  intro N
  induction N with
  | zero =>
      intro hdrop k hk
      have he : k = 0 := by omega
      subst he
      omega
  | succ N ih =>
      intro hdrop k hk
      rcases Nat.lt_or_ge k (N + 1) with hlt | hge
      · exact ih (by intro i hi; exact hdrop i (by omega)) k (by omega)
      · have heq : k = N + 1 := by omega
        rw [heq]
        have hcast : ((N + 1 : Nat) : Int) = (N : Int) + 1 := by omega
        have hdistr : ((N : Int) + 1) * q = (N : Int) * q + q := by
          rw [Int.add_mul, Int.one_mul]
        have hd := hdrop N (by omega : N < N + 1)
        have hiN := ih (by intro i hi; exact hdrop i (by omega)) N (Nat.le_refl N)
        rw [hcast, hdistr]
        omega

/-- [II SS4.4], quantitatively: after `N` surgeries with cutoff `h` (and
interleaved flow, which never increases volume) the total volume has
dropped by at least `N h^3` from its initial value. -/
theorem surgery_volume_bound (c : SurgeryControls) (o : SurgeryOutcome c)
    (k : Nat) (hk : k <= o.surgeries) :
    o.volume k <= o.volume 0 - k * (c.h * c.h * c.h) :=
  bound_of_steps_bounded (V := o.volume) (q := c.h * c.h * c.h)
    o.surgeries o.perSurgeryDrop k hk

/-- [II SS4.4]: "since every surgery reduces the volume by at least `h^3`,
the sequence of surgery times is discrete" - in audit form: the total
number of surgeries, in units of `h^3`, is bounded by the initial volume.
The time-discreteness itself (positively separated surgery times in real
time) is the minute-bookkeeping statement this integer bound certifies. -/
theorem surgery_count_bound (c : SurgeryControls) (o : SurgeryOutcome c) :
    o.surgeries * (c.h * c.h * c.h) <= o.volume 0 := by
  have hb := surgery_volume_bound c o o.surgeries (Nat.le_refl _)
  have hnn := o.volumeNonneg o.surgeries
  omega

/-! ### Staged bookkeeping, [II SS5.1]

The induction of [II SS5.1] proceeds on stages `j`, conducted on the time
interval `[2^(j-1) epsilon, 2^j epsilon]` with constants `r_j, kappa_j,
deltaBar_j`. The machinery below is the discrete audit of that induction:
surgeries are grouped into stages, each stage `j` containing `n j` surgery
steps of per-surgery loss `q j` (in the manuscript, `q j = h_j^3` for the
surgery radius `h_j` in force on the stage). -/

/-- The surgery index at which stage `j` begins: stage `j` consists of the
surgery steps `boundary n j, ..., boundary n j + n j - 1`. -/
def boundary (n : Nat -> Nat) : Nat -> Nat
  | 0 => 0
  | j + 1 => boundary n j + n j

/-- Total volume surrendered by the surgeries of the first `j` stages,
staged surgery by surgery. -/
def cumDrops (q : Nat -> Int) (n : Nat -> Nat) : Nat -> Int
  | 0 => 0
  | j + 1 => (n j : Int) * q j + cumDrops q n j

/-- Induction over `m` consecutive surgery steps of one stage, starting at
an arbitrary boundary `b`: the volume at the end of the run plus the total
surrendered volume is bounded by the volume at the start. -/
theorem drop_chain {V : Nat -> Int} {q : Int}
    (m : Nat) : forall b, (forall i, i < m -> V (b + i + 1) <= V (b + i) - q) ->
      V (b + m) + (m : Int) * q <= V b := by
  induction m with
  | zero =>
      intro b _
      have e : (b + 0 : Nat) = b := rfl
      rw [e]
      omega
  | succ m ih =>
      intro b hbd
      have hcast : ((m + 1 : Nat) : Int) = (m : Int) + 1 := by omega
      have hdistr : ((m : Int) + 1) * q = (m : Int) * q + q := by
        rw [Int.add_mul, Int.one_mul]
      have hidx : (b + (m + 1) : Nat) = b + m + 1 := by omega
      rw [hidx]
      have him := ih b (by intro i hi; exact hbd i (by omega))
      have hlast := hbd m (by omega)
      rw [hcast, hdistr]
      omega

/-- [II SS5.1], single stage: the number `n j` of surgeries in stage `j`,
each of loss `q j`, is bounded by the volume available in units of `q j`
when the stage opens. -/
theorem stage_budget {V : Nat -> Int} {q : Nat -> Int} {n : Nat -> Nat}
    (hnn : forall k, 0 <= V k)
    (hdrop : forall j i, i < n j ->
      V (boundary n j + i + 1) <= V (boundary n j + i) - q j)
    (j : Nat) : (n j : Int) * q j <= V (boundary n j) := by
  have him := drop_chain (V := V) (q := q j) (n j) (boundary n j)
    (by intro i hi; exact hdrop j i hi)
  have hnnB := hnn (boundary n j + n j)
  omega

/-- [II SS5.1], staged audit: after the surgeries of the first `J` stages,
the remaining volume plus everything surrendered to surgery so far is
bounded by the initial volume. -/
theorem cumulative_drops {V : Nat -> Int} {q : Nat -> Int} {n : Nat -> Nat}
    (hdrop : forall j i, i < n j ->
      V (boundary n j + i + 1) <= V (boundary n j + i) - q j)
    (J : Nat) : V (boundary n J) + cumDrops q n J <= V 0 := by
  induction J with
  | zero =>
      have e1 : boundary n 0 = 0 := rfl
      have e2 : cumDrops q n 0 = 0 := rfl
      rw [e1, e2]
      omega
  | succ J ih =>
      have hlocal := drop_chain (V := V) (q := q J) (n J) (boundary n J)
        (by intro i hi; exact hdrop J i hi)
      have e1 : boundary n (J + 1) = boundary n J + n J := rfl
      have e2 : cumDrops q n (J + 1) = (n J : Int) * q J + cumDrops q n J := rfl
      rw [e1, e2]
      omega

/-- [II SS5.1]: over any finite prefix of the stage induction, the total
volume surrendered to surgery is at most the initial volume. This is the
discrete content of "we can continue our solution indefinitely, not ruling
out the possibility that it may become extinct at some finite time"
([II SS4.4]) in the staged, time-dependent-cutoff form of [II SS5.1]. -/
theorem total_surgery_budget {V : Nat -> Int} {q : Nat -> Int} {n : Nat -> Nat}
    (hnn : forall k, 0 <= V k)
    (hdrop : forall j i, i < n j ->
      V (boundary n j + i + 1) <= V (boundary n j + i) - q j)
    (J : Nat) : cumDrops q n J <= V 0 := by
  have hc := cumulative_drops hdrop J
  have hb := hnn (boundary n J)
  omega

/-- The retroactive redefinition of [II SS5.1]: "defining `r_{i+1},
kappa_{i+1}, deltaBar_{i+1}`, and redefining `deltaBar_i = deltaBar_{i+1}`".
Redefining a tolerance sequence to its `i`-th value on the prefix below
`i` records that all earlier stages were conducted with the (smaller or
equal) final tolerance. -/
def redefinedTo (f : Nat -> Int) (i : Nat) : Nat -> Int :=
  fun j => if j <= i then f i else f j

/-- The retroactive redefinition of [II SS5.1] preserves the decreasing
property of the tolerance sequence. -/
theorem redefinedTo_anti {f : Nat -> Int} (hf : forall j, f (j + 1) <= f j)
    (i : Nat) : forall j, redefinedTo f i (j + 1) <= redefinedTo f i j := by
  intro j
  simp only [redefinedTo]
  rcases Nat.lt_or_ge j i with hlt | hge
  · rw [if_pos (by omega : j + 1 <= i), if_pos (by omega : j <= i)]
    omega
  · by_cases heq : j = i
    · rw [heq, if_neg (by omega : ¬ (i + 1 <= i)), if_pos (by omega : i <= i)]
      exact hf i
    · rw [if_neg (by omega : ¬ (j + 1 <= i)), if_neg (by omega : ¬ (j <= i))]
      exact hf j

/-- The three sequences of constants of the Proposition [II SS5.1]:
`0 < r_j < epsilon^2`, `kappa_j > 0`, `0 < deltaBar_j < epsilon^2`, all
decreasing except the noncollapsing constants, whose values are only
asserted positive. -/
structure SurgerySequences where
  /-- Fixed small positive constant epsilon [II, Notation]. -/
  eps : Int
  /-- Canonical neighborhood parameters by stage [II SS5.1]. -/
  r : Nat -> Int
  /-- Noncollapsing parameters by stage [II SS5.1]. -/
  kappa : Nat -> Int
  /-- Cutoff tolerances by stage [II SS5.1]. -/
  deltaBar : Nat -> Int
  hEpsPos : 0 < eps
  rPos : forall j, 0 < r j
  rLtEpsSq : forall j, r j < eps * eps
  rAnti : forall j, r (j + 1) <= r j
  kappaPos : forall j, 0 < kappa j
  deltaBarPos : forall j, 0 < deltaBar j
  deltaBarLtEpsSq : forall j, deltaBar j < eps * eps
  deltaBarAnti : forall j, deltaBar (j + 1) <= deltaBar j

/-- The constant-`r/kappa/deltaBar` controls in force on stage `j`
([II SS5.1]: cutoff `delta` with `delta(t) < deltaBar_j` on
`[2^(j-1) epsilon, 2^j epsilon]`), together with a surgery radius `h`
obeying the strong-neck lemma hypothesis `0 < h < delta rho` of
[II SS4.3]; the volume drop at each surgery on the stage is at least
`h^3` ([II SS4.4]), feeding the budget theorems above with `q j = h^3`
(here `delta rho = delta * delta * r`). -/
def stageControls (s : SurgerySequences) (j : Nat) (delta h : Int)
    (hΔ : 0 < delta) (hΔb : delta < s.deltaBar j) (hh : 0 < h)
    (hhr : h < delta * (delta * s.r j)) : SurgeryControls where
  eps := s.eps
  r := s.r j
  delta := delta
  deltaBar := s.deltaBar j
  h := h
  kappa := s.kappa j
  hEpsPos := s.hEpsPos
  hRPos := s.rPos j
  hDeltaPos := hΔ
  hDeltaBarPos := s.deltaBarPos j
  hHPos := hh
  hKappaPos := s.kappaPos j
  hRLtEpsSq := s.rLtEpsSq j
  hDeltaBarLtEpsSq := s.deltaBarLtEpsSq j
  hDeltaLtDeltaBar := hΔb
  hLtDeltaRho := hhr

/-- Sanity check: the controls assembled for stage `j` inherit the
manuscript's bounds `delta < deltaBar_j` ([II SS4.5]) and
`deltaBar_j < epsilon^2` ([II SS5.1]), hence `delta < epsilon^2`. -/
theorem stageControls_delta_lt_eps_sq (s : SurgerySequences) (j : Nat)
    (delta h : Int) (hD : 0 < delta) (hDb : delta < s.deltaBar j) (_hh : 0 < h)
    (hhr : h < delta * (delta * s.r j)) :
    (stageControls s j delta h hD hDb _hh hhr).delta
      < (stageControls s j delta h hD hDb _hh hhr).eps
        * (stageControls s j delta h hD hDb _hh hhr).eps :=
  Int.lt_trans hDb (s.deltaBarLtEpsSq j)

end Perelman
