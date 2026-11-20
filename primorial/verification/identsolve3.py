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

# 1-indexed: X[k] = log N_k = theta(p_k);  Pv[k] = prod_{p<=p_k} p/(p-1)
X = [0.0] * (n + 1)
Pv = [0.0] * (n + 1)
th = 0.0
prod = 1.0
for j, p in enumerate(primes):
    th += math.log(p)
    prod *= p / (p - 1.0)
    X[j + 1] = th
    Pv[j + 1] = prod

print("k        H_k          y=s/u          x             x*u-eps_next   x vs H_{k+1}   errs(y,x,eps)")
for k in [10, 100, 1000, 10**4, 10**5, 10**6, 2 * 10**6]:
    pk = primes[k - 1]; pk1 = primes[k]
    Xk = X[k]; g = math.log(pk1); u = g / Xk
    A = math.log(Xk); A1 = math.log(X[k + 1])
    r = 1.0 / (pk1 - 1.0); Q = 1.0 + r
    y = (Q * A - A1) / u
    err_y = abs((A1 + y * u) / A - Q) / Q
    s = r * A - math.log(1.0 + u)
    rel_sy = abs(y * u - s) / max(abs(s), 1e-300)
    eps_k = (Pv[k] - eg * A) / eg
    H_k = eps_k / u
    x = y + Q * H_k
    err_x = abs((A1 + x * u) / (A + H_k * u) - Q) / Q
    eps_next = (Pv[k + 1] - eg * A1) / eg
    err_eps = abs(x * u - eps_next) / abs(eps_next)
    u_next = math.log(primes[k + 1]) / X[k + 1]
    H_next = eps_next / u_next
    D = Xk - pk
    print(f"{k:<8d} {H_k:>12.6f} {y:>14.6e} {x:>13.6f} {err_eps:.1e}   {x - H_next:>12.4f}   "
          f"{err_y:.1e} {err_x:.1e}   y*u=s: {rel_sy:.1e}  D={D:.3f}")

# census: sign of s_k vs sign of D_k = theta(p_k) - p_k, over all k in range
neg_s = pos_s = 0
mismatch = 0
Ds = []
first_pos = None
for k in range(2, n + 1):
    pk = primes[k - 1]
    Xk = X[k]
    A = math.log(Xk); A1 = math.log(X[k])
    # s_k = (1+r)A - A1 with r = 1/(p_k - 1)  [transport step i -> i uses p at i, fine at index k]
    s = A * pk / (pk - 1.0) - A1
    # sign comparison handled below against D_k at same index
    Ds.append((s, Xk - pk))
for s, D in Ds:
    if s < 0: neg_s += 1
    else:
        pos_s += 1
        if first_pos is None:
            first_pos = True
    if (s < 0) != (D < 0):
        mismatch += 1
tot = neg_s + pos_s
print(f"\ncensus (k=2..{n}): s_k<0: {neg_s}, s_k>=0: {pos_s}, sign(s)!=sign(D): {mismatch}")
print(f"D_k=theta(p_k)-p_k >0 anywhere: {sum(1 for _, D in Ds if D > 0)}")
