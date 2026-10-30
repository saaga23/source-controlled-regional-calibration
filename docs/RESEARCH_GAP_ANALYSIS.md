# Research Gap Analysis

**Date:** 2026-10-30 · **Companion docs:** `LITERATURE_REVIEW.md`, `FUTURE_RESEARCH.md`, `RESEARCH_ROADMAP.md`

## The gap this study fills

**Unresolved question in the literature:** when regional comparisons report that models are less accurate or more overconfident on Africa-related content, is the *region* doing the causal work — or is it the *benchmark source* doing the work of region?

**What exists:**

1. Strong evidence of **geographic disparities** in accuracy (Manvi et al. ICML 2024 [V]; Mirza et al. 2024 [V]; Moayeri et al. FAccT 2024 [P]; Coelho et al. 2025 [V-leaning]; Decoupes et al. 2025 [P]).
2. Established **calibration measurement methods** for LLMs (verbalized confidence: Kadavath 2022 [V], Tian 2023 [V]; consistency signals: Wang 2023 [P], Wang 2024 [V]; metric critiques: Si 2022 [V], Huang 2024 [V]).
3. Mature **African-NLP benchmarks** (IrokoBench/AfriMMLU: Adelani 2025 [V]; AfroBench: Ojo 2025 [P]; Global-MMLU: Singh 2025 [V]).
4. Direct evidence that **construction choices move results**: Global-MMLU's own audit shows model rankings change on culturally sensitive subsets, and 84.9% of geographic questions concern North America/Europe [V]; Chhikara (2025) [P] shows distractor augmentation shifts calibration.

**What was missing — and is still only partially supplied by this study:**

1. **No source-controlled regional calibration audit existed.** Prior Africa-vs-Europe comparisons mixed sources across arms (AfriMMLU for Africa; Global-MMLU/Wikidata for Europe), making region ⊕ source inseparable. This study supplies the first (to our knowledge, and bounded by our search) source-controlled slice: both arms from Global-MMLU, same language, matched category/difficulty/cultural-sensitivity composition.
2. **Calibration was under-studied relative to accuracy** in regional audits — disparities had been shown for correctness, but "does the model know when it is wrong, per region?" had not been asked under source control.
3. **No within-study causal test of the confound.** This study is a *necessary* source-controlled baseline, but the mixed-source vs. source-controlled comparison is between studies with different items and models. A matched experimental design (same models, both conditions) remains open — the single most valuable follow-up (see `FUTURE_RESEARCH.md`, direction 3).

## What this study establishes / does not establish

| Established (verified in this repo) | Not established |
|---|---|
| Under source control (GM-only, 180 items, 7 models): no significant accuracy gap (87.5% vs 85.6%, χ²=0.823, p=.364) | That regional effects do not exist anywhere — only that they are not detected under this design (MDE d≈0.43 at 80% power) |
| No detectable higher wrong-answer confidence for Africa (0.761 vs 0.832; d=−0.317; MWU p=.234; qid-permutation p=.726) | Equivalence of the regions (equivalence testing underpowered; CI includes practically large values) |
| High-confidence error rate lower for Africa (CHR 10.5% vs 13.6%) — descriptive, no inferential test | Causality of source confounding (between-study comparison only; no matched design) |
| Calibration varies strongly by model (ECE 3.7%–13.6%), region-by-model asymmetries exist | Generalization beyond medium difficulty, English, history-heavy content, and the 7-model panel |

## How the gap statement is bounded (honesty requirements)

- The "first" claim is bounded: *"to our knowledge, no prior source-controlled regional calibration audit"* — based on the search in `LITERATURE_REVIEW.md`; it is falsifiable and should be re-checked at submission time.
- Null results are reported as nulls, never as equivalence.
- The confounding explanation is stated as **consistent with**, not proven by, the data.
