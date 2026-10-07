# -*- coding: utf-8 -*-
"""Faithful Python port of PlatEMO UniformPoint.m NBI / MUD, then inter-vector
angle statistics to test the Case-C mechanism claim."""
import numpy as np
from math import comb
from itertools import combinations

# ---------- UniformPoint: NBI ----------
def nchoosek(n, k):
    if k < 0 or n < 0 or k > n:
        return 0
    return comb(n, k)

def gen_nbi(N, M):
    """Exact port of the NBI branch, returning the vector set W and its size."""
    H1 = 1
    while nchoosek(H1 + M, M - 1) <= N:
        H1 += 1
    # W = nchoosek(1:H1+M-1, M-1) - repmat(0:M-2, rows, 1) - 1
    idx = np.array(list(combinations(range(1, H1 + M), M - 1)), dtype=float)
    off = np.arange(0, M - 1, dtype=float)[None, :]
    W = idx - off - 1.0
    # W = ([W, zeros+H1] - [zeros, W]) / H1
    right = np.concatenate([W, np.full((W.shape[0], 1), float(H1))], axis=1)
    left = np.concatenate([np.zeros((W.shape[0], 1)), W], axis=1)
    W1 = (right - left) / H1
    Wout = W1
    if H1 < M:
        H2 = 0
        while nchoosek(H1 + M - 1, M - 1) + nchoosek(H2 + M, M - 1) <= N:
            H2 += 1
        if H2 > 0:
            idx2 = np.array(list(combinations(range(1, H2 + M), M - 1)), dtype=float)
            Wb = idx2 - np.arange(0, M - 1, dtype=float)[None, :] - 1.0
            right2 = np.concatenate([Wb, np.full((Wb.shape[0], 1), float(H2))], axis=1)
            left2 = np.concatenate([np.zeros((Wb.shape[0], 1)), Wb], axis=1)
            W2 = (right2 - left2) / H2
            Wout = np.vstack([W1, W2 / 2.0 + 1.0 / (2.0 * M)])
    Wout = np.maximum(Wout, 1e-6)
    return Wout

# ---------- UniformPoint: MUD (via GoodLatticePoint) ----------
def calcd2(UT):
    n, s = UT.shape
    X = (2.0 * UT - 1.0) / (2.0 * n)
    CS1 = np.sum(np.prod(2 + np.abs(X - 0.5) - (X - 0.5) ** 2, axis=1))
    CS2 = 0.0
    for i in range(n):
        d = np.abs(X[i, :][None, :] - X)
        CS2 += np.sum(np.prod(1 + 0.5 * np.abs(X[i, :][None, :] - 0.5)
                               + 0.5 * np.abs(X - 0.5)
                               - 0.5 * d, axis=1))
    return (13.0 / 12.0) ** s - (2.0 ** (1 - s)) / n * CS1 + CS2 / (n ** 2)

def good_lattice_point(N, M):
    import math
    hm = np.array([i for i in range(1, N + 1) if math.gcd(i, N) == 1])
    udt = np.mod(np.outer(np.arange(1, N + 1), hm), N)
    udt[udt == 0] = N
    ncomb = nchoosek(len(hm), M)
    if ncomb < 1e4:
        best, bestcd = None, np.inf
        for c in combinations(range(len(hm)), M):
            UT = udt[:, list(c)]
            cd = calcd2(UT)
            if cd < bestcd:
                bestcd, best = cd, UT
        Data = best
    else:
        bestcd, besti = np.inf, 1
        for i in range(1, N + 1):
            UT = np.mod(np.outer(np.arange(1, N + 1), i ** np.arange(0, M)), N)
            cd = calcd2(UT)
            if cd < bestcd:
                bestcd, besti = cd, i
        Data = np.mod(np.outer(np.arange(1, N + 1), besti ** np.arange(0, M)), N)
        Data[Data == 0] = N
    return (Data - 1.0) / (N - 1.0)

def gen_mud(N, M):
    X = good_lattice_point(N, M - 1) ** (1.0 / np.arange(M - 1, 0, -1)[None, :])
    X = np.maximum(X, 1e-6)
    W = np.zeros((N, M))
    W[:, :-1] = (1 - X) * np.cumprod(X, axis=1) / X
    W[:, -1] = np.prod(X, axis=1)
    return W

# ---------- angle statistics ----------
def min_angle(vs):
    """Normalise rows to unit length, return the full pairwise angle matrix's
    off-diagonal minimum (degrees) and the sorted list of per-vector gamma_i."""
    n = np.sqrt((vs ** 2).sum(axis=1, keepdims=True))
    U = vs / n
    C = np.clip(U @ U.T, -1.0, 1.0)
    A = np.degrees(np.arccos(C))
    np.fill_diagonal(A, np.inf)
    g = A.min(axis=1)
    return float(g.min()), np.sort(g)

if __name__ == '__main__':
    for (N, M) in [(100, 3), (100, 5), (100, 8), (200, 3), (300, 3)]:
        Wn = gen_nbi(N, M)
        try:
            Wm = gen_mud(N, M)
        except Exception as e:
            print(f'N={N} M={M}: MUD failed ({e})')
            continue
        gn, _ = min_angle(Wn)
        gm, _ = min_angle(Wm)
        # duplicate count in NBI two-layer construction
        un = np.unique(np.round(Wn, 12), axis=0)
        print(f'N={N:4d} M={M}: |NBI|={len(Wn):4d} minAngle={gn:9.4f} deg | '
              f'|MUD|={len(Wm):4d} minAngle={gm:9.4f} deg | NBI unique rows={len(un)}')
