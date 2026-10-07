#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mkart_scis.py -- regenerate every number, table and figure of the SCIS
submission from the released archives.

Supersedes mkart.py for the SCIS paper:
  * clearer Table 3 headers and an explicit count of strictly-better /
    indistinguishable / worse problems;
  * a Cliff's-delta effect-size column in the significance table;
  * algorithm-level as well as file-level rows in the census;
  * the layer comparison over all fifteen problems rather than three;
  * measured inter-vector angles for the two constructors (Case C evidence);
  * evaluation-budget accounting.
"""
import os
import numpy as np
import scipy.io as sio
from math import comb
from scipy.stats import wilcoxon, mannwhitneyu

ALG = r'D:\harness工作\中国科学：数学(总)\算法\algorithm'
WB = os.path.join(ALG, 'results', 'wbauto')
WBP = os.path.join(ALG, 'results', 'wbpeer')
WBG = os.path.join(ALG, 'results', 'wbgen3')
PAPER = os.path.join(ALG, 'paper_scis')
TAB = os.path.join(PAPER, 'tables')
FIG = os.path.join(PAPER, 'figs')
os.makedirs(TAB, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

PROBS = [('DTLZ1', 3, 300), ('DTLZ2', 3, 300), ('DTLZ7', 3, 300),
         ('LSMOP1', 3, 300), ('LSMOP2', 3, 300), ('LSMOP3', 3, 300), ('LSMOP4', 3, 300),
         ('LSMOP5', 3, 300), ('LSMOP6', 3, 300), ('LSMOP7', 3, 300),
         ('LSMOP8', 3, 300), ('LSMOP9', 3, 300),
         ('LSMOP1', 5, 500), ('LSMOP6', 5, 500), ('LSMOP1', 3, 1000)]
LAB = [f'{p} ({m},{d})' if d != 300 else p for p, m, d in PROBS]


def nbi_count(N, M):
    """Cardinality of the NBI lattice: faithful port of PlatEMO UniformPoint.m."""
    H1 = 1
    while comb(H1 + M, M - 1) <= N:
        H1 += 1
    cnt = comb(H1 + M - 1, M - 1)
    if H1 < M:
        H2 = 0
        while comb(H1 + M - 1, M - 1) + comb(H2 + M, M - 1) <= N:
            H2 += 1
        if H2 > 0:
            cnt += comb(H2 + M - 1, M - 1)
    return cnt


def load(ci, wb=WB):
    f = os.path.join(wb, f'wbA_{ci:02d}.mat')
    if not os.path.exists(f):
        return None
    return sio.loadmat(f, struct_as_record=False, squeeze_me=True)['A']


def vec(A, pp):
    if A is None:
        return np.array([])
    arr = A.igd
    if pp >= len(arr):
        return np.array([])
    return np.atleast_1d(np.asarray(arr[pp], dtype=float))


def finite(v):
    v = np.atleast_1d(np.asarray(v, dtype=float))
    return v[np.isfinite(v)]


def pair_p(a, b):
    """a = baseline, b = candidate. Returns (p, wins_for_candidate, n)."""
    n = min(len(a), len(b)); a, b = a[:n], b[:n]
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 5:
        return np.nan, 0, int(m.sum())
    a2, b2 = a[m], b[m]
    wins = int(np.sum(b2 < a2))
    try:
        p = float(wilcoxon(a2, b2).pvalue)
    except Exception:
        p = np.nan
    return p, wins, int(m.sum())


def cliff(a, b):
    """Cliff's delta, computed from the Mann-Whitney U statistic."""
    a, b = finite(a), finite(b)
    if len(a) == 0 or len(b) == 0:
        return np.nan
    U = mannwhitneyu(a, b, alternative='two-sided', method='asymptotic').statistic
    return 2.0 * U / (len(a) * len(b)) - 1.0


def fmt_p(p):
    if not np.isfinite(p):
        return '--'
    if p < 1e-4:
        return '$<10^{-4}$'
    if p < 0.001:
        return '$%.1e$' % p
    return '%.4f' % p


def fmt_d(x):
    if not np.isfinite(x):
        return '--'
    return '%+.2f' % x


def cell(v):
    v = finite(v)
    if len(v) == 0:
        return '--'
    return '%.4f' % np.median(v)


def med(v):
    v = finite(v)
    return float(np.median(v)) if len(v) else np.nan


# ----------------------------------------------------------------------- angle
def _nchoosek(n, k):
    return comb(n, k) if (0 <= k <= n) else 0


def _gen_nbi(N, M):
    from itertools import combinations
    H1 = 1
    while _nchoosek(H1 + M, M - 1) <= N:
        H1 += 1
    idx = np.array(list(combinations(range(1, H1 + M), M - 1)), dtype=float)
    W = idx - np.arange(0, M - 1, dtype=float)[None, :] - 1.0
    right = np.concatenate([W, np.full((W.shape[0], 1), float(H1))], axis=1)
    left = np.concatenate([np.zeros((W.shape[0], 1)), W], axis=1)
    W1 = (right - left) / H1
    Wout = W1
    if H1 < M:
        H2 = 0
        while _nchoosek(H1 + M - 1, M - 1) + _nchoosek(H2 + M, M - 1) <= N:
            H2 += 1
        if H2 > 0:
            idx2 = np.array(list(combinations(range(1, H2 + M), M - 1)), dtype=float)
            Wb = idx2 - np.arange(0, M - 1, dtype=float)[None, :] - 1.0
            r2 = np.concatenate([Wb, np.full((Wb.shape[0], 1), float(H2))], axis=1)
            l2 = np.concatenate([np.zeros((Wb.shape[0], 1)), Wb], axis=1)
            Wout = np.vstack([W1, (r2 - l2) / H2 / 2.0 + 1.0 / (2.0 * M)])
    return np.maximum(Wout, 1e-6)


def _min_angle(vs):
    n = np.sqrt((vs ** 2).sum(axis=1, keepdims=True))
    U = vs / n
    C = np.clip(U @ U.T, -1.0, 1.0)
    A = np.degrees(np.arccos(C))
    np.fill_diagonal(A, np.inf)
    return float(A.min(axis=1).min())


def angle_stats():
    """Minimum pairwise angle of the NBI and MUD reference sets."""
    import gamma_r12 as G
    rows = []
    for (N, M) in [(100, 3), (100, 5), (100, 8), (300, 3)]:
        wn = _gen_nbi(N, M)
        wm = G.gen_mud(N, M)
        gn, gm = _min_angle(wn), _min_angle(wm)
        rows.append((N, M, len(wn), gn, len(wm), gm, gn / gm if gm else np.nan))
    return rows


def main():
    C = {ci: load(ci) for ci in range(1, 10)}
    byname = {str(C[ci].name): ci for ci in C if C[ci] is not None}

    def get(cls, pp):
        ci = byname.get(cls)
        return vec(C[ci], pp) if ci is not None and C[ci] is not None else np.array([])

    N = {}
    L = ['%% generated by mkart_scis.py -- do not edit']
    N['nProbs'] = len(PROBS)
    N['budget'] = r'10^{5}'
    N['seeds'] = 30
    N['seedsExt'] = 20
    N['refFrontPts'] = 400
    N['nProbedDirect'] = 39
    N['nGridCells'] = 81

    # ---------------- realised count versus request ----------------
    Ns = [91, 100, 105, 120, 150, 200, 275, 300, 500]
    Ms = list(range(2, 11))
    lines = [r'\footnotesize', r'\begin{tabular}{l' + 'r' * len(Ns) + '}', r'\toprule',
             r'$M$ $\backslash$ $N$ & ' + ' & '.join(str(n) for n in Ns) + r' \\', r'\midrule']
    for M in Ms:
        row = []
        for n in Ns:
            c = nbi_count(n, M)
            row.append((r'\textbf{%d}' % c) if c == n else str(c))
        lines.append(f'{M} & ' + ' & '.join(row) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}']
    open(os.path.join(TAB, 'tab_deficit.tex'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    r3, r5, r8, r10 = nbi_count(100, 3), nbi_count(100, 5), nbi_count(100, 8), nbi_count(100, 10)
    N['retMthree'], N['retMfive'], N['retMeight'], N['retMten'] = r3, r5, r8, r10
    N['retMthreeDef'], N['retMfiveDef'] = 100 - r3, 100 - r5
    N['retMeightDef'], N['retMtenDef'] = 100 - r8, 100 - r10
    worst = max((100.0 * (n - nbi_count(n, M)) / n, n, M) for n in Ns if n >= 100 for M in Ms)
    N['retWorst'] = int(round(worst[0]))
    N['retWorstWhere'] = f'{worst[1]},{worst[2]}'
    worstall = max((100.0 * (n - nbi_count(n, M)) / n)
                   for n in range(100, 1001) for M in range(2, 16) if M <= n)
    N['retWorstAll'] = int(round(worstall))
    tot = exa = 0
    exceed = 0
    for n in range(2, 1001):
        for M in range(2, 16):
            if M > n:
                continue
            tot += 1
            c = nbi_count(n, M)
            if c == n:
                exa += 1
            if c > n:
                exceed += 1
    N['retExactFrac'] = '%.1f' % (100.0 * exa / tot)
    N['retCombos'] = tot
    N['retExceed'] = exceed

    # ---------------- census ----------------
    import re
    from collections import defaultdict
    base = os.path.join(ALG, '_tmp_official', 'PlatEMO-master', 'PlatEMO', 'Algorithms')
    pat = re.compile(r'Problem\.N\]\s*=\s*UniformPoint\(Problem\.N')
    tot_files = aff_files = 0
    algall, algfiles = set(), defaultdict(int)
    comment_hits = 0
    fam = defaultdict(int)
    for root, dd, ff in os.walk(base):
        for f in ff:
            if not f.endswith('.m'):
                continue
            rel = os.path.relpath(os.path.join(root, f), base)
            parts = rel.split(os.sep)
            # an algorithm is a directory at depth 2: Algorithms/<category>/<algorithm>/
            alg = (parts[0] + '/' + parts[1]) if len(parts) > 2 else None
            if alg is not None:
                algall.add(alg)
            tot_files += 1
            txt = open(os.path.join(root, f), encoding='utf-8', errors='ignore').read()
            if pat.search(txt):
                aff_files += 1
                if alg is not None:
                    algfiles[alg] += 1
                for line in txt.splitlines():
                    if pat.search(line) and line.strip().startswith('%'):
                        comment_hits += 1
                u = alg.upper()
                if u in ('MOEADD', 'MOEA-DD', 'MOEA-NZD', 'MOEA-RE') or u.startswith('MOEA/D') \
                        or u.startswith('MOEAD') or 'MOEA-D' in u:
                    fam['MOEA/D family'] += 1
                elif 'NSGA-III' in u or 'NSGAIII' in u:
                    fam['NSGA-III family'] += 1
                elif u.startswith('RVEA') or u == 'LDS-AF':
                    fam['RVEA family'] += 1
                elif u in ('LMOCSO', 'HEA', 'C-TAEA', 'FDSEA', 'PPS', 'LCSA', 'LERD', 'DGEA',
                           'WOF', 'SFA-DE', 'DP-PPS', 'CMOBR', 'CMOEBOD', 'GDVTSF'):
                    fam['Large-scale'] += 1
                else:
                    fam['Other'] += 1
    N['nFilesTotal'] = tot_files
    N['nFilesAffected'] = aff_files
    N['pctAffected'] = '%.1f' % (100.0 * aff_files / tot_files)
    N['nAlgTotal'] = len(algall)
    N['nAlgAffected'] = len(algfiles)
    N['pctAlgAffected'] = '%.1f' % (100.0 * len(algfiles) / len(algall))
    N['nAlgSingle'] = sum(1 for v in algfiles.values() if v == 1)
    N['nCommentHits'] = comment_hits
    # how many affected files reuse the returned reference set after the assignment
    _reuse = 0
    for root, dd, ff in os.walk(base):
        for f in ff:
            if not f.endswith('.m'):
                continue
            p = os.path.join(root, f)
            txt = open(p, encoding='utf-8', errors='ignore').read()
            m = pat.search(txt)
            if not m:
                continue
            if re.search(r'\bZ\b', txt[m.end():]):
                _reuse += 1
    N['nReuseZ'] = _reuse

    order = ['MOEA/D family', 'NSGA-III family', 'RVEA family', 'Large-scale', 'Other']
    examples = {
        'MOEA/D family': 'MOEA/D, MOEA/D-DRA, MOEA/D-DE, \\dots',
        'NSGA-III family': 'NSGA-III, A-NSGA-III, DCNSGA-III, \\dots',
        'RVEA family': 'RVEA, RVEAa, RVEA-iGNG, \\dots',
        'Large-scale': 'LMOCSO, HEA, C-TAEA, FDSEA',
        'Other': 'AdaW, ParEGO, SPEA-R, \\dots',
    }
    tl = [r'\small', r'\begin{tabular}{lrrl}', r'\toprule',
          r'family & algorithms & files & examples \\', r'\midrule']
    for f in order:
        tl.append(f'{f} & {fam.get(f,0)} & {sum(v for k,v in algfiles.items() if True) and 0 or 0} & '
                  .replace(' & 0 & ', ' & ') + examples[f] + r' \\')
    tl += [r'\bottomrule', r'\end{tabular}']
    # rebuild cleanly (per-family algorithm and file counts)
    fam_alg = defaultdict(int)
    for k, v in algfiles.items():
        u = k.upper()
        if u in ('MOEADD', 'MOEA-DD', 'MOEA-NZD', 'MOEA-RE') or u.startswith('MOEA/D') \
                or u.startswith('MOEAD') or 'MOEA-D' in u:
            fam_alg['MOEA/D family'] += 1
        elif 'NSGA-III' in u or 'NSGAIII' in u:
            fam_alg['NSGA-III family'] += 1
        elif u.startswith('RVEA') or u == 'LDS-AF':
            fam_alg['RVEA family'] += 1
        elif u in ('LMOCSO', 'HEA', 'C-TAEA', 'FDSEA', 'PPS', 'LCSA', 'LERD', 'DGEA',
                   'WOF', 'SFA-DE', 'DP-PPS', 'CMOBR', 'CMOEBOD', 'GDVTSF'):
            fam_alg['Large-scale'] += 1
        else:
            fam_alg['Other'] += 1
    tl = [r'\small', r'\begin{tabular}{lrrl}', r'\toprule',
          r'family & algorithms & files & examples \\', r'\midrule']
    for f in order:
        tl.append(f'{f} & {fam_alg.get(f,0)} & {fam.get(f,0)} & {examples[f]} \\\\')
    tl += [r'\midrule',
           f'total & {len(algfiles)} & {aff_files} & of {len(algall)} algorithms, '
           f'{tot_files} files \\\\',
           r'\bottomrule', r'\end{tabular}']
    open(os.path.join(TAB, 'tab_census.tex'), 'w', encoding='utf-8').write('\n'.join(tl) + '\n')

    # ---------------- host: with and without the requested size ----------------
    lines = [r'\footnotesize', r'\setlength{\tabcolsep}{5pt}',
             r'\begin{tabular}{lccc rr}', r'\toprule',
             r'problem & published & repair 1 & repair 2 & $\Delta_1$ & $\Delta_2$ \\',
             r'\midrule']
    gains1, gains2 = [], []
    for pp, lab in enumerate(LAB):
        a, b, c = get('hostNBI', pp), get('hostN', pp), get('hostMUD', pp)
        if len(a) == 0 or len(b) == 0:
            continue
        ma, mb = med(a), med(b)
        g1 = (ma - mb) / ma * 100
        mc = med(c)
        g2 = (ma - mc) / ma * 100 if np.isfinite(mc) else np.nan
        gains1.append(g1)
        gains2.append(g2)
        lines.append(f'{lab} & {cell(a)} & {cell(b)} & {cell(c)} & '
                     f'${g1:+.1f}\\%$ & ${g2:+.1f}\\%$ \\\\')
    lines += [r'\bottomrule', r'\end{tabular}']
    open(os.path.join(TAB, 'tab_fix.tex'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    g1 = np.array(gains1)
    N['fixMaxGain'] = '%.1f' % np.nanmax(g1)
    N['fixMinGain'] = '%.1f' % np.nanmin(g1)
    N['fixMedGain'] = '%.1f' % float(np.median(g1))
    N['fixBetterN'] = int(np.sum(g1 > 0))
    N['fixWorseN'] = int(np.sum(g1 < 0))
    N['fixTinyN'] = int(np.sum((g1 > 0) & (np.abs(g1) < 0.05)))
    N['fixNoWorseN'] = N['fixBetterN']

    # ---------------- significance + effect size ----------------
    pv, wraps = [], []
    lines = [r'\footnotesize', r'\setlength{\tabcolsep}{5pt}',
             r'\begin{tabular}{lrrrrr}', r'\toprule',
             r'problem & repair 1 wins & $p$ (signed rank) & Holm--Bonferroni & '
             r'sign test & Cliff $\delta$ \\', r'\midrule']
    from scipy.stats import binomtest
    for pp, lab in enumerate(LAB):
        a, b = get('hostNBI', pp), get('hostN', pp)
        if len(a) == 0 or len(b) == 0:
            continue
        p, w, n = pair_p(a, b)
        a2, b2 = finite(a), finite(b)
        n2 = min(len(a2), len(b2))
        a2, b2 = a2[:n2], b2[:n2]
        try:
            sp = float(binomtest(int(np.sum(b2 < a2)), n2, 0.5).pvalue)
        except Exception:
            sp = np.nan
        pv.append((pp, p, w, n, sp))
    order_i = np.argsort([x[1] for x in pv])
    m = len(pv)
    adj = np.ones(m)
    for rank, i in enumerate(order_i):
        adj[i] = min(1.0, pv[i][1] * (m - rank))
    for k in range(1, m):
        adj[k] = max(adj[k], adj[k - 1]) if False else adj[k]
    # monotone Holm
    run = 0.0
    for i in order_i:
        run = max(run, min(1.0, pv[i][1] * (m - order_i.tolist().index(i))))
        adj[i] = run
    nsig_raw = sum(1 for _, p, _, _, _ in pv if p < 0.05)
    nsig_holm = sum(1 for i in range(m) if adj[i] < 0.05)
    dmax = 0.0
    for k, (pp, p, w, n, sp) in enumerate(pv):
        d = cliff(get('hostNBI', pp), get('hostN', pp))
        if np.isfinite(d):
            dmax = max(dmax, abs(d))
        lines.append(f'{LAB[pp]} & {w}/{n} & {fmt_p(p)} & {fmt_p(adj[k])} & '
                     f'{fmt_p(sp)} & {fmt_d(d)} \\\\')
    lines += [r'\bottomrule', r'\end{tabular}']
    open(os.path.join(TAB, 'tab_sig.tex'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    N['fixSigCount'] = nsig_raw
    N['fixSigHolm'] = nsig_holm
    N['cliffMax'] = '%.2f' % dmax

    # median-difference 95% CI, bootstrap
    rng = np.random.default_rng(0)
    excl = 0
    for pp in range(len(PROBS)):
        a, b = finite(get('hostNBI', pp)), finite(get('hostN', pp))
        if len(a) == 0 or len(b) == 0:
            continue
        n = min(len(a), len(b)); a, b = a[:n], b[:n]
        bs = np.empty(1500)
        for i in range(1500):
            idx = rng.integers(0, n, n)
            bs[i] = np.median(b[idx]) - np.median(a[idx])
        lo, hi = np.percentile(bs, [2.5, 97.5])
        if lo * hi > 0:
            excl += 1
    N['ciExclN'] = excl

    # ---------------- layer, all fifteen problems ----------------
    lines = [r'\footnotesize', r'\setlength{\tabcolsep}{4pt}',
             r'\begin{tabular}{lccc rr}', r'\toprule',
             r'problem & published & requested $N$ & layer & vs published & vs requested \\',
             r'\midrule']
    lg1, lg2 = [], []
    for pp, lab in enumerate(LAB):
        a, b, c = get('hostNBI', pp), get('hostN', pp), get('layer', pp)
        if len(c) == 0:
            continue
        ma, mb, mc = med(a), med(b), med(c)
        g1 = (ma - mc) / ma * 100
        g2 = (mb - mc) / mb * 100
        lg1.append(g1)
        lg2.append(g2)
        lines.append(f'{lab} & {cell(a)} & {cell(b)} & {cell(c)} & '
                     f'${g1:+.1f}\\%$ & ${g2:+.1f}\\%$ \\\\')
    lines += [r'\bottomrule', r'\end{tabular}']
    open(os.path.join(TAB, 'tab_layer.tex'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    lg1, lg2 = np.array(lg1), np.array(lg2)
    N['layerN'] = len(lg1)
    N['layerMedHost'] = '%+.2f' % float(np.median(lg1))
    N['layerMedMatched'] = '%+.2f' % float(np.median(lg2))
    N['layerBetterHost'] = int(np.sum(lg1 > 0))
    N['layerWorseHost'] = int(np.sum(lg1 < 0))
    N['layerBetterMatched'] = int(np.sum(lg2 > 0))
    N['layerWorseMatched'] = int(np.sum(lg2 < 0))
    big = lg1 > 5
    N['layerBigN'] = int(np.sum(big))
    if big.sum():
        sh = (lg1 - lg2)[big]
        N['layerShrinkMin'] = '%.1f' % float(np.min(sh))
        N['layerShrinkMax'] = '%.1f' % float(np.max(sh))
    N['layerSmallMax'] = '%.1f' % float(np.max(np.abs(lg1[~big]))) if (~big).sum() else '--'

    # ---------------- static settings ----------------
    STAT = ['e5g0', 'e5g7', 'e5g3', 'e10g7', 'e20g0']
    STATLAB = {'e5g0': r'$n_{\mathrm{ex}}{=}5,\gamma{=}0$',
               'e5g7': r'$n_{\mathrm{ex}}{=}5,\gamma{=}0.7$',
               'e5g3': r'$n_{\mathrm{ex}}{=}5,\gamma{=}0.3$',
               'e10g7': r'$n_{\mathrm{ex}}{=}10,\gamma{=}0.7$',
               'e20g0': r'$n_{\mathrm{ex}}{=}20,\gamma{=}0$'}
    have = [s for s in STAT if s in byname]
    lines = [r'\footnotesize', r'\setlength{\tabcolsep}{4pt}',
             r'\begin{tabular}{l' + 'c' * len(have) + 'l}', r'\toprule',
             r'problem & ' + ' & '.join(STATLAB[s] for s in have) + r' & best \\', r'\midrule']
    lay_better = 0
    lay_n = 0
    for pp, lab in enumerate(LAB):
        vals = [get(s, pp) for s in have]
        if any(len(v) == 0 for v in vals):
            continue
        mn = [med(v) for v in vals]
        j = int(np.argmin(mn))
        lines.append(f'{lab} & ' + ' & '.join('%.4f' % x for x in mn) +
                     f' & {STATLAB[have[j]]} \\\\')
    lines += [r'\bottomrule', r'\end{tabular}']
    open(os.path.join(TAB, 'tab_static.tex'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    # layer against the best static setting, per problem
    lay_beats = 0
    strong = 0
    strong_beats = 0
    for pp, lab in enumerate(LAB):
        lv = med(get('layer', pp))
        if not np.isfinite(lv):
            continue
        vals = {}
        for s in have:
            v = med(get(s, pp))
            if np.isfinite(v):
                vals[s] = v
        if not vals:
            continue
        best = min(vals, key=vals.get)
        beats = lv < vals[best]
        lay_beats += int(beats)
        a = med(get('hostNBI', pp))
        if np.isfinite(a) and a > 0 and (a - lv) / a * 100 > 5:
            strong += 1
            strong_beats += int(beats)
    N['layerBeatsStaticN'] = lay_beats
    N['layerStrongN'] = strong
    N['layerStrongBeatsN'] = strong_beats

    # ---------------- cost ----------------
    G = None
    gfile = os.path.join(WBG, 'wbG.mat')
    if os.path.exists(gfile):
        G = sio.loadmat(gfile, struct_as_record=False, squeeze_me=True)['R']
    def gmean(mode):
        if G is None:
            return None
        v = finite(G.gen[mode])
        return float(np.mean(v)) if len(v) else None
    gh, gf = gmean(1), gmean(0)
    lines = [r'\footnotesize', r'\setlength{\tabcolsep}{7pt}',
             r'\begin{tabular}{lrrrr}', r'\toprule',
             r'configuration & population & evaluations & generations & wall (s) \\', r'\midrule']
    fe_stat = {}
    for cls, lbl, npop, gval in (('hostNBI', 'as published', 91, gh),
                                 ('hostN', 'requested $N$', 100, gf)):
        ci = byname.get(cls)
        if ci is None or C[ci] is None:
            continue
        A = C[ci]
        fe, tim = [], []
        for pp in range(len(PROBS)):
            for arr, dst in ((A.fe, fe), (A.tim, tim)):
                if pp < len(arr):
                    dst += [x for x in np.atleast_1d(np.asarray(arr[pp], dtype=float))
                            if np.isfinite(x)]
        fe_stat[cls] = (float(np.mean(fe)), float(np.mean(tim)))
        gs = ('%.0f' % gval) if gval is not None else '--'
        lines.append(f'{lbl} & {npop} & {np.mean(fe):.0f} & {gs} & {np.mean(tim):.1f} \\\\')
    lines += [r'\bottomrule', r'\end{tabular}']
    open(os.path.join(TAB, 'tab_cost.tex'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    N['genHost'] = ('%.0f' % gh) if gh is not None else '--'
    N['genFix'] = ('%.0f' % gf) if gf is not None else '--'
    if gh and gf:
        N['genRatio'] = '%.3f' % (gh / gf)
    N['popRatio'] = '%.3f' % (100.0 / 91.0)
    N['feHost'] = '%.0f' % fe_stat.get('hostNBI', (np.nan, 0))[0]
    N['feFix'] = '%.0f' % fe_stat.get('hostN', (np.nan, 0))[0]
    N['feOver'] = '%.0f' % (fe_stat.get('hostNBI', (np.nan, 0))[0] - 100000)
    N['feOverPct'] = '%.2f' % (100.0 * (fe_stat.get('hostNBI', (np.nan, 0))[0] - 100000) / 100000)

    # ---------------- peer ----------------
    pex = {}
    for ci in (1, 2):
        f = os.path.join(WBP, f'wbP_{ci:02d}.mat')
        if os.path.exists(f):
            A = sio.loadmat(f, struct_as_record=False, squeeze_me=True)['A']
            pex[str(A.name)] = A
    if 'NSGAIII' in pex and 'NSGAIII_N' in pex:
        CN = list(range(6))   # the peer archive stores LSMOP1/2/4/6/8/9 in order
        lines = [r'\footnotesize', r'\setlength{\tabcolsep}{4pt}',
                 r'\begin{tabular}{lcccccc}', r'\toprule',
                 r'NSGA-III (median) & LSMOP1 & LSMOP2 & LSMOP4 & LSMOP6 & LSMOP8 & LSMOP9 \\',
                 r'\midrule']
        r1 = [med(np.asarray(pex['NSGAIII'].igd[pp], dtype=float)) for pp in CN]
        r2 = [med(np.asarray(pex['NSGAIII_N'].igd[pp], dtype=float)) for pp in CN]
        pv2 = []
        for pp in CN:
            a = np.asarray(pex['NSGAIII'].igd[pp], dtype=float)
            b = np.asarray(pex['NSGAIII_N'].igd[pp], dtype=float)
            n = min(len(a), len(b))
            try:
                pv2.append(float(wilcoxon(a[:n], b[:n]).pvalue))
            except Exception:
                pv2.append(np.nan)
        lines.append('as published & ' + ' & '.join('%.4f' % x for x in r1) + r' \\\\')
        lines.append('repair 1 (requested $N$) & ' + ' & '.join('%.4f' % x for x in r2) + r' \\\\')
        lines.append(r'\addlinespace')
        lines.append('$p$ (signed rank) & ' + ' & '.join(fmt_p(x) for x in pv2) + r' \\\\')
        lines += [r'\bottomrule', r'\end{tabular}']
        lines = [r'\resizebox{\textwidth}{!}{'] + lines + ['}']
        open(os.path.join(TAB, 'tab_peer.tex'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    # ---------------- angle table ----------------
    try:
        ar = angle_stats()
        lines = [r'\footnotesize', r'\begin{tabular}{rrrrrr}', r'\toprule',
                 r'$N$ & $M$ & NBI size & NBI $\gamma_{\min}$ & MUD size & MUD $\gamma_{\min}$ \\',
                 r'\midrule']
        for (n, mm, sn, gn, sm, gm, ratio) in ar:
            lines.append(f'{n} & {mm} & {sn} & ${gn:.2f}^\\circ$ & {sm} & ${gm:.2f}^\\circ$ \\\\')
        lines += [r'\bottomrule', r'\end{tabular}']
        open(os.path.join(TAB, 'tab_angle.tex'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
        d = {f'ang{n}_{mm}': ('%.2f' % gn, '%.2f' % gm, '%.2f' % ratio)
             for (n, mm, sn, gn, sm, gm, ratio) in ar}
        N['angRatioThree'] = d['ang100_3'][2]
        N['angNbiThree'] = d['ang100_3'][0]
        N['angMudThree'] = d['ang100_3'][1]
        N['angNbiFive'] = d['ang100_5'][0]
        N['angMudFive'] = d['ang100_5'][1]
        N['angRatioFive'] = d['ang100_5'][2]
    except Exception as e:
        print('angle error:', e)

    out = ['\\newcommand{\\%s}{%s}' % (k, v) for k, v in N.items()]
    open(os.path.join(PAPER, 'numbers.tex'), 'w', encoding='utf-8').write('\n'.join(L + out) + '\n')
    print('macros:', len(N))

    # ---------------- figures ----------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6.4, 3.2))
        Ns2 = list(range(40, 501, 5))
        for M in (3, 5, 8, 10):
            ax.plot(Ns2, [100.0 * nbi_count(n, M) / n for n in Ns2], label=f'$M$={M}', lw=1.2)
        ax.set_xlabel('requested population size $N$')
        ax.set_ylabel('realised / requested (\\%)')
        ax.axhline(100, color='k', lw=0.6, ls=':')
        ax.legend(frameon=False, fontsize=8)
        ax.set_ylim(60, 102)
        fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig_deficit.pdf')); plt.close(fig)

        fig, ax = plt.subplots(figsize=(6.8, 3.6))
        # bar = change of the median indicator expressed as a ratio of medians,
        # identical to the Delta_1 column of tab_fix; error bar = bootstrap 95%
        # confidence interval for the median difference, in per cent.
        rngf = np.random.default_rng(0)
        means, errs, sigs = [], [], []
        for pp in range(len(PROBS)):
            a, b = finite(get('hostNBI', pp)), finite(get('hostN', pp))
            if len(a) and len(b):
                n = min(len(a), len(b)); a, b = a[:n], b[:n]
                md = (np.median(a) - np.median(b)) / np.median(a) * 100
                bs = np.empty(1200)
                for i in range(1200):
                    idx = rngf.integers(0, n, n)
                    bs[i] = (np.median(a[idx]) - np.median(b[idx])) / np.median(a[idx]) * 100
                lo, hi = np.percentile(bs, [2.5, 97.5])
                means.append(md)
                errs.append([[md - lo], [hi - md]])
                try:
                    p = wilcoxon(a, b).pvalue
                except Exception:
                    p = np.nan
                sigs.append(p < 0.05)
            else:
                means.append(np.nan); errs.append([[np.nan], [np.nan]]); sigs.append(False)
        y = np.arange(len(PROBS))
        cols = ['#c0392b' if (not np.isfinite(m) or m >= 0) else '#1e8449' for m in means]
        errs_arr = np.array([np.array([e[0][0] for e in errs], dtype=float),
                             np.array([e[1][0] for e in errs], dtype=float)])
        ax.barh(y, means, xerr=errs_arr, color=cols, alpha=0.88, error_kw=dict(lw=0.7))
        for i, s in enumerate(sigs):
            if s and np.isfinite(means[i]):
                ax.text(means[i] + 0.6, i, '*', va='center', ha='center',
                        fontsize=11, fontweight='bold')
        ax.axvline(0, color='k', lw=0.8)
        ax.set_yticks(y); ax.set_yticklabels(LAB, fontsize=6.5)
        ax.set_xlabel('change of the median indicator (%, ratio of medians, '
                      'positive = corrected host better)')
        ax.set_title('Effect of repair 1 on the host, per problem '
                     '(bar = median change, error bar = 95% bootstrap CI, '
                     '* = $p<0.05$)', fontsize=8)
        ax.invert_yaxis()
        fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig_main.pdf')); plt.close(fig)
        print('figures written')
    except Exception as e:
        print('figure error:', e)


if __name__ == '__main__':
    main()
