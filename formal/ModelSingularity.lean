namespace ModelSingularity

/-- 2^k >= k+1 : the doubling archimedean fact (gradient readings double every four windows). -/
theorem powTwoGe (k : Nat) : 2 ^ k ≥ k + 1 := by
  induction k with
  | zero => omega
  | succ k ih =>
      have h : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
      omega

/-- 4^k >= k+1 : the quartering archimedean fact (time gaps quarter every window). -/
theorem powFourGe (k : Nat) : 4 ^ k ≥ k + 1 := by
  induction k with
  | zero => omega
  | succ k ih =>
      have h : 4 ^ (k + 1) = 4 * 4 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
      omega

/-- Gradient divergence along the cascade: any monotone-in-doubling readings sequence
(G (k+1) >= 2 * G k, launched positive) eventually exceeds every bound. -/
theorem gradDiverges
    (G : Nat → Nat) (hgrow : ∀ k, G (k + 1) ≥ 2 * G k) (hg0 : G 0 ≥ 1) (B : Nat) :
    ∃ k, G k ≥ B := by
  induction B with
  | zero => exact ⟨0, by omega⟩
  | succ B ih =>
      obtain ⟨k, hk⟩ := ih
      have hg := hgrow k
      by_cases hb : B = 0
      · exact ⟨0, by omega⟩
      · exact ⟨k + 1, by omega⟩

/-- Time-gap vanishing: quartering gaps with positive launch gap pass below every
1/m threshold: exists k with Δ * m <= 4^k, i.e. Delta/4^k <= 1/m. -/
theorem gapVanishes (Δ m : Nat) (_hm : 0 < m) :
    ∃ k, Δ * m ≤ 4 ^ k := by
  refine ⟨Δ * m, ?_⟩
  have h := powFourGe (Δ * m)
  omega

#print axioms powTwoGe
#print axioms powFourGe
#print axioms gradDiverges
#print axioms gapVanishes

end ModelSingularity
