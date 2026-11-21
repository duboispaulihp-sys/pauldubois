#!/usr/bin/env python3
"""chainform.py -- does the chained constant-offset two-form close onto the
anchored transport chain (Theorem 8)?

Family under test (one identity per line i = 1, 2, 3, ...):

    p_{k+i}/(p_{k+i}-1) = (A_{k+i} - H_i - c_i)/(A_{k+i-1} - H_{i-1} - c_{i-1}),
    c_j = log(p_{k+j}/log N_k) = log p_{k+j} - A_k.

Two readings of the offset (cmodes):
    "shared" : c_j = c_1 for every line (including the seed line, c_0 := c_1);
    "perline": c_j = log p_{k+j} - A_k on line j (c_0 := c_1 for the seed).

Two H-conventions (modes), i.e. two ways to write B_i := A - scale*H - c:
    "uscaled": scale = u_k  (H in fixed anchor units; physical chain: u_k H = eps)
    "bare"   : scale = 1    (H in physical units;      physical chain: H = eps/u_k)

The identity asserts B_i = Q_{k+i-1} B_{i-1} with Q = p_{k+i}/(p_{k+i}-1),
hence B_i = B_0 * prod_{j<i} Q  -- a "phantom chain" that silently discards
the accumulated residual.  On the TRUE anchored chain (physical seed
H_0 = eps_k/u_k at fixed scale u_k, so H_j = eps_{k+j}/u_k exactly, with the
transport law eps_{n+1} = (1+r_n) eps_n + s_n, s_n = r_n A_n - log1p(u_n))
the residuals of the asserted identity are exactly, at true index n = k+j-1:

    uscaled, shared:  beta2_j = -2 s_n + c_1 r_n
    bare,    shared:  beta1_j = -s_n (1 + 1/u_k) + c_1 r_n
    perline        :  same cores, c-part  -c_j + Q c_{j-1}  with
                      c_j = log p_{k+j} - A_k  (c_0 := c_1 on the seed line).

So the constant-offset family is an eps-scale approximation, not a closure;
the script measures the residuals, the phantom chains

    H^def_i = (A_{k+i} - c_i - B_0 * prod_{j<i}(1+r)) / scale,

and the true chain H_j = eps_{k+j}/u_k for seeds {H_k, H_k-5, H_k-20, 0,
-1000}, reporting first sign flips.

Passes:
    cheap: anchors k in {1e3, 1e4, 1e5, 1e6}, windows <= 1.5e6 (sieve to 3.5e7);
    deep : anchor K = 1e8, window W = 5e6 (segmented sieve to 2.2e9), anchor
           data cross-checked against h1_at_1e8_results.txt.

Pure Python 3, no dependencies.
"""

import math
import os
import time
from math import isqrt, log, log1p

EULER_GAMMA = 0.5772156649015328606065
INV_E_GAMMA = math.exp(-EULER_GAMMA)

LIMIT_CHEAP = 35_000_000
CHEAP_CFG = ((1_000, 1_500_000), (10_000, 1_500_000),
             (100_000, 1_500_000), (1_000_000, 1_000_000))
SEG_SPAN = 100_000_000

DEEP_LIMIT = 2_200_000_000
DEEP_K = 100_000_000
DEEP_W = 5_000_000
DEEP_CHECKS = (1, 2, 1_000, 10_000, 100_000, 1_000_000, 5_000_000)

CERT = {
    "p_K": 2038074743,
    "X_K": 2038030124.4153652,
    "A_K": 21.435249552999508,
    "u_K": 1.0517642105918211e-08,
    "r_K": 4.906591379928533e-10,
    "s_K": -2.409822713811072e-13,
    "eps_K": 4.346192849735457e-05,
    "H_K": 4132.288212478614,
}
CERT_TOL = 1e-6

VARIANTS = ("uscaled", "bare")
CMODES = ("shared", "perline")

T0 = time.time()
OUT = []


def stamp():
    return "[%7.1fs]" % (time.time() - T0)


def out(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


def rel(a, b):
    return abs(a - b) / abs(b) if b else abs(a - b)


def primes_upto(limit):
    """Plain odd sieve; yields all primes p <= limit."""
    if limit < 2:
        return
    yield 2
    if limit < 3:
        return
    size = (limit - 1) // 2
    sieve = bytearray([1]) * (size + 1)
    sieve[0] = 0
    i = 1
    while True:
        v = 2 * i + 1
        if v * v > limit:
            break
        if sieve[i]:
            start = (v * v - 1) // 2
            sieve[start::v] = bytearray(len(range(start, size + 1, v)))
        i += 1
    for i in range(1, size + 1):
        if sieve[i]:
            yield 2 * i + 1


def window_primes(a, e, base):
    """All primes in [a, e] with a odd >= 3, given base primes for marking."""
    size = (e - a) // 2 + 1
    sieve = bytearray([1]) * size
    for q in base:
        if q == 2:
            continue
        if q * q > e:
            break
        start = q * q
        if start < a:
            start = ((a + q - 1) // q) * q
        if start % 2 == 0:
            start += q
        i0 = (start - a) // 2
        if i0 < size:
            sieve[i0::q] = bytearray(len(range(i0, size, q)))
    res = []
    for i in range(size):
        if sieve[i]:
            res.append(a + 2 * i)
    return res


def primes_theta(limit, seg_span):
    """Yield (n, p, lp, X_prev): the n-th prime (n = 1, 2, ...) with
    X_prev = theta(p_{n-1}); theta is re-anchored per segment through
    math.fsum over per-segment exact partial sums (Neumaier-safe)."""
    base = list(primes_upto(isqrt(limit) + 1))
    lp2 = math.log(2.0)
    parts = [lp2]
    closed = math.fsum(parts)
    n = 1
    yield (1, 2, lp2, 0.0)
    a = 3
    while a <= limit:
        e = min(a + seg_span - 2, limit)
        seg = []
        partial = 0.0
        for p in window_primes(a, e, base):
            lp = math.log(p)
            yield (n + 1, p, lp, closed + partial)
            seg.append(lp)
            partial += lp
            n += 1
        if seg:
            parts.append(math.fsum(seg))
            closed = math.fsum(parts)
        a = e + 2


def run_walk(gen, walks, tag):
    active = list(walks)
    lv = 0.0
    lvc = 0.0
    for (n, p, lp, x_prev) in gen:
        y = log1p(1.0 / (p - 1.0))
        t = lv + y
        if abs(lv) >= abs(y):
            d = (lv - t) + y
        else:
            d = (y - t) + lv
        lv = t
        lvc += d
        lvt = lv + lvc
        for w in active:
            w.process(n, p, lp, x_prev, lvt)
    for w in walks:
        w.state = 2


class AnchorWalk:
    """One anchor k with a window of W steps through the prime stream."""

    def __init__(self, k, w):
        self.k = k
        self.w = w
        self.state = 0          # 0 waiting, 1 live, 2 done
        self.checkpoints = ()
        self.p_k = 0
        self.x_k = 0.0
        self.a_k = 0.0
        self.eps_k = 0.0
        self.lp_next = 0.0
        self.c1 = 0.0
        self.u_k = 0.0
        self.r_1 = 0.0
        self.s_1 = 0.0
        self.h0 = 0.0
        self.h_c = 0.0
        self.pi_w = 1.0
        self.eps = 0.0
        self.gp_prev = 0.0
        self.b_prev = None
        self.seeds = ()
        self.ph_t = {}
        self.ph_info = {}
        self.tr = {}
        self.h_true_last = 0.0
        self.stats = {(v, cm): [0, None, None, None, None]
                      for v in VARIANTS for cm in CMODES}
        self.errmax = {(v, cm): 0.0 for v in VARIANTS for cm in CMODES}
        self.first3 = []
        self.cp_rows = {}

    def process(self, n, p, lp, x_prev, lv):
        if self.state == 0:
            if n != self.k:
                return
            self.p_k = p
            self.x_k = x_prev + lp
            self.a_k = log(self.x_k)
            self.eps_k = math.exp(lv) * INV_E_GAMMA - self.a_k
            self.gp_prev = lp
            self.eps = self.eps_k
            self.pi_w = 1.0
            self.state = 1
            return
        if self.state != 1:
            return
        j = n - self.k
        if j > self.w:
            self.state = 2
            return

        a_prev = log(x_prev)
        u = lp / x_prev
        r = 1.0 / (p - 1.0)
        q = 1.0 + r
        l1u = log1p(u)
        s = r * a_prev - l1u
        a_new = log(x_prev + lp)
        eps_new = q * self.eps + s
        h_true = eps_new / u if j == 1 else eps_new / self.u_k

        if j == 1:
            self.c1 = lp - self.a_k
            self.u_k = u
            self.r_1 = r
            self.s_1 = s
            self.h0 = self.eps_k / u
            self.h_c = -s / (r * u)
            self.lp_next = lp
            seeds = [self.h0, self.h0 - 5.0, self.h0 - 20.0, 0.0, -1000.0]
            sd = []
            seen = set()
            for s0 in seeds:
                if s0 not in seen:
                    seen.add(s0)
                    sd.append(s0)
            self.seeds = tuple(sd)
            for mode in VARIANTS:
                sc = u if mode == "uscaled" else 1.0
                for seed in self.seeds:
                    self.ph_t[(mode, seed)] = self.a_k - sc * seed - self.c1
                    for cm in CMODES:
                        self.ph_info[(mode, cm, seed)] = [None, None]
            for seed in self.seeds:
                self.tr[seed] = [seed - self.h0, None]
            b0s = self.a_k - self.eps_k - self.c1
            b0b = self.a_k - self.h0 - self.c1
            self.b_prev = {("uscaled", "shared"): b0s,
                           ("uscaled", "perline"): b0s,
                           ("bare", "shared"): b0b,
                           ("bare", "perline"): b0b}

        self.eps = eps_new
        self.pi_w *= q
        self.h_true_last = h_true

        b_now = {}
        for cm in CMODES:
            c_j = self.c1 if cm == "shared" else (lp - self.a_k)
            b_now[("uscaled", cm)] = a_new - eps_new - c_j
            b_now[("bare", cm)] = a_new - h_true - c_j

        core2 = l1u - r * a_prev - s
        core1 = l1u - r * a_prev - s / self.u_k
        row = {}
        for cm in CMODES:
            if cm == "shared":
                rc = self.c1 * r
            else:
                c_prev = self.c1 if j == 1 else (self.gp_prev - self.a_k)
                rc = -(lp - self.a_k) + q * c_prev
            for variant, core in (("uscaled", core2), ("bare", core1)):
                pred = core + rc
                meas = b_now[(variant, cm)] - q * self.b_prev[(variant, cm)]
                st = self.stats[(variant, cm)]
                st[0] += 1
                if st[1] is None or pred < st[1]:
                    st[1] = pred
                if st[2] is None or pred > st[2]:
                    st[2] = pred
                if st[3] is None or meas < st[3]:
                    st[3] = meas
                if st[4] is None or meas > st[4]:
                    st[4] = meas
                e = abs(meas - pred)
                if e > self.errmax[(variant, cm)]:
                    self.errmax[(variant, cm)] = e
                row[(variant, cm)] = (meas, pred)
        self.b_prev = b_now
        self.gp_prev = lp

        for key in self.ph_t:
            self.ph_t[key] *= q
        for (mode, cm, seed), info in self.ph_info.items():
            t = self.ph_t[(mode, seed)]
            c_ph = self.c1 if cm == "shared" else (lp - self.a_k)
            scale = self.u_k if mode == "uscaled" else 1.0
            hph = (a_new - c_ph - t) / scale
            info[1] = hph
            if info[0] is None and hph <= 0.0:
                info[0] = j
        for seed, ent in self.tr.items():
            ent[0] *= q
            if ent[1] is None and h_true + ent[0] <= 0.0:
                ent[1] = j

        if j <= 3:
            row["eps_direct"] = math.exp(lv) * INV_E_GAMMA - a_new
            row["eps_prop"] = eps_new
            self.first3.append((j, dict(row)))
        if j in self.checkpoints:
            r_ = {"H_true": h_true}
            for key in (("uscaled", "shared", self.h0),
                        ("bare", "shared", self.h0),
                        ("uscaled", "perline", self.h0),
                        ("bare", "perline", self.h0),
                        ("uscaled", "shared", 0.0),
                        ("bare", "shared", 0.0)):
                r_[key] = self.ph_info[key][1]
            self.cp_rows[j] = r_

    def report(self, deep):
        k, w = self.k, self.w
        out("")
        out("== anchor k = %d, window W = %d ==" % (k, w))
        out("p_k = %d" % self.p_k)
        out("X_k = theta(p_k)          = %.17g" % self.x_k)
        out("A_k = log X_k             = %.17g" % self.a_k)
        out("eps_k = P~/e^gamma - A_k  = %.17g" % self.eps_k)
        out("u_k = log p_(k+1)/X_k     = %.17g  (log p_(k+1) = %.17g)"
            % (self.u_k, self.lp_next))
        out("r_1 = 1/(p_(k+1)-1)       = %.17g" % self.r_1)
        out("s_1 = r A_k - log1p(u_k)  = %.17g" % self.s_1)
        out("H_c(k) = -s_1/(r_1 u_k)   = %.17g" % self.h_c)
        out("H_phys(k) = eps_k/u_k     = %.17g" % self.h0)
        out("Theta prod P_W = prod (1+r) over window = %.17g" % self.pi_w)
        out("")
        out("residuals beta_j = B_j - Q B_(j-1) of the proposed two-form on the")
        out("true chain (measured) vs exact closed forms (predicted):")
        out("  variant   cmode      n        pred_min          pred_max          "
            "meas_min          meas_max          max|meas-pred|")
        for variant in VARIANTS:
            for cm in CMODES:
                st = self.stats[(variant, cm)]
                out("  %-8s  %-8s  %6d  %+.6e  %+.6e  %+.6e  %+.6e  %.3e"
                    % (variant, cm, st[0], st[1], st[2], st[3], st[4],
                       self.errmax[(variant, cm)]))
        if deep:
            out("")
            out("exact residuals for the first three steps (measured vs predicted):")
            for (j, row) in self.first3:
                out(" step j = %d:" % j)
                for variant in VARIANTS:
                    for cm in CMODES:
                        meas, pred = row[(variant, cm)]
                        out("   %-8s %-8s  meas %+.17e  pred %+.17e  diff %+.2e"
                            % (variant, cm, meas, pred, meas - pred))
                out("   eps check: transported %+.17e vs direct sieve %+.17e (diff %+.2e)"
                    % (row["eps_prop"], row["eps_direct"],
                       row["eps_direct"] - row["eps_prop"]))
        if self.cp_rows:
            out("")
            out("checkpoint values (H_true = eps_(k+j)/u_k true chain; H_def = phantom):")
            for j, r_ in sorted(self.cp_rows.items()):
                out(" step j = %d: H_true = %+.17e" % (j, r_["H_true"]))
                out("   (uscaled,shared,H_k)   = %+.17e   (bare,shared,H_k)   = %+.17e"
                    % (r_[("uscaled", "shared", self.h0)],
                       r_[("bare", "shared", self.h0)]))
                out("   (uscaled,perline,H_k)  = %+.17e   (bare,perline,H_k)  = %+.17e"
                    % (r_[("uscaled", "perline", self.h0)],
                       r_[("bare", "perline", self.h0)]))
                out("   (uscaled,shared,0)     = %+.17e   (bare,shared,0)     = %+.17e"
                    % (r_[("uscaled", "shared", 0.0)],
                       r_[("bare", "shared", 0.0)]))
        out("")
        out("phantom chains H_def (family closure), first flip j (None = none in window):")
        out("  seed              mode      cmode      flip_j   H_def at last step")
        for variant in VARIANTS:
            for cm in CMODES:
                for seed in self.seeds:
                    info = self.ph_info[(variant, cm, seed)]
                    out("  %-17s  %-8s  %-8s  %6s   %+.6e"
                        % ("%.10g" % seed, variant, cm,
                           str(info[0]) if info[0] is not None else "none",
                           info[1]))
        out("")
        out("true anchored chain (Theorem 8, seeds; first flip j or none):")
        for seed in self.seeds:
            ent = self.tr[seed]
            out("  seed %-17s  flip_j %s"
                % ("%.10g" % seed,
                   str(ent[1]) if ent[1] is not None else "none"))


def certify(walk):
    out("")
    out("== certification of the K = 1e8 anchor against h1_at_1e8_results.txt ==")
    ok_all = True
    if walk.p_k == CERT["p_K"]:
        out("  p_K = %d  PASS (the 1e8-th prime matches the certified value exactly)"
            % walk.p_k)
    else:
        ok_all = False
        out("  p_K = %d  FAIL (certified %d)" % (walk.p_k, CERT["p_K"]))
    for name in ("X_K", "A_K", "u_K", "r_K", "s_K", "eps_K", "H_K"):
        got = {"X_K": walk.x_k, "A_K": walk.a_k, "u_K": walk.u_k,
               "r_K": walk.r_1, "s_K": walk.s_1, "eps_K": walk.eps_k,
               "H_K": walk.h0}[name]
        e = rel(got, CERT[name])
        ok = e <= CERT_TOL
        ok_all = ok_all and ok
        out("  %-5s run %.17g  certified %.17g  rel.err %.2e  %s"
            % (name, got, CERT[name], e, "PASS" if ok else "FAIL"))
    out("  overall: %s" % ("PASS" if ok_all else "FAIL"))


def main():
    out("== chainform.py ", stamp(), " ==")
    out("Does the chained constant-offset two-form")
    out("    p_(k+i)/(p_(k+i)-1) = (A_(k+i) - H_i - c_i)/(A_(k+i-1) - H_(i-1) - c_(i-1)),")
    out("    c_j = log(p_(k+j)/log N_k),  log N_k = exp(theta(p_k)),")
    out("close onto the anchored transport chain of Theorem 8?  (Residuals,")
    out("phantom chains implied by the closure, and true chains are measured.)")
    out("epsilon = P~/e^gamma - A with A = log theta; H = eps/u_k at fixed")
    out("anchor scale; transport eps_(n+1) = (1+r_n) eps_n + s_n,")
    out("s_n = r_n A_n - log1p(u_n), u_n = log p_(n+1)/theta(p_n).")

    out("")
    out("### CHEAP PASS: flat/segmented sieve, primes to %d" % LIMIT_CHEAP)
    walks = []
    for k, w in CHEAP_CFG:
        aw = AnchorWalk(k, w)
        aw.checkpoints = tuple(x for x in (1, 10_000, 1_000_000) if x <= w)
        walks.append(aw)
    run_walk(primes_theta(LIMIT_CHEAP, SEG_SPAN), walks, "cheap")
    for aw in walks:
        aw.report(deep=False)

    out("")
    out("### DEEP PASS: segmented sieve, primes to %d, anchor K = %d, W = %d"
        % (DEEP_LIMIT, DEEP_K, DEEP_W))
    walk = AnchorWalk(DEEP_K, DEEP_W)
    walk.checkpoints = DEEP_CHECKS
    run_walk(primes_theta(DEEP_LIMIT, SEG_SPAN), [walk], "deep")
    certify(walk)
    walk.report(deep=True)

    out("")
    out("== end of chainform.py ", stamp(), " ==")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "chainform_results.txt")
    with open(path, "w") as f:
        f.write("\n".join(OUT) + "\n")
    print("results written to", path)


if __name__ == "__main__":
    main()
