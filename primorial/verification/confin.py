import math
k = 10**8
Theta = 2.965083464
# stored: acc_j = (k+1)*Sum_{i<=j} l_i/((k+i)(k+i+1))  from the hpos.py run
acc = {10**6: 0.028849, 10**7: 0.265092, 2*10**7: 0.486376, 3*10**7: 0.673905, 4*10**7: 0.834870}
def h(h0, j):
    Pj = (k+j+1)/(k+1)
    return 1 + Pj*(h0 - 1 + acc[j])
def lo(h0, j):  return 1 + (k+j+1)/(k+1)*(h0-1)
def hi(h0, j):  return 1 + (k+j+1)/(k+1)*(h0-1+Theta)
print("sandwich check  lo <= h <= hi, and delta_j = hi_j - h_j vs  l(k+j)+1/log(k+j)")
for h0 in [5.0, -1.93, -2.0, 1.0-Theta]:
    print(f"h0 = {h0}")
    for j in sorted(acc):
        hv, lv, uv = h(h0,j), lo(h0,j), hi(h0,j)
        d_j = uv - hv
        x0 = k+j
        approx = math.log(math.log(x0)) + 1/math.log(x0)
        ok = "OK" if (lv-1e-9 <= hv <= uv+1e-9) else "FAIL"
        print(f"  j={j:>9}: h={hv:>10.5f}  [{lv:>10.5f}, {uv:>10.5f}] {ok}   delta={d_j:.5f} vs l+1/L={approx:.5f}")
