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

print("k        y=s/u         H1=eps_{k+1}/u   H2=eps_{k+2}/u   x=eps_{k+3}/u+corr   err_H2   err_x")
for k in [10, 100, 1000, 10**4, 10**5, 10**6]:
    Xk = X[k]
    A = math.log(Xk)
    u = math.log(primes[k]) / Xk
    r = 1.0 / (primes[k] - 1.0); Q = 1.0 + r
    H_k = eps(k) / u
    s = r * A - math.log1p(u)
    y = s / u
    E1 = s + Q * H_k * u
    H1 = E1 / u
    r1 = 1.0 / (primes[k + 1] - 1.0); Q1 = 1.0 + r1
    A1 = math.log(X[k + 1])
    H2 = (Q1 * (A1 + E1) - math.log(X[k + 2])) / u
    err_H2 = abs(H2 - eps(k + 2) / u) / abs(eps(k + 2) / u)
    r2 = 1.0 / (primes[k + 2] - 1.0); Q2 = 1.0 + r2
    A2 = math.log(X[k + 2])
    x = (Q2 * (A2 + H_k * u) - math.log(X[k + 3])) / u
    s2 = r2 * A2 - math.log1p(math.log(primes[k + 3]) / X[k + 2])
    x_alt = ((1.0 + r2) * eps(k) + s2) / u
    err_x = abs(x - x_alt) / abs(x)
    print(f"{k:<8d} {y:>12.4e} {H1:>13.4f} {H2:>13.4f} {x:>17.6f}   {err_H2:.1e}  {err_x:.1e}")

cH1 = cH2 = cx = cy = 0
for k in range(2, n - 3):
    Xk = X[k]
    A = math.log(Xk)
    u = math.log(primes[k]) / Xk
    r = 1.0 / (primes[k] - 1.0); Q = 1.0 + r
    s_ = r * A - math.log1p(u)
    E1 = s_ + Q * eps(k)
    H1 = E1 / u
    r1 = 1.0 / (primes[k + 1] - 1.0)
    A1 = math.log(X[k + 1])
    H2 = ((1.0 + r1) * (A1 + E1) - math.log(X[k + 2])) / u
    r2 = 1.0 / (primes[k + 2] - 1.0)
    A2 = math.log(X[k + 2])
    x = ((1.0 + r2) * (A2 + eps(k)) - math.log(X[k + 3])) / u
    if H1 <= 0: cH1 += 1
    if H2 <= 0: cH2 += 1
    if x <= 0: cx += 1
    if s_ >= 0: cy += 1
print(f"\ncensus k=2..{n-4}: H1<=0: {cH1}, H2<=0: {cH2}, x<=0: {cx}, s>=0 (y>=0): {cy}")
