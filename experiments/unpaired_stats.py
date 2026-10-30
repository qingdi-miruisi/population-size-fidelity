import sys, numpy as np
sys.path.insert(0,'wb_run3'); import sizematch as S
from scipy.stats import mannwhitneyu, wilcoxon
arms=S.load_arms(); pub,rep=arms['hostNBI'],arms['hostN']
rows=[]
for pp,(p,m,d) in enumerate(S.PROBS):
    PF=S.make_pf(p,m)
    a=[S.my_igd(x,PF) for x in S.runs(pub,pp)]
    b=[S.my_igd(x,PF) for x in S.runs(rep,pp)]
    n=min(len(a),len(b)); a,b=a[:n],b[:n]
    pu=mannwhitneyu(a,b,alternative='two-sided').pvalue
    try: ppv=wilcoxon(a,b).pvalue
    except Exception: ppv=float('nan')
    rows.append((S.LAB[pp],pu,ppv)); print(f'{S.LAB[pp]:18s} {pu:10.4f} {ppv:9.4f}', flush=True)
ps=np.array([[r[1],r[2]] for r in rows])
order=np.argsort(ps[:,0]); holm=np.empty(len(ps)); mt=0
for rank,i in enumerate(order):
    mt=max(mt,min(1,(len(ps)-rank)*ps[i,0])); holm[i]=mt
print('\nunpaired p<0.05:', int((ps[:,0]<0.05).sum()))
print('unpaired Holm survivors:', int((holm<0.05).sum()), [rows[i][0] for i in range(len(holm)) if holm[i]<0.05])
print('paired p<0.05:', int(np.nansum(ps[:,1]<0.05)))
