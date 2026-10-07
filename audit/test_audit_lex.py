# -*- coding: utf-8 -*-
"""test_audit_lex.py -- positive and negative tests for the lexical audit.

Each case is a small MATLAB snippet with a known expected verdict.  The audit
must find the assignment in the positives and miss it in the negatives; a
negative that is missed because the pattern is assembled dynamically is a
documented limitation, marked LIMIT rather than PASS.

Run:  python test_audit_lex.py
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit13_lex import strip_matlab, PAT

CASES = [
    # (name, source, expect_match)
    ('plain assignment',
     "function f()\n  [Z,Problem.N] = UniformPoint(Problem.N,Problem.M);\nend\n", True),
    ('spaces around the operator',
     "[Z, Problem.N]   =   UniformPoint( Problem.N , Problem.M);", True),
    ('split over a line continuation',
     "[Z,Problem.N] = ...\n    UniformPoint(Problem.N,Problem.M);", True),
    ('line comment only',
     "% [Z,Problem.N] = UniformPoint(Problem.N,Problem.M);", False),
    ('trailing comment after other code',
     "x = 1;  % [Z,Problem.N] = UniformPoint(Problem.N,Problem.M);", False),
    ('block comment',
     "%{\n[Z,Problem.N] = UniformPoint(Problem.N,Problem.M);\n%}", False),
    ('single-quoted string',
     "s = '[Z,Problem.N] = UniformPoint(Problem.N,Problem.M);';", False),
    ('double-quoted string',
     's = "[Z,Problem.N] = UniformPoint(Problem.N,Problem.M);";', False),
    ('string containing a percent sign',
     "s = '100% done'; [Z,Problem.N] = UniformPoint(Problem.N,Problem.M);", True),
    ('transpose before the hit',
     "A = B'; [Z,Problem.N] = UniformPoint(Problem.N,Problem.M);", True),
    ('escaped quote inside a string',
     "s = 'it''s [Z,Problem.N] = UniformPoint(Problem.N,Problem.M);';", False),
    ('assembled dynamically (documented limitation)',
     "expr = '[Z,Problem.N] = UniformPoint(Problem.N,Problem.M);';\neval(expr);", False),
    ('name built with sprintf (documented limitation)',
     "cmd = sprintf('[Z,Problem.N] = %s(Problem.N,Problem.M);','UniformPoint');\neval(cmd);", False),
    ('assignment in a different helper file, live',
     "function g(P)\n  [W,P.N] = UniformPoint(P.N,P.M);\nend\n", False),
]

LIMIT = {'assembled dynamically (documented limitation)',
         'name built with sprintf (documented limitation)'}


def main():
    npass = nfail = nlimit = 0
    print('%-52s %-10s %-10s %s' % ('case', 'expected', 'found', 'verdict'))
    print('-' * 88)
    for name, src, expect in CASES:
        clean = strip_matlab(src)
        got = bool(PAT.search(clean))
        if name in LIMIT:
            verdict = 'LIMIT (known, disclosed)'
            nlimit += 1
        elif got == expect:
            verdict = 'PASS'
            npass += 1
        else:
            verdict = 'FAIL'
            nfail += 1
        print('%-52s %-10s %-10s %s' % (name, expect, got, verdict))
    print('-' * 88)
    print('passed %d, failed %d, disclosed limitations %d' % (npass, nfail, nlimit))
    return 1 if nfail else 0


if __name__ == '__main__':
    sys.exit(main())
