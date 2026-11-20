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

bad_ub = bad_lb = 0
asym_max = 0.0
asym_at = 0
for k in range(2, n):
    pk = primes[k - 1]; pk1 = primes[k]
    Xk = X[k]
    A = math.log(Xk)
    u = math.log(pk1) / Xk
    r = 1.0 / (pk1 - 1.0)
    s = r * A - math.log(1.0 + u)
    ub = r * A - u + u * u / 2.0
    lb = r * A - u + u * u / 2.0 - u**3 / 3.0
    if not (lb <= s <= ub): 
        if s > ub: bad_ub += 1
        else: bad_lb += 1
    G = pk1 - pk
    asym = ((1.0 + math.log(pk)) * (Xk - pk - G) + 0.5 * math.log(pk) ** 2) / (pk * pk)
    if abs(s - asym) > asym_max:
        asym_max = abs(s - asym)
        asym_at = k
print(f"alternating bound violations: above-UB: {bad_ub}, below-LB: {bad_lb} (of {n-2})")
print(f"max |s - asymptotic| : {asym_max:.3e} at k={asym_at}")
