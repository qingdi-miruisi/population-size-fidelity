# population-size-fidelity

Reference data, audit scripts and experiment code for the manuscript

> **A population-size fidelity framework for reference-vector multi-objective
> evolutionary algorithms with an audit of PlatEMO**

submitted as a RESEARCH PAPER to *SCIENCE CHINA Information Sciences*.

---

## What this repository is about

A reference-vector multi-objective evolutionary algorithm derives its population
from a reference-vector constructor. The credibility of a comparison between two
such algorithms rests on the population size actually used being the one the
study reports — and that assumption can fail silently.

We separate three quantities that are usually conflated:

| symbol | meaning |
|---|---|
| `N_req` | the size the study requests and declares |
| `N_real` | the size the method actually evaluates |
| `N_rep` | the size the run records |

The framework has four parts: a fidelity principle (a definition plus two
propositions with proofs), an audit, a catalogue of algorithm-dependent
corrections, and a reporting protocol. Applied to PlatEMO 4.16 it finds the
assignment `[Z,Problem.N] = UniformPoint(Problem.N,Problem.M);` in **84 of 1887**
algorithm source files, belonging to **83 of the platform's 360 algorithms**.

The consequence is easiest to see directly. All of the following are launched
with `N_req = 100` at three objectives in the same release:

| algorithm | `N_req` | `N_real` | `N_rep` |
|---|---|---|---|
| NSGA-III, MOEA/D, FDSEA, HEA, C-TAEA | 100 | 91 | 91 |
| RVEA | 100 | 83 | 91 |
| DGEA | 100 | 80 | 91 |
| LMOCSO | 100 | 66 | 91 |
| RVEAa | 100 | 31 | 91 |
| NSGA-II, SPEA2, IBEA | 100 | 100 | 100 |

The platform is *not* misreporting: it faithfully records what happened. What is
missing is any signal that the request was not honoured, so a table that prints
`N = 100` for NSGA-III and for NSGA-II compares 91 individuals with 100.

The same nominal request also means different things in different libraries. At
eight objectives, `N_req = 100` realises **72** directions in PlatEMO and **36**
in pymoo — a factor of two.

## Layout

```
audit/            the audit itself
  audit13_lex.py        lexical audit (comments and strings removed first)
  audit13.m             AST pass and the dynamic three-quantity probe
  audit13_lex.csv       per-file classification, with line numbers
  audit13_dyn.csv       the three quantities for 16 algorithms
  affected_files.csv    the 84 affected files, with algorithm, line and code

experiments/      how the numbers were produced
  wbauto.m              the round-3 configuration grid
  wb13.m                the round-13 arms (declared-size arm, K sweep)
  make_paper_artifacts.py    regenerates tables/, figs/ and numbers.tex
  make_audit_artifacts.py    regenerates the audit-derived tables
  cross_platform.py          the PlatEMO / pymoo comparison
  reference_direction_angles.py

data/             released data
  L_NM_table.csv                the complete realised-count table, 13 895 rows
  affected_files.csv            copy of the audit listing
  trace_three_quantities.csv    the three quantities per algorithm
  xplatform.csv                 cross-library comparison
  angles.csv                    minimum inter-vector angle, default vs exactly-N
  results/                      raw per-run archives (.mat), one per configuration

paper/            the manuscript source
  main.tex, numbers*.tex, tables/, figs/
  SCIS2026.cls, scis.bst        the official SCIENCE CHINA Information Sciences class
  platemo/UniformPoint.m        the audited constructor, for reference
  platemo/PROBLEM.m             the problem superclass (a handle class)
```

## Reproducing the results

**Environment.** MATLAB R2026a with PlatEMO 4.16, and Python 3.13 with
`numpy`, `scipy`, `matplotlib` (and `pymoo` 0.6.2 for the cross-library check).
All optimisation runs are single-threaded and seeded; the reported statistics
are reproducible from the archives in `data/results/` without re-running
anything.

**Regenerate every table and figure from the archives:**

```bash
python experiments/make_paper_artifacts.py     # tables/, figs/, numbers.tex
python experiments/make_audit_artifacts.py     # audit tables and macros
python experiments/cross_platform.py           # the PlatEMO / pymoo table
```

**Rebuild the paper** (must be `pdflatex`; the class loads `breakurl`, which is
dvips-only, so `xelatex` aborts with spurious `\pdf@box` errors):

```bash
cd paper && pdflatex main.tex && pdflatex main.tex && pdflatex main.tex
```

**Re-run the optimisation experiments** (about two hours on 16 cores; three
configurations, run one per process):

```bash
WB13CI=1 matlab -batch "wb13" &
WB13CI=2 matlab -batch "wb13" &
WB13CI=3 matlab -batch "wb13"
```

**Re-run the audit:**

```bash
python audit/audit13_lex.py        # lexical pass over the algorithm tree
matlab -batch "audit13('dyn')"     # three-quantity trace
```

## The audit in one line

```
Problem\.N\]\s*=\s*UniformPoint\(\s*Problem\.N
```

matched only against source text whose comments and string literals have been
replaced by blanks, and only on a live statement.

## Provenance and scope

Every reported quantity is generated from a released archive by a script in
this repository; no number in the manuscript was entered by hand. The census is
a measurement of **PlatEMO 4.16** and not a survey of the field. The audit is
lexical, so it can in principle miss a call assembled dynamically; we treat it
as a lower bound and inspected the surviving hits by hand. The empirical
comparison between the declared and the realised configuration coincides by
construction with a difference in population size, so the study quantifies a
reporting error rather than an intrinsic property of fidelity. These limits are
stated in the manuscript.

## Licence

- **Code** (`audit/`, `experiments/`): MIT — see `LICENSE`.
- **Data and derived tables** (`data/`, `paper/tables/`, `paper/figs/`):
  CC BY 4.0 — see `LICENSE-DATA`.

PlatEMO itself is distributed under its own licence and is **not** included
here; only two files are reproduced for reference, with their origin noted.

## Citation

Repository: <https://github.com/qingdi-mirusi/population-size-fidelity>

See `CITATION.cff`. The repository accompanies the manuscript; the final
article identifier will be added here once the paper is published.
