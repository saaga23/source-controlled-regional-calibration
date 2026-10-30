# Results

**Status:** all values below were re-verified on 2026-10-30 directly from `data/raw/03_openrouter_outputs_v18_correct.csv` (SHA-256 `1915a77c…`) in this repository, using the verification scripts in `scripts/verification/` and `scripts/robustness/`. Frozen evidence copies: `results/reports/`.

## Run quality

| Quantity | Value |
|---|---|
| Model-item pairs | 1,260 (180 items × 7 models) |
| Model-purpose calls | 2,520 (greedy + VCE per pair) |
| Parse/API failures | 0 |
| Total tokens | 4,448,016 (4,435,416 in / 12,600 out) |
| Total cost | $0.6556 |

## Headline results (primary signal: VCE)

| Metric | Africa | Europe | Ratio A/E | Test | p |
|---|---|---|---|---|---|
| Accuracy (H1) | 87.5% (551/630) | 85.6% (539/630) | 1.022 | χ² = 0.823; qid-perm; cluster-robust logit | .364 / .677 / .646 |
| Wrong-answer VCE (H3) | 0.761 (n=79) | 0.832 (n=91) | 0.915 | MWU; qid-perm | .234 / .726 |
| CHR₀.₇₀ (H2, descriptive) | 10.5% (601) | 13.6% (609) | 0.769 | — (no inferential test) | — |
| Pooled ECE | 0.048 (95% cluster-bootstrap CI [0.032, 0.083]) | | | | |
| Pooled Brier | 0.114 | | | | |
| Pooled AUROC | 0.679 | | | | |

Effect size (H3, descriptive): Cohen's d = −0.317, 95% parametric CI [−0.621, −0.014] — the point estimate points **toward lower** wrong-answer confidence on Africa, and the CI is not formal inferential evidence under clustering (permutation test carries that role).

## What was observed

1. **No detectable accuracy gap** between Africa- and Europe-tagged items under source control (all three inferential approaches agree).
2. **No detectable Africa-overconfidence signature**: wrong-answer confidence is not higher for Africa; the point estimate leans the other way.
3. **Fewer confident errors on Africa**: CHR 10.5% vs 13.6% (ratio 0.77) — descriptive.
4. **Calibration varies strongly by model**, not uniformly by region: ECE from 3.7% (GPT-4o-mini) to 13.6% (Gemma-4-31B); model effects dominate region effects in the mixed models (Gemma +4.05, Llama +2.73 on the logit-confidence scale, both p<.001; qid variance 1.30, p<.001).
5. **Region-by-model asymmetries exist but are model-specific**: DeepSeek and Claude have higher Africa ECE; GPT-4.1-Nano and Llama have higher Europe ECE.

## What was not observed

- No statistically significant regional accuracy difference.
- No statistically significant regional difference in wrong-answer confidence (pooled or per model after Holm correction).
- No uniform regional overconfidence pattern in any metric.
- No equivalence — see `RESULT_INTERPRETATION.md`.

## Per-model tables (verified)

**CHR(τ=0.70) by model** (fraction wrong among high-confidence predictions; N = high-confidence predictions):

| Model | CHR Af | N Af | CHR Eu | N Eu | Ratio |
|---|---|---|---|---|---|
| Claude | 0.025 | 79 | 0.060 | 83 | 0.420 |
| DeepSeek | 0.068 | 88 | 0.122 | 90 | 0.558 |
| Gemini | 0.063 | 79 | 0.096 | 83 | 0.657 |
| Gemma | 0.125 | 88 | 0.125 | 88 | 1.000 |
| GPT-4o (mini) | 0.135 | 89 | 0.161 | 87 | 0.838 |
| GPT-4.1n | 0.189 | 90 | 0.244 | 90 | 0.773 |
| Llama | 0.114 | 88 | 0.136 | 88 | 0.833 |
| **Pooled** | **0.105** | **601** | **0.136** | **609** | **0.769** |

**Wrong-answer confidence by model** (mean VCE on wrong answers; MWU p):

| Model | N Af | N Eu | Mean Af | Mean Eu | MWU p |
|---|---|---|---|---|---|
| Claude | 9 | 8 | 0.477 | 0.644 | .265 |
| DeepSeek | 7 | 11 | 0.693 | 0.845 | .251 |
| Gemini | 10 | 11 | 0.700 | 0.785 | .432 |
| Gemma | 12 | 11 | 0.908 | 0.973 | .668 |
| GPT-4o | 12 | 15 | 0.825 | 0.773 | .362 |
| GPT-4.1n | 17 | 22 | 0.841 | 0.861 | .530 |
| Llama | 12 | 13 | 0.742 | 0.874 | .496 |
| **Pooled** | **79** | **91** | **0.761** | **0.832** | **.234** |

**VCE calibration by model** (ECE 10-bin / Brier / AUROC):

| Model | ECE Af | ECE Eu | ECE all | Brier | AUROC |
|---|---|---|---|---|---|
| Claude | 0.086 | 0.059 | 0.064 | 0.065 | 0.841 |
| DeepSeek | 0.082 | 0.030 | 0.053 | 0.081 | 0.757 |
| Gemini | 0.090 | 0.101 | 0.093 | 0.112 | 0.674 |
| Gemma | 0.132 | 0.139 | 0.136 | 0.135 | 0.594 |
| GPT-4o | 0.037 | 0.079 | 0.054 | 0.120 | 0.732 |
| GPT-4.1n | 0.051 | 0.123 | 0.086 | 0.173 | 0.610 |
| Llama | 0.063 | 0.102 | 0.082 | 0.113 | 0.710 |

## Verification trail (commands and outcome, 2026-10-30)

| Command | Outcome |
|---|---|
| `python scripts/verification/verify_v18_lmm_ece.py` | EXIT 0; every Table-2 and Table-4 value reproduced to 3 decimals; 0 mismatches |
| `python scripts/robustness/permutation_audit.py` | qid-level permutation p-values reproduced (H1 .677; H3 .726); log: `results/reports/permutation_audit_rerun_2026-10-30.log` |
| `python scripts/verification/verify_consistency.py` | 71/71 checks PASS |
| `python scripts/verification/verify_table4.py` | mixed-effects coefficients verified |
| `python scripts/robustness/final_validation_pass.py` | LOMO, permutation, power, diagnostics — PASS |
| `pytest tests/ -q` | metric/dataset tests PASS (see `tests/`) |
