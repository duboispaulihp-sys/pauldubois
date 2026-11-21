namespace DriftControl

/-- Prefix sum: sumTo f K = f 0 + ... + f (K-1). -/
def sumTo (f : Nat → Int) : Nat → Int
  | 0 => 0
  | K + 1 => sumTo f K + f K

variable {dhat tau : Nat → Int}

/-- Monotone two-channel potential with the aggregated adversarial source
(mu <= 3/4, all channels simultaneous). -/
theorem phiMonoAll
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * tau n)
    (hdec : ∀ n, 30000000 * tau (n + 1) ≤ 22500000 * tau n)
    (hd0 : dhat 0 ≤ 1000000) (ht0 : tau 0 ≤ 39174)
    (hnn : ∀ n, 0 ≤ dhat n) (hnt : ∀ n, 0 ≤ tau n) (K : Nat) :
    sumTo dhat K * 29970000 * 7500000 + 7500000 * 30000000 * dhat K
        + 30000000 * 30000000 * tau K
      ≤ 7500000 * 30000000 * 1000000 + 30000000 * 30000000 * 39174 := by
  induction K with
  | zero =>
      have h1 := hd0
      have h2 := ht0
      have hz : sumTo dhat 0 = 0 := rfl
      omega
  | succ K ih =>
      have h1 := hstep K
      have h2 := hdec K
      have e1 : sumTo dhat (K + 1) = sumTo dhat K + dhat K := rfl
      omega

/-- Controller headline, every constructed error channel adversarial at once:
launch 1/30, intrinsic 1.3e-3, bending 5.8e-6, all decaying at mu <= 3/4 —
the prefix sums never exceed 1542000 = 0.0514 * D, for every K. -/
theorem controlTheorem
    (hstep : ∀ n, 30000000 * dhat (n + 1) ≤ 30000 * dhat n + 30000000 * tau n)
    (hdec : ∀ n, 30000000 * tau (n + 1) ≤ 22500000 * tau n)
    (hd0 : dhat 0 ≤ 1000000) (ht0 : tau 0 ≤ 39174)
    (hnn : ∀ n, 0 ≤ dhat n) (hnt : ∀ n, 0 ≤ tau n) (K : Nat) :
    sumTo dhat K ≤ 1542000 := by
  have h1 := phiMonoAll hstep hdec hd0 ht0 hnn hnt K
  have h2 := hnn K
  have h3 := hnt K
  have h4 : 7500000 * 30000000 * 1000000 + 30000000 * 30000000 * 39174
      ≤ 1542000 * (29970000 * 7500000) := by decide
  omega

/-- Structural necessity of decay: a persistent per-window floor of the intrinsic
level (39000) forces linear growth of the prefix sums, forever. -/
theorem linearGrowth
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

/-- Fatal-floor instance: after 400 windows the prefix sums exceed not just the
tightest anchor head 1541354 but the all-sigma capped budget 7/90 * D = 2333333. -/
theorem fatalFloor
    (hexact : ∀ n, 30000000 * dhat (n + 1) = 30000 * dhat n + 30000000 * 39000)
    (hnn : ∀ n, 0 ≤ dhat n) :
    15600000 ≤ sumTo dhat 401 ∧ 2333333 < 15600000 := by
  have h := linearGrowth hexact hnn 400
  exact ⟨h, by decide⟩

#print axioms phiMonoAll
#print axioms controlTheorem
#print axioms linearGrowth
#print axioms fatalFloor

end DriftControl
