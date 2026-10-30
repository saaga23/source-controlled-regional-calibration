# Known Limitations

Complete and honest enumeration. Ordered roughly by how much they constrain interpretation.

## Design limitations

1. **Single benchmark source (by design, but single).** All items come from Global-MMLU. The source-controlled null says nothing about African-built benchmarks (AfriMMLU etc.), which may differ in language, translation quality, or distractor design. Directly testing source control *against* mixed sources in one design is future work.
2. **180-item hard ceiling.** The Africa-tagged GM pool exhausts at 90 items. This caps power: MDE ≈ Cohen's d = 0.433 at 80% power; effects smaller than ~d 0.4 remain possible and unexcluded. Null results are not equivalence.
3. **Medium difficulty only.** Findings may not transfer to easy or hard items; the difficulty band was chosen to keep models off ceiling/floor, but generalization across the spectrum is untested.
4. **Binary regional aggregation.** "Africa" (54 countries) and "Europe" are monolithic tags. No country-, language-community-, or subregion-level analysis is powered. All regional claims are aggregate-level.
5. **History-heavy content.** ≈71% of items are history-adjacent (world history, prehistory, US history), reflecting Global-MMLU's tag distribution rather than a sampling choice. Topical generalization is limited.

## Instrumentation limitations

6. **Single prompt template.** One template per purpose for all models/items; no few-shot, no system prompts. Prompt phrasing and ordering are known to shift outputs and confidence; template sensitivity is bounded only by the upstream VCE sensitivity report, not exhaustively.
7. **Temperature asymmetry.** Greedy answers use temperature 0 (closed) / 0.8 (open-weight); VCE uses temperature 0. Cross-model comparisons of confidence inherit this asymmetry (documented; not removed post hoc).
8. **VCE is a stated belief.** Verbalized confidence can diverge from sampling behavior; only one primary signal is used (MSP/CoCoA reported as supporting data, not validated methods).
9. **No post-hoc calibration baselines.** Temperature scaling, Platt scaling, histogram binning were not evaluated; the study reports raw verbalized confidence only.
10. **AUPRC not reported.** With ≈87% base accuracy, AUROC is optimistic relative to precision-recall; AUPRC should be added in future evaluations.

## Inference limitations

11. **Parametric CI on d assumes independence** (violated under item clustering); it is descriptive. The permutation test is the inferential evidence.
12. **Per-model tests are small-n** (7–29 wrong answers per arm per model); non-significance per model is a sample-size statement.
13. **No CHR inferential test.** CHR comparisons are descriptive only.
14. **Between-study confounding comparison.** The source-confounding interpretation rests on a between-study contrast (different items, models); no within-study causal test exists.

## Data limitations

15. **Benchmark label noise.** 12/180 (6.7%) content-label mismatches (US-history content tagged Africa/Europe), kept in primary analysis with a leave-out check; region tags otherwise taken from Global-MMLU without full blind re-annotation.
16. **English-only.** No multilingual evaluation; multilingual calibration is known to differ (Zhou et al. 2025 [P]).

## Model-panel limitations

17. **Seven models, English routes only**, spanning 2024–2026 releases; not all major families or closed systems; results may not transfer to newer or larger models; model versions are pinned only as recorded in the run manifest.

## Reproducibility scope

18. **Fresh inference requires OpenRouter** and the models to still be routed; model unavailability should be documented rather than substituted (see README reproduction section). All *analysis* is reproducible without any API access from the released raw CSV.
