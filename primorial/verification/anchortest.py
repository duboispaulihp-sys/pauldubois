import math

LIMIT = 35_000_000
sieve = bytearray(b'\x01') * (LIMIT + 1)
sieve[0:2] = b'\x00\x00'
i = 2
while i * i <= LIMIT:
    if sieve[i]:
        sieve[i*i::i] = b'\x00' * len(sieve[i*i::i])
    i += 1
primes = [i for i in range(2, LIMIT + 1) if sieve[i]]
n = len(primes)
eg = math.exp(0.5772156649015329)

X = [0.0] * (n + 1)
Pv = [0.0] * (n + 1)
th = 0.0
prod = 1.0
for j, p in enumerate(primes):
    th += math.log(p)
    prod *= p / (p - 1.0)
    X[j + 1] = th
    Pv[j + 1] = prod

def eps(kk):
    return (Pv[kk] - eg * math.log(X[kk])) / eg

K = 500_000                      # anchor index (p_K = 7,368,787)
Xk = X[K]
u = math.log(primes[K]) / Xk     # level-K scaling
A = math.log(Xk)
r = 1.0 / (primes[K] - 1.0)
Q = 1.0 + r
epsK = eps(K)
Hphys = epsK / u
print(f"anchor: p_K={primes[K]}, X_K={Xk:.2f}, u={u:.4e}, eps_K={epsK:.6e}, H_K={Hphys:.4f}")

# precompute per-step arrays for iteration j = K .. n-3
print("building step arrays ...")
ss = [0.0] * (n - 2)
rr = [0.0] * (n - 2)
for j in range(2, n - 2):
    rr[j] = 1.0 / (primes[j] - 1.0)
    ss[j] = rr[j] * math.log(X[j]) - math.log1p(math.log(primes[j]) / X[j])

def iterate(E0, seed_eps_mult):
    # chain: E_{j+1} = (1+rr[j]) E_j + ss[j], starting at index K with E0
    E = E0
    inv0 = (E0 - epsK) / Pv[K]     # invariant: E_j/P_j - eps_j/P_j = inv0
    worst_inv = 0.0
    cross = None
    j = K
    while j < n - 3:
        j += 1
        E = (1.0 + rr[j - 1]) * E + ss[j - 1]
        d = abs(E / Pv[j] - eps(j) / Pv[j] - inv0) / max(abs(inv0), 1e-30)
        if d > worst_inv:
            worst_inv = d
        if E <= 0 and cross is None:
            cross = j
            break
    return E, worst_inv, cross

# seed 1: physical
E, wi, cr = iterate(epsK, 1)
print(f"seed H=H_K (physical): no crossing={cr is None}, invariant rel err max={wi:.1e}")
# seed 2: E0 = epsK/2  (H = H_K/2)
E, wi, cr = iterate(epsK / 2, 0.5)
if cr:
    j = cr
    rho = primes[j] / primes[K] / (primes[j] / primes[K])
    rho = primes[j] / primes[K]
    print(f"seed H=H_K/2: crosses at j={j}, p={primes[j]}, rho={rho:.3f} "
          f"(predict ~3.44), inv rel err max={wi:.1e}")
else:
    print(f"seed H=H_K/2: no crossing yet, E_final={E:.3e}, inv err={wi:.1e}")
# seed 3: E0 = 1.5 epsK
E, wi, cr = iterate(1.5 * epsK, 1.5)
print(f"seed H=1.5 H_K: crossing={cr}, E_final/P ratio={E / Pv[n-4]:.3e} vs "
      f"predict {(0.5*epsK)/Pv[K]:.3e}, inv err={wi:.1e}")
# seed 4: near-physical
E, wi, cr = iterate(epsK * (1 - 1e-3), 0.999)
print(f"seed H=0.999 H_K: crossing={cr}, inv err={wi:.1e}")
