# Cover letter — SCIENCE CHINA Information Sciences

**To:** The Editor-in-Chief, *SCIENCE CHINA Information Sciences*
**From:** Yuxuan Zhang (corresponding author)
Graduate School, Army Engineering University of PLA, Nanjing 210007, China
E-mail: 3150644070@qq.com

**Date:** 7 October 2026

**Article type:** RESEARCH PAPER

**Manuscript title:** A population-size fidelity framework for reference-vector
multi-objective evolutionary algorithms with an audit of PlatEMO

---

Dear Editor,

I am pleased to submit the manuscript above as a RESEARCH PAPER to
*SCIENCE CHINA Information Sciences*. The manuscript is prepared with the
official `SCIS2026` LaTeX class and complies with the journal's preparation
requirements; all materials needed to reproduce every table and figure are
released, and the paper is 13 pages.

## What the paper reports

The credibility of a comparison between evolutionary multi-objective algorithms
rests on a quantity that is reported everywhere and checked almost nowhere: the
population size actually used. The paper shows that this quantity can fail
silently, and it converts the observation into a reusable instrument rather
than a single platform report. The instrument — a *population-size fidelity*
framework — separates three quantities that studies conflate (the size
requested, the size evaluated, and the size recorded) and has four parts:

1. a fidelity principle, formalised as a definition together with two
   propositions: the drift introduced by a lattice constructor is one-signed,
   and under a fixed evaluation budget it inflates the number of generations
   completed. Both statements are verified over 13,895 combinations and against
   the platform's own constructor;
2. an auditing procedure, given as an algorithm, that locates the offending
   constructor calls in any code base that returns a reference set together
   with its size;
3. a catalogue of corrections, which shows that the repair is
   algorithm-dependent through three cases realised by real algorithms —
   NSGA-III accepts a one-line repair, MOEA/D requires an exactly-*N*
   constructor, and RVEA and LMOCSO need a bounded-angle constructor. The
   mechanism of this last case is measured rather than asserted: the
   exactly-*N* constructor reduces the smallest inter-vector angle by a factor
   of 1.45 at three objectives and 2.31 at five;
4. a reporting protocol given as a seven-column table schema with three
   decision rules, so that a study can adopt it directly.

The consequence is measured rather than argued. A dynamic trace of sixteen
reference-vector algorithms shows that configuring 100 yields a realised
population of 91 for the affected algorithms, of 83, 80, 66 and 31 for RVEA,
DGEA, LMOCSO and RVEAa, and of exactly 100 for NSGA-II, SPEA2 and IBEA, which
carry no such assignment. A table that reports *N* = 100 for NSGA-III and for
NSGA-II is therefore comparing 91 individuals with 100. We also ran a control
arm configured at the size it realises: on all fifteen problems of the suite
the declared and published configurations are statistically
indistinguishable, which is the direct demonstration that the published run
*is* a run at the smaller size.

Applied to PlatEMO 4.16, the framework finds the assignment in 84 of 1,887
algorithm source files, belonging to 83 of the 360 algorithms in the release.
The default constructor returns the largest admissible lattice size not
exceeding the request and never adds individuals, so the realised population is
a downward rounding of the requested one, exact in only 8.7% of combinations;
100 is realised as 91 at three objectives and as 65 at ten, a shortfall of up to
45% at unfavourable combinations. On a fifteen-problem large-scale suite,
restoring the requested size improves the host's median indicator on 13
problems and leaves 2 worse, with a bootstrap confidence interval for the median
difference excluding zero on 8 and Cliff's delta reaching 0.64. The paper is
explicit that this comparison measures the difference between the declared and
the realised condition — which by construction coincides with a difference in
population size — and not an intrinsic property of fidelity. The audit is
portable, and we demonstrate it rather than assert it: on pymoo the trigger is
absent, which is a genuine negative result, while the underlying arithmetic
still differs, so that at eight objectives the same nominal *N* = 100 realises
72 directions in PlatEMO and 36 in pymoo.

## Why it fits *SCIENCE CHINA Information Sciences*

The journal publishes work across computer science and technology, and
systematic methodological work on the reliability of computational experiments
falls squarely within that remit. The paper is not a software defect report: it
addresses a general reporting failure of a widely used class of algorithms,
supplies a checkable procedure with a proven core, and quantifies the
consequences with a paired statistical design and effect sizes on a standard
large-scale benchmark suite. Its results are actionable for the journal's
readership, since the audit can be run unchanged on any library with the same
constructor pattern.

The manuscript cites current work on the subject, including the analysis of
implementation differences across thirteen metaheuristic frameworks, formal
treatment of population-size specification for fair comparison, and recent
surveys of large-scale and expensive multi-objective optimisation; more than
half of the 29 references are from the last three years.

## What the paper does not claim

The paper does not claim that fidelity has an effect separable from the
population size, and it does not claim that the rounding performed by a simplex
lattice is a defect — that rounding is unavoidable and the write-back is often
deliberate. It claims only that publishing a size the run did not use changes
the conclusion a study draws. The audit covers one platform at one version and
does not survey the field, a limitation stated in the paper. The adaptive layer
used as a case study is not proposed as a contribution; on the contrary, the
paper reports that the evidence previously supporting it was largely the
population-size artefact, which is the honest conclusion that motivated the
work.

## Declarations

- The manuscript has not been published previously and is not under
  consideration elsewhere; it is not a duplicate submission.
- The author declares no competing financial interests.
- No external funding supported this work.
- Data and code availability: all materials are publicly available at
  **https://github.com/qingdi-miruisi/population-size-fidelity** (tag
  `v1.0-scissubmission`). The release contains the audit script, the per-file
  audit listing with line numbers, the complete realised-count table $L(N,M)$
  over 13,895 combinations, the three-quantity trace of sixteen algorithms, the
  cross-library comparison, the measured inter-vector angles, the corrected
  variants for the three repair cases, the driver scripts that regenerate every
  table and figure, and the raw per-run archives.
- There is a single author, who approves the submission.

Thank you for considering this submission.

Sincerely,

**Yuxuan Zhang** (corresponding author)
Graduate School, Army Engineering University of PLA
Nanjing 210007, China
E-mail: 3150644070@qq.com
