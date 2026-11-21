namespace DriftReductionV1

/-- Prefix sum of the window-excess sequence: sumTo f K = f 0 + ... + f (K-1). -/
def sumTo (f : Nat → Int) : Nat → Int
  | 0 => 0
  | K + 1 => sumTo f K + f K

variable {dhat chat : Nat → Int}

/-- Prefix sums are nondecreasing for nonnegative sequences. -/
theorem sumToMono (hnn : ∀ n, 0 ≤ dhat n) (K : Nat) :
    sumTo dhat K ≤ sumTo dhat (K + 1) := by
  have e : sumTo dhat (K + 1) = sumTo dhat K + dhat K := rfl
  have h := hnn K
  omega

/-- Telescoping identity: under the exact coupling recursion the prefix sums satisfy
D * dhat(n+1) = Q * dhat n + D * chat n exactly, and summing it over the first K windows
gives the resolved form below (D = 30000000, Q = 30000). -/
theorem sumToTelescope
    (hexact : ∀ n, 30000000 * dhat (n + 1) = 30000 * dhat n + 30000000 * chat n)
    (K : Nat) :
    30000000 * sumTo dhat (K + 1)
      = 30000 * sumTo dhat K + 30000000 * dhat 0 + 30000000 * sumTo chat K := by
  induction K with
  | zero =>
      have e1 : sumTo dhat (0 + 1) = sumTo dhat 0 + dhat 0 := rfl
      have e2 : sumTo dhat 0 = 0 := rfl
      have e3 : sumTo chat 0 = 0 := rfl
      omega
  | succ K ih =>
      have e1 : sumTo dhat (K + 1 + 1) = sumTo dhat (K + 1) + dhat (K + 1) := rfl
      have e2 : sumTo dhat (K + 1) = sumTo dhat K + dhat K := rfl
      have e3 : sumTo chat (K + 1 + 1) = sumTo chat (K + 1) + chat (K + 1) := rfl
      have e4 : sumTo chat (K + 1) = sumTo chat K + chat K := rfl
      have h1 := hexact K
      omega

/-- Upper potential for the source channel: if the source contracts at
mu <= 28736617/30000000 per window, then (D-X) * sumTo chat K + D * chat K <= D * chat 0,
so the whole released source is at most chat 0 * D / (D - X). -/
theorem chatUpperBound
    (hdec : ∀ n, 30000000 * chat (n + 1) ≤ 28736617 * chat n) (K : Nat) :
    1263383 * sumTo chat K + 30000000 * chat K ≤ 30000000 * chat 0 := by
  induction K with
  | zero =>
      have e : sumTo chat 0 = 0 := rfl
      omega
  | succ K ih =>
      have e : sumTo chat (K + 1) = sumTo chat K + chat K := rfl
      have h1 := hdec K
      omega

/-- Lower potential for the source channel: if the source contracts at
mu >= 28770000/30000000 per window (alpha = 0.060-level decay, the no-go regime),
then (D-Xd) * sumTo chat K + D * chat K >= D * chat 0: the released source is at least
chat 0 * D / (D - Xd) in the limit. -/
theorem chatLowerBound
    (hdec : ∀ n, 30000000 * chat (n + 1) ≥ 28770000 * chat n) (K : Nat) :
    1230000 * sumTo chat K + 30000000 * chat K ≥ 30000000 * chat 0 := by
  induction K with
  | zero =>
      have e : sumTo chat 0 = 0 := rfl
      omega
  | succ K ih =>
      have e : sumTo chat (K + 1) = sumTo chat K + chat K := rfl
      have h1 := hdec K
      omega

/-- Anchor 1 (sigma = 7.3303): the two-channel potential is monotone with
contraction Q/D = 1/1000 and decay X/D = 27832580/30000000 (mu <= 0.927753,
alpha >= 0.10819). -/
theorem phiMono1
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * chat n)
    (hdec : ∀ n, 30000000 * chat (n + 1) ≤ 27832580 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (_hnn : ∀ n, 0 ≤ dhat n) (_hnc : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K * 29970000 * 2167420 + 2167420 * 30000000 * dhat K
        + 30000000 * 30000000 * chat K
      ≤ 2167420 * 30000000 * 1000000 + 30000000 * 30000000 * 39000 := by
  induction K with
  | zero =>
      have h1 := hd0
      have h2 := hc0
      have hz : sumTo dhat 0 = 0 := rfl
      omega
  | succ K ih =>
      have h1 := hstep K
      have h2 := hdec K
      have e1 : sumTo dhat (K + 1) = sumTo dhat K + dhat K := rfl
      omega

/-- Threshold instance 1: with alpha >= 0.10819 decay the prefix sums never exceed
1541354 = floor(0.05137848 * D), the budget head at the lower band end, for every K. -/
theorem driftBound1
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * chat n)
    (hdec : ∀ n, 30000000 * chat (n + 1) ≤ 27832580 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (hnn : ∀ n, 0 ≤ dhat n) (hnc : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K ≤ 1541354 := by
  have h1 := phiMono1 hstep hdec hd0 hc0 hnn hnc K
  have h2 := hnn K
  have h3 := hnc K
  have h4 : 2167420 * 30000000 * 1000000 + 30000000 * 30000000 * 39000
      ≤ 1541354 * (29970000 * 2167420) := by decide
  omega

/-- Anchor 2 (sigma = 7.5772): monotone potential with decay
X/D = 28423857/30000000 (mu <= 0.947462, alpha >= 0.07786). -/
theorem phiMono2
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * chat n)
    (hdec : ∀ n, 30000000 * chat (n + 1) ≤ 28423857 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (_hnn : ∀ n, 0 ≤ dhat n) (_hnc : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K * 29970000 * 1576143 + 1576143 * 30000000 * dhat K
        + 30000000 * 30000000 * chat K
      ≤ 1576143 * 30000000 * 1000000 + 30000000 * 30000000 * 39000 := by
  induction K with
  | zero =>
      have h1 := hd0
      have h2 := hc0
      have hz : sumTo dhat 0 = 0 := rfl
      omega
  | succ K ih =>
      have h1 := hstep K
      have h2 := hdec K
      have e1 : sumTo dhat (K + 1) = sumTo dhat K + dhat K := rfl
      omega

/-- Threshold instance 2: with alpha >= 0.07786 decay the prefix sums never exceed
1744063 = floor(0.05813545 * D), the budget head at the mid band point, for every K. -/
theorem driftBound2
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * chat n)
    (hdec : ∀ n, 30000000 * chat (n + 1) ≤ 28423857 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (hnn : ∀ n, 0 ≤ dhat n) (hnc : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K ≤ 1744063 := by
  have h1 := phiMono2 hstep hdec hd0 hc0 hnn hnc K
  have h2 := hnn K
  have h3 := hnc K
  have h4 : 1576143 * 30000000 * 1000000 + 30000000 * 30000000 * 39000
      ≤ 1744063 * (29970000 * 1576143) := by decide
  omega

/-- Anchor 3 (sigma = 7.8240): monotone potential with decay
X/D = 28736617/30000000 (mu <= 0.957887, alpha >= 0.06207). -/
theorem phiMono3
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * chat n)
    (hdec : ∀ n, 30000000 * chat (n + 1) ≤ 28736617 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (_hnn : ∀ n, 0 ≤ dhat n) (_hnc : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K * 29970000 * 1263383 + 1263383 * 30000000 * dhat K
        + 30000000 * 30000000 * chat K
      ≤ 1263383 * 30000000 * 1000000 + 30000000 * 30000000 * 39000 := by
  induction K with
  | zero =>
      have h1 := hd0
      have h2 := hc0
      have hz : sumTo dhat 0 = 0 := rfl
      omega
  | succ K ih =>
      have h1 := hstep K
      have h2 := hdec K
      have e1 : sumTo dhat (K + 1) = sumTo dhat K + dhat K := rfl
      omega

/-- Threshold instance 3: with alpha >= 0.06207 decay the prefix sums never exceed
1928014 = floor(0.06426717 * D), the budget head at the upper band end, for every K. -/
theorem driftBound3
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * chat n)
    (hdec : ∀ n, 30000000 * chat (n + 1) ≤ 28736617 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (hnn : ∀ n, 0 ≤ dhat n) (hnc : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K ≤ 1928014 := by
  have h1 := phiMono3 hstep hdec hd0 hc0 hnn hnc K
  have h2 := hnn K
  have h3 := hnc K
  have h4 : 1263383 * 30000000 * 1000000 + 30000000 * 30000000 * 39000
      ≤ 1928014 * (29970000 * 1263383) := by decide
  omega

/-- Divergence calibration: a constant source releases at least its own level into
every window from the first on; the prefix sums then grow linearly. -/
theorem constantSourceDiverges
    (hexact : ∀ n, 30000000 * dhat (n + 1) = 30000 * dhat n + 30000000 * 39000)
    (hnn : ∀ n, 0 ≤ dhat n) (K : Nat) :
    39000 * (K : Int) ≤ sumTo dhat (K + 1) := by
  have hlow : ∀ n, 39000 ≤ dhat (n + 1) := by
    intro n
    have h1 := hexact n
    have h2 := hnn n
    omega
  induction K with
  | zero =>
      have h := hnn 0
      have e : sumTo dhat (0 + 1) = sumTo dhat 0 + dhat 0 := rfl
      have e0 : sumTo dhat 0 = 0 := rfl
      omega
  | succ K ih =>
      have h1 := hlow K
      have hdef : sumTo dhat (K + 1 + 1) = sumTo dhat (K + 1) + dhat (K + 1) := rfl
      have hK : ((39000 : Int) * ((K + 1 : Nat))) = 39000 * (K : Int) + 39000 := by omega
      omega

#print axioms sumToMono
#print axioms sumToTelescope
#print axioms chatUpperBound
#print axioms chatLowerBound
#print axioms phiMono1
#print axioms driftBound1
#print axioms phiMono2
#print axioms driftBound2
#print axioms phiMono3
#print axioms driftBound3
#print axioms constantSourceDiverges

end DriftReductionV1
