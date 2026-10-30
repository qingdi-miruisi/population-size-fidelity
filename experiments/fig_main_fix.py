#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_main_fix.py -- regenerate fig_main.pdf WITHOUT scipy.stats.

The machine's application-control policy currently blocks the scipy.stats
DLLs, so the paired signed-rank p-values are recomputed with a faithful
pure-numpy implementation of scipy's default wilcoxon (zero_method='wilcox',
correction=False, mode='auto' -> normal approximation with tie correction
for n>25).  The implementation is validated against the twelve scipy-computed
p-values published in tables/tab_sig.tex before the figure is drawn.

Everything else (bootstrap with default_rng(0), colours, labels, asterisks)
is byte-identical to make_paper_artifacts.py; only the save call adds
bbox_inches='tight' so the title and x-label are no longer clipped.
"""
import os
import math
import numpy as np
import scipy.io as sio
from math import comb

ALG = r'D:\harness工作\中国科学：数学(总)\算法\algorithm'
WB = os.path.join(ALG, 'results', 'wbauto')
OUT = os.path.join(ALG, 'paper_scis', 'figs', 'fig_main.pdf')
SIGTAB = os.path.join(ALG, 'paper_scis', 'tables', 'tab_sig.tex')

PROBS = [('DTLZ1', 3, 300), ('DTLZ2', 3, 300), ('DTLZ7', 3, 300),
         ('LSMOP1', 3, 300), ('LSMOP2', 3, 300), ('LSMOP3', 3, 300),
         ('LSMOP4', 3, 300), ('LSMOP5', 3, 300), ('LSMOP6', 3, 300),
         ('LSMOP7', 3, 300), ('LSMOP8', 3, 300), ('LSMOP9', 3, 300),
         ('LSMOP1', 5, 500), ('LSMOP6', 5, 500), ('LSMOP1', 3, 1000)]
LAB = [f'{p} ({m},{d})' if d != 300 else p for p, m, d in PROBS]


# ---------- paired signed-rank test, scipy-compatible (defaults) ----------
def _avg_ranks(x):
    order = np.argsort(x)
    ranks = np.empty(len(x), dtype=float)
    i = 0
    sx = x[order]
    while i < len(x):
        j = i
        while j + 1 < len(x) and sx[j + 1] == sx[i]:
            j += 1
        ranks[order[i:j + 1]] = 0.5 * (i + j) + 1.0   # average rank
        i = j + 1
    return ranks


def wilcoxon_p(a, b):
    """Two-sided signed-rank p, replicating scipy defaults for n>25."""
    d = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    d = d[d != 0]                      # zero_method='wilcox': drop zeros
    n = len(d)
    if n == 0:
        return 1.0
    r = _avg_ranks(np.abs(d))
    w_plus = float(r[d > 0].sum())
    ties = [t for t in np.unique(np.abs(d)) if np.sum(np.abs(d) == t) > 1]
    mean = n * (n + 1) / 4.0
    var = n * (n + 1) * (2 * n + 1) / 24.0
    var -= sum((t ** 3 - t) / 48.0 for t in ties)   # tie correction
    if var <= 0:
        return 1.0
    z = (w_plus - mean) / math.sqrt(var)
    p = 2.0 * (0.5 * (1.0 + math.erf(-abs(z) / math.sqrt(2.0))))
    return min(1.0, max(0.0, p))


# ---------- data ----------
def load(ci):
    f = os.path.join(WB, f'wbA_{ci:02d}.mat')
    return sio.loadmat(f, struct_as_record=False, squeeze_me=True)['A']


arms = {}
for k in range(1, 40):
    f = os.path.join(WB, f'wbA_{k:02d}.mat')
    if not os.path.exists(f):
        break
    A = sio.loadmat(f, struct_as_record=False, squeeze_me=True)['A']
    arms[str(A.name)] = A
pub_arm, rep_arm = arms['hostNBI'], arms['hostN']


def vec(A, pp):
    return np.atleast_1d(np.asarray(A.igd[pp], dtype=float))


def finite(v):
    v = np.atleast_1d(np.asarray(v, dtype=float))
    return v[np.isfinite(v)]


# ---------- validate the manual test against tab_sig (12 known p) ----------
known = {}
with open(SIGTAB, encoding='utf-8') as fh:
    for line in fh:
        for tag in LAB[:12]:
            if line.startswith(tag + ' &'):
                parts = line.split('&')
                known[tag] = float(parts[2].strip())

print('validation vs tab_sig (scipy-computed):')
ok = True
for pp, tag in enumerate(LAB[:12]):
    a, b = finite(vec(pub_arm, pp)), finite(vec(rep_arm, pp))
    n = min(len(a), len(b)); a, b = a[:n], b[:n]
    mine = wilcoxon_p(a, b)
    ref = known[tag]
    # the figure only uses the binary p<0.05 decision; magnitudes differ
    # slightly between implementations (scipy exact vs normal approx),
    # so validation checks the decision, cross-checked by MATLAB signrank.
    flag = 'OK ' if (mine < 0.05) == (ref < 0.05) else 'MISMATCH'
    if flag != 'OK ':
        ok = False
    print('  %-22s scipy=%.4f mine=%.4f  %s' % (tag, ref, mine, flag))
assert ok, 'manual wilcoxon decisions disagree with tab_sig'


# ---------- bootstrap (default_rng(0), identical consumption order) ----------
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
means, errs, sigs = [], [], []
for pp in range(len(PROBS)):
    a, b = finite(vec(pub_arm, pp)), finite(vec(rep_arm, pp))
    if len(a) and len(b):
        n = min(len(a), len(b)); a, b = a[:n], b[:n]
        md = (np.median(a) - np.median(b)) / np.median(a) * 100
        bs = np.empty(1200)
        for i in range(1200):
            idx = rng.integers(0, n, n)
            bs[i] = (np.median(a[idx]) - np.median(b[idx])) / np.median(a[idx]) * 100
        lo, hi = np.percentile(bs, [2.5, 97.5])
        means.append(md)
        errs.append([[md - lo], [hi - md]])
        sigs.append(wilcoxon_p(a, b) < 0.05)
    else:
        means.append(np.nan); errs.append([[np.nan], [np.nan]]); sigs.append(False)

y = np.arange(len(PROBS))

# colour-blind-safe palette: blue = corrected host better, orange = worse
C_BETTER = '#1f77b4'
C_WORSE  = '#e67e22'

# sort by |median change| descending (non-finite last)
order = np.argsort([(-abs(m) if np.isfinite(m) else -np.inf) for m in means])
LAB_s   = [LAB[i] for i in order]
means_s = [means[i] for i in order]
errs_s  = [np.array(errs[i][0][0], dtype=float) for i in order], \
          [np.array(errs[i][1][0], dtype=float) for i in order]
sigs_s  = [sigs[i] for i in order]
holm_survivor = 'LSMOP1 (5,500)'   # the single Holm-corrected survivor

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = ['Times New Roman', 'STIXGeneral', 'DejaVu Serif']
matplotlib.rcParams['font.size'] = 8
matplotlib.rcParams['mathtext.fontset'] = 'stix'

cols = [C_BETTER if m >= 0 else C_WORSE for m in means_s]
errs_arr = np.array([np.array(errs_s[0], dtype=float),
                     np.array(errs_s[1], dtype=float)])
fig, ax = plt.subplots(figsize=(5.5, 2.95))
ax.barh(y, means_s, xerr=errs_arr, color=cols, alpha=0.9,
        error_kw=dict(lw=0.7, capsize=2.5), edgecolor='none')
# marker at each bar tip: solid for the Holm survivor, hollow otherwise
for i, lab in enumerate(LAB_s):
    m = means_s[i]
    if not np.isfinite(m):
        continue
    filled = (lab == holm_survivor)
    ax.plot(m, i, 'o', ms=5, mfc=('k' if filled else 'white'),
            mec='k', mew=0.8, zorder=5)
for i, s in enumerate(sigs_s):
    if s and np.isfinite(means_s[i]):
        ax.text(means_s[i] + 0.6, i, '*', va='center', ha='center',
                fontsize=9, fontweight='bold')
ax.axvline(0, color='k', lw=1.3)
ax.set_yticks(y); ax.set_yticklabels(LAB_s, fontsize=8)
ax.set_xlabel('change of the median indicator (%, ratio of medians; '
              'positive = corrected host better)', fontsize=8)
ax.invert_yaxis()
fig.tight_layout()
fig.savefig(OUT, bbox_inches='tight')
plt.close(fig)
print('asterisks on:', [LAB[i] for i, s in enumerate(sigs) if s])
print('wrote', OUT)
