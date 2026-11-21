from math import log

k = 10**8
l0 = log(log(k))
LOGK = log(k)

# ---- 1. Exact partial sum S_J = sum_{i=1}^{J} ell_i/((k+i)(k+i+1)), J = 2e7, + asymptotic tail
J = 20_000_000
S = 0.0
for i in range(1, J+1):
    S += log(log(k+i))/((k+i)*(k+i+1))

# tail: (k+1)*int_J^inf ell(t)/((k+t)(k+t+1)) dt ~ (k+1)*[ ell(X)/(X) + 1/(X lg X)(1 - 1/lg X + 2/lg^2 X - 6/lg^3 X) ], X=k+J
X = k + J
lg = log(X)
ellX = log(lg)
tail1 = ellX/X
W = (1/lg)*(1 - 1/lg + 2/lg**2 - 6/lg**3)
tail = (k+1)/X*(ellX + W)
Theta = (k+1)*(S + (tail - tail1*0)/1)  # tail computed above already ~ integral approx incl. both parts
Theta = (k+1)*S + (k+1)/X*(ellX + W)
print(f"Theta_k = (k+1)*S_inf = {Theta:.9f}")
print(f"  components: S_J*(k+1) = {(k+1)*S:.9f}, tail-contribution = {(k+1)/X*(ellX+W):.9f}")
print(f"  asymptotic check: ell_0 + (1/log k)*(1-1/lg k+2/lg^2 k...) = {l0:.9f} vs Theta - ell_0 = {Theta-l0:.9f}")
th_mono  = 1 - log(log(k+1))
th_slope = 1 - Theta
th_above1= 1 - log(log(k+1))/(k+2)
print(f"thresholds: stay->1: {th_above1:.12f}   monotone: {th_mono:.12f}   slope>0: {th_slope:.12f}")

# ---- 2. closed form vs direct iteration (independent check), h0=5, j=2e5
def iterate(h0, Jit):
    phi = h0 - 1.0
    track = {}
    for j in range(1, Jit+1):
        phi = phi*(1 + 1/(k+j)) + log(log(k+j))/(k+j)
        if j == Jit: track['phi'] = phi
    return track['phi']
Jc = 200_000
phi_iter = iterate(5.0, Jc)
S_c = 0.0
for i in range(1, Jc+1):
    S_c += log(log(k+i))/((k+i)*(k+i+1))
phi_closed = ((k+Jc+1)/(k+1))*(5.0-1.0) + (k+Jc+1)*S_c
print(f"\nclosed-form check: phi_iter={phi_iter:.12f} phi_closed={phi_closed:.12f} diff={abs(phi_iter-phi_closed):.2e}")

# ---- 3. trajectory census for several h0 (decreasing-candidates iterated longer)
def census(h0, Jit):
    phi = h0 - 1.0
    d0 = phi + log(log(k+1))                       # Delta_0 = phi_0 + ell_1  (increment numerator at first step)
    prev = h0; downs = ups = 0; mn = h0; argmn = 0
    pts = {}
    for j in range(1, Jit+1):
        phi = phi*(1 + 1/(k+j)) + log(log(k+j))/(k+j)
        h = 1.0 + phi
        if h < prev: downs += 1
        elif h > prev: ups += 1
        if h < mn: mn, argmn = h, j
        prev = h
        if j in (10**5, 10**6, 10**7, 2*10**7): pts[j] = h
    return d0, ups, downs, mn, argmn, pts

print(f"\n{'h0':>7} {'Delta0':>10} {'ups':>7} {'downs':>7} {'min':>12} {'at j':>10} {'h(1e5)':>11} {'h(1e7)':>11} {'h(2e7)':>11}")
for h0, Jit in ((5.0,2_000_000),(1.0,2_000_000),(0.0,2_000_000),(-1.5,2_000_000),
                (-1.9,2_000_000),(-1.93,20_000_000),(-1.95,20_000_000),(-2.0,20_000_000),(-3.0,20_000_000)):
    d0, ups, downs, mn, argmn, pts = census(h0, Jit)
    print(f"{h0:>7} {d0:>10.6f} {ups:>7} {downs:>7} {mn:>12.6f} {argmn:>10} "
          f"{pts[10**5]:>11.5f} {pts[10**7]:>11.5f} {pts[2*10**7]:>11.5f}")

# ---- 4. simple predictor h_j ~ 1 + (1+j/k)(h0-1+Theta) - ell_{j+1} vs exact
for h0 in (5.0, -1.95):
    d0, ups, downs, mn, argmn, pts = census(h0, 20_000_000) if h0 < 0 else census(h0, 2_000_000)
    j = 2*10**7 if h0 < 0 else 2*10**6
    ell = log(log(k+j+1))
    pred = 1 + (1+j/k)*(h0-1+Theta) - ell
    ex = pts[j] if j in pts else None
    print(f"\nh0={h0}: predictor at j={j}: {pred:.6f}  vs exact {ex:.6f}  err={abs(pred-ex):.2e}")
    print(f"  healing: Delta0 + 1/log k (leading) = {d0 + 1/LOGK:.6f};  B_inf = h0-1+Theta = {h0-1+Theta:.6f}")
