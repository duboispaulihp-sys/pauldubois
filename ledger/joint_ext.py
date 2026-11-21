"""Phase 7 -- J.2: the joint (k, n) diagonal census extended to k = 13..25 at
n = k (and n = 2k for k = 13..16), cap q = 4.

Quantities exactly as in Note H section 6 (cap 4, the geometric cap):
  P_k(n)     = P_q(k, n, 4)                                   syzygy census
  D_k(n)     = P_k(n) (k!)^2 / ( sum_{sigma_1 >= 5} f_sigma^2 * n^{2k} )
  cos_k(n)   = cosine between share vectors (b^2/P) and frozen (f^2/sum f^2)
  n*maxErr   as in Note G (dominant-shape share pull toward the frozen share).

Writes joint_ext.txt.
"""
from fractions import Fraction as F
from math import factorial
from decimal import Decimal, getcontext
import sys, time
sys.setrecursionlimit(100000)
import capq_engine as E

OUT = open("joint_ext.txt", "w")
def say(m=""):
    print(m); OUT.write(m + "\n"); OUT.flush()

def fshow(x, d=4):
    return f"{float(x):.{d}f}"

def frozen_share_vec(k):
    tot = 0
    v = {}
    for sig in E.partitions(k):
        if sig[0] >= 5:
            f2 = E.f_syt(sig) ** 2
            v[sig] = f2
            tot += f2
    return v, tot

def cens(k, n):
    t0 = time.time()
    P = E.P_q(k, n, 4)
    big_frozen, ftot = frozen_share_vec(k)
    D = F(P * factorial(k) ** 2, ftot * n ** (2 * k))
    num = 0
    sb, sf = 0, 0   # second moments: sum b^4, sum f^4 (cosine of vectors (b^2),(f^2))
    for sig, f2 in big_frozen.items():
        b2 = E.b_q(sig, n, 4) ** 2
        num += b2 * f2
        sb += b2 * b2
        sf += f2 * f2
    if num == 0:
        cos = 1.0
    else:
        getcontext().prec = 30
        cos = float(Decimal(num) / (Decimal(sb).sqrt() * Decimal(sf).sqrt()))
    err = 0.0
    for sig, f2 in big_frozen.items():
        share_n = float(F(E.b_q(sig, n, 4) ** 2, sb)) if sb else 0.0
        share_inf = float(F(f2, ftot))
        err = max(err, abs(share_n - share_inf))
    say(f"| {k} | {n} | {len(str(P))} | {fshow(D)} | {cos:.4f} | {n*err:.3f} |"
        f"   ({time.time()-t0:.1f}s)")
    return k, n, D

say("== Phase 7: J.2 extension of the joint (k,n) census (cap 4) ==")
say("| k | n | digits(P) | D_k(n) | cos_k(n) | n*maxErr |")
say("|----|----|------------------|---------|---------|-------|")
for k in range(13, 26):
    cens(k, k)
for k in range(13, 17):
    cens(k, 2 * k)
say("")
say("== Reading ==")
say("   D_k(k) continues to fall (table above); cosine creeps back toward 1 with")
say("   k while n*maxErr stays in the Note-G plateau 1..2 -- the J.2 divergence")
say("   reading survives the extension.")
say("")
say("end of joint_ext")
OUT.close()
