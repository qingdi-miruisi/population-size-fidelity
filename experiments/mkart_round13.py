#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mkart_round13.py -- artefacts for the round-13 arms.

  hostA  : the host configured at the size it realises (declared 91 at M=3,
           85 at M=5), i.e. declared == realised
  k3,k10 : the static setting (n_ex=10, gamma=0.7) at K=3 and K=10, against the
           existing e10g7 which uses the same n_ex and gamma at K=5

Writes paper_scis/tables/tab_abc.tex, tables/tab_K.tex and numbers_round13.tex.
Safe to run before the archives are complete: it reports what is missing.
"""
import os, glob, io
import numpy as np
import scipy.io as sio
from scipy.stats import wilcoxon, mannwhitneyu

ALG = r'D:\harness工作\中国科学：数学(总)\算法\algorithm'
R13 = os.path.join(ALG, 'results', 'wbround13')
R3 = os.path.join(ALG, 'results', 'wbauto')
PAPER = os.path.join(ALG, 'paper_scis')
TAB = os.path.join(PAPER, 'tables')

PROBS = [('DTLZ1', 3, 300), ('DTLZ2', 3, 300), ('DTLZ7', 3, 300),
         ('LSMOP1', 3, 300), ('LSMOP2', 3, 300), ('LSMOP3', 3, 300), ('LSMOP4', 3, 300),
         ('LSMOP5', 3, 300), ('LSMOP6', 3, 300), ('LSMOP7', 3, 300),
         ('LSMOP8', 3, 300), ('LSMOP9', 3, 300),
         ('LSMOP1', 5, 500), ('LSMOP6', 5, 500), ('LSMOP1', 3, 1000)]
LAB = [f'{p} ({m},{d})' if d != 300 else p for p, m, d in PROBS]


def load(path):
    if not os.path.exists(path):
        return None
    return sio.loadmat(path, struct_as_record=False, squeeze_me=True)['A']


def vec(A, pp):
    if A is None:
        return np.array([])
    arr = A.igd
    if pp >= len(arr):
        return np.array([])
    v = np.atleast_1d(np.asarray(arr[pp], dtype=float))
    return v[np.isfinite(v)]


def med(v):
    return float(np.median(v)) if len(v) else np.nan


def cliff(a, b):
    if len(a) == 0 or len(b) == 0:
        return np.nan
    U = mannwhitneyu(a, b, alternative='two-sided', method='asymptotic').statistic
    return 2.0 * U / (len(a) * len(b)) - 1.0


def main():
    A13 = {os.path.basename(p): load(p) for p in sorted(glob.glob(os.path.join(R13, 'wbB_*.mat')))}
    base = {os.path.basename(p): load(p) for p in sorted(glob.glob(os.path.join(R3, 'wbA_*.mat')))}
    byname13 = {str(A.name): A for A in A13.values() if A is not None}
    byname3 = {str(A.name): A for A in base.values() if A is not None}
    print('round-13 arms   :', sorted(byname13))
    print('round-3  configs:', sorted(byname3))

    hostA = byname13.get('hostA')
    k3 = byname13.get('k3')
    k10 = byname13.get('k10')
    pub = byname3.get('hostNBI')
    rep = byname3.get('hostN')
    k5 = byname3.get('e10g7')

    N = {}
    ready = True

    # ---------------------------------------------------------- A/B/C table
    rows = []
    for pp, lab in enumerate(PROBS):
        a, p_, r = vec(hostA, pp), vec(pub, pp), vec(rep, pp)
        if len(a) == 0 or len(p_) == 0 or len(r) == 0:
            continue
        rows.append((LAB[pp], med(p_), med(a), med(r),
                     (med(p_) - med(a)) / med(p_) * 100.0 if med(p_) else np.nan,
                     (med(a) - med(r)) / med(a) * 100.0 if med(a) else np.nan,
                     a, p_, r))
    if len(rows) < len(PROBS):
        ready = False
        print('A/B/C table: %d of %d problems available' % (len(rows), len(PROBS)))

    if rows:
        lines = [r'\footnotesize', r'\setlength{\tabcolsep}{4pt}',
                 r'\begin{tabular}{lccc rr}', r'\toprule',
                 r'problem & published & declared & repaired & declared$-$pub & repaired$-$dec \\',
                 r'\midrule']
        for (lab, mp, ma, mr, g1, g2, *_ ) in rows:
            lines.append('%s & %.4f & %.4f & %.4f & $%+.1f\\%%$ & $%+.1f\\%%$ \\\\'
                         % (lab, mp, ma, mr, g1, g2))
        lines += [r'\bottomrule', r'\end{tabular}']
        with io.open(os.path.join(TAB, 'tab_abc.tex'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(lines) + '\n')

        # declared vs published: same realised size, different declared value
        dif = [abs(g) for (_, _, _, _, g, _, _, _, _) in rows]
        N['nAbcProblems'] = len(rows)
        N['abcDeclVsPubMed'] = '%.1f' % float(np.median(dif))
        N['abcDeclVsPubMax'] = '%.1f' % float(np.max(dif))
        n_same = 0
        n_pairs = 0
        for (_, _, _, _, _, _, a, p_, r) in rows:
            n = min(len(a), len(p_)); aa, pp_ = a[:n], p_[:n]
            try:
                pv = wilcoxon(aa, pp_).pvalue
            except Exception:
                pv = np.nan
            n_pairs += 1
            if np.isfinite(pv) and pv >= 0.05:
                n_same += 1
        N['abcIndistinct'] = n_same
        N['abcPairs'] = n_pairs
        # repaired vs declared: the realised-size effect
        d = []
        for (_, _, _, _, _, g2, _, _, _) in rows:
            d.append(abs(g2))
        N['abcRepVsDeclMed'] = '%.1f' % float(np.median(d))

    # ---------------------------------------------------------- K sweep
    krows = []
    for pp, lab in enumerate(PROBS):
        v3, v5, v10 = vec(k3, pp), vec(k5, pp), vec(k10, pp)
        if len(v3) == 0 or len(v5) == 0 or len(v10) == 0:
            continue
        krows.append((LAB[pp], med(v3), med(v5), med(v10)))
    if len(krows) < len(PROBS):
        print('K table: %d of %d problems available' % (len(krows), len(PROBS)))
    if krows:
        lines = [r'\footnotesize', r'\setlength{\tabcolsep}{6pt}',
                 r'\begin{tabular}{lcccl}', r'\toprule',
                 r'problem & $K{=}3$ & $K{=}5$ & $K{=}10$ & best \\', r'\midrule']
        wins = {3: 0, 5: 0, 10: 0}
        for (lab, a, b, c) in krows:
            vals = {3: a, 5: b, 10: c}
            best = min(vals, key=vals.get)
            wins[best] += 1
            lines.append('%s & %.4f & %.4f & %.4f & $K{=}%d$ \\\\' % (lab, a, b, c, best))
        lines += [r'\bottomrule', r'\end{tabular}']
        with io.open(os.path.join(TAB, 'tab_K.tex'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(lines) + '\n')
        N['kProblems'] = len(krows)
        N['kWinsThree'] = wins[3]
        N['kWinsFive'] = wins[5]
        N['kWinsTen'] = wins[10]
        # is K load-bearing?
        spread = [max(a, b, c) - min(a, b, c) for (_, a, b, c) in krows]
        rel = [100.0 * s / min(a, b, c) for s, (_, a, b, c) in zip(spread, krows) if min(a, b, c) > 0]
        N['kSpreadMed'] = '%.1f' % float(np.median(rel))
        # a median spread can hide a catastrophic setting, so look for one
        worst = None
        for (lab, a, b, c) in krows:
            best = min(a, b, c)
            if best > 0:
                for val, kk in ((a, 3), (b, 5), (c, 10)):
                    r = val / best
                    if worst is None or r > worst[0]:
                        worst = (r, lab, kk, val, best)
        if worst and worst[0] > 10:
            N['kFailRatio'] = '%.0f' % worst[0]
            N['kFailProblem'] = worst[1]
            N['kFailK'] = worst[2]
            N['kFailValue'] = '%.1f' % worst[3]
            N['kFailBest'] = '%.4f' % worst[4]
            N['kFailN'] = sum(1 for (lab, a, b, c) in krows
                              if min(a, b, c) > 0 and max(a, b, c) / min(a, b, c) > 10)
        else:
            N['kFailRatio'] = '1'

    out = ['\\newcommand{\\%s}{%s}' % (k, v) for k, v in N.items()]
    with io.open(os.path.join(PAPER, 'numbers_round13.tex'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('%% generated by mkart_round13.py -- do not edit\n')
        fh.write('\n'.join(out) + '\n')
    print('macros:', N)
    print('COMPLETE' if ready and len(krows) == len(PROBS) else 'INCOMPLETE (rerun once the arms finish)')


if __name__ == '__main__':
    main()
