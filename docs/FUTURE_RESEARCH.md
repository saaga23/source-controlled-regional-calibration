# Future Research

**Principle:** directions are **prioritized by expected contribution per unit of cost**, not listed as a wish list. Each entry states the unresolved question, what exists, what is missing, a design sketch, requirements, and risks. Costs marked honestly; nothing below is authorized to spend money without owner approval.

## Priority 1 — Within-study matched-source vs. source-controlled experiment (the causal test)

- **Unresolved question:** is the regional overconfidence reported in mixed-source audits *caused* by source mixing?
- **Exists:** a between-study contrast (this project's source-controlled null vs. earlier mixed-source findings); different items and models, so not causal.
- **Missing:** one experiment, same models, both conditions: (a) mixed-source arm (AfriMMLU Africa items + Global-MMLU Europe items) and (b) source-controlled arm (GM-only), identical models, prompts, and decoding.
- **Design sketch:** within-model 2×2 (condition × region), same metric suite; item-level random effects; qid-level permutation within arm; report interaction of condition × region — the causal estimate is whether the Africa-overconfidence effect *appears* only in the mixed-source arm.
- **Data requirements:** AfriMMLU items (public), Global-MMLU (public); need ~100+ mixed-source item pairs for adequate power — AfriMMLU's size supports this (unlike GM-only's 90-item ceiling).
- **Statistical requirements:** pre-registered directional test with qid-level permutation; power analysis before running (target MDE ≈ d 0.3 requires ~200 wrong answers — feasible with 2 arms × 7 models × ~200 items).
- **Cost:** modest API cost (order of $1–3 at the prices recorded in this project's manifest); **requires owner authorization.**
- **Expected contribution:** converts a plausibility argument into a direct causal test; publishable as a standalone methods paper.
- **Risks:** AfriMMLU licensing and translation-quality measurement; condition asymmetries (item count differs across arms — handled by design, must be reported).

## Priority 2 — Larger source-controlled samples via multi-benchmark pooling

- **Unresolved question:** does the source-controlled null hold beyond 180 items and beyond Global-MMLU's history-heavy content?
- **Missing:** Global-MMLU's Africa-tagged pool is exhausted — but other region-tagged benchmarks could provide matched arms (e.g., additional culturally tagged MMLU variants as they are released).
- **Design:** pool region-tagged items across benchmarks *within* each region only if construction provenance is held constant per arm; stratify by source *within* the analysis to avoid reintroducing the confound.
- **Requirements:** a second region-tagged benchmark with harmonized difficulty metadata; pre-registered analysis plan.
- **Cost:** $0 analysis if model outputs already exist for the new benchmark; otherwise API cost.
- **Risks:** pooling across benchmarks re-imports source variance — the very confound this project warns about; only defensible with per-source stratification.

## Priority 3 — Multilingual regional calibration

- **Unresolved question:** does the source-controlled null hold outside English? Zhou et al. (2025) [P] report worse calibration in non-English settings.
- **Design:** Global-MMLU's parallel translations permit exactly the same audit per language (Africa-tagged vs Europe-tagged items within one language), across several languages.
- **Requirements:** translation-quality metadata per language (Global-MMLU provides annotation provenance); API budget scales with languages × models × items.
- **Contribution:** separates "regional content" effects from "language of evaluation" effects — currently indistinguishable.
- **Cost:** linear in languages evaluated; e.g., 5 languages ≈ 5× the original run's cost (order of $3); requires authorization.
- **Risks:** translation artifacts (Global-MMLU's own motivation); model coverage of lower-resource languages.

## Priority 4 — Prompt-template sensitivity

- **Unresolved question:** how much of the measured calibration is template-specific?
- **Design:** ≥5 templates (paraphrase + format variations), 1–2 models, 180 items; report VCE distribution shifts and metric stability.
- **Cost:** small (order of cents at recorded prices); requires authorization.
- **Contribution:** quantifies the single-template limitation (manuscript limitation 6).

## Priority 5 — Post-hoc calibration baselines

- **Unresolved question:** does standard post-hoc calibration (temperature scaling, Platt, histogram binning) close per-model gaps, and does it interact with region?
- **Design:** fit post-hoc layers on a calibration split (held-out items or models), evaluate per region; report ECE/Brier before/after.
- **Requirements:** a split protocol that respects item clustering; care that post-hoc fitting does not leak item information.
- **Cost:** $0 (uses existing outputs).
- **Contribution:** tells practitioners whether regional miscalibration is fixable post hoc — directly actionable.

## Priority 6 — Broader uncertainty measurement

- **Unresolved question:** do the null regional results hold for signals beyond VCE/MSP (semantic entropy, sampling dispersion, token-level confidence where accessible)?
- **Design:** add signals to the same 180-item run; same inferential discipline.
- **Cost:** modest API cost; requires authorization.
- **Contribution:** strengthens the "no uniform regional overconfidence" conclusion against signal-choice objections.

## Priority 7 — Temporal stability

- **Unresolved question:** are regional calibration patterns stable across model versions (models change under the same API name)?
- **Design:** re-run the identical protocol when model versions rotate; compare against the frozen v18 outputs using the same item IDs.
- **Cost:** ~$0.66 per re-run; requires authorization.
- **Contribution:** turns a snapshot into a longitudinal audit; complements Mirza et al.'s cross-version factuality findings.

## Explicitly not priorities (and why)

- **Country-level analysis of the current 180 items:** unpowered (90 items per region cannot support 54-country contrasts).
- **New Africa-specific benchmark construction:** valuable but a separate project; this repository's contribution is the *audit method*, and priority 1–3 reuse existing public data.
- **Leaderboard participation:** the 180-item slice is not a ranking instrument (dataset card, out-of-scope uses).
