namespace DriftCritical

/-- Prefix sum of the window sequence: sumTo f K = f 0 + ... + f (K-1). -/
def sumTo (f : Nat → Int) : Nat → Int
  | 0 => 0
  | K + 1 => sumTo f K + f K

variable {dhat chat : Nat → Int}

/-- Definitional step equation for sumTo. -/
theorem sumToStep (f : Nat → Int) (K : Nat) : sumTo f (K + 1) = sumTo f K + f K := rfl

/-- The exact 1000/999 accounting identity under the coupling recursion
D * dhat(n+1) = Q * dhat n + D * chat n (D = 30000000, Q = 30000), valid at
every window K: (D - Q) * sumTo dhat K + D * dhat K = D * (dhat 0 + sumTo chat K).
This is the feedback telescoping: the prefix sums of the response are exactly
(1000/999) times (launch + released source), minus the boundary correction
D * dhat K that keeps every finite prefix at or below the limit value. -/
theorem telescope
    (hexact : ∀ n, 30000000 * dhat (n + 1) = 30000 * dhat n + 30000000 * chat n)
    (K : Nat) :
    29970000 * sumTo dhat K + 30000000 * dhat K
      = 30000000 * (dhat 0 + sumTo chat K) := by
  induction K with
  | zero =>
      have e1 : sumTo dhat 0 = 0 := rfl
      have e2 : sumTo chat 0 = 0 := rfl
      omega
  | succ m ih =>
      have eD : sumTo dhat (m + 1) = sumTo dhat m + dhat m := rfl
      have eC : sumTo chat (m + 1) = sumTo chat m + chat m := rfl
      have hx : 30000000 * dhat (m + 1) = 30000 * dhat m + 30000000 * chat m := hexact m
      omega

/-- Source potential at the exact critical ratio of anchor 1:
if the source contracts at ratio at most 250406323/269906323 per window, then
19500000 * sumTo chat K + 269906323 * chat K <= 269906323 * chat 0 at every
window K, so the total released source is at most
269906323 * chat 0 / 19500000. -/
theorem chatBound1
    (hle : ∀ n, 269906323 * chat (n + 1) ≤ 250406323 * chat n) (K : Nat) :
    19500000 * sumTo chat K + 269906323 * chat K ≤ 269906323 * chat 0 := by
  induction K with
  | zero =>
      have e : sumTo chat 0 = 0 := rfl
      omega
  | succ m ih =>
      have eC : sumTo chat (m + 1) = sumTo chat m + chat m := rfl
      have hx : 269906323 * chat (m + 1) ≤ 250406323 * chat m := hle m
      omega

/-- Source potential at the exact critical ratio of anchor 2:
if the source contracts at ratio at most 703318937/742318937 per window, then
39000000 * sumTo chat K + 742318937 * chat K <= 742318937 * chat 0 at every
window K. -/
theorem chatBound2
    (hle : ∀ n, 742318937 * chat (n + 1) ≤ 703318937 * chat n) (K : Nat) :
    39000000 * sumTo chat K + 742318937 * chat K ≤ 742318937 * chat 0 := by
  induction K with
  | zero =>
      have e : sumTo chat 0 = 0 := rfl
      omega
  | succ m ih =>
      have eC : sumTo chat (m + 1) = sumTo chat m + chat m := rfl
      have hx : 742318937 * chat (m + 1) ≤ 703318937 * chat m := hle m
      omega

/-- Source potential at the exact critical ratio of anchor 3:
if the source contracts at ratio at most 443542993/463042993 per window, then
19500000 * sumTo chat K + 463042993 * chat K <= 463042993 * chat 0 at every
window K. -/
theorem chatBound3
    (hle : ∀ n, 463042993 * chat (n + 1) ≤ 443542993 * chat n) (K : Nat) :
    19500000 * sumTo chat K + 463042993 * chat K ≤ 463042993 * chat 0 := by
  induction K with
  | zero =>
      have e : sumTo chat 0 = 0 := rfl
      omega
  | succ m ih =>
      have eC : sumTo chat (m + 1) = sumTo chat m + chat m := rfl
      have hx : 463042993 * chat (m + 1) ≤ 443542993 * chat m := hle m
      omega

/-- criticalNever1: the boundary of the dichotomy at anchor 1. Under the exact
coupling recursion, with the launch at its cap (dhat 0 <= 1000000), the source
floor at its cap (chat 0 <= 39000), and the source contracting at ratio at most
the exact critical 250406323/269906323 = 0.927753 per window, the prefix sums
never exceed the budget head 1541354, at ANY window K. The certificate is exact:
the boundary identity 29970000 * 19500000 * 1541354
= 30000000 * (19500000 * 1000000 + 269906323 * 39000) holds with equality, so
the head is saturated in the limit but never breached. -/
theorem criticalNever1
    (hexact : ∀ n, 30000000 * dhat (n + 1) = 30000 * dhat n + 30000000 * chat n)
    (hle : ∀ n, 269906323 * chat (n + 1) ≤ 250406323 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (hnn : ∀ n, 0 ≤ dhat n) (hnt : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K ≤ 1541354 := by
  have htel := telescope hexact K
  have hbc := chatBound1 hle K
  have hB := hnn K
  have hF := hnt K
  omega

/-- criticalNever2: the boundary of the dichotomy at anchor 2. Same hypotheses
with the exact critical ratio 703318937/742318937 = 0.947462 per window; the
prefix sums never exceed the budget head 1744063, at any window K. -/
theorem criticalNever2
    (hexact : ∀ n, 30000000 * dhat (n + 1) = 30000 * dhat n + 30000000 * chat n)
    (hle : ∀ n, 742318937 * chat (n + 1) ≤ 703318937 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (hnn : ∀ n, 0 ≤ dhat n) (hnt : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K ≤ 1744063 := by
  have htel := telescope hexact K
  have hbc := chatBound2 hle K
  have hB := hnn K
  have hF := hnt K
  omega

/-- criticalNever3: the boundary of the dichotomy at anchor 3. Same hypotheses
with the exact critical ratio 443542993/463042993 = 0.957887 per window; the
prefix sums never exceed the budget head 1928014, at any window K. -/
theorem criticalNever3
    (hexact : ∀ n, 30000000 * dhat (n + 1) = 30000 * dhat n + 30000000 * chat n)
    (hle : ∀ n, 463042993 * chat (n + 1) ≤ 443542993 * chat n)
    (hd0 : dhat 0 ≤ 1000000) (hc0 : chat 0 ≤ 39000)
    (hnn : ∀ n, 0 ≤ dhat n) (hnt : ∀ n, 0 ≤ chat n) (K : Nat) :
    sumTo dhat K ≤ 1928014 := by
  have htel := telescope hexact K
  have hbc := chatBound3 hle K
  have hB := hnn K
  have hF := hnt K
  omega

#print axioms telescope
#print axioms chatBound1
#print axioms chatBound2
#print axioms chatBound3
#print axioms criticalNever1
#print axioms criticalNever2
#print axioms criticalNever3

end DriftCritical
