# Ethics Statement

## Purpose

This work documents a measurement-validity concern in AI evaluation: regional audits that compare models across *different* benchmark sources can attribute to "region" what is actually an artifact of benchmark construction. The aim is more accurate and more equitable evaluation — not to disparage any model, vendor, region, or language community.

## Human subjects

No human subjects were involved. No new human annotations were collected for the released dataset; the content-label check was performed by the project author on already-public benchmark items. The upstream Global-MMLU dataset was produced with compensated professional and community annotators (Singh et al., 2025).

## Data

All items are from Global-MMLU (Apache-2.0, public); model outputs are our own recorded API responses. No personal data, no user-generated content beyond public benchmark items, no restricted material.

## Regional framing

"Africa" and "Europe" are Global-MMLU's cultural region tags on benchmark items. They are not claims about individuals, countries, or test-taker populations. The repository consistently treats these as aggregate labels with documented limitations (binary aggregation; 54-country diversity within "Africa" is unmodeled).

## Fairness implications of the findings

The null findings caution *against* acting on source-confounded regional audits (e.g., retraining or restricting models based on a gap that may be a benchmark artifact). They equally caution *against* declaring regions equivalent — the design cannot detect smaller effects.

## AI assistance

Generative AI tools were used for language editing, research planning, methodological critique, statistical-audit reasoning, and debugging, under human review and verification. All design decisions, analyses, factual claims, and final content were verified by the author against the underlying data; the author takes full responsibility.
