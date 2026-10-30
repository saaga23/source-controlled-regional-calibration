# Literature Review

**Scope:** LLM confidence and calibration; regional/geographical evaluation; benchmark validity and construction; statistical methodology; evaluation and fairness implications. **Freshness:** prioritizes 2023–2026 work while retaining foundational literature. **Verification:** every entry carries a verification status — see `REFERENCE_VERIFICATION.md` (V = externally verified, P = pending re-verification; details quoted from the manuscript bibliography for P entries).

---

## A. LLM confidence and calibration

**Foundations.** Guo et al. (ICML 2017, [PMLR v70](https://proceedings.mlr.press/v70/guo17a.html)) [V] established the modern calibration toolkit — Expected Calibration Error (ECE), reliability diagrams, and temperature scaling — for neural classifiers. Niculescu-Mizil & Caruana (ICML 2005) [P] is the earlier statistical treatment of why predicted probabilities are not naturally calibrated under supervised learning.

**Verbalized confidence.** Kadavath et al. (2022, [arXiv:2207.05221](https://arxiv.org/abs/2207.05221)) [V] showed large models can self-evaluate: when formatted properly, their stated confidence on multiple-choice and true/false items is largely calibrated. Lin et al. (TMLR 2022) [P] taught models to *express* uncertainty in words; Tian et al. (EMNLP 2023, [link](https://aclanthology.org/2023.emnlp-main.330/)) [V] showed that simply asking (prompted verbalized confidence) calibrates RLHF-tuned models better than sampling-based alternatives. Mielke et al. (TACL 2022) [P] trained dialogue agents to produce calibrated verbal uncertainty. Xiong et al. (ICLR 2024) [P] evaluated confidence elicitation broadly and found verbalized confidence frequently overconfident, with consistency-based signals helping.

**Consistency-based signals.** Wang et al. (ICLR 2023) [P] introduced self-consistency (majority voting over sampled reasoning paths); Kuhn et al. (ICLR 2023) [P] defined semantic uncertainty via clustering of generated answers; Manakul et al. (EMNLP 2023, [link](https://aclanthology.org/2023.emnlp-main.488/)) [V] operationalized sampling consistency as a black-box hallucination detector (SelfCheckGPT). Wang et al. (EMNLP 2024 Findings, [link](https://aclanthology.org/2024.findings-emnlp.354/)) [V] showed self-consistency improves calibration for math reasoning. Together these underpin the MSP signal used (as a supporting analysis) in this project.

**Metric critiques.** Si et al. (EMNLP 2022 Findings, [link](https://aclanthology.org/2022.findings-emnlp.206/)) [V] demonstrated that aggregate ECE can be gamed by flat, uninformative confidence — a key reason this project reports ECE alongside Brier, AUROC, and CHR rather than a single headline number. Huang et al. (EMNLP 2024, [link](https://aclanthology.org/2024.emnlp-main.18/)) [V] proposed rank-calibration as a threshold-free diagnostic. Zhang et al. (EMNLP 2024, [link](https://aclanthology.org/2024.emnlp-main.318/)) [V] decomposed confidence into question uncertainty and answer fidelity — relevant because distractor design (a source-specific property) plausibly affects exactly this decomposition.

**Overconfidence and variation.** Steyvers et al. (2024, [arXiv:2401.13835](https://arxiv.org/abs/2401.13835)) [V] documented systematic gaps between model and human confidence. Chhikara (TMLR 2025) [P] examined distractor-augmented prompting effects on confidence — evidence that item-construction choices move calibration, which is the mechanism this project is worried about at the benchmark level. Xia et al. (2026) [P] argue calibration must be probed under language variation. Zhou et al. (2025) [P] report that non-English settings calibrate worse overall and that intermediate representations can carry calibration signal.

**Relevance to this project.** None of these works asks whether *regional* calibration comparisons are internally valid. They supply the signal (VCE, MSP), the metrics (ECE, Brier, AUROC), and the warnings (ECE gameability; prompt and distractor sensitivity) that make the confound concern concrete.

## B. Regional and geographical evaluation

Manvi et al. (ICML 2024, [PMLR v235](https://proceedings.mlr.press/v235/manvi24a.html)) [V] found LLMs systematically biased against lower-income regions, Africa included — on recommendations, dialect, and pronunciation tasks. Mirza et al. (2024, [arXiv:2401.17839](https://arxiv.org/abs/2401.17839)) [V] (Global-Liar) measured factuality of statements across regions and time, reporting a Global-North advantage. Moayeri et al. (FAccT 2024) [P] (WorldBench) built country-level factual questions and found higher error rates for lower-income countries, especially Sub-Saharan Africa. Coelho et al. (2025) [V-leaning] showed that retrieval augmentation does not close the geographic fact-checking gap. Decoupes et al. (Machine Learning, 2025) [P] proposed distortion measures exposing Western overrepresentation and African underrepresentation in model knowledge. Rystrom et al. (2025) [P] found multilingual capability does not imply cultural alignment.

**African-NLP benchmarks.** Adelani et al. (NAACL 2025, [arXiv:2406.03368](https://arxiv.org/abs/2406.03368)) [V] released IrokoBench (AfriMMLU, AfriXNLI, AfriMGSM) for 17 African languages. Ojo et al. (ACL Findings 2025) [P] released AfroBench covering 64 languages × 15 tasks. Singh et al. (ACL 2025, [arXiv:2412.03304](https://arxiv.org/abs/2412.03304)) [V] released Global-MMLU: a culturally aware re-creation of MMLU in 42 languages with per-item region and cultural-sensitivity tags, built with compensated professional and community annotators. Guan et al. (COLING 2025) [P] (SAGED) provide a bias-benchmarking pipeline with fairness calibration.

**Relevance to this project.** These works establish *that* geographic disparities exist. What they do not establish is what such disparities mean for **calibration**, nor whether apparent regional overconfidence is a property of models or of the comparison design. Critically, the Africa-side evidence in earlier cross-regional work came from African-built benchmarks (AfriMMLU) while Europe-side evidence came from Global-MMLU or Wikidata — so region moved together with source.

## C. Benchmark validity and construction

The manuscript's central methodological concern — **benchmark-source confounding** — sits within a broader validity literature:

- **Construct validity of benchmarks:** whether a benchmark measures what it claims (knowledge vs. format artifact). Zhang et al. (EMNLP 2024) [V] fidelity decomposition and Chhikara (2025) [P] distractor effects show that item-construction choices measurably move confidence and accuracy; Global-MMLU itself ([arXiv:2412.03304](https://arxiv.org/abs/2412.03304)) [V] demonstrated that model *rankings* change depending on whether culturally sensitive subsets are used, and that machine-translated MMLU distorts evaluation.
- **Sampling and representativeness:** Global-MMLU's finding that 84.9% of geographic questions concern North America or Europe [V] is direct evidence that unstratified geographic evaluation is composition-confounded.
- **Contamination and leakage:** standard concerns (training/test overlap) are not the focus here but interact with regional slices: if African items are rarer in training corpora, difficulty and contamination both differ by region.
- **Label quality:** the 12 content-label mismatches found during this project's human check (6.7% of the sample) are a concrete, small-documented instance of metadata noise in a flagship benchmark.

**Gap:** the literature documents geographic disparities and construction artifacts separately; it does not test whether *regional calibration conclusions* survive holding benchmark source constant. That is the contribution of this project.

## D. Statistical and methodological validity

Four methodological issues shape the analysis design:

1. **Clustered observations.** Each question is answered by all seven models; the seven observations per question are not independent. Row-level permutation is invalid for this structure — it shreds item-level heterogeneity (difficulty, content) and produces anti-conservative p-values. This project therefore permutes **region labels at the question-ID level** (preserving each item's seven observations together; seed 20260622, 10,000 permutations), and reports cluster-robust logistic regression (SEs clustered by question ID) for accuracy and a logit-normal mixed model with question-ID random intercept for confidence.
2. **Calibration metrics and their limitations.** ECE depends on binning (equal-width vs equal-mass) and can be gamed by flat confidence [V: Si et al.]. This project reports both binning schemes, Brier (a strictly proper score), AUROC (discrimination), and CHR (operational threshold view), and provides cluster-bootstrap CIs (2,000 resamples for paired comparisons; 100 for individual metrics; NumPy seed 20260622).
3. **Significance vs. equivalence.** Failure to reject a null hypothesis is not evidence of equivalence. This project reports the minimum detectable effect (MDE ≈ Cohen's d = 0.433 at 80% power; raw-scale MDE 0.099 on the 0–1 VCE scale) and explicitly declines an equivalence claim.
4. **Power.** With 170 wrong answers (79/91), power is ~49% for d = 0.30, ~90% for d = 0.50, ~100% for d = 1.00. The design can reliably detect moderate-to-large effects only.

## E. Evaluation and fairness implications

If regional comparisons are source-confounded, then downstream harm propagates: (i) **model comparisons** — vendor rankings on "regional fairness" may reflect benchmark construction, not model behavior; (ii) **fairness claims** — a documented "regional overconfidence gap" could trigger costly mitigation targeting the wrong cause; (iii) **confidence-based decision systems** — deployment thresholds calibrated on mixed-source audits mis-estimate per-region risk; (iv) **automated evaluation pipelines** — dashboards that aggregate regional slices inherit the confound silently; (v) **resource allocation** — benchmark investments may be steered by artifacts of source mixing.

The manuscript's framing is deliberately careful: the source-controlled null *is consistent with* source confounding in earlier work, but item-selection and model-panel differences between studies prevent a definitive causal attribution — a directly controlled mixed-source vs. source-controlled experiment remains future work (see `docs/RESEARCH_ROADMAP.md`).

---

*All linked sources above were fetched and checked on 2026-10-30; entries marked [P] are quoted from the manuscript bibliography and flagged for re-verification in `REFERENCE_VERIFICATION.md`.*
