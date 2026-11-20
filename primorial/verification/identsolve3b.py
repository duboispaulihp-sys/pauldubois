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

max_res = 0.0
neg_eps = 0
pos_diff = 0
leg1_ok = True
for k in range(2, n - 1):
    pk1 = primes[k]
    Xk = X[k]
    A = math.log(Xk); A1 = math.log(X[k + 1])
    r = 1.0 / (pk1 - 1.0)
    eps_k = (Pv[k] - eg * A) / eg
    eps_next = (Pv[k + 1] - eg * A1) / eg
    s = r * A - math.log(1.0 + math.log(pk1) / Xk)
    res = abs(eps_next - (1.0 + r) * eps_k - s)
    if res > max_res:
        max_res = res
    if eps_next < 0: neg_eps += 1
    u = math.log(pk1) / Xk
    u_next = math.log(primes[k + 1]) / X[k + 1]
    if u <= u_next:
        leg1_ok = False
    # x - H_{k+1} = eps_next*(u_next - u)/(u*u_next); sign = sign(eps_next)*sign(u_next-u)
    if eps_next * (u_next - u) > 0:
        pos_diff += 1
print(f"transport residual max: {max_res:.2e}")
print(f"eps_k < 0 count: {neg_eps} (of {n})")
print(f"u_k > u_{k+1} for all k in range: {leg1_ok}")
print(f"(x - H_(k+1)) > 0 count: {pos_diff}")
