# Data Directory — Canonical Dataset Metadata

## Canonical Raw CSV
- **Path:** `data/raw/03_openrouter_outputs_v18_correct.csv`
- **Hash (SHA-256):** `1915a77c02ff1f08a87f8b2950f2e2c5e3041a353f7e26f456dd700543a6807d`
- **Row count:** 2,520
- **Unique QIDs:** 180
- **Model count:** 7
- **Africa / Europe split:** 90 / 90
- **Generation route:** OpenRouter API
- **Temperatures:** 0.0 (closed models), 0.8 (open models)
- **Purpose columns:** `greedy`, `vce`
- **Cost:** $0.66
- **Date:** 2026-07-13

## Provenance
Derived from Global-MMLU (Singh et al., 2025). Items curated to 180 medium-difficulty GM-only questions (90 Africa-tagged, 90 Europe-tagged). Content-label mismatch check identified 12 mismatched items (6.7%) kept in main analysis with leave-them-out robustness check.

## VCE Formula
Verbalized confidence (VCE) collected via prompt asking model to state "0-100 guess of how likely its answer is correct". No self-consistency sampling.

## Directory Layout
- `data/raw/` — raw experimental outputs (canonical CSV)
- `data/curated/` — curated datasets (180-item JSON)
- `data/metadata/` — schema definitions, dictionaries

## Canonical Curated Dataset
- **Path:** `data/curated/02_gm_only_180_items.json`
- **Items:** 180 Global-MMLU questions, balanced 90 Africa / 90 Europe
