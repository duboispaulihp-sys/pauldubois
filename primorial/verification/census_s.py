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

neg_s = pos_s = mismatch = neg_D = 0
smin = 1e300
smax = -1e300
for k in range(2, n):
    pk = primes[k - 1]
    A = math.log(X[k]); A1 = math.log(X[k + 1])
    s = A * primes[k] / (primes[k] - 1.0) - A1   # transport step s_k, k -> k+1
    D = X[k] - pk
    if s < 0: neg_s += 1
    else: pos_s += 1
    if D < 0: neg_D += 1
    if (s < 0) != (D < 0): mismatch += 1
    if s < smin: smin = s
    if s > smax: smax = s
tot = neg_s + pos_s
print(f"k=2..{n-1}: s<0: {neg_s}, s>=0: {pos_s}, sign mismatch: {mismatch}, D<0: {neg_D}")
print(f"s range: [{smin:.3e}, {smax:.3e}]")
