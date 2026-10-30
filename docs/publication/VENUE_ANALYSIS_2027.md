# Venue Analysis 2027

**Research date of this analysis:** 2026-10-30. All deadline data below was taken from **official conference websites** on that date. Venues whose 2027 calls were not yet announced at analysis time are marked **TBA** — they are candidates to re-check, not recommendations. This analysis does not assume any submission has or has not been made; submission status is tracked (if at all) in the private project records, not in this public repository.

## Verified venues (official CFP pages checked 2026-10-30)

### ACM FAccT 2027 — Fairness, Accountability, Transparency
- **Official site:** https://facctconference.org/2027/cfp.html (page updated 2026-10-29)
- **Scope fit:** strong — "Evaluations and evaluation practices" focus area explicitly includes audits of models/benchmarks, evaluation metrics and measurement practices; "Algorithmic fairness and bias" and "Sociotechnical evaluations of data, models, and systems" topics.
- **Key dates (AoE):** abstract **2026-10-27 (passed)**; full paper **2026-11-03**; first-round decisions 2026-12-22; revisions due 2027-01-28; final notification 2027-03-23; conference **2027-06-21/24** (location per site: Porto, Portugal — listed on the conference home page as the venue city).
- **Format:** ≤14 pages excluding references (+1 endmatter page for ethics/adverse-impact statements); ACM TAPS workflow (LaTeX `acmart`); OpenReview.
- **Anonymity:** mandatory (double-blind); violations desk-rejected.
- **Dual submission:** not allowed while under review elsewhere.
- **Reproducibility/dataset expectations:** no dedicated track, but evaluation-audit papers routinely release code/data; this repository satisfies that norm.
- **Feasibility note:** the abstract deadline passed 2026-10-27. Submission is only possible if an abstract was already registered before that deadline; otherwise this venue is **not available** for this work. FAccT also *requires all authors to sign up to review* — non-compliance can cause (desk) rejection.

### ACL 2027 — 65th Annual Meeting of the ACL
- **Official site:** https://2027.aclweb.org/ (CFP published 2026-09-29)
- **Scope fit:** strong — LLM evaluation, calibration/uncertainty, African NLP and benchmark construction are core *ACL themes; the manuscript is already in ACL two-column format (`acl.sty`, ARR style).
- **Key dates:** **ARR submission deadline 2027-01-04** (11:59pm UTC−12); commitment, notification, camera-ready **TBA**; conference **2027-08-17/22, Kyoto, Japan** (main conference Aug 20–22).
- **Format:** ACL Rolling Review (ARR) — submit to ARR by Jan 4, 2027, then commit to ACL 2027. Standard ARR length (8 pages main + unlimited references; long paper). Anonymized per ARR policy.
- **Datasets/benchmarks:** ACL welcomes resource papers; this repo (dataset card, provenance, reconstruction scripts) aligns with ACL's resource-track expectations.
- **AI-use policy:** follows ACL/ARR author guidelines — check the current ARR policies page at submission time (policies on AI assistance disclosure have been evolving; verify the January 2027 cycle's requirements).

## Candidates with 2027 calls not yet announced (TBA — re-check before planning)

| Venue | Why plausible | Status |
|---|---|---|
| EACL 2027 | NLP evaluation; regional/multilingual focus | 2027 CFP not announced at analysis date (TBA) |
| AISTATS 2027 | Statistical methodology (mixed models, calibration) | 2027 CFP not announced at analysis date (TBA) |
| NeurIPS 2027 (Datasets & Benchmarks) | Dataset/benchmark contribution framing | 2027 CFP not announced (historically ~May deadlines) (TBA) |
| ICLR 2028 | Evaluation/reliability themes; earliest cycle after a Jan 2027 ARR miss | 2028 CFP not announced (TBA) |
| EMNLP 2027 | NLP; ARR mid-2027 cycle | 2027 CFP not announced (TBA) |

## Venue-fit matrix (verified venues only)

| Criterion | FAccT 2027 | ACL 2027 |
|---|---|---|
| Topical fit (source-controlled benchmark validity; regional calibration audit) | Strong (evaluation practices focus area) | Strong (evaluation + African NLP + resources) |
| Manuscript format compatibility | Needs conversion to ACM `acmart` (TAPS) | Already in ACL format |
| Deadline feasibility from 2026-10-30 | Abstract deadline passed (Nov 3 paper deadline unreachable without a registered abstract) | ARR Jan 4, 2027 — ~9 weeks away |
| Anonymity | Required | Required (ARR) |
| Community fit for the null-result methodology contribution | Strong (audit culture) | Strong (evaluation track record) |
| Dual-submission constraint | Conflicts with any concurrent ARR review | Compatible with publishing repo now |

## Recommendation

1. **Primary target: ACL 2027 via ARR, submission deadline 2027-01-04.** Best format fit (manuscript is already ACL/ARR-formatted), adequate runway, evaluation + resource expectations match the contribution, and the public repository aligns with ACL's resource norms.
2. **Alternative A: FAccT 2027** — only viable if an abstract was registered by 2026-10-27; would require conversion to ACM TAPS format and adding a stronger sociotechnical implications section.
3. **Alternative B: EMNLP 2027 / NeurIPS 2027 D&B** — re-check when CFPs are announced (TBA); both would benefit from the additional experiments in `SUBMISSION_ROADMAP_2027.md` first.

## Changes needed to strengthen the manuscript (per venue)

- **For ACL 2027 (primary):** (i) tighten the abstract to lead with the *validity requirement* framing; (ii) expand limitations on model-panel size in response to likely reviewer questions; (iii) ensure the ARR reproducibility checklist links this repository; (iv) confirm AI-use disclosure against the January 2027 ARR policy.
- **For FAccT 2027 (if viable):** (i) recast related work with the evaluation-practices literature; (ii) add explicit adverse-impact/ethics endmatter; (iii) convert to `acmart` TAPS.

## Date-stamp honesty

Deadlines above were verified on **2026-10-30** from the official pages linked. Conference deadlines change; re-verify at the official pages before committing to any submission plan. Nothing in this repository should be read as asserting that the paper has been submitted to, accepted by, or is under review at any venue.
