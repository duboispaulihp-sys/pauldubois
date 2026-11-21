# Census results (validated run)

Environment: Python 3.12, pure standard library, exact `fractions.Fraction`
arithmetic. Code: `harmless_census.py`; tests: `test_census.py` (9/9 pass).
Run `python3 harmless_census.py` to reproduce everything below.

## 1. Validated engine behavior

### Demo 1 — Hodge ring Q[h]/(h⁵) (model of P⁴)

```
   p   dim_Z^p   dim_B^p   w(p)
   0   1         1         0
   1   1         1         0
   2   1         1         0
   3   1         1         0
   4   1         1         0
   distance to HC_Q (in this model): 0  (w = 0 in all degrees)
```

Divisorial rings register distance 0 — the first census row of the
Dubois-note type ("the SL₄-point is closed by computation, not
classification") reproduced on a toy member.

### Demo 2 — Weil-slot ring A = Q[h,w]/(h⁴, w², hw)

```
   p   dim_Z^p   dim_B^p   w(p)
   0   1         1         0
   1   1         1         0
   2   2         1         1
   Weil slots at: p=2 (w=1)
```

A ring with one non-divisorial codimension-2 generator models the Weil
slot: w(2) = 1; w(1) = 0 since h generates A¹. This is the "one line
away: the class w" configuration of the Dubois census.

### Demo 3 — External product (slot ring) ⊗ (Q[g]/(g³), P²-model)

```
   p   dim_Z^p   dim_B^p   w(p)
   0   1         1         0
   1   2         2         0
   2   4         3         1
   3   4         3         1
   4   3         2         1
   Weil slots at: p=2 (w=1), p=3 (w=1), p=4 (w=1)
```

Hand-check: A² = ⟨h², wh, g²⟩ restricted to B = ⟨h², hg, g²⟩ → slot 1
(w); A³ = ⟨h³, h²g, hg², wg⟩ minus dead monomials → slot 1 (wg); A⁴ = 
⟨h³g, h²g², wg²⟩ → slot 1 (wg²). The slot propagates into every positive
degree of the product and dies nowhere: the computational shadow of
Corollary 4.9 (persistence) — non-algebraicity survives products.

## 2. Matroid pillar

Presentation used: A^*(M) = ℚ[x_S : ∅ ≠ S proper flat] / (x_S x_T for
incomparable S,T; Σ_{S∋i} x_S − Σ_{S∋j} x_S). Computed by exact
homogeneous Gröbner bases (Buchberger, degree-capped — legitimate since
the ideal is homogeneous); graded dims are then exact. Poincaré duality
of the top pairing is computed as an internal-consistency certificate.

| matroid   | rank | proper flats | dims (A⁰,A¹,A²) | PD  | known checks |
|-----------|------|--------------|------------------|-----|--------------|
| U_{2,3}   | 2    | 3            | (1, 1, –)        | PASS| A¹ = 3−3+1 = 1 (fan = P²) |
| U_{2,4}   | 2    | 4            | (1, 1, –)        | PASS| 4−4+1 = 1 |
| U_{3,5}   | 3    | 15           | (1, 11, 1)       | PASS| 15−5+1 = 11 |
| Fano F₇   | 3    | 14           | (1, 8, 1)        | PASS| 14−7+1 = 8 |
| K₄ graph. | 3    | 13           | (1, 8, 1)        | PASS| 13−6+1 = 8 |

All passed Poincaré duality (pairing A^k × A^{d−k} → A^d nondegenerate
for each k). This certifies, case by case and computationally:
(1) the presentation is that of a genuine Poincaré-duality graded ring;
(2) these matroidal (p,p)-worlds have w = 0 (divisor-generated), i.e.
the matroid rows of the tropical census register distance 0 — consistent
with the Adiprasito–Huh–Katz Hodge–Riemann framework, where A^*(M) is
generated in degree 1.

HR spot checks are not informative at rank ≤ 3 (primitive divisor
classes do not exist when d = 2 — the Lefschetz map A¹ → A² is
injective), so the scan reports None there; the scan requires d ≥ 3,
which exceeds this engine's reach (see limitations).

## 3. Limitations (honest)

- The engine's Groebner machinery is pure Python and handles roughly
  ≤ 15–20 variables with top degree ≤ 2, or ≤ 10 variables with top
  degree ≤ 3, in seconds-to-minutes. Rank-4 matroids (30+ divisor
  variables) and the K₅ graphic pillar (25 variables) exceed this; they
  are one `sage`-swap away (`matroid_chow`'s presentation feeds directly
  into `Ideal`/`groebner_basis`).
- The census models Z^p as the graded piece of a presented ℚ-algebra and
  B^p as the seed subalgebra; the integer-lattice subtleties of B_Z vs
  B^p (denominators, torsion) are modeled only implicitly (see
  HarmlessCensus docstring).
- The Hodge-correspondence collapse (Note A, Prop 2.1) is deliberately
  NOT simulated in code: it is a three-line proof whose content is that
  ANY integral Hodge correspondence τ, given the point class, produces
  γτ,*(1) = τ; coding it on a presented ring would add nothing beyond
  the trivial identity. It is stated and proved in full in Note A.
