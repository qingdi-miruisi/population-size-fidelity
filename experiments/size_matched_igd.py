# -*- coding: utf-8 -*-
"""Size-matched IGD control (Table S8 / Section 5.3).

The released per-run archives store the final objective matrix of every run, so
the size-matched control can be recomputed from them: each repaired front is
downsampled to the published arm's realised size and IGD is recomputed against
the same reference front. Reference fronts are reconstructed in pure Python from
PlatEMO's GetOptimum(400) (UniformPoint NBI / grid), without MATLAB.

Run from the repository root or from experiments/:
    python experiments/size_matched_igd.py
Requires: numpy, scipy (for the v5 .mat archives).
"""
import os
import sys
import numpy as np
import scipy.io as sio

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reference_direction_angles import gen_nbi          # exact NBI port

WB = os.path.abspath(os.path.join(HERE, '..', 'data', 'results'))

PROBS = [('DTLZ1', 3, 300), ('DTLZ2', 3, 300), ('DTLZ7', 3, 300),
         ('LSMOP1', 3, 300), ('LSMOP2', 3, 300), ('LSMOP3', 3, 300),
         ('LSMOP4', 3, 300), ('LSMOP5', 3, 300), ('LSMOP6', 3, 300),
         ('LSMOP7', 3, 300), ('LSMOP8', 3, 300), ('LSMOP9', 3, 300),
         ('LSMOP1', 5, 500), ('LSMOP6', 5, 500), ('LSMOP1', 3, 1000)]
LAB = [f'{p} ({m},{d})' if d != 300 else p for p, m, d in PROBS]


def gen_grid(N, M):
    k = int(np.ceil(N ** (1.0 / M)))
    gap = np.linspace(0, 1, k)
    G = np.meshgrid(*([gap] * M), indexing='ij')
    return np.column_stack([g.ravel() for g in G])


def uni(N, M, method='NBI'):
    return gen_nbi(N, M) if method == 'NBI' else gen_grid(N, M)


def sphere(W):
    return W / np.linalg.norm(W, axis=1, keepdims=True)


def ishikawa(N, M):
    itv = [0, 0.251412, 0.631627, 0.859401]
    med = (itv[1] - itv[0]) / (itv[3] - itv[2] + itv[1] - itv[0])
    X = uni(N, M - 1, 'grid').copy()
    lo = X <= med
    X[lo] = X[lo] * (itv[1] - itv[0]) / med + itv[0]
    X[~lo] = (X[~lo] - med) * (itv[3] - itv[2]) / (1 - med) + itv[2]
    tail = 2 * (M - np.sum(X / 2 * (1 + np.sin(3 * np.pi * X)), axis=1, keepdims=True))
    return np.hstack([X, tail])


def make_pf(name, M):
    N = 400
    if name == 'DTLZ1':
        return uni(N, M) / 2.0
    if name == 'DTLZ2':
        return sphere(uni(N, M))
    if name == 'DTLZ7':
        return ishikawa(N, M)
    n = int(name[5:])
    if n <= 4:
        return uni(N, M)
    if n <= 8:
        return sphere(uni(N, M))
    return ishikawa(N, M)


def nd_first(P):
    n = len(P)
    dom = np.zeros((n, n), dtype=bool)
    for i in range(n):
        dom[i] = np.all(P[i] <= P, axis=1) & np.any(P[i] < P, axis=1)
    return P[dom.sum(axis=0) == 0]


def my_igd(objs, PF):
    sub = nd_first(np.asarray(objs, float))
    if len(sub) == 0:
        return np.inf
    lo, hi = PF.min(axis=0), PF.max(axis=0)
    rng = np.where(hi > lo, hi - lo, 1.0)
    Sx = (sub - lo) / rng
    Pp = (PF - lo) / rng
    d = ((Pp[:, None, :] - Sx[None, :, :]) ** 2).sum(axis=2)
    return float(np.sqrt(d.min(axis=1)).mean())


def maximin(P, k):
    c = P.mean(axis=0)
    idx = [int(np.argmax(((P - c) ** 2).sum(axis=1)))]
    d = np.linalg.norm(P - P[idx[0]], axis=1)
    for _ in range(k - 1):
        j = int(np.argmax(d))
        idx.append(j)
        d = np.minimum(d, np.linalg.norm(P - P[j], axis=1))
    return P[idx]


def load_arms():
    arms = {}
    for k in range(1, 60):
        f = os.path.join(WB, f'wbA_{k:02d}.mat')
        if not os.path.exists(f):
            break
        A = sio.loadmat(f, struct_as_record=False, squeeze_me=True)['A']
        arms[str(A.name)] = A
    return arms


def runs(A, pp):
    return [np.atleast_2d(np.asarray(o, float)) for o in A.objs[pp]]


def main():
    arms = load_arms()
    pub, rep = arms['hostNBI'], arms['hostN']
    rng = np.random.default_rng(0)
    print(f'{"problem":18s} {"raw":>7s} {"maximin":>8s} {"random":>7s}')
    gains = []
    for pp, (p, m, d) in enumerate(PROBS):
        PF = make_pf(p, m)
        pr, rr = runs(pub, pp), runs(rep, pp)
        n = min(len(pr), len(rr))
        pr, rr = pr[:n], rr[:n]
        mdp = np.median([my_igd(a, PF) for a in pr])
        md_rep = np.median([my_igd(b, PF) for b in rr])
        gm, gr = [], []
        for a, b in zip(pr, rr):
            k = len(a)
            lo, hi = PF.min(0), PF.max(0)
            rg = np.where(hi > lo, hi - lo, 1.0)
            sel = maximin((b - lo) / rg, k) * rg + lo
            gm.append(my_igd(sel, PF))
            gr.append(np.median([my_igd(b[rng.choice(len(b), k, replace=False)], PF)
                                 for _ in range(200)]))
        g_raw = 100 * (mdp - md_rep) / mdp
        g_mx = 100 * (mdp - np.median(gm)) / mdp
        g_rd = 100 * (mdp - np.median(gr)) / mdp
        gains.append((g_raw, g_mx, g_rd))
        print(f'{LAB[pp]:18s} {g_raw:7.2f} {g_mx:8.2f} {g_rd:7.2f}')
    g = np.array(gains)
    print('\nmedian: raw %.2f | maximin %.2f | random %.2f' % tuple(np.median(g, axis=0)))
    print('better/15 (|gain|>0.05%%): raw %d | maximin %d | random %d' % tuple((g > 0.05).sum(axis=0)))


if __name__ == '__main__':
    main()
