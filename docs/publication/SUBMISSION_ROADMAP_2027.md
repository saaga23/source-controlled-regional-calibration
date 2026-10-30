# Submission Roadmap 2027

**Date:** 2026-10-30 · **Companion:** `VENUE_ANALYSIS_2027.md` (verified deadlines with official links)

## Target: ACL 2027 via ARR — ARR deadline 2027-01-04 (AoE)

Countdown from 2026-10-30: **≈ 9 weeks**.

### Week-by-week plan

| Window | Work item |
|---|---|
| Oct 30 – Nov 8, 2026 | Freeze the public repository (this release). Manuscript pass 1: tighten abstract around the validity-requirement contribution; verify every number against `docs/results/RESULTS.md`; confirm all citations per `REFERENCE_VERIFICATION.md` (resolve the PENDING entries). |
| Nov 9 – Nov 22, 2026 | Manuscript pass 2: limitations section expanded per `docs/results/KNOWN_LIMITATIONS.md`; add explicit equivalence-testing discussion; ensure Analysis Plan chronology (pre-specified H3, two-sided reporting) is unambiguous. Internal review: documentation audit checklist (README 12-question test in `docs/FINAL_REPOSITORY_AUDIT.md`). |
| Nov 23 – Dec 13, 2026 | Optional (recommended, owner decision — costs API budget): one strengthening experiment that does not change the study, e.g., AUPRC computation (no cost) and a prompt-template sensitivity run on a subset (small API cost; requires owner authorization). |
| Dec 14 – Dec 27, 2026 | ARR formatting pass: anonymize (check CITATION/repo links for deanonymization), reproducibility checklist, limit compliance (8 pages main text), AI-assistance statement per the January 2027 ARR policy (verify policy text). |
| Dec 28, 2026 – Jan 3, 2027 | Full internal verification rerun: `pytest tests/`, verification scripts, hash checks. Buffer for OpenReview/ARR submission mechanics. |
| **Jan 4, 2027** | **ARR submission deadline (11:59pm UTC−12).** |

### Pre-submission checklist

- [ ] All `PENDING` reference verifications resolved (`docs/literature/REFERENCE_VERIFICATION.md`)
- [ ] Manuscript numbers = repository numbers (single source of truth: raw CSV)
- [ ] Anonymity audit: no author names, no deanonymizing repo links in the PDF (link the anonymous repo mirror if ARR requires)
- [ ] AI-assistance disclosure matches the then-current ARR policy
- [ ] Reproducibility checklist completed
- [ ] No claim of submission status anywhere in public materials until verified

## Alternatives

- **FAccT 2027:** only if an abstract was registered by 2026-10-27 (deadline now passed); needs ACM TAPS conversion + sociotechnical framing; final notification 2027-03-23.
- **EMNLP 2027 / NeurIPS 2027 D&B:** CFPs TBA at analysis date; if the ARR cycle is missed, use the extra months for the matched-source experiment (future work #1) and target these with a stronger paper.

## Budget honesty

- Repository publication and analysis reproduction: **$0** (all local analysis runs from released outputs).
- Optional prompt-sensitivity run: small API cost — requires explicit owner authorization before spending (not authorized by this repository's creation).
- Fresh full inference: ≈ $0.66 at run-time prices (documented in `EXPERIMENT_PROTOCOL.md`).
