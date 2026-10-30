# Result Interpretation

## The main claim, stated carefully

**Observed:** on a source-controlled slice (Global-MMLU only, 180 items, 7 models, English, medium difficulty), there is no statistically detectable regional difference in accuracy or in wrong-answer confidence, and the high-confidence error rate is descriptively *lower* for Africa-tagged items.

**Claimed:** apparent regional overconfidence (as reported in earlier mixed-source comparisons) *can be an artifact of mixing benchmark sources*, and audits that hold source constant give a clearer picture of regional calibration.

**Not claimed:** that source confounding is *proven* to be the cause; that no regional effects exist; that the regions are calibrated *equivalently*.

## Why the null result is informative here — and what limits it

1. **Power is adequate for the effect originally reported.** The design has ≈80% power at d = 0.43, ≈90% at d = 0.50, and ≈100% at d = 1.00. Earlier mixed-source work reported effects around d ≈ 1. If an effect of that magnitude existed under source control, this design would very likely have detected it. Its absence is therefore *meaningful evidence against* an effect of the originally reported size — under this design.
2. **But it is not equivalence.** Smaller effects (d ≲ 0.43) remain compatible with the data. No TOST was run (underpowered at this n). All "no difference" statements in this repository mean "not detected," never "equal."
3. **Between-study comparison, not causal proof.** The mixed-source and source-controlled studies differ in items, difficulty band, and model panel. The disappearance of the effect is *consistent with* source confounding, but a within-study matched design (same models, both conditions) is required for causal attribution — that is the top future-work item (`FUTURE_RESEARCH.md`).
4. **Direction of the residual point estimate.** Wrong-answer confidence leans toward *lower* confidence on Africa (d = −0.317), and CHR favors Africa (0.77). Under a source-confounding explanation, removing the source artifact should not create a new direction of bias; a modest reverse tilt is compatible with the matched composition (e.g., the Africa-tagged arm's subject mix) but is not interpretable as a "reverse overconfidence" finding given the null permutation result.

## What the mixed models add

Model fixed effects dominate region effects (Gemma +4.05, Llama +2.73 on logit-confidence vs region +0.15, p=.42). Question-ID variance is large (σ² = 1.30, p<.001): item difficulty is a first-order driver of confidence. Practical reading: **calibration is mostly a property of the model (and the item), not of the region** — and any regional signal that exists is model-specific (DeepSeek/Claude worse on Africa-ECE; GPT-4.1-Nano/Llama worse on Europe-ECE), which is why aggregate "regional calibration" dashboards can mislead.

## Why this matters for the field

- **Auditing practice:** regional fairness audits that swap benchmarks across regions should be treated as measuring region+source, not region. Source control is cheap (this run cost $0.66) and belongs in the standard toolkit.
- **Deployment:** confidence-based routing/thresholding decisions calibrated on mixed-source audits mis-estimate per-region risk in an unknown direction.
- **Benchmark building:** region tags without content validation are metadata, not ground truth — this audit's own 12/180 flagged labels illustrate the failure mode, and the leave-out check shows how to bound its influence.

## Honest accounting of alternative explanations

| Alternative explanation for the null | Assessment |
|---|---|
| Insufficient power for the *original* effect size | Ruled out for d ≈ 1 (power ≈ 1.0); not ruled out for d < 0.43 |
| Different items (medium difficulty) mask the effect | Possible; difficulty restriction is a stated limitation; full-spectrum replication is future work |
| Different model panel than earlier studies | Possible; the panel is small and English-centric |
| English-only evaluation masks region effects | Possible; multilingual replication is future work |
| Ceiling effects compress the contrast | Partially relevant (accuracy ≈ 87%); wrong-answer confidence is less affected (n=170 wrong answers) |
| Source confounding in earlier work | Consistent with all observations; not proven |

## Framing discipline used throughout this repository

- "No statistically significant X" — never "no X".
- Descriptive vs inferential status labeled per metric (CHR is descriptive).
- Pre-specified vs exploratory chronology disclosed (`EXPERIMENT_PROTOCOL.md`).
- The 12 flagged items are called label noise, kept in primary analysis, with a leave-out check.
