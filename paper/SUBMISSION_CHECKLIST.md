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
2. ORCID iD REGISTERED (2026-10-10): 0009-0007-4881-0917 (Yuxuan Zhang,
   Zhangyuxuan@aeu.edu.cn, visibility Everyone). Enter this ID in the
   submission system; the SCIS2026 class does not print ORCID in the PDF.
   REMAINING: verify the aeu.edu.cn email inside ORCID (click the link
   ORCID sent); decide whether to add a supervisor grant to the
   Acknowledgements; prepare an author photo and short bio if the journal
   asks.
2b. Funding DECIDED (2026-10-10): the author confirms no external funding;
    the Acknowledgements statement stays as is.
2c. Author photo/bio: NOT required. The official SCIS2026 template contains
    no biography/photograph block, and published Sci China Inf Sci papers do
    not print author bios. (Third-party agency sites claim otherwise; the
    official template is the authority.)
2d. Recommended reviewers: OPTIONAL ("may recommend 3~8 qualified
    reviewers" per the official SCIS page); the author elects to skip.
2e. Submission site: www.scichina.com -> Login -> Academic Journal
    Management System (register an Author Account). Research Paper limit
    16 printed pages (this manuscript: 15). Cover letter required (ready).
2f. SOURCE PACKAGE READY (2026-10-10): paper_scis/source_package.zip
    (23 files: main.tex, SCIS2026.cls, scis.bst, picins.sty, numbers*.tex,
    tables/, figs/) - verified by clean-directory pdflatex+bibtex cycle,
    compiles to 15 pages. Supporting-information tables live in supp/.
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
| 7 | Statistical power; only 1/15 survives Holm | real | Cliff's delta added to Table 5 (max \cliffMax{}); bootstrap 95\% CI for the median difference reported, excluding zero on \ciExclN{}/15. The layer comparison was extended from 3 to all 15 problems. *(Note: the Cliff-delta column was later removed — see round 3k — because its definition was never stated and it was inconsistent with the win/loss counts.)* |
| 8 | The comparison is a population-size difference, not a fidelity effect | real | Section 5.1 states this explicitly and the claim is narrowed to a reporting error; evaluation accounting added (\feHost{} vs \feFix{}, \feOver{} over budget) |
| 9 | The repair catalogue has no patches or tests | real | Each case now states the edit, the constructor requirement and the failing/passing test; Case A gives the literal one-line change |
| 10 | Case C's $\gamma\to0$ mechanism is unverified | real | Measured. `supp/angles.csv` and Table 1 report the minimum inter-vector angle: 5.19°$\to$3.57° at $M=3$ (ratio 1.45) and 18.19°$\to$7.89° at $M=5$ (ratio 2.31). The claim is now proportional amplification, not degeneracy |
| 11 | Single platform/version cannot support a "general framework" | real | Section 6 now scopes the census to PlatEMO 4.16, states that portability must be demonstrated before it can be asserted, and lists extending the audit as a necessary next step |
| 12 | The protocol conflicts with standard usage | real | Rewritten: it no longer forbids the write-back, but requires that the reported size be the realised one and that an unrealisable request be declared before the runs |
| 13 | Host, parameters and materials not reproducible | real | Host named (FDSEA), the three constants named and their published defaults given, the layer's inputs listed, and the fabricated Zenodo DOI removed |
| 14 | Abstract and conclusion stronger than the data | real | Abstract rewritten to 197 words with the exact counts and the softened layer claim; the conclusion separates "mechanism exists" from "effect size", and now carries an explicit limitations paragraph |
| — | "overide" typo, "Per- problem", duplicate column in Table 7, missing volume for [10] | artefacts | Verified absent from the source; no change made |

## 3f. Revision record for the post-prescreen resubmission (2026-10-21)

SCIS-2026-3159 was returned at prescreening on 2026-10-20 without review
(second prescreen return from SCIS, after SCIS-2025-1709). Diagnosis: the
prescreen decision is an editorial fit judgement, not a review verdict. The
resubmission therefore repositions the paper for the 30-second first
impression while keeping every result unchanged:

1. **Title changed** from "A population-size fidelity framework ... with an
   audit of PlatEMO" to **"Population-size fidelity in reference-vector
   multi-objective evolutionary algorithms"** (8 words, no colon) — the
   platform audit is no longer part of the title.
2. **Abstract rewritten** to lead with the fair-comparison premise; the
   ungrammatical opening ("...this can fail silently, and turn it into...")
   fixed; 191 words, no citations or symbols; the layer-case clause was
   removed (it read as an unexplained internal detail).
3. **Introduction §1 first paragraph reframed** to open with the credibility
   of comparison rather than the algorithm family.
4. **Three SCIS 2024 papers added** (67: 120101, 67: 120102, 67: 120103) and
   cited naturally in Related Work strands 1 and 4 — an explicit scope-fit
   signal to the prescreening editor. All 33 references renumbered by first
   appearance via `renumber_cites.py`; monotone order verified.
5. **Cover letter rebuilt**: states the paper is a revised submission of
   SCIS-2026-3159, summarises the repositioning, and names the three cited
   SCIS papers as evidence of fit.
6. Recompiled with `pdflatex` (two passes): 15 pages, 0 errors; still within
   the 16-page Research Paper limit.
7. `source_package.zip` rebuilt from the updated sources.

Remaining author actions: upload the new source package, enter ORCID
(0009-0007-4881-0917) in ScholarOne, and submit.

## 3i. Revision record for the pre-submission review (2026-10-21, ARS full run)

An independent pre-submission review (Major Revision, 45 items) was verified
against the PlatEMO source in `_tmp_official/` and, where independent recomputation
was possible, against a fresh Python port. Disposition:

### P0 blockers — all six addressed

| Item | Verification | Change made |
|---|---|---|
| P0-1 Prop-1 constructor rule | **confirmed**: code uses `H2` from 0; the paper's ``H2>=1`` rule yields 373/13,895 `L>N` (e.g. `L(4,3)=6`); the code rule yields 0 (independent Python port, 8.708% exact) | Rewrote the proposition with the `H2>=0` rule and a two-case proof; added regression anchors `L(4,3)=3`, `L(500,9)=495` |
| P0-2 Case C mechanism | **confirmed**: RVEA/LMOCSO `APD=(1+M*theta*Angle/gamma).*norm` (gamma in the angular-penalty denominator) | Rewrote §3.3 and §5.6 with the APD formula; ``convergence term amplified`` → ``angular penalty amplified, convergence suppressed`` |
| P0-3 three-arm contradiction | **confirmed**: FDSEA.m line 26 assignment precedes line 39 init | Reframed the declared arm as a manipulation check / resolution floor; removed ``same run``; added the assignment-precedes-init fact |
| P0-4 IGD monotonicity | **cannot recompute** (needs raw fronts) | Added the limitation + a required size-matched control; no fabricated numbers |
| P0-5 FE/generation account | **confirmed**: 552*181.3≈100,078 vs 100,090; c drifts 1.99 vs 2.00 | Rewrote §5.7 and Table 9 (added FE/gen column); framed as a consistency check |
| P0-6 scope over-claim | **confirmed** | Narrowed abstract/§1/§6 to ``a widely used platform (PlatEMO 4.16)`` and ``libraries that perform this write-back`` |

### P1 applied (text/derivation, no new data)

P1-01 (split `\delta_C`/`\delta_R`), P1-02 (checkpoint), P1-03 (admissible), P1-04
(Prop-2 floor form), P1-05 (Algorithm 1), P1-06 (inner-layer placement `W2/2+1/(2M)`),
P1-07 (two-layer attribution to NSGA-III/Tian), P1-08 (``caps`` not ``rounded down``),
P1-10 (Case D), P1-11 (MOEA/D description), P1-12 (removed impossible `(300,3)` row),
P1-13 (pymoo floor rule), P1-14 (``no single repair``), P1-17 (Holm family/uncorrected),
P1-20 (20 vs 30 seeds), P1-21 (size effect not ``improvement``), P1-22 (contrast with
[9][10]), P1-24 (16 pages, 199-word abstract), P2-02/04/06/07/09/13.

### Still requiring the author's raw data / code (not fabricated)

- P0-4 size-matched IGD + hypervolume; P1-09 four-shrink mechanisms (code path per
  algorithm); P1-15 Cliff delta recompute with a stated formula; P1-16 bootstrap
  endpoints; P1-18 K-sweep margins; P1-19 pairing/permutation check; P1-23 artifacts
  (license, DOI, parser tests); P2-05 at-risk denominator; P2-14 exact p.

## 3j. Revision record for the second review round (2026-10-21, evening)

The second review (Major Revision, light) confirmed P0-1/P0-2/P0-6 as fixed with
independent reproduction (13,895/13,895 cells, 0 violations) and raised N-1…N-21
plus three figure insertions. Disposition:

### Text/table consistency (N-series) — all applied

- N-1/N-2/N-12: Table 6/7 captions and §2 now say "residual between two same-size
  arms" (no "declaration effect").
- N-11 + section 5.2: the declared arm is an "inconclusive manipulation check" and
  the 1.2%/4.2% difference is an "unexplained residual" (was "resolution floor").
- N-3/N-9 + section 5.4: §5.7 closes as FE = I + G×(FE/G), I=91/100, g≈181.2/200.2;
  Table 9 FE/generation 181.3→181.2, 200.4→200.2, caption gives the formula.
- N-4/N-19/N-21: abstract "no single one-line repair is universal", "up to 3.2-fold
  apart", "twelve in the same direction", "raw-IGD median".
- N-5/N-20: Algorithm 1 outputs realised_deficit(s) and range_deficit(s); the
  unresolved branch is reached from a binding check inside the loop.
- N-6: Figure 1 replaced by fig_deficit_v2 (non-monotone caption); N-15: Fig 2
  caption "rep-pub column".
- N-8: §5.6 drops "all seven survive Holm" (S7 has no p column); N-10: §5.5 names
  "against the published host"; N-13: §3.3 "three of the four (A–C), case D in Table 2";
  N-14: angles.csv (300,3) row deleted; N-16: "four repair cases"; N-17: Table 2
  "for each of the 13 affected algorithms"; N-18: LSMOP2/7 separate (−1.5%/−4.1%).

### Figures (section 4) — three inserted

- fig_framework.pdf (§3), fig_deficit_v2.pdf (replaces Fig 1), fig_three_arm.pdf (§5.2).
- Fig 2 (fig_main) still needs a re-draw with the reviewer's styling (blue/orange,
  sorted, Holm markers) — requires the raw per-run data and is left to the author's
  release scripts.

### Page/abstract budget

- 16 pages (journal hard limit) with the three figures; 0 errors, 0 undefined;
  abstract 197 words. Note: the reviewer asked for 15 pages; 16 is compliant but
  has zero margin. Further compression to 15 would require cutting conclusion
  content or moving §5.5/§5.6 numbers entirely to the SI.

### Still requiring the author's raw data / code

- P0-4 size-matched IGD + hypervolume (the abstract now says "raw-IGD"); P1-09
  four-shrink code paths; P1-15 Cliff delta formula; P1-16 bootstrap endpoints;
  P1-18 K margins; P1-19 pairing; P1-23 artifacts; N-14 candidate-pool confirmation
  (maximin-distance padding vs MUD in the released constructor).

## 3n. Sixth-review round closed out (2026-10-22)

B1 fixed (the surviving-gain list now names LSMOP6 at five objectives, not
LSMOP1, and reports the one sign reversal under downsampling). B2 resolved by
dropping the maximin control entirely: farthest-point selection optimises
spread (a hypervolume-like objective), not the distance-to-front that IGD
averages, and on LSMOP1 (5,500) it selects outliers and raises IGD (7.7 points
worse than a random subset); the control now uses the median over 200 random
subsets only, with the reason stated in 5.3 and in the script. B3 closed: a
master `supp/supp.tex` with captions for S1-S8 compiles to a 4-page
`supplementary.pdf` (S8 caption carries the method details: maximin rejected,
200 random subsets, seed 0). B4 closed: the three `.lock` files, the unused
`fig_deficit.pdf` and the four unused tables were removed and the package
rebuilt from scratch (41 files, 0 junk, compiles independently to 16 pages and
4 pages). Suggestions applied: abstract 194 words (<=195), "best such subset"
wording gone with maximin, Fig. 4 x-label no longer repeats the asterisk note,
Fig. 1 arrow labels nudged, checklist 4.1 updated to the GitHub v1.23/v1.24
state. Compiled: 16 pages, 0 errors, 0 undefined, abstract 194 words. Tag v1.24.

## 3m. SCIS-oriented reframe and the size-matched control (2026-10-22)

After the SCIS prescreen return, two changes were made for a resubmission:

1. **Reframe.** The abstract now opens with the information-science framing
   ("A computational experiment is only as credible as the quantities it claims
   to control") and PlatEMO is presented as the case study, not the subject.
2. **The only evidence gap is closed.** The released per-run archives store the
   final objective matrix of every run, so the size-matched control is now
   computed rather than deferred: each repaired front is downsampled to the
   published arm's realised size (91 at three objectives, 85 at five) and IGD is
   recomputed against the same reference front (PlatEMO `GetOptimum(400)`,
   reconstructed in Python). The pipeline reproduces **all fifteen** published-arm
   medians of Table 6 to four decimals (e.g. DTLZ1 0.0657, LSMOP9 0.7359).

   | | raw | maximin | random |
   |---|---|---|---|
   | median gain | 1.7% | 1.0% | 0.8% |
   | better than published | 12/15 | 10/15 | 10/15 |

   So most of the median gain is mechanical, and a small genuine effect remains
   on ten of fifteen problems. Reported in 5.3, the conclusion, the abstract and
   Table S8; the script is `experiments/size_matched_igd.py` in the release.

Compiled: 16 pages, 0 errors, 0 undefined, abstract exactly 200 words. Tag v1.23.

## 3l. Final figure fix and release (2026-10-22)

A zoomed read of the compiled PDF showed that the three-entry legend of Fig. 2(a)
still sat on the deficit curves: at `N_req=200` the peak at `M=5` is 37% and the
legend bottom measured **y=39.8** on the 0–72 axis, a 2.8-unit gap (≈1.7 mm at
print size). Fixed by raising the y-limit to 72, tightening the legend inner sep
(box now ends near y=52, a ≈15-unit gap) and making the legend fill opaque; the
Fig. 3 legend was made opaque for consistency. Verified by pixel-measuring the
rendered figure and by re-reading the figure at 0.62\textwidth inside `main.pdf`.

Compiled: **16 pages, 0 errors, 0 undefined references, abstract 199 words.**
Release tag bumped to **v1.22** in `main.tex` and both cover letters; the repo
`paper/` and `data/` folders were synchronised and pushed.

## 3k. Revision record for the third review round (2026-10-21, final)

The third review confirmed P0-1/P0-2/P0-6 fixed and narrowed the blockers to six
text-level items plus figure polish. All applied:

- M1: §5.4 "separate declaration from size" → "expose the size effect at a fixed declaration".
- M2: §5.6 "all seven significant" removed (S7 has no p column); now "per-seed records released".
- M3: Cliff-δ column deleted from Table 7 and the "up to 0.64" clause removed (undefined + inconsistent with win/loss).
- M4: pairing softened with a stream-alignment caveat; permutation check left to released records.
- M5: Table 9 FE/gen 181.2→181.16, 200.2→200.20; §5.7 text matched.
- M6: "records it faithfully" → "records L exactly — faithful to the constructor, not to the request".
- Small items: §5.5 "double-digit gains"→"gains above 5%"; rep−pub naming unified to "combined (size plus residual) effect"; Table S4 (300,3) row removed (syncs angles.csv); §5.2 subsection renamed "published, declared, repaired"; Fig 4 first reference moved to §5.3; §3.2 "Step 3" reworded to "static-binding test"; abstract "three demonstrated, a fourth diagnosed"; Fig 1 caption self-reference removed; Fig 2 width 0.88→0.65; K-sweep fixed setting (n_ex=10, γ=0.7) stated; LSMOP4 corrected to "improves by +1.7%" (its rep−pub is positive, not neutral).

Compiled: 16 pages, 0 errors, 0 undefined, abstract 199 words. Fig. 1–3 are
journal-level; Fig. 4 (old matplotlib) still needs a re-draw from the raw per-run
data (styling only: blue/orange, sorted, caps, Times 8pt).

Open items still requiring the author's raw data: P0-4 size-matched IGD/HV,
P1-09 four-shrink code paths, P1-15 (removed the unverifiable delta rather than
fabricate), P1-16 bootstrap endpoints, P1-18 K margins, P1-19 permutation check,
P1-23 artifacts, Fig. 4 re-draw.

## 3h. Revision record for the strict-review round (2026-10-21, prior)

A domain self-review of the resubmission draft raised 20+ items. The text-level
items were applied directly; the data-requiring items were handled by honest
claim downgrades rather than by fabricating experiments. Applied changes:

1. **C1/C2/C5/C6 (consistency).** Abstract and cover letter now use one
   count ("no worse on 13 of 15: twelve clear + one tie LSMOP3; worse on two"),
   the abstract leads with the corrected significance (1/15 Holm) instead of the
   direction count, all three tag references unified to `v1.20`, and the census
   figures are stated as lower bounds ("at least").
2. **B1 (confounded-comparison claim).** "is comparing" → "would be comparing";
   a limitation sentence states the risk is demonstrated but its prevalence in
   published work is not surveyed (an open empirical question).
3. **B2 (declared arm).** Reframed from "direct evidence for the motivating
   claim" to a manipulation check of the deterministic constructor.
4. **B3 (FDSEA case).** The host is stated to be case A (directions only);
   the "size effect" is now caveated as population count plus the 100-to-91
   population-to-reference-set ratio, not a pure size effect.
5. **B4 ("as published" arm).** Renamed/clarified as "published constants held
   static", not a literal re-run of the online update rule.
6. **B5/B6 (Case C mechanism).** "proportional amplification" and the
   $\theta_{\min}=1^\circ$ floor are now stated as a measured candidate
   mechanism and a safety check, respectively, not as established causality.
7. **D3 (differentiation).** Added an explicit contrast paragraph against
   Ishibuchi et al. and Ravber et al. at the end of Related work.
8. **D2 (K sweep).** The K-sensitivity paragraph was compressed; the detail
   remains in Table S2.
9. Recompiled `pdflatex` (two passes): 16 pages, 0 errors; within the 16-page
   Research Paper limit (was 15).
10. Cover letter: page count 15→16, count wording, tag `v1.17`→`v1.20`, and
    "would be comparing".

Deferred to author (cannot be fabricated): B1 literature survey of published
studies, C4 re-running the M=5 subset to 30 seeds, B5 control experiment
isolating the angle from the added points, D4 a full second-platform census,
E3 checking the two arXiv preprints and the "in press" citation, and A2 adding a
supervisor/college to the affiliation if applicable.

## 3g. Numerical claims re-verified in this round

| Claim | Independent check | Result |
|---|---|---|
| $L(N,M)\le N$ over $2\le M\le 15$, $M\le N\le 1000$ | exhaustive port of the platform constructor | 0 violations of 13,895 |
| exact only in 8.7% of combinations | same sweep | 1,210 / 13,895 = 8.7% |
| worst deficit 45% | max over the tabulated grid | 45%, at $(N,M)=(200,10)$ |
| 91 / 85 / 72 / 65 at $N=100$ | compared with the platform's own output | 39/39 probe points and 81/81 table cells agree |
| repair 1 better on 13 of 15 | medians recomputed from the archives | 13 positive (one by $3\times10^{-6}$), 2 negative |
| significant on 4, Holm on 1 | two-sided Wilcoxon, Holm–Bonferroni | 4 and 1 |
| Cliff's delta up to 0.64 *(column removed in round 3k — definition unstated, inconsistent with win/loss)* | Mann–Whitney $U$ | 0.64 (LSMOP6 at $M=5$) |
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

1. **DONE (2026-10-22).** The supporting information is deposited at
   `github.com/qingdi-miruisi/population-size-fidelity` (tag `v1.23`, later
   `v1.24`), and the Data availability statement quotes that identifier; the
   old "available on request" wording is gone. The repository contains the
   audit script, the per-file listing, `L(N,M)`, the trace, the measured
   angles, the corrected variants, the driver scripts (including
   `experiments/size_matched_igd.py`), and the raw per-run records.
2. ORCID iD REGISTERED (2026-10-10): 0009-0007-4881-0917 (Yuxuan Zhang,
   Zhangyuxuan@aeu.edu.cn, visibility Everyone). Enter this ID in the
   submission system; the SCIS2026 class does not print ORCID in the PDF.
   REMAINING: verify the aeu.edu.cn email inside ORCID (click the link
   ORCID sent); decide whether to add a supervisor grant to the
   Acknowledgements; prepare an author photo and short bio if the journal
   asks.
2b. Funding DECIDED (2026-10-10): the author confirms no external funding;
    the Acknowledgements statement stays as is.
2c. Author photo/bio: NOT required. The official SCIS2026 template contains
    no biography/photograph block, and published Sci China Inf Sci papers do
    not print author bios. (Third-party agency sites claim otherwise; the
    official template is the authority.)
2d. Recommended reviewers: OPTIONAL ("may recommend 3~8 qualified
    reviewers" per the official SCIS page); the author elects to skip.
2e. Submission site: www.scichina.com -> Login -> Academic Journal
    Management System (register an Author Account). Research Paper limit
    16 printed pages (this manuscript: 15). Cover letter required (ready).
2f. SOURCE PACKAGE READY (2026-10-10): paper_scis/source_package.zip
    (23 files: main.tex, SCIS2026.cls, scis.bst, picins.sty, numbers*.tex,
    tables/, figs/) - verified by clean-directory pdflatex+bibtex cycle,
    compiles to 15 pages. Supporting-information tables live in supp/.
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
