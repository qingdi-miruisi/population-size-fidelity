#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mkart_cat.py -- Table S7 (catalogue validation, cases B and C) from
results/wbcat/wbC_*.mat, plus the summary macros for Section 5.6.

Arms: MOEAD_PUB/MOEAD_MUD (case B), RVEA_PUB/RVEA_N(MUD)/RVEA_BA and
LMOCSO_PUB/LMOCSO_MUD/LMOCSO_BA (case C).  DTLZ1-7, M=3, D=M+4 (release
default), N_req=100, budget 1e5, 30 seeds.
Writes data/tableS7_peers.tex (supp copy) and prints key numbers.
"""
import glob, os
import numpy as np
import scipy.io as sio

ROOT = r'D:\harness工作\中国科学：数学(总)\算法\algorithm'
RES = os.path.join(ROOT, 'results', 'wbcat')
OUT_REPO = os.path.join(ROOT, 'population-size-fidelity', 'data', 'tableS7_peers.tex')
OUT_SUPP = os.path.join(ROOT, 'paper_scis', 'supp', 'tableS7_peers.tex')

ARMS = [('MOEAD_PUB', 'pub'), ('MOEAD_MUD', 'r2'),
        ('RVEA_PUB', 'pub'), ('RVEA_N', 'r2'), ('RVEA_BA', 'ba'),
        ('LMOCSO_PUB', 'pub'), ('LMOCSO_MUD', 'r2'), ('LMOCSO_BA', 'ba')]
PROBS = ['DTLZ1', 'DTLZ2', 'DTLZ3', 'DTLZ4', 'DTLZ5', 'DTLZ6', 'DTLZ7']


def load_arm(name):
    for p in glob.glob(os.path.join(RES, 'wbC_*.mat')):
        A = sio.loadmat(p, struct_as_record=False, squeeze_me=True)['A']
        if str(A.name) == name:
            return A
    return None


def med_vec(A, pp):
    if A is None:
        return np.array([])
    v = np.atleast_1d(np.asarray(A.igd[pp], dtype=float))
    return v[np.isfinite(v)]


def fmt(m):
    return '%.4f' % m if np.isfinite(m) else '--'


def main():
    data = {n: load_arm(n) for n, _ in ARMS}
    rows = []
    for pp, pr in enumerate(PROBS):
        cells, meds = [], {}
        for n, _ in ARMS:
            v = med_vec(data[n], pp)
            m = float(np.median(v)) if len(v) else np.nan
            meds[n] = m
            cells.append(fmt(m))
        rows.append((pr, cells, meds))

    hdr = ('problem & \\multicolumn{2}{c}{MOEA/D} & \\multicolumn{3}{c}{RVEA} & \\multicolumn{3}{c}{LMOCSO} \\\\\n'
           '\\cmidrule(lr){2-3}\\cmidrule(lr){4-6}\\cmidrule(lr){7-9}\n'
           ' & pub & repair 2 & pub & repair 2 & bounded & pub & repair 2 & bounded \\\\')
    lines = ['\\scriptsize', '\\setlength{\\tabcolsep}{3.5pt}',
             '\\begin{tabular}{lrrrrrrrr}', '\\toprule', hdr, '\\midrule']
    for pr, cells, _ in rows:
        lines.append(pr + ' & ' + ' & '.join(cells) + ' \\\\')
    lines += ['\\bottomrule', '\\end{tabular}']
    body = '\n'.join(lines) + '\n'

    for out in (OUT_REPO, OUT_SUPP):
        with open(out, 'w', encoding='utf-8') as fh:
            fh.write(body)
    print('wrote', OUT_REPO)

    # ---- key numbers for Section 5.6 ----
    print('\n--- median IGD (DTLZ1) ---')
    for n, _ in ARMS:
        print('%-11s %s' % (n, fmt(rows[0][2][n])))
    print('\n--- Nreal ranges over completed runs ---')
    for n, _ in ARMS:
        A = data[n]
        if A is None:
            continue
        vals = np.concatenate([np.atleast_1d(np.asarray(x, dtype=float)) for x in A.Nreal])
        vals = vals[np.isfinite(vals)]
        print('%-11s min=%d max=%d  (runs=%d)' % (n, vals.min(), vals.max(), len(vals)))


if __name__ == '__main__':
    main()
