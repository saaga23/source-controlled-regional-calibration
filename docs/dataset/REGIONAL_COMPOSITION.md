# Regional Composition — AfriKnow GM-only v3

## Headline composition

| Arm | Items | Share |
|---|---|---|
| Africa-tagged | 90 | 50% |
| Europe-tagged | 90 | 50% |
| Total | 180 | 100% |

Both arms are drawn from the identical source benchmark (Global-MMLU, English, medium difficulty), with matched subject-category and cultural-sensitivity composition (`DATA_QUALITY_REPORT.md`).

## What "Africa-tagged" and "Europe-tagged" mean here

The labels are **Global-MMLU's cultural region tags**: items whose content is culturally located in (or specific to) Africa vs. Europe. They are *not* claims about test-taker populations, and they are not geography of the question's factual domain — e.g., 12 US-history questions carry these tags (6/6) and are handled as documented label noise with a leave-them-out robustness check.

## Composition facts that matter for interpretation

1. **Ceiling structure.** The 90-item Africa arm is the *exhaustive* set of Global-MMLU items surviving the filters; the Europe arm is matched to it. Region is therefore fully crossed with nothing — but both arms are finite and small.
2. **History-heavy content.** ~71% of items come from history-adjacent subjects (world history 86, prehistory 30, US history 12). Cross-category claims are underpowered; the category-sensitivity evidence file (`results/reports/category_sensitivity_final.csv`) reports per-category checks.
3. **Cultural sensitivity is balanced** (16 CS / 7 CA / 67 untagged per arm), so CS status cannot confound the regional contrast.
4. **Aggregation caveat.** "Africa" aggregates 54 countries; "Europe" aggregates ~45. All regional conclusions are at this aggregate level only (manuscript Limitation 5).

## Position in the design

```
Global-MMLU (en, 14,042 test items)
  → region-tagged pool
    → medium difficulty
      → strict matching (category, difficulty, CS tag)
        → 90 Africa (exhaustive) + 90 Europe (matched)
```

The composition is the design: any measured Africa–Europe difference on this slice cannot be attributed to benchmark source, language, answer format, difficulty band, or CS composition — only to region-entangled content and sampling noise within the matched categories.
