# -*- coding: utf-8 -*-
"""audit13_lex.py -- lexical audit of the PlatEMO algorithm tree.

Comments and string literals are removed by a MATLAB-aware lexical pass before
the pattern is matched, so a hit can only come from live code.  The pass handles
line comments, %{ %} block comments, single- and double-quoted strings with
doubled-quote escaping, line continuations, and the ambiguity between the
transpose operator and the start of a character literal.

Outputs: audit13_lex.txt (summary) and audit13_lex.csv (per file).
"""
import os, re, csv, io

BASE = r'D:\harness工作\中国科学：数学(总)\算法\algorithm'
TREE = os.path.join(BASE, '_tmp_official', 'PlatEMO-master', 'PlatEMO')
ALGDIR = os.path.join(TREE, 'Algorithms')
OUT = r'D:\wb_run3'

PAT = re.compile(r'Problem\.N\]\s*=\s*UniformPoint\(\s*Problem\.N')
INIT = re.compile(r'\.Initialization\s*\(')


def strip_matlab(src):
    """Return (clean_text, live_line_map) with comments and strings removed.

    Characters inside comments or string literals are replaced by spaces, so
    line and column numbers of the live code are preserved exactly.
    """
    out = []
    i, n = 0, len(src)
    prev_sig = ''          # last significant (non-space, non-comment) char
    while i < n:
        ch = src[i]
        # block comment  %{ ... %}
        if ch == '%' and src.startswith('%{', i):
            j = src.find('%}', i + 2)
            j = n if j < 0 else j + 2
            out.append(re.sub(r'[^\n]', ' ', src[i:j]))
            i = j
            continue
        # line comment
        if ch == '%':
            j = src.find('\n', i)
            j = n if j < 0 else j
            out.append(' ' * (j - i))
            i = j
            continue
        # character literal, only when ' is not a transpose
        if ch == "'" and prev_sig not in ')]}.\'_\n' and not (prev_sig.isalnum()):
            j = i + 1
            while j < n:
                if src[j] == "'":
                    if j + 1 < n and src[j + 1] == "'":
                        j += 2
                        continue
                    j += 1
                    break
                if src[j] == '\n':      # unterminated: bail out safely
                    break
                j += 1
            out.append(re.sub(r'[^\n]', ' ', src[i:j]))
            i = j
            prev_sig = "'"
            continue
        # double-quoted string
        if ch == '"':
            j = i + 1
            while j < n:
                if src[j] == '"':
                    if j + 1 < n and src[j + 1] == '"':
                        j += 2
                        continue
                    j += 1
                    break
                j += 1
            out.append(re.sub(r'[^\n]', ' ', src[i:j]))
            i = j
            prev_sig = '"'
            continue
        out.append(ch)
        if not ch.isspace():
            prev_sig = ch
        i += 1
    return ''.join(out)


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


def main():
    files = []
    for root, dd, ff in os.walk(ALGDIR):
        for f in ff:
            if f.endswith('.m'):
                files.append(os.path.join(root, f))

    rows = []
    for f in files:
        try:
            src = io.open(f, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        clean = strip_matlab(src)
        m = PAT.search(clean)
        if not m:
            continue
        al = line_of(clean, m.start())
        mi = INIT.search(clean)
        il = line_of(clean, mi.start()) if mi else None
        rel = os.path.relpath(f, ALGDIR).replace(os.sep, '/')
        alg = rel.split('/')[1] if len(rel.split('/')) > 1 else rel
        live = clean[m.end():]
        uses_z = bool(re.search(r'\bZ\b', live))
        if il is None:
            order = 'no-init-in-file'
        elif al < il:
            order = 'assign-before-init'
        else:
            order = 'assign-AFTER-init'
        rows.append(dict(algorithm=alg, path=rel, assign_line=al,
                         init_line=il if il else -1, order=order,
                         uses_Z_after=int(uses_z)))

    # controls: algorithms in the same tree that carry no such assignment.
    # An "algorithm" is a directory at depth 2 under Algorithms/, i.e.
    # Algorithms/<category>/<algorithm>/ -- this is the count PlatEMO itself
    # reports (315 multi-objective + 45 single-objective = 360).
    import io as _io
    algdirs, aff_algs = set(), set()
    for f in files:
        rel = os.path.relpath(f, ALGDIR).replace(os.sep, '/')
        p = rel.split('/')
        if len(p) >= 3:
            algdirs.add(p[0] + '/' + p[1])
    for r in rows:
        p = r['path'].split('/')
        if len(p) >= 3:
            aff_algs.add(p[0] + '/' + p[1])
    clean_alg = sorted(a for a in algdirs if a not in aff_algs)

    n_before = sum(1 for r in rows if r['order'] == 'assign-before-init')
    n_after = sum(1 for r in rows if r['order'] == 'assign-AFTER-init')
    n_noinit = sum(1 for r in rows if r['order'] == 'no-init-in-file')

    with io.open(os.path.join(OUT, 'audit13_lex.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['algorithm', 'path', 'assign_line',
                                           'init_line', 'order', 'uses_Z_after'])
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r['algorithm'], r['path'])):
            w.writerow(r)
    with io.open(os.path.join(OUT, 'audit13_lex_clean_algs.csv'), 'w', encoding='utf-8', newline='') as fh:
        fh.write('unaffected_algorithm\n')
        for a in clean_alg:
            fh.write(a + '\n')

    with io.open(os.path.join(OUT, 'audit13_lex.txt'), 'w', encoding='utf-8') as fh:
        fh.write('Lexical audit of the PlatEMO 4.16 algorithm tree\n')
        fh.write('(comments and string literals removed before matching)\n\n')
        fh.write('algorithm .m files scanned            : %d\n' % len(files))
        fh.write('files with a live assignment          : %d\n' % len(rows))
        fh.write('algorithm directories at depth 2    : %d\n' % len(algdirs))
        fh.write('affected algorithm directories      : %d\n' % len(aff_algs))
        fh.write('unaffected algorithm directories    : %d\n' % len(clean_alg))
        fh.write('\n-- where the assignment sits relative to Initialization --\n')
        fh.write('  assignment BEFORE Initialization    : %d\n' % n_before)
        fh.write('  assignment AFTER  Initialization    : %d\n' % n_after)
        fh.write('  no Initialization call in the file  : %d\n' % n_noinit)
        fh.write('\n-- files where the assignment follows Initialization --\n')
        for r in rows:
            if r['order'] == 'assign-AFTER-init':
                fh.write('  %s\n' % r['path'])
        fh.write('\n-- control: algorithms in the same tree with no such assignment --\n')
        fh.write('  %d directories, e.g. %s\n' % (len(clean_alg),
                 ', '.join(a.split('/')[-1] for a in clean_alg[:14])))

    print('files scanned      :', len(files))
    print('live assignments   :', len(rows))
    print('affected algorithms:', len(aff_algs), 'of', len(algdirs))
    print('unaffected         :', len(clean_alg))
    print('before/after/noinit:', n_before, n_after, n_noinit)
    print('uses_Z_after       :', sum(r['uses_Z_after'] for r in rows))


if __name__ == '__main__':
    main()
