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

print("k       u_k        u/2         u^2/2       |y|        err_s/(u^2/2) err_y/(u/2)  |y| vs (1+log p)|D|/(p log p)")
for k in [10, 100, 1000, 10**4, 10**5, 10**6, 2 * 10**6]:
    pk = primes[k - 1]; pk1 = primes[k]
    Xk = X[k]
    A = math.log(Xk); A1 = math.log(X[k + 1])
    g = math.log(pk1)
    u = g / Xk
    r = 1.0 / (pk1 - 1.0)
    Q = 1.0 + r
    s = r * A - math.log(1.0 + u)
    s_lin = r * A - u
    err_s = s - s_lin                      # expect +u^2/2 - u^3/3 + ...
    ratio_s = err_s / (u * u / 2.0)
    y = s / u
    y_lin = s_lin / u
    err_y = y - y_lin                      # expect +u/2 - u^2/3 + ...
    ratio_y = err_y / (u / 2.0)
    D = Xk - pk
    mainD = (1.0 + math.log(pk)) * abs(D) / (pk * math.log(pk))
    # series check: s - (rA - u + u^2/2 - u^3/3 + u^4/4)  ~  -u^5/5
    ser = r * A - u + u * u / 2.0 - u**3 / 3.0 + u**4 / 4.0
    print(f"{k:<8d} {u:.3e} {u/2:.3e}  {u*u/2:.3e}  {abs(y):.3e}  {ratio_s:+.6f}  {ratio_y:+.6f}   |y|/mainD = {abs(y)/mainD:.4f}   series resid {abs(s - ser):.1e}")

# error in x vs H_{k+1}: eps*(u_next-u)/(u*u_next), compare against u^2/2
print("\nk        x - H_{k+1}          u^2/2          |x-H|/u^2/2")
for k in [10, 100, 1000, 10**4, 10**5, 10**6, 2 * 10**6]:
    pk = primes[k - 1]; pk1 = primes[k]
    Xk = X[k]
    A = math.log(Xk); A1 = math.log(X[k + 1])
    g = math.log(pk1)
    u = g / Xk
    r = 1.0 / (pk1 - 1.0)
    Q = 1.0 + r
    eps_k = (Pv[k] - eg * A) / eg
    H_k = eps_k / u
    x = (Q * A - A1) / u + Q * H_k
    u_next = math.log(primes[k + 1]) / X[k + 1]
    eps_next = (Pv[k + 1] - eg * A1) / eg
    H_next = eps_next / u_next
    print(f"{k:<8d} {x - H_next:>14.4e}   {u*u/2:.3e}   {abs(x - H_next)/(u*u/2):.3e}")
