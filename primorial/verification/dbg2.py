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

X = [0.0] * (n + 1)
th = 0.0
for j, p in enumerate(primes):
    th += math.log(p)
    X[j + 1] = th

maxviol = 0.0
for k in range(2, n):
    pk = primes[k - 1]; pk1 = primes[k]
    Xk = X[k]
    A = math.log(Xk)
    u = math.log(pk1) / Xk
    r = 1.0 / (pk1 - 1.0)
    s = r * A - math.log1p(u)
    lb = r * A - u + u * u / 2.0 - u**3 / 3.0
    if s < lb:
        maxviol = max(maxviol, lb - s)
print(f"max LB violation magnitude: {maxviol:.3e}  (analytic interval width u^3/3 ~ 5e-20; float noise in u ~ 6e-20)")

for k in [10**3, 10**4, 10**5, 10**6, 2 * 10**6]:
    pk = primes[k - 1]; pk1 = primes[k]
    Xk = X[k]
    A = math.log(Xk)
    u = math.log(pk1) / Xk
    r = 1.0 / (pk1 - 1.0)
    s = r * A - math.log1p(u)
    G = pk1 - pk
    asym = ((1.0 + math.log(pk)) * (Xk - pk - G) + 0.5 * math.log(pk) ** 2) / (pk * pk)
    print(f"k={k:>8d}: s = {s:.6e}   asym = {asym:.6e}   rel.dev = {abs(s-asym)/abs(s):.2e}")
