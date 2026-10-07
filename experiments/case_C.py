# -*- coding: utf-8 -*-
"""case_C.py -- implement and validate the bounded-angle reference constructor
proposed for Case C, and report whether it does what the paper claims.

Construction: take the largest admissible Das-Dennis lattice L <= N, then add the
N - L remaining directions one at a time, each chosen from a candidate pool to
maximise the smallest angle to the directions already present, rejecting any
candidate whose inclusion would drive that angle below a floor theta_min.

Output: D:/wb_run3/case_C.csv  + console report.
"""
import io, csv, numpy as np
from math import comb
from itertools import combinations

OUT = r'D:\wb_run3\case_C.csv'
THETA_MIN = 1.0


def lattice(N, M):
    """the two-layer Das-Dennis lattice, as in the paper"""
    H1 = 1
    while comb(H1 + M, M - 1) <= N:
        H1 += 1
    idx = np.array(list(combinations(range(1, H1 + M), M - 1)), dtype=float)
    W = idx - np.arange(0, M - 1, dtype=float)[None, :] - 1.0
    right = np.concatenate([W, np.full((W.shape[0], 1), float(H1))], axis=1)
    left = np.concatenate([np.zeros((W.shape[0], 1)), W], axis=1)
    W1 = (right - left) / H1
    out = W1
    if H1 < M:
        H2 = 0
        while comb(H1 + M - 1, M - 1) + comb(H2 + M, M - 1) <= N:
            H2 += 1
        if H2 > 0:
            i2 = np.array(list(combinations(range(1, H2 + M), M - 1)), dtype=float)
            Wb = i2 - np.arange(0, M - 1, dtype=float)[None, :] - 1.0
            r2 = np.concatenate([Wb, np.full((Wb.shape[0], 1), float(H2))], axis=1)
            l2 = np.concatenate([np.zeros((Wb.shape[0], 1)), Wb], axis=1)
            out = np.vstack([W1, (r2 - l2) / H2 / 2.0 + 1.0 / (2.0 * M)])
    return np.maximum(out, 1e-6)


def min_angle(V):
    U = V / np.sqrt((V ** 2).sum(axis=1, keepdims=True))
    A = np.degrees(np.arccos(np.clip(U @ U.T, -1.0, 1.0)))
    np.fill_diagonal(A, np.inf)
    return float(A.min(axis=1).min())


def candidate_pool(M, step=40):
    """directions on the unit simplex, used as padding candidates"""
    pts = []
    for i in range(1, step):
        for j in range(1, step - i):
            k = step - i - j
            if k <= 0:
                continue
            pts.append([i / step, j / step, k / step])
    if M != 3:                      # generic fill for M > 3
        rng = np.random.default_rng(0)
        g = rng.dirichlet(np.ones(M), size=6000)
        pts = list(g)
    return np.array(pts)


def bounded_angle(N, M):
    base = lattice(N, M)
    L = len(base)
    if L >= N:                      # nothing to pad: no fallback involved
        return base, L, False, min_angle(base)
    pool = candidate_pool(M)
    U = base / np.sqrt((base ** 2).sum(axis=1, keepdims=True))
    chosen = list(base)
    Uc = list(U)
    need = N - L
    fell_back = False
    for _ in range(need):
        best, best_ang = None, -1.0
        for cand in pool:
            u = cand / np.linalg.norm(cand)
            angs = [np.degrees(np.arccos(np.clip(u @ uc, -1, 1))) for uc in Uc]
            a = float(np.min(angs))
            if a > best_ang:
                best_ang, best = a, u
        if best is None or best_ang < THETA_MIN:
            fell_back = True
            break
        chosen.append(best)
        Uc.append(best)
    V = np.array(chosen)
    return V, len(V), fell_back, min_angle(V)


def main():
    rows = []
    print('%-6s %-4s %-10s %-14s %-10s %-8s' %
          ('N', 'M', 'lattice L', 'final size', 'gamma_min', 'fallback'))
    print('-' * 62)
    for (N, M) in [(100, 3), (100, 5), (100, 8), (300, 3)]:
        try:
            V, sz, fb, g = bounded_angle(N, M)
            print('%-6d %-4d %-10d %-14d %-10.2f %-8s' % (N, M, len(lattice(N, M)), sz, g, fb))
            rows.append([N, M, len(lattice(N, M)), sz, round(g, 4), int(fb), round(THETA_MIN, 2)])
        except Exception as e:
            print('%-6d %-4d FAILED: %s' % (N, M, e))
            rows.append([N, M, '', '', '', '', THETA_MIN])
    with io.open(OUT, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['N_requested', 'M', 'lattice_L', 'final_size',
                    'gamma_min_deg', 'fallback_triggered', 'theta_min_deg'])
        w.writerows(rows)
    print('\nwrote', OUT)


if __name__ == '__main__':
    main()
