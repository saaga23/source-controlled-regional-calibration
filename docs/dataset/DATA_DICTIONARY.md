# Data Dictionary

## `data/curated/02_gm_only_180_items.json`

Top level: `seed` (42), `n_total` (180), `n_africa` (90), `n_europe` (90), `gm_only` (true), `description`, `items` (list of 180 objects).

### Item fields

| Field | Type | Values / format | Description |
|---|---|---|---|
| `id` | string | e.g. `GM-AF-prehistory-test-79` | Unique item identifier; encodes region tag, subject, split, and upstream index |
| `source` | string | `Global-MMLU (ACL 2025)` | Provenance of the item |
| `region` | string | `Africa` \| `Europe` | Global-MMLU cultural region tag (the audit's grouping variable) |
| `group` | string | e.g. `GM_Europe_-` | Matching group key (region + CS tag) used in stratification |
| `cat` | string | MMLU subject slug (e.g. `prehistory`) | Subject category |
| `diff` | string | `medium` | Difficulty band (only medium retained) |
| `q` | string | free text | Question text (English) |
| `ch` | list[string] | 4 elements | Answer options |
| `a` | integer | 0–3 | Index of correct option in `ch` |
| `cs` | string | `CS` \| `CA` \| `-` | Global-MMLU cultural-sensitivity tag (culturally sensitive / culturally aware / untagged) |
| `lang` | string | `en` | Language |
| `gm_only` | bool | `true` | Design flag: item is part of the GM-only core |
| `gm_match_level` | string | `strict` | Matching strictness achieved for this item |

## `data/raw/03_openrouter_outputs_v18_correct.csv` (2,520 rows; one per model-item-purpose)

| Column | Type | Description |
|---|---|---|
| `item_idx` | int | Position of the item in the evaluation order (seed 42 shuffle) |
| `id` | string | Item ID; joins to curated file |
| `qid` | string | Question-cluster ID used for permutation/mixed-effects (item-level clustering) |
| `region` | string | `Africa` \| `Europe` |
| `model` | string | Short model key (`claude-sonnet-4.6`, `deepseek-v3.2`, `gemini-2.5-flash-lite`, `gemma-4-31b`, `gpt-4o-mini`, `gpt41-nano`, `llama-3.3-70b`) |
| `model_id` | string | OpenRouter model identifier used in the API call |
| `model_class` | string | `closed` \| `open` (weight availability) |
| `correct_letter` | string | Gold option letter (A–D), from curated `a` |
| `cat` | string | Subject category (copied for convenience) |
| `diff` | string | Difficulty band |
| `source` | string | Benchmark source string |
| `input_tokens` | int | Prompt tokens billed |
| `output_tokens` | int | Completion tokens billed |
| `cost_usd` | float | Billed cost of the call (USD) |
| `timestamp` | string | UTC call timestamp |
| `purpose` | string | `greedy` (answer elicitation) or `vce` (confidence elicitation) |
| `pred` | string | Predicted option letter (both purposes; `vce` rows repeat the greedy answer being rated) |
| `correct` | int | 1 if `pred == correct_letter` else 0 |
| `vce` | float | Verbalized confidence in [0,1] (0–100 integer ÷ 100); `vce`-purpose rows only |
| `sc_agree` | float | Mean self-consistency: share of 5 samples at temperature 0.8 agreeing with the greedy answer |
| `cocoa_fixed` | float | Fixed composite `CoCoA_α = α·VCE + (1−α)·MSP` (α as registered in the run manifest) |
| `greedy_text` | string | Raw model output text for the greedy call |
| `provider` | string | OpenRouter route/provider serving the call |

## Derived field definitions (used in analysis)

| Field | Definition |
|---|---|
| Accuracy | mean of `correct` over greedy rows |
| CHR(τ) | P(`correct` = 0 \| `vce` ≥ τ), computed over `vce`-purpose rows; primary τ = 0.70 |
| Wrong-answer VCE | mean `vce` over `vce` rows with `correct` = 0 |
| ECE | Σ_b (n_b/N)·|acc_b − conf_b| over 10 equal-width bins of `vce` |
| Brier | mean (vce − correct)² |
| AUROC | ROC AUC of `vce` as discriminator of `correct` |

See `docs/methodology/METRIC_DEFINITIONS.md` for equations, limitations, and binning sensitivity.
