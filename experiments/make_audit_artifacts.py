#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mkart_audit.py -- generate the audit-derived figures, tables and macros.

Reads the outputs of the round-13 audit
    D:/wb_run3/audit13_dyn.csv      three-quantity trace of sixteen algorithms
    D:/wb_run3/audit13_lex.csv      per-file lexical classification
    D:/wb_run3/audit13_lex.txt      summary
and writes
    paper_scis/tables/tab_trace.tex
    paper_scis/supp/trace_three_quantities.csv
    paper_scis/numbers_audit.tex
"""
import os, io, csv

SRC = r'D:\wb_run3'
PAPER = r'D:\harness工作\中国科学：数学(总)\算法\algorithm\paper_scis'
TAB = os.path.join(PAPER, 'tables')
SUPP = os.path.join(PAPER, 'supp')
os.makedirs(TAB, exist_ok=True)
os.makedirs(SUPP, exist_ok=True)

DYN = os.path.join(SRC, 'audit13_dyn.csv')
LEX = os.path.join(SRC, 'audit13_lex.csv')
LEXTXT = os.path.join(SRC, 'audit13_lex.txt')



# PlatEMO class name -> the name the paper and the reader should see
DISPLAY = {
    'NSGAIII': 'NSGA-III', 'NSGAII': 'NSGA-II', 'MOEAD': 'MOEA/D',
    'MOEADDRA': 'MOEA/D-DRA', 'MOEADDE': 'MOEA/D-DE', 'MOEADSTM': 'MOEA/D-STM',
    'CTAEA': 'C-TAEA', 'RVEA': 'RVEA', 'RVEAa': 'RVEAa', 'LMOCSO': 'LMOCSO',
    'FDSEA': 'FDSEA', 'HEA': 'HEA', 'DGEA': 'DGEA', 'PPS': 'PPS',
    'SPEA2': 'SPEA2', 'IBEA': 'IBEA',
}


def disp(name):
    return DISPLAY.get(name, name)

def read_dyn():
    rows = []
    with io.open(DYN, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    return rows


def read_lex():
    rows = []
    with io.open(LEX, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    return rows


def main():
    dyn = read_dyn()
    lex = read_lex()
    N = {}

    # ---------------------------------------------------------- trace table
    # affected = the realised count is below the request; control = equal
    aff, ctl = [], []
    for r in dyn:
        try:
            nreq = int(r['N_req']); nreal = int(r['N_real'])
        except (ValueError, KeyError):
            continue
        (aff if nreal < nreq else ctl).append(r)

    lines = [r'\footnotesize', r'\setlength{\tabcolsep}{5pt}',
             r'\begin{tabular}{lrrrrl}', r'\toprule',
             r'algorithm & $N_{\mathrm{req}}$ & $L$ & $N_{\mathrm{real}}$ & $N_{\mathrm{rep}}$ & status \\',
             r'\midrule']
    for r in aff:
        lines.append('%s & %s & %s & %s & %s & diverges \\\\' % (
            disp(r['algorithm']), r['N_req'], r['UniformPoint_returned'],
            r['N_real'], r['Problem_N_after']))
    lines.append(r'\addlinespace')
    for r in ctl:
        lines.append('%s & %s & %s & %s & %s & faithful \\\\' % (
            disp(r['algorithm']), r['N_req'], r['UniformPoint_returned'],
            r['N_real'], r['Problem_N_after']))
    lines += [r'\bottomrule', r'\end{tabular}']
    with io.open(os.path.join(TAB, 'tab_trace.tex'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines) + '\n')

    N['nTraced'] = len(aff) + len(ctl)
    N['nTracedAff'] = len(aff)
    N['nTracedCtl'] = len(ctl)
    N['nRealMin'] = min((int(r['N_real']) for r in aff), default=91)
    N['nRealMinAlg'] = disp(next((r['algorithm'] for r in aff
                                  if int(r['N_real']) == N['nRealMin']), ''))
    N['ctlNames'] = ', '.join(disp(r['algorithm']) for r in ctl)

    with io.open(os.path.join(SUPP, 'trace_three_quantities.csv'), 'w',
                 encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['algorithm', 'N_requested', 'constructor_returned',
                    'N_realised', 'Problem_N_after_run', 'status'])
        for r in aff + ctl:
            w.writerow([r['algorithm'], r['N_req'], r['UniformPoint_returned'],
                        r['N_real'], r['Problem_N_after'],
                        'diverges' if r in aff else 'faithful'])

    # ---------------------------------------------------------- lexical census
    n_files = len(lex)
    n_before = sum(1 for r in lex if r['order'] == 'assign-before-init')
    n_after = sum(1 for r in lex if r['order'] == 'assign-AFTER-init')
    n_noinit = sum(1 for r in lex if r['order'] == 'no-init-in-file')
    n_z = sum(1 for r in lex if r['uses_Z_after'] == '1')
    N['nLexFiles'] = n_files
    N['nLexBefore'] = n_before
    N['nLexAfter'] = n_after
    N['nLexNoInit'] = n_noinit
    N['nLexReuseZ'] = n_z
    N['pctLexBefore'] = '%.0f' % (100.0 * n_before / max(1, n_files))
    if os.path.exists(LEXTXT):
        txt = io.open(LEXTXT, encoding='utf-8').read()
        import re
        # nAlgTotal / nAlgAffected / pctAlgAffected / nFilesTotal are emitted by
        # mkart_scis.py from the same tree, so they are not repeated here.
        m = re.search(r'unaffected algorithm directories\s*:\s*(\d+)', txt)
        if m:
            N['nAlgFaithful'] = int(m.group(1))

    out = ['\\newcommand{\\%s}{%s}' % (k, v) for k, v in N.items()]
    with io.open(os.path.join(PAPER, 'numbers_audit.tex'), 'w',
                 encoding='utf-8', newline='\n') as fh:
        fh.write('%% generated by mkart_audit.py -- do not edit\n')
        fh.write('\n'.join(out) + '\n')

    print('traced algorithms      :', N['nTraced'],
          '(diverging %d, faithful %d)' % (N['nTracedAff'], N['nTracedCtl']))
    print('min realised population:', N['nRealMin'], 'in', N['nRealMinAlg'])
    print('lexical files          :', n_files, '| before/after/noinit:',
          n_before, n_after, n_noinit, '| reuse Z:', n_z)
    print('algorithms             :', N.get('nAlgAffected'), 'of', N.get('nAlgTotal'))
    print('wrote tab_trace.tex, trace_three_quantities.csv, numbers_audit.tex')


if __name__ == '__main__':
    main()
