import math
LIMIT = 35_000_000
sieve = bytearray(b'\x01')*(LIMIT+1); sieve[0:2]=b'\x00\x00'
i = 2
while i*i <= LIMIT:
    if sieve[i]: sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
    i += 1
primes = [i for i in range(2, LIMIT+1) if sieve[i]]
np_ = len(primes)
# Xs[j+1] = theta(p_j): true X_j = Xs[j+1]
Xs = [0.0]*(np_+2)
theta = 0.0
for jj in range(1, np_+1):
    theta += math.log(primes[jj-1])
    Xs[jj+1] = theta
# X_true[j] = Xs[j+1];  g_j = log p_{j+1} = log(primes[j])
# exact test: u_{k+1} > u_{2k}:  log(p_{k+2}) * X_{2k} > log(p_{2k+1}) * X_{k+1}
viol = 0; minm = 1.0; argm = 0
minnu = 1e9; argnu = 0
lrmax = 0.0; argl = 0
for k in range(2, 10**6+1):
    gk1 = math.log(primes[k+1])       # log p_{k+2}
    g2k = math.log(primes[2*k])       # log p_{2k+1}
    Xk1 = Xs[k+2]; X2k = Xs[2*k+1]
    lhs = gk1*X2k; rhs = g2k*Xk1
    if lhs <= rhs: viol += 1
    m = (lhs-rhs)/lhs
    if m < minm: minm, argm = m, k
    nu = (X2k - Xk1)*gk1/(Xk1*(g2k-gk1))
    if nu < minnu: minnu, argnu = nu, k
    lr = g2k - gk1
    if lr > lrmax: lrmax, argl = lr, k
print(f"leg2 EXACT (u_(k+1) > u_(2k), 2<=k<=1e6): violations={viol}, min rel margin={minm:.5f} at k={argm}")
print(f"sufficient-bound nu: min={minnu:.4f} at k={argnu}")
print(f"sup (g_(2k)-g_(k+1)) = log(p_(2k+1)/p_(k+2)) = {lrmax:.5f} at k={argl} (ratio {math.exp(lrmax):.4f})")
