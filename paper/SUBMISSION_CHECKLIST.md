# SCI CHINA Information Sciences — submission checklist and revision record

**Manuscript:** A population-size fidelity framework for reference-vector
multi-objective evolutionary algorithms with an audit of PlatEMO

**Article type:** RESEARCH PAPER

**Corresponding author:** Yuxuan Zhang, Graduate School, Army Engineering
University of PLA, Nanjing 210007, China — 3150644070@qq.com

---

## 1. Journal compliance (verified against the official SCIS requirements)

| Requirement | Source | Status |
|---|---|---|
| Official LaTeX class `SCIS2026.cls` used | scis-template.zip | yes |
| **Compiled with `pdflatex`, not `xelatex`** | class uses `breakurl` (dvips-only) | yes — xelatex produces 79 spurious errors |
| Article type RESEARCH PAPER | info for authors | yes |
| Length ≤ 16 printed pages | info for authors | 13 pages |
| Title ≤ 20 words, no colon | manuscript format | 14 words, no colon |
| Family names in upper case | manuscript format | "Yuxuan ZHANG" |
| Affiliation with post code | manuscript format | "Nanjing 210007, China" |
| Abstract 100–200 words, no citations, no symbols | manuscript format | 197 words, none |
| Keywords 5–8 | manuscript format | 7 |
| Introduction without subtitles | manuscript format | no subtitles |
| Introduction does not describe the article structure | manuscript format | removed |
| Figures ≥ 600 dpi, Times New Roman 8 pt, 5 px lines | manuscript format | vector PDFs (resolution-independent) |
| Equations numbered in order | manuscript format | yes |
| **Tables centred within the text column** | class sample uses full-width `tabular*` | yes — `\centering` on all 9 tables |
| References numbered in square brackets, **cited in order of first appearance** | reference format | yes — renumbered; order verified monotone |
| References: family name + given-name initials, > 3 authors use "et al." | reference format | yes |
| References: sentence-case titles, ISO journal abbreviations | reference format | yes |
| Recent references cited (within 3 years) | reference format | 15 of 29 (52%) |
| No orphan or dangling references | — | 0 and 0 |
| **Conflict of interest statement before the reference list** | info for authors (mandatory) | yes — added |
| **Author contributions statement** | info for authors | yes — added |
| **Data availability statement** | research data policy | yes — added |

## 2. Reproducibility

- `pdflatex` (three passes): 0 errors, 0 undefined references, 0 undefined
  citations, 0 overfull boxes.
- Every number in the text is produced by `numbers.tex`, generated from the
  raw per-run archives by a single script, so text and tables cannot drift
  apart.
- All experiments are single-threaded and reproducible from the seed.

## 2a. Numerical audit performed at this revision

The following were re-derived from first principles and cross-checked against
the released PlatEMO source and the raw per-run archives:

| Quantity | Claim | Independent check | Result |
|---|---|---|---|
| `NBI(N,M)` cardinality | 91/85/72/65 at M=3/5/8/10, N=100 | faithful translation of `UniformPoint.m` `NBI` branch | 39/39 points match the MATLAB output; 81/81 cells of Table 2 match |
| never exceeds the request | Proposition 1 | exhaustive scan `2<=M<=15`, `M<=N<=1000` | 0 violations |
| exact only rarely | 8.7% | same scan (13,895 combinations, 1,210 exact) | 8.7% |
| worst deficit | 45% | max over N in the table, M=2..10 | 45% at (N=200, M=10) |
| repair 1 better | 13 of 15 | recomputed from `wbA_*.mat` medians | 13 positive, 2 negative, 0 tie |
| significant (uncorrected) | 4 of 15 | two-sided Wilcoxon signed-rank on the paired seeds | 4 (DTLZ1, LSMOP8, LSMOP1(5,500), LSMOP6(5,500)) |
| significant (Holm) | 1 | Holm–Bonferroni over 15 comparisons | 1 (LSMOP1(5,500), an M=5 instance) |

The `fixBetterN = 13` count is genuine: LSMOP3 has a median gain of
`+2.8e-7`, a real (if negligible) positive, so it counts as not-worse while
LSMOP2 and LSMOP7 are the only two negative cases.

## 3. Revision record for this retarget (Applied Soft Computing → SCIS)

The manuscript was repositioned from a platform audit into a methodological
framework, as follows.

1. **Title and framing.** The paper is now built around a named instrument,
   *population-size fidelity*, with PlatEMO 4.16 as a case study rather than
   the subject.
2. **New framework section (Section 3).** Adds a definition, **Proposition 1**
   (the drift of a lattice constructor is one-signed and can only remove
   individuals) with proof, **Proposition 2** (under a fixed budget the drift
   inflates the number of generations by $(N-L)/L$) with proof, **Algorithm 1**
   (the audit), the three-case repair catalogue, and the reporting protocol.
3. **Related work** cites the closest antecedent: the study of thirteen
   metaheuristic frameworks whose implementation differences change comparison
   outcomes, together with formal work on population-size specification for
   fair comparison and work on reproducibility in evolutionary computation.
4. **Format.** Rebuilt on `SCIS2026.cls`; abstract trimmed to 192 words;
   Introduction freed of subtitles and of any description of the article
   structure; conference references reformatted to the SCIS style.
5. **Terminology unified** as "repair 1 / repair 2" in text and tables; all
   cross-references converted from hard-coded numbers to `\ref` labels after an
   error was found in one of them.

## 3a. Revision record for the pre-submission self-review

1. **Table alignment fixed.** The official sample presents tables as
   full-width `tabular*`, which are centred by construction; this manuscript
   used plain `tabular`, which left-aligns. `\centering` was added to all
   eight `table` environments, matching the visual convention of the template.
2. **Compilation engine corrected.** The class loads `breakurl`, a dvips-only
   package. Under `xelatex` this produces 79 `\pdf@box` errors; under
   `pdflatex` the same source compiles with 0. The build instructions now
   specify `pdflatex`.
3. **Mandatory declarations added.** A Conflict of interest statement and an
   Author contributions statement were added immediately before the reference
   list, as the Information for Authors requires; the repository URL in the
   Data availability statement was filled in.
4. **Appendix removed.** The former Appendix A reported a negative result on
   a regime-detector for the scheduling layer, which is explicitly a case
   study rather than a contribution. It was removed to keep the paper focused
   and to bring the length to 10 pages.
5. **Citation line and author mark filled** (`\AuthorCitation`,
   `\AuthorMark`) so the running head and the self-citation line are complete.
6. **Reference details verified** against publisher records for the
   Informatica, Expert Systems, Swarm and Evolutionary Computation and
   Journal of Membrane Computing entries, and the arXiv entries reformatted
   to the SCIS convention.
7. **Proposition 1 proof tightened** to follow the released `UniformPoint.m`
   `NBI` branch exactly, including the `H1 < M` gate on the second layer and
   the precise equality condition.

## 4. Items the author must complete before uploading

1. **Nothing to fill in for the data statement.** The repository is live at
   `github.com/qingdi-miruisi/population-size-fidelity` (tag `v1.1-final`) and
   the Data availability statement already quotes it. A DOI was considered and
   deliberately **not** pursued: Zenodo is unreachable from the author's
   network, and a GitHub URL pinned to a tag is accepted practice. If a DOI is
   wanted later, `deposit/` holds a ready upload package and the dataset
   description for ScienceDB or OSF.
2. Confirm the ORCID iD, to be entered in the submission system.
3. Record the exact PlatEMO 4.16 archive hash (the release note is dated
   July 2026, 360 algorithms, 630 problems) in the repository README.
4. **Build with `pdflatex`** (three passes). Do not use `xelatex`: the class
   loads `breakurl`, which is dvips-only, and xelatex will abort with
   `\pdf@box` errors that are not present in the source.
5. Keep `picins.sty`: the official class requires it, it is not part of a
   minimal TeX Live installation, and a no-op stub is sufficient because the
   manuscript never uses `\parpic`. The stub is for local compilation only and
   is not part of the submission.

## 3b. Revision record for the reviewer-response round (round 12)

A domain review of the submitted draft raised fourteen items. Each was triaged
against the source, the platform code and the raw archives; the disposition is
recorded below together with the change made. Items that were PDF-extraction
artefacts are listed as such.

| # | Reviewer point | Verdict | Action |
|---|---|---|---|
| 1 | The paper never shows that the platform reports $N_{\rm req}$ rather than the updated field | real | Added a paragraph in Section 1 and a definition over three quantities, with the observability argument. The generation ratio \genFix{}/\genHost{} is now given as direct evidence |
| 2 | A Das–Dennis round-down is being mislabelled as silent infidelity | real (framing) | Section 4.1 now states that the rounding is a mathematical property of the lattice and cites Das and Dennis; the audited object is the write-back, not the rounding |
| 3 | Proposition 1 ignores duplicates, boundaries and constructor branches | partly real | Boundary cases and the $H_1<M$ gate are explicit; the (incorrect) duplicate-exclusion argument was replaced by the correct observation that a coincidence can only reinforce the inequality. Verified over 13,895 combinations with 0 violations |
| 4 | Proposition 2's premise conflicts with the write-back | real (framing) | The premise is now stated over reporting: $N_{\rm req}=N$ stated, $N_{\rm real}=L$ realised |
| 5 | 84/1887 is a file count, and matches may sit in comments | real | The census now reports both levels: 84 files, 83 of 363 algorithms, 0 matches on commented lines. `supp/affected_files.csv` lists every file with algorithm, line and code |
| 6 | Table 1 damaged; Table 3 headers cryptic; "13 better" contradicts a printed $+0.0\%$ | mixed | Table 1 is intact (extraction artefact). Table 3 headers renamed to `published`/`repair 1`/`repair 2`/$\Delta_1$/$\Delta_2$, with a caption note that $+0.0\%$ is below display precision. Text now gives 13 better / 2 worse and names the marginal case (LSMOP3, $3\times10^{-6}$) |
| 7 | Statistical power; only 1/15 survives Holm | real | Cliff's delta added to Table 5 (max \cliffMax{}); bootstrap 95\% CI for the median difference reported, excluding zero on \ciExclN{}/15. The layer comparison was extended from 3 to all 15 problems |
| 8 | The comparison is a population-size difference, not a fidelity effect | real | Section 5.1 states this explicitly and the claim is narrowed to a reporting error; evaluation accounting added (\feHost{} vs \feFix{}, \feOver{} over budget) |
| 9 | The repair catalogue has no patches or tests | real | Each case now states the edit, the constructor requirement and the failing/passing test; Case A gives the literal one-line change |
| 10 | Case C's $\gamma\to0$ mechanism is unverified | real | Measured. `supp/angles.csv` and Table 1 report the minimum inter-vector angle: 5.19°$\to$3.57° at $M=3$ (ratio 1.45) and 18.19°$\to$7.89° at $M=5$ (ratio 2.31). The claim is now proportional amplification, not degeneracy |
| 11 | Single platform/version cannot support a "general framework" | real | Section 6 now scopes the census to PlatEMO 4.16, states that portability must be demonstrated before it can be asserted, and lists extending the audit as a necessary next step |
| 12 | The protocol conflicts with standard usage | real | Rewritten: it no longer forbids the write-back, but requires that the reported size be the realised one and that an unrealisable request be declared before the runs |
| 13 | Host, parameters and materials not reproducible | real | Host named (FDSEA), the three constants named and their published defaults given, the layer's inputs listed, and the fabricated Zenodo DOI removed |
| 14 | Abstract and conclusion stronger than the data | real | Abstract rewritten to 197 words with the exact counts and the softened layer claim; the conclusion separates "mechanism exists" from "effect size", and now carries an explicit limitations paragraph |
| — | "overide" typo, "Per- problem", duplicate column in Table 7, missing volume for [10] | artefacts | Verified absent from the source; no change made |

## 3c. Numerical claims re-verified in this round

| Claim | Independent check | Result |
|---|---|---|
| $L(N,M)\le N$ over $2\le M\le 15$, $M\le N\le 1000$ | exhaustive port of the platform constructor | 0 violations of 13,895 |
| exact only in 8.7% of combinations | same sweep | 1,210 / 13,895 = 8.7% |
| worst deficit 45% | max over the tabulated grid | 45%, at $(N,M)=(200,10)$ |
| 91 / 85 / 72 / 65 at $N=100$ | compared with the platform's own output | 39/39 probe points and 81/81 table cells agree |
| repair 1 better on 13 of 15 | medians recomputed from the archives | 13 positive (one by $3\times10^{-6}$), 2 negative |
| significant on 4, Holm on 1 | two-sided Wilcoxon, Holm–Bonferroni | 4 and 1 |
| Cliff's delta up to 0.64 | Mann–Whitney $U$ | 0.64 (LSMOP6 at $M=5$) |
| CI excluding zero on 8 of 15 | bootstrap, 1,500 resamples | 8 |
| generations 552 vs 499 | `results/wbgen3/wbG.mat` | 552 and 499, all runs identical |
| layer better on 10/15 and 8/15 | recomputed | 10 vs published, 8 vs requested size |
| layer beats the best static setting on 2/15 | recomputed per problem | 2 |
| minimum angle 5.19°→3.57°, 18.19°→7.89° | independent Python port of both constructors | reproduced |

## 3d. Supplementary files prepared (in `supp/`)

- `L_NM_table.csv` — the complete realised-count table, 13,895 rows.
- `affected_files.csv` — the 84 affected files with algorithm, path, line and code.
- `angles.csv` — the measured inter-vector angles of the two constructors.

## 4. Items the author must complete before uploading

1. **Deposit the supporting information** (audit script, `supp/*.csv`, corrected
   variants, driver scripts, raw per-run records) in a public repository and
   quote the resulting identifier in the Data availability statement. The
   statement currently says the materials are available on request, which is
   acceptable at submission but weaker than an archive.
2. Confirm the ORCID iD, to be entered in the submission system.
3. Record the exact PlatEMO 4.16 archive hash in the repository README (the
   release note is dated July 2026, 360 algorithms, 630 problems).
4. **Build with `pdflatex`** (three passes). Do not use `xelatex`: the class
   loads `breakurl`, which is dvips-only, and xelatex will abort with
   `\pdf@box` errors that are not present in the source.
5. Keep `picins.sty`: the official class requires it and it is not part of a
   minimal TeX Live installation; a no-op stub suffices because the manuscript
   never uses `\parpic`. It is for local compilation only.

## 3e. Revision record for the second reviewer-response round (round 13)

The review raised twenty items. Two of them turned out to be **correct, and they
forced a change to the paper's central claim**, which we verified with MATLAB
before rewriting anything.

### The claim that had to change

The previous version said the platform "reports the requested size while the run
realises a smaller one". Direct measurement shows this is wrong: `PROBLEM` is a
handle class, so the write-back mutates the caller's object, and after a run
`Problem.N` is 91 and the platform's own record is 91.

```
NSGAIII configured N=100 -> Problem.N after Solve = 91, population in result = 91
FDSEA   configured N=100 -> 91 / 91      MOEAD  -> 91 / 91
RVEA    configured N=100 -> 91 / 83      LMOCSO -> 91 / 66
RVEAa   configured N=100 -> 91 / 31      DGEA   -> 91 / 80
NSGAII, SPEA2, IBEA (unaffected controls) -> 100 / 100
```

The corrected claim is stronger and is now the paper's thesis: the platform is
faithful, the *declaration* is not, and the consequence is a **confounded
comparison** — a table that reports `N = 100` for NSGA-III and NSGA-II is
comparing 91 individuals with 100.

### Disposition of the twenty items

| # | Point | Verdict | Action |
|---|---|---|---|
| 1 | Never shown that the platform records `N_req` rather than the updated field | **real, and it overturned our framing** | Three-quantity trace added (Table 6, 16 algorithms). Abstract, Section 1, Section 3.1 and 4.1 rewritten. The paper now states that the platform is faithful |
| 2 | Time-ordering hole: the write-back may not change the realised count | **not reproduced** | Lexical audit orders the assignment against `Initialization`: 62 before, 6 after (FDV, GLMO, WASF-GA, GWASF-GA, LCSA, POCEA), 16 with no call in the file. Reported as such |
| 3 | Tables 1–2 damaged and mutually inconsistent | **extraction artefact** | Rendered page 6: Table 2 is intact (9×9, bold diagonal). The 45% vs 75% wording is now explicit: *in the table* 45%, *over the whole scanned range* 75% |
| 4 | "13 improved" contradicts a printed `+0.0%` | real | Stated as 13 better / 2 worse with the marginal case (LSMOP3, 3e-6) named, plus a caption note |
| 5 | 84/1887 files vs 83/363 algorithms vs "ships 360 algorithms" | real | Counting reconciled at depth 2: **360 algorithm directories** (matching PlatEMO's own figure), 83 affected, 1887 files. Both levels reported |
| 6 | Sections 3.3/3.4 missing although the abstract claims four parts | real | Both restored: 3.3 is the catalogue with edit/test per case, 3.4 is the protocol |
| 7 | Case C cites the wrong table for the angle data | real | Dedicated Table 1 added; the section cites it |
| 8 | No control separating the reporting error from the population-size effect | real | Third arm run (`hostA`, declared == realised). Published vs declared is statistically indistinguishable; the realised-size effect is measured separately |
| 9 | Bootstrap CIs not multiplicity-corrected | real | CIs labelled exploratory; the abstract leads with the Holm-corrected count |
| 10 | Data availability not reproducible | real | Repository created and pushed; the statement now carries the URL and an itemised list |
| 11 | Portability asserted, not demonstrated | **real, now closed with data** | pymoo 0.6.2 audited: the trigger is **absent** (negative result), but the arithmetic differs — at M=8 the same `N=100` gives 72 vs 36. Table 7 added |
| 12 | Spelling and title errors | artefact | "ive static setings" and "overide" do not exist in the source |
| 13 | Protocol must give column names and rules | real | Replaced by a seven-column schema with three decision rules |
| 14 | Static matching is not robust | real | MATLAB-aware lexical pass (line/block comments, string literals, transpose ambiguity); stated as lexical and a lower bound; 84 hits hand-checked |
| 15 | `L` defined as rows or distinct directions? | real | The proof no longer relies on exclusion of coincidences; a coincidence can only reinforce the inequality |
| 16 | K fixed while the layer varies it | real | K in {3,5,10} swept; K is load-bearing (median spread reported) |
| 17 | No benchmark for the repairs | partly addressed | Repair outcomes demonstrated as failure modes; an IGD benchmark of the three repairs remains future work and is listed as a limitation |
| 18 | "excludes zero on eight" alongside "Holm 1" misleads | real | Abstract and 5.2 now distinguish the corrected test from the exploratory CI |
| 19 | Justification of the scan range | real | Range is stated as the scanned range; the complete table is released |
| 20 | Protocol conflicts with standard usage | real | The protocol no longer forbids the write-back; it requires the reported size to be the realised one |

### Repository

`https://github.com/qingdi-miruisi/population-size-fidelity` — 71 files, 19 MB,
tag `v1.1-final`. Contains the audit, the experiment harnesses, every
generator script, all derived CSV tables and the **raw per-run archives**.
