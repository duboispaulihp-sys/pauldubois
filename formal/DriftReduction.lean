namespace DriftReduction

/-- Prefix sum of the window-excess sequence: sumTo f K = f 0 + ... + f (K-1). -/
def sumTo (f : Nat → Int) : Nat → Int
  | 0 => 0
  | K + 1 => sumTo f K + f K

variable {dhat chat : Nat → Int}

/-- Monotone two-channel potential, scale D = 30000000, contraction Q/D = 1/1000,
decay X/D = 3/4, launch delta0 <= 1000000 (= 1/30), source chat0 <= 39000 (= 13/10000). -/
theorem phiMono
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * chat n)
    (hdec : ∀ n, 30000000 * chat (n + 1) ≤ 22500000 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (_hnn : ∀ n, 0 ≤ dhat n) (_hnc : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K * 29970000 * 7500000 + 7500000 * 30000000 * dhat K
        + 30000000 * 30000000 * chat K
      ≤ 7500000 * 30000000 * 1000000 + 30000000 * 30000000 * 39000 := by
  induction K with
  | zero =>
      have h1 := hd0
      have h2 := hc0
      simp only [sumTo]
      omega
  | succ K ih =>
      have h1 := hstep K
      have h2 := hdec K
      simp only [sumTo]
      omega

/-- Headline bound: prefix sums never exceed 1542000 = 0.0514 * 30000000. -/
theorem driftBound
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * chat n)
    (hdec : ∀ n, 30000000 * chat (n + 1) ≤ 22500000 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (hnn : ∀ n, 0 ≤ dhat n) (hnc : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K ≤ 1542000 := by
  have h1 := phiMono hstep hdec hd0 hc0 hnn hnc K
  have h2 := hnn K
  have h3 := hnc K
  have h4 : 7500000 * 30000000 * 1000000 + 30000000 * 30000000 * 39000
      ≤ 1542000 * (29970000 * 7500000) := by decide
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
      simp only [sumTo]
      omega
  | succ K ih =>
      have h1 := hlow K
      have hdef : sumTo dhat (K + 1 + 1) = sumTo dhat (K + 1) + dhat (K + 1) := rfl
      have hK : ((39000 : Int) * ((K + 1 : Nat))) = 39000 * (K : Int) + 39000 := by omega
      omega

#print axioms phiMono
#print axioms driftBound
#print axioms constantSourceDiverges

end DriftReduction
