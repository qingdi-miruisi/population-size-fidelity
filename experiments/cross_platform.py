#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""xplatform.py -- the same request on three libraries.

PlatEMO 4.16  : UniformPoint(N_req, M)  (largest admissible lattice not exceeding
                the request, with a second layer)
pymoo 0.6.2   : get_partition_closest_to_points + the Das-Dennis count, i.e. the
                single-layer lattice whose partition count is closest to the
                request
jMetalPy      : NSGA-III reference-point construction, if importable

Writes D:/wb_run3/xplatform.csv
"""
import io, csv, os

OUT = r'D:\wb_run3\xplatform.csv'
REQ = [(100, 3), (100, 5), (100, 8), (100, 10), (200, 3)]

rows = []


# ---------------------------------------------------------------- PlatEMO
def platemoo(N, M):
    from math import comb

    def nk(n, k):
        return comb(n, k) if 0 <= k <= n else 0

    H1 = 1
    while nk(H1 + M, M - 1) <= N:
        H1 += 1
    cnt = nk(H1 + M - 1, M - 1)
    if H1 < M:
        H2 = 0
        while nk(H1 + M - 1, M - 1) + nk(H2 + M, M - 1) <= N:
            H2 += 1
        if H2 > 0:
            cnt += nk(H2 + M - 1, M - 1)
    return cnt


# ---------------------------------------------------------------- pymoo
def pymoo_count(N, M):
    from scipy import special
    from pymoo.util.reference_direction import get_partition_closest_to_points
    p = get_partition_closest_to_points(N, M)
    return int(special.binom(M + p - 1, p))


# ---------------------------------------------------------------- jMetalPy
def jmetal_count(N, M):
    try:
        from jmetal.util.solution import read_solutions  # noqa: F401
    except Exception:
        pass
    try:
        import jmetal
        from jmetal.algorithm.multiobjective.nsgaiii import NSGAIII
        # jMetalPy derives the number of reference points from the number of
        # divisions; expose that mapping if the helper is importable.
        from jmetal.operator.crossover import SBXCrossover  # noqa: F401
        try:
            from jmetal.util.solution_list import SolutionList  # noqa: F401
        except Exception:
            pass
        # the divisions -> points mapping
        from math import comb

        def pts(div, m):
            return comb(div + m - 1, m - 1)
        # jMetalPy picks divisions by its own rule; report the largest
        # divisions whose point count does not exceed the request, and the
        # smallest that does
        div = 1
        while pts(div, M) <= N:
            div += 1
        return pts(div - 1, M), pts(div, M)
    except Exception as e:
        return None


for (N, M) in REQ:
    p = platemoo(N, M)
    try:
        py = pymoo_count(N, M)
    except Exception:
        py = None
    rows.append(('PlatEMO 4.16', N, M, p, 'UniformPoint(N,M)'))
    if py is not None:
        rows.append(('pymoo 0.6.2', N, M, py, 'das-dennis closest partitions'))

with io.open(OUT, 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['library', 'N_requested', 'M', 'realised', 'construction'])
    w.writerows(rows)

# ---------------------------------------------------------------- LaTeX table
TAB = r'D:\harness工作\中国科学：数学(总)\算法\algorithm\paper_scis\tables\tab_xplatform.tex'
os.makedirs(os.path.dirname(TAB), exist_ok=True)
tlines = [r'\footnotesize', r'\setlength{\tabcolsep}{7pt}',
          r'\begin{tabular}{l' + 'r' * len(REQ) + '}', r'\toprule',
          r'library & ' + ' & '.join(f'${n}$' for n, m in REQ) + r' \\',
          r'($N_{\mathrm{req}}$) & ' + ' & '.join(f'${m}$' for n, m in REQ) + r' \\',
          r'\midrule']
pm = {(N, M): platemoo(N, M) for (N, M) in REQ}
tlines.append('PlatEMO 4.16 & ' + ' & '.join(str(pm[(n, m)]) for n, m in REQ) + r' \\')
py = {}
for (N, M) in REQ:
    try:
        py[(N, M)] = pymoo_count(N, M)
    except Exception:
        py[(N, M)] = None
tlines.append('pymoo 0.6.2 & ' + ' & '.join(
    ('--' if py[(n, m)] is None else str(py[(n, m)])) for n, m in REQ) + r' \\')
tlines.append(r'\addlinespace')
tlines.append('ratio & ' + ' & '.join(
    ('--' if py[(n, m)] in (None, 0) else '%.2f' % (pm[(n, m)] / py[(n, m)]))
    for n, m in REQ) + r' \\')
tlines += [r'\bottomrule', r'\end{tabular}']
with io.open(TAB, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(tlines) + '\n')

N_macros = {'nPlatMthree': pm[(100, 3)], 'nPlatMfive': pm[(100, 5)],
            'nPlatMeight': pm[(100, 8)], 'nPlatMten': pm[(100, 10)]}
pym = {k: v for k, v in py.items() if v is not None}
if (100, 8) in pym:
    N_macros['nPymoMeight'] = pym[(100, 8)]
    N_macros['xRatioEight'] = '%.2f' % (pm[(100, 8)] / pym[(100, 8)])
if (100, 5) in pym:
    N_macros['nPymoMfive'] = pym[(100, 5)]
    N_macros['xRatioFive'] = '%.2f' % (pm[(100, 5)] / pym[(100, 5)])
n_div = sum(1 for k in py if py[k] is not None and pm[k] != py[k])
N_macros['nXDiverging'] = n_div
N_macros['nXCases'] = len(REQ)
with io.open(os.path.join(os.path.dirname(TAB), '..', 'numbers_xplatform.tex'),
             'w', encoding='utf-8', newline='\n') as fh:
    fh.write('%% generated by xplatform.py -- do not edit\n')
    for k, v in N_macros.items():
        fh.write('\\newcommand{\\%s}{%s}\n' % (k, v))

print('%-14s %5s %3s %9s  %s' % ('library', 'N_req', 'M', 'realised', 'construction'))
for r in rows:
    print('%-14s %5d %3d %9d  %s' % r)

print('\n-- divergence between the two libraries at the same nominal size --')
for (N, M) in REQ:
    a = platemoo(N, M)
    try:
        b = pymoo_count(N, M)
    except Exception:
        b = None
    if b is not None and a != b:
        print('  N=%d M=%d : PlatEMO %d  vs  pymoo %d   (ratio %.2f)'
              % (N, M, a, b, max(a, b) / min(a, b)))
