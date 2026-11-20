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

print("k        y_new=s/u        y_old=(eps_{k+1}-2s)/u   eps_{k+1}      2s_k           margin")
for k in [10, 100, 1000, 10**4, 10**5, 10**6, 2 * 10**6]:
    pk = primes[k - 1]; pk1 = primes[k]
    Xk = X[k]
    A = math.log(Xk); A1 = math.log(X[k + 1])
    u = math.log(pk1) / Xk
    r = 1.0 / (pk1 - 1.0); Q = 1.0 + r
    s = r * A - math.log(1.0 + u)
    eps_next = (Pv[k + 1] - eg * A1) / eg
    y_new = s / u
    y_old = (eps_next - 2.0 * s) / u
    print(f"{k:<8d} {y_new:>13.4e}  {y_old:>16.6f}  {eps_next:>12.4e}  {2*s:>13.4e}  {eps_next - 2*s:.4e}")

c_nnew = c_pold = c_mold = 0
min_margin = 1e300
for k in range(2, n - 1):
    pk = primes[k - 1]
    A = math.log(X[k]); A1 = math.log(X[k + 1])
    u = math.log(primes[k]) / X[k]
    r = 1.0 / (primes[k] - 1.0)
    s = r * A - math.log(1.0 + u)
    eps_next = (Pv[k + 1] - eg * A1) / eg
    if y_c := (s >= 0): pass
    if s >= 0: c_nnew += 1
    margin = eps_next - 2.0 * s
    if margin <= 0: c_mold += 1
    if margin < min_margin: min_margin = margin
print(f"\ncensus k=2..{n-2}:  y_new = s_k/u_k >= 0 count: {c_nnew}   margin eps_(k+1)-2s_k <= 0 count: {c_mold}")
print(f"min margin: {min_margin:.4e}")
