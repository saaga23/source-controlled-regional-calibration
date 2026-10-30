# Experiment Protocol

**Experiment ID:** AFRIKNOW_V18 · **Inference provider:** OpenRouter · **Run:** 1,260 model-item pairs → 2,520 model-purpose calls, zero failures · **Total cost:** $0.6556 · **Total tokens:** 4,448,016 (4,435,416 in / 12,600 out)

## Phase timeline (from project records)

| Phase | What happened | Key artifact |
|---|---|---|
| 1. Power analysis | Pre-analysis power assessment for the regional comparison | `results/reports/power_mde_final.json` |
| 2. Sample design | GM-only pool construction, medium-difficulty filter, strict matching; annotation sub-phase sample (120 items, 2026-07-06) | `data/metadata/02_sample_design_manifest.json` |
| 3. Dataset freeze | AfriKnow GM-only v3 frozen (180 items, seed 42) | `data/curated/02_gm_only_180_items.json` |
| 4. Human content-label check | Item-level review; 12 mismatches flagged (6/6), kept with leave-out check | `DATASET_CONSTRUCTION.md` (docs/dataset/) |
| 5. Inference | 7-model OpenRouter run: greedy + VCE per item; audit trail logged | `data/raw/03_openrouter_outputs_v18_correct.csv`, `reproducibility/run_logs/05_audit_trail.jsonl` |
| 6. Analysis & verification | Hypothesis tests, mixed-effects, ECE/Brier/AUROC, robustness suite | `results/reports/*`, `scripts/verification/*` |

## Hypotheses and their chronology (recorded honestly)

| Hypothesis | Content | Status at analysis time |
|---|---|---|
| **H3** (wrong-answer confidence) | Pre-specified, **directional** (one-sided: Africa > Europe) — specified before the GM-only evaluation was executed | Reported as **two-sided** because data were gathered before the analysis plan was final; this weakening is disclosed in the manuscript |
| **H1** (accuracy) | Added during first data inspection as a supporting signal | Not pre-specified |
| **H2** (CHR) | Added during first data inspection as a supporting signal; descriptive only | Not pre-specified |
| Post-hoc | Mixed-effects models, sensitivity analyses | Labeled post-hoc throughout |

No analysis was conditioned on observed effect sizes; the complete 7-model panel is reported without selection.

## Inference configuration

- **Answers (greedy):** temperature 0 for closed models, 0.8 for open-weight models; single call per item-model.
- **Confidence (VCE):** temperature 0, single pass, fed the greedy answer verbatim.
- **Self-consistency (MSP):** 5 samples, temperature 0.8.
- **Item ordering:** random seed 42. **Analysis randomness:** NumPy seed 20260622 (permutation 10,000; bootstrap 100/2,000 resamples).
- **Prompts:** two templates, identical for all models/items, no few-shot or system prompts (verbatim in `reproducibility/prompts/prompts.py` and manuscript Appendix B). Parsing: first integer (answer) / first 0–100 integer (confidence) via regex; trailing text ignored.

## Model panel

| Model | OpenRouter key in data |
|---|---|
| Claude-Sonnet-4.6 | `claude-sonnet-4.6` |
| DeepSeek-V3.2 | `deepseek-v3.2` |
| Gemini-2.5-Flash-Lite | `gemini-2.5-flash-lite` |
| Gemma-4-31B | `gemma-4-31b` |
| GPT-4o-mini | `gpt-4o-mini` |
| GPT-4.1-Nano | `gpt41-nano` |
| Llama-3.3-70B | `llama-3.3-70b` |

Exact routes, pricing, and per-call metadata are in `data/metadata/03_openrouter_manifest_v18.json`. Selection rationale and limitations (family diversity, size spread, recency, within budget; English routes only): `METHODOLOGY.md` §2.

## Run quality

- Every model completed all 180 items for both purposes: **0 parse failures, 0 API failures, 0 unparseable predictions** (per run manifest and audit trail).
- Cost per model: see `METHODOLOGY.md` §2 table (range $0.0616–$0.1700; total $0.6556).
- Raw responses (`greedy_text`) retained in the raw CSV; audit trail (`05_audit_trail.jsonl`) records SHA-256 input/output hashes per phase.

## Reproduction classes

- **Class A (no API cost):** all analyses, verifications, figures, and tables — run from the released raw CSV. This is the default reproduction path.
- **Class B (API cost, ~$0.66 at run time):** fresh inference. Requires `OPENROUTER_API_KEY` (see `.env.example`). Model availability may have changed since the run; if a route is gone, document the unavailability — do not silently substitute models.
