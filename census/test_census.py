"""Unit tests for harmless_census.py.  Run: python3 test_census.py"""

from fractions import Fraction as fr
from itertools import combinations

from harmless_census import (GradedRing, HarmlessCensus, external_product,
                             matroid_chow, pd_check, LinAlg, hr_spot_check)


def fail(msg):
    raise AssertionError(msg)


def test_p4_model():
    ring = GradedRing(["h"], [1], [{(5,): fr(1)}], 4)
    assert [ring.dim(p) for p in range(5)] == [1, 1, 1, 1, 1]
    hc = HarmlessCensus(ring, [(1, {(1,): fr(1)})], "P4")
    table = hc.census()
    assert all(row["dim_Z"] == 1 and row["dim_B"] == 1 and row["w"] == 0
               for row in table), table


def test_slot_ring():
    srels = [{(4, 0): fr(1)}, {(0, 2): fr(1)}, {(1, 1): fr(1)}]
    ring = GradedRing(["h", "w"], [1, 2], srels, 2)
    assert [ring.dim(p) for p in range(3)] == [1, 1, 2]
    hc = HarmlessCensus(ring, [(1, {(1, 0): fr(1)})], "slot")
    table = hc.census()
    assert [row["dim_Z"] for row in table] == [1, 1, 2]
    assert [row["dim_B"] for row in table] == [1, 1, 1]
    assert [row["w"] for row in table] == [0, 0, 1]


def test_external_product_slots():
    srels = [{(4, 0): fr(1)}, {(0, 2): fr(1)}, {(1, 1): fr(1)}]
    slot = GradedRing(["h", "w"], [1, 2], srels, 2)
    p2 = GradedRing(["g"], [1], [{(3,): fr(1)}], 2)
    hc1 = HarmlessCensus(slot, [(1, {(1, 0): fr(1)})])
    hc2 = HarmlessCensus(p2, [(1, {(1,): fr(1)})])
    prod = external_product(hc1, hc2, "slot x P2")
    table = prod.census(4)
    assert [row["dim_Z"] for row in table] == [1, 2, 4, 4, 3], table
    assert [row["dim_B"] for row in table] == [1, 2, 3, 3, 2], table
    # the w-slot propagates to every positive degree (Cor 4.9 in ring form)
    assert [row["w"] for row in table] == [0, 0, 1, 1, 1], table


def test_gb_closure():
    # g^3 = 0 must also kill g^4 in a ring of top degree 4
    ring = GradedRing(["g"], [1], [{(3,): fr(1)}], 4)
    assert [ring.dim(p) for p in range(5)] == [1, 1, 1, 0, 0], \
        [ring.basis(p) for p in range(5)]


def test_linalg():
    rows = [[fr(1), fr(2)], [fr(2), fr(4)]]
    assert LinAlg.rank(rows) == 1


def test_uniform_dims():
    # dim A^1(U_{r,n}) = # proper nondempty flats - n + 1
    for (r, n) in [(2, 3), (2, 4)]:
        circ = [list(c) for c in combinations(range(1, n + 1), r + 1)]
        res = matroid_chow(list(range(1, n + 1)), circ, "U")
        flats_proper = len(res["ring"].names)
        expected = flats_proper - n + 1
        got = dict(res["dims"])[1]
        assert got == expected, (r, n, got, expected)


def test_fano_pd():
    lines = [[1, 2, 3], [1, 4, 5], [1, 6, 7], [2, 4, 6], [2, 5, 7],
             [3, 4, 7], [3, 5, 6]]
    ovals = [sorted({1, 2, 3, 4, 5, 6, 7} - {a, b, c}) for (a, b, c) in lines]
    res = matroid_chow([1, 2, 3, 4, 5, 6, 7], lines + ovals, "Fano")
    assert res["rank"] == 3
    assert dict(res["dims"]) == {0: 1, 1: 8, 2: 1}, res["dims"]
    pd = pd_check(res)
    assert pd is not None and all(d == r for (_, d, r) in pd), pd


def test_k4_pd_and_dims():
    circ = [[1, 2, 4], [1, 3, 5], [2, 3, 6], [4, 5, 6],
            [1, 3, 4, 6], [1, 2, 5, 6], [2, 3, 4, 5]]
    res = matroid_chow([1, 2, 3, 4, 5, 6], circ, "K4")
    assert res["rank"] == 3
    assert dict(res["dims"]) == {0: 1, 1: 8, 2: 1}, res["dims"]
    pd = pd_check(res)
    assert pd is not None and all(d == r for (_, d, r) in pd), pd


def test_hr_vacuous_small():
    lines = [[1, 2, 3], [1, 4, 5], [1, 6, 7], [2, 4, 6], [2, 5, 7],
             [3, 4, 7], [3, 5, 6]]
    ovals = [sorted({1, 2, 3, 4, 5, 6, 7} - {a, b, c}) for (a, b, c) in lines]
    res = matroid_chow([1, 2, 3, 4, 5, 6, 7], lines + ovals, "Fano")
    # d = 2: primitive divisor classes are trivial; scan reports None
    assert hr_spot_check(res) is None


ALL_TESTS = [test_p4_model, test_slot_ring, test_external_product_slots,
             test_gb_closure, test_linalg, test_uniform_dims,
             test_fano_pd, test_k4_pd_and_dims, test_hr_vacuous_small]

if __name__ == "__main__":
    for t in ALL_TESTS:
        t()
        print("PASS:", t.__name__)
    print("all %d tests passed" % len(ALL_TESTS))
