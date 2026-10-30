# -*- coding: utf-8 -*-
"""Indicator agreement: exact hypervolume counterpart of the IGD comparison (Table S8, last column).

For each of the fifteen problems the published and repaired fronts are normalised
by the reference front's per-dimension range, the non-dominated subset is taken,
and the exact hypervolume is computed with a reference point at 1.1 (raised if a
front leaves the box). The sign of the hypervolume change is compared with the
sign of the IGD change.

Requires: numpy, scipy, pymoo.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from size_matched_igd import (load_arms, make_pf, my_igd, nd_first, runs,
                              PROBS, LAB)
from pymoo.indicators.hv import HV


def main():
    arms = load_arms()
    pub, rep = arms['hostNBI'], arms['hostN']
    print(f'{"problem":18s} {"IGD gain %":>11s} {"HV gain %":>10s} {"agree":>6s}')
    agree = 0
    hv_med = []
    for pp, (p, m, d) in enumerate(PROBS):
        PF = make_pf(p, m)
        lo, hi = PF.min(0), PF.max(0)
        rg = np.where(hi > lo, hi - lo, 1.0)
        pr, rr = runs(pub, pp), runs(rep, pp)
        n = min(len(pr), len(rr))
        pr, rr = pr[:n], rr[:n]

        pts = [(nd_first(x) - lo) / rg for x in pr + rr]
        mx = max(float(np.max(P)) for P in pts)
        hv = HV(ref_point=np.full(PF.shape[1], max(1.1, mx + 0.1)))

        ip = [my_igd(a, PF) for a in pr]
        ir = [my_igd(b, PF) for b in rr]
        hp = [float(hv((nd_first(a) - lo) / rg)) for a in pr]
        hr = [float(hv((nd_first(b) - lo) / rg)) for b in rr]

        g_igd = 100 * (np.median(ip) - np.median(ir)) / np.median(ip)
        g_hv = 100 * (np.median(hr) - np.median(hp)) / np.median(hp)
        hv_med.append(g_hv)
        ok = np.sign(g_igd) == np.sign(g_hv)
        agree += int(ok)
        print(f'{LAB[pp]:18s} {g_igd:11.2f} {g_hv:10.2f} {"yes" if ok else "NO":>6s}')

    print('\nsign agreement: %d/15' % agree)
    print('median IGD gain %.2f%% | median HV gain %.2f%%'
          % (np.median([100 * (np.median([my_igd(a, make_pf(p, m)) for a in runs(pub, pp)])
                               - np.median([my_igd(b, make_pf(p, m)) for b in runs(rep, pp)]))
                        / np.median([my_igd(a, make_pf(p, m)) for a in runs(pub, pp)])
                        for pp, (p, m, d) in enumerate(PROBS)]),
             np.median(hv_med)))


if __name__ == '__main__':
    main()
