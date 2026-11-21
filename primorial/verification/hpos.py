import math
k = 10**8
Theta = 2.965083464
checkpoints = [10**6, 10**7, 2*10**7, 3*10**7, 4*10**7]
recs = {}
s = 0.0
cross = None
kp1 = k + 1.0
for i in range(1, 4*10**7 + 1):
    t = k + i
    lt = math.log(t)
    s += math.log(lt)/(t*(t+1.0))
    if i in checkpoints:
        recs[i] = s
    if cross is None:
        B = -1.5 + kp1*s
        h = 1.0 + (1.0 + (i+1.0)/kp1)*B
        if h > 0:
            cross = (i, h)
print("h0=-0.5 first crossing:", cross)
print("j'acc at checkpoints:")
for j in checkpoints:
    acc = kp1*recs[j]
    fac = 1.0 + (j+1.0)/kp1
    h_th = 1.0 + fac*(-Theta + acc)     # threshold h0 = 1-Theta_k
    l_j = math.log(math.log(k + j))
    print(f"j={j:>9}: acc={acc:.6f}  h(threshold)={h_th:.6f}  -loglog(k+j)={-l_j:.6f}")
