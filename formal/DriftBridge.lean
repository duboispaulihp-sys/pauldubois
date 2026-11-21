namespace DriftBridge

/-- Prefix sum: sumTo f K = f 0 + ... + f (K-1). -/
def sumTo (f : Nat → Int) : Nat → Int
  | 0 => 0
  | K + 1 => sumTo f K + f K

variable {dhat : Nat → Int}

/-- Geometric envelope (no source channel): if the window excess contracts at
mu = X/D per window, then (D - X) * sumTo dhat K + D * dhat K <= D * dhat 0, so the
whole cascade releases at most dhat 0 * D / (D - X). This is the machine form of the
Alpöge-Buckmaster transcription delta_n <= C e^{-kappa sigma_n}: with S = log 2 and
kappa = 1/4, mu = 2^{-1/4} and X = 25226893 = ceil(mu * D). -/
theorem geometricEnvelope
    (hgeo : ∀ n, 30000000 * dhat (n + 1) ≤ 25226893 * dhat n)
    (hnn : ∀ n, 0 ≤ dhat n) (K : Nat) :
    4773107 * sumTo dhat K + 30000000 * dhat K ≤ 30000000 * dhat 0 := by
  induction K with
  | zero =>
      have e : sumTo dhat 0 = 0 := rfl
      omega
  | succ K ih =>
      have e : sumTo dhat (K + 1) = sumTo dhat K + dhat K := rfl
      have h1 := hgeo K
      have h2 := hnn K
      omega

/-- Bridge instance at the maximal AB rate (kappa = 1/4, S = log 2): if the launch
window excess is at most 245230 (= the C_max(1/4) reading capped inside the budget),
then the prefix sums never exceed 1541354 = floor(0.05137848 * D), for every K. -/
theorem bridgeInstance
    (hgeo : ∀ n, 30000000 * dhat (n + 1) ≤ 25226893 * dhat n)
    (hd0 : dhat 0 ≤ 245230) (hnn : ∀ n, 0 ≤ dhat n) (K : Nat) :
    sumTo dhat K ≤ 1541354 := by
  have h1 := geometricEnvelope hgeo hnn K
  have h2 := hnn K
  have h3 := hd0
  have h4 : 30000000 * 245230 ≤ 1541354 * 4773107 := by decide
  omega

#print axioms geometricEnvelope
#print axioms bridgeInstance

end DriftBridge
