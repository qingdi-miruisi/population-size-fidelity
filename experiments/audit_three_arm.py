# -*- coding: utf-8 -*-
"""Round-12 reviewer-response analysis: three-arm control, effect sizes, gamma_min, census."""
import os, sys, glob, json
import numpy as np
import scipy.io as sio
from scipy.stats import wilcoxon, mannwhitneyu

WB = os.path.join(r'D:\harness工作\中国科学：数学(总)\算法\algorithm', 'results', 'wbauto')
os.chdir(WB)

cfgs = {}
for f in sorted(glob.glob('wbA_*.mat')):
    A = sio.loadmat(f, struct_as_record=False, squeeze_me=True)['A']
    cfgs[A.name] = A

P = [('DTLZ1',3,300),('DTLZ2',3,300),('DTLZ7',3,300),
     ('LSMOP1',3,300),('LSMOP2',3,300),('LSMOP3',3,300),('LSMOP4',3,300),
     ('LSMOP5',3,300),('LSMOP6',3,300),('LSMOP7',3,300),('LSMOP8',3,300),('LSMOP9',3,300),
     ('LSMOP1',5,500),('LSMOP6',5,500),('LSMOP1',3,1000)]
LAB = [f'{p} ({m},{d})' if d != 300 else p for p, m, d in P]

def v(name, pp):
    arr = cfgs[name].igd
    if pp >= len(arr):
        return np.array([], dtype=float)
    return np.atleast_1d(np.asarray(arr[pp], dtype=float))

def cliff(a, b):
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) == 0 or len(b) == 0:
        return np.nan
    U = mannwhitneyu(a, b, alternative='two-sided', method='asymptotic').statistic
    return 2.0 * U / (len(a) * len(b)) - 1.0

out = {}
out['configs'] = sorted(cfgs.keys())

# ---- three-arm control -------------------------------------------------
arms = []
for pp, lab in enumerate(LAB):
    a, b, c = v('hostNBI', pp), v('host91', pp), v('hostN', pp)
    if len(b) == 0:
        continue
    n = min(len(a), len(b)); n2 = min(len(b), len(c))
    try: p1 = float(wilcoxon(a[:n], b[:n]).pvalue)
    except Exception: p1 = float('nan')
    try: p2 = float(wilcoxon(b[:n2], c[:n2]).pvalue)
    except Exception: p2 = float('nan')
    arms.append(dict(prob=lab, n=int(len(b)),
                     med_nbi=float(np.nanmedian(a)), med_91=float(np.nanmedian(b)),
                     med_100=float(np.nanmedian(c)),
                     p_nbi_91=p1, d_nbi_91=cliff(a, b),
                     p_91_100=p2, d_91_100=cliff(b, c)))
out['three_arm'] = arms

# ---- effect size hostNBI vs hostN, all 15 ------------------------------
rng = np.random.default_rng(0)
eff = []
for pp, lab in enumerate(LAB):
    a, b = v('hostNBI', pp), v('hostN', pp)
    if len(a) == 0 or len(b) == 0:
        continue
    m = a[np.isfinite(a)]; q = b[np.isfinite(b)]
    n = min(len(m), len(q)); m, q = m[:n], q[:n]
    md = float(np.median(q) - np.median(m))
    bs = np.empty(1500)
    for i in range(1500):
        idx = rng.integers(0, n, n)
        bs[i] = np.median(q[idx]) - np.median(m[idx])
    lo, hi = np.percentile(bs, [2.5, 97.5])
    eff.append(dict(prob=lab, cliff=cliff(a, b), dmed=md,
                    lo=float(lo), hi=float(hi), crosses0=bool(lo * hi < 0)))
out['effect'] = eff

# ---- layer vs both references, all 15 ---------------------------------
lay = []
for pp, lab in enumerate(LAB):
    a, b, c = v('hostNBI', pp), v('hostN', pp), v('layer', pp)
    if len(c) == 0:
        continue
    ma, mb, mc = np.nanmedian(a), np.nanmedian(b), np.nanmedian(c)
    g1 = (ma - mc) / ma * 100.0 if ma else np.nan
    g2 = (mb - mc) / mb * 100.0 if mb else np.nan
    n = min(len(a), len(c)); n2 = min(len(b), len(c))
    try: p1 = float(wilcoxon(a[:n], c[:n]).pvalue)
    except Exception: p1 = float('nan')
    try: p2 = float(wilcoxon(b[:n2], c[:n2]).pvalue)
    except Exception: p2 = float('nan')
    lay.append(dict(prob=lab, host=float(ma), hostN=float(mb), layer=float(mc),
                    g_vs_host=float(g1), g_vs_hostN=float(g2), p1=p1, p2=p2))
out['layer'] = lay

# ---- static best per problem vs layer ---------------------------------
STAT = ['e5g0','e5g7','e5g3','e10g7','e20g0']
st = []
for pp, lab in enumerate(LAB):
    vals = {}
    for s in STAT:
        if s in cfgs:
            vv = np.atleast_1d(np.asarray(cfgs[s].igd[pp], dtype=float))
            if len(vv): vals[s] = float(np.nanmedian(vv))
    if not vals: continue
    best = min(vals, key=vals.get)
    st.append(dict(prob=lab, best=best, bestval=vals[best],
                   layerv=float(np.nanmedian(v('layer', pp))) if len(v('layer', pp)) else np.nan))
out['static_best'] = st

with open(r'D:\wb_run3\audit_r12.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1)

# ---- console summary ---------------------------------------------------
print('configs:', out['configs'])
print('\n=== three-arm control (problems run at N_req=91 too) ===')
print(f"{'prob':12s}{'medNBI':>9s}{'med91':>9s}{'med100':>9s}{'p(NBI,91)':>11s}{'D':>7s}{'p(91,100)':>11s}{'D':>7s}")
for r in arms:
    print(f"{r['prob']:12s}{r['med_nbi']:9.4f}{r['med_91']:9.4f}{r['med_100']:9.4f}"
          f"{r['p_nbi_91']:11.4f}{r['d_nbi_91']:+7.3f}{r['p_91_100']:11.4f}{r['d_91_100']:+7.3f}")

print('\n=== effect size NBI vs hostN (15) ===')
signif = 0
for r in eff:
    flag = 'CI crosses 0' if r['crosses0'] else 'CI > 0'
    if not r['crosses0']: signif += 1
    print(f"  {r['prob']:16s} Cliff={r['cliff']:+.3f} dMed={r['dmed']:+.5f} "
          f"[{r['lo']:+.5f},{r['hi']:+.5f}] {flag}")
print(f"  problems whose median-difference 95% CI excludes 0: {signif}/{len(eff)}")

print('\n=== layer vs host and hostN, all 15 ===')
for r in lay:
    print(f"  {r['prob']:16s} layer-host={r['g_vs_host']:+7.2f}% (p={r['p1']:.4f})  "
          f"layer-hostN={r['g_vs_hostN']:+7.2f}% (p={r['p2']:.4f})")
