#!/usr/bin/env python3
"""
Final high-value validation pass for AfriKnow.
$0-cost re-analyses using existing v18 data.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "raw" / "03_openrouter_outputs_v18_correct.csv"
OUT = ROOT / "final_validation_outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(CSV)
greedy = df[df["purpose"] == "greedy"].copy()
vce = df[df["purpose"] == "vce"].copy()

MODELS = [
    "claude-sonnet-4.6", "deepseek-v3.2", "gemini-2.5-flash-lite",
    "gemma-4-31b", "gpt-4o-mini", "gpt41-nano", "llama-3.3-70b"
]

def compute_ece(conf, corr, n_bins=10):
    c = np.asarray(conf, dtype=float)
    r = np.asarray(corr, dtype=float)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    edges[0] -= 1e-9
    edges[-1] += 1e-9
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (c > lo) & (c <= hi)
        if mask.sum() == 0:
            continue
        ece += (mask.sum() / len(c)) * abs(r[mask].mean() - c[mask].mean())
    return float(ece)

def brier(conf, corr):
    return float(np.mean((np.asarray(conf, float) - np.asarray(corr, float)) ** 2))

# ============================================================================
# 1. LEAVE-ONE-MODEL-OUT ROBUSTNESS
# ============================================================================
print("=" * 72)
print("1. LEAVE-ONE-MODEL-OUT ROBUSTNESS")
print("=" * 72)

lomo_results = []
for drop in MODELS:
    sub = greedy[greedy["model"] != drop].copy()
    sub_vce = vce[vce["model"] != drop].copy()
    
    # H1: accuracy chi2
    af_g = sub[sub["region"] == "Africa"]
    eu_g = sub[sub["region"] == "Europe"]
    af_acc = af_g["correct"].mean()
    eu_acc = eu_g["correct"].mean()
    n_af_g = len(af_g)
    n_eu_g = len(eu_g)
    crosstab = pd.crosstab(sub["region"], sub["correct"])
    chi2, p_chi2, dof, expected = stats.chi2_contingency(crosstab)
    
    # H3: wrong-answer VCE
    af_wrong = sub_vce[(sub_vce["region"] == "Africa") & (sub_vce["correct"] == 0)]
    eu_wrong = sub_vce[(sub_vce["region"] == "Europe") & (sub_vce["correct"] == 0)]
    af_mean = af_wrong["vce"].mean() if len(af_wrong) > 0 else np.nan
    eu_mean = eu_wrong["vce"].mean() if len(eu_wrong) > 0 else np.nan
    n_af_w = len(af_wrong)
    n_eu_w = len(eu_wrong)
    
    if n_af_w > 1 and n_eu_w > 1:
        u_stat, p_mwu = stats.mannwhitneyu(af_wrong["vce"], eu_wrong["vce"], alternative='two-sided')
        pooled_std = np.sqrt(af_wrong["vce"].var(ddof=1) / n_af_w + eu_wrong["vce"].var(ddof=1) / n_eu_w)
        d = (af_mean - eu_mean) / pooled_std if pooled_std > 0 else np.nan
    else:
        p_mwu = np.nan
        d = np.nan
    
    # CHR at tau=0.70
    high_conf = sub_vce[sub_vce["vce"] >= 0.70]
    af_chr = (high_conf[(high_conf["region"] == "Africa") & (high_conf["correct"] == 0)].shape[0] / 
              high_conf[high_conf["region"] == "Africa"].shape[0]) if high_conf[high_conf["region"] == "Africa"].shape[0] > 0 else np.nan
    eu_chr = (high_conf[(high_conf["region"] == "Europe") & (high_conf["correct"] == 0)].shape[0] / 
              high_conf[high_conf["region"] == "Europe"].shape[0]) if high_conf[high_conf["region"] == "Europe"].shape[0] > 0 else np.nan
    chr_ratio = af_chr / eu_chr if eu_chr > 0 else np.nan
    
    # Pooled ECE
    pooled_ece = compute_ece(sub_vce["vce"], sub_vce["correct"])
    
    # Mixed-effects (simplified - just region coefficients)
    try:
        acc_m = smf.glm("correct ~ region + model", sub, family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": sub["qid"]})
        beta_acc = acc_m.params["region[T.Europe]"]
        p_acc = acc_m.pvalues["region[T.Europe]"]
    except Exception as e:
        beta_acc = np.nan
        p_acc = np.nan
    
    try:
        v = sub_vce.dropna(subset=["vce"]).copy()
        v["logit_c"] = np.log(v["vce"].clip(0.001, 0.999) / (1 - v["vce"].clip(0.001, 0.999)))
        v["region"] = pd.Categorical(v["region"], categories=["Africa", "Europe"])
        v["model"] = pd.Categorical(v["model"], categories=[m for m in MODELS if m != drop])
        conf_m = smf.mixedlm("logit_c ~ region + model", v, groups=v["qid"]).fit(reml=True, method="cg", maxiter=5000)
        beta_conf = conf_m.params["region[T.Europe]"]
        p_conf = conf_m.pvalues["region[T.Europe]"]
    except Exception as e:
        beta_conf = np.nan
        p_conf = np.nan
    
    conclusion = "STABLE"
    if p_chi2 < 0.05 or p_mwu < 0.05:
        conclusion = "SENSITIVE"
    
    lomo_results.append({
        "model_removed": drop,
        "n_greedy": len(sub),
        "n_vce": len(sub_vce),
        "accuracy_africa": af_acc,
        "accuracy_europe": eu_acc,
        "chi2": chi2,
        "p_chi2": p_chi2,
        "h3_af_mean": af_mean,
        "h3_eu_mean": eu_mean,
        "h3_n_af": n_af_w,
        "h3_n_eu": n_eu_w,
        "cohens_d": d,
        "p_mwu": p_mwu,
        "chr_africa": af_chr,
        "chr_europe": eu_chr,
        "chr_ratio": chr_ratio,
        "pooled_ece": pooled_ece,
        "beta_accuracy": beta_acc,
        "p_accuracy": p_acc,
        "beta_confidence": beta_conf,
        "p_confidence": p_conf,
        "conclusion": conclusion,
    })
    
    print(f"\nDropped: {drop}")
    print(f"  Accuracy: Af={af_acc:.3f} Eu={eu_acc:.3f} chi2={chi2:.3f} p={p_chi2:.3f}")
    print(f"  H3: Af={af_mean:.3f} Eu={eu_mean:.3f} d={d:.3f} p={p_mwu:.3f}")
    print(f"  CHR ratio: {chr_ratio:.3f}")
    print(f"  Pooled ECE: {pooled_ece:.4f}")
    print(f"  Mixed-effects: acc beta={beta_acc:.3f} p={p_acc:.3f} | conf beta={beta_conf:.3f} p={p_conf:.3f}")
    print(f"  Conclusion: {conclusion}")

lomo_df = pd.DataFrame(lomo_results)
lomo_df.to_csv(OUT / "leave_one_model_out_results.csv", index=False)
print(f"\nLeave-one-model-out results saved to {OUT / 'leave_one_model_out_results.csv'}")

# Check if any drop changes conclusion
sensitive = lomo_df[lomo_df["conclusion"] == "SENSITIVE"]
print(f"\nModels that materially change result: {len(sensitive)}")
if len(sensitive) > 0:
    print(sensitive[["model_removed", "p_chi2", "p_mwu", "cohens_d"]])

# ============================================================================
# 2. STATISTICAL ROBUSTNESS: Permutation test on H1 and H3
# ============================================================================
print("\n" + "=" * 72)
print("2. PERMUTATION TEST ROBUSTNESS")
print("=" * 72)

N_PERM = 10000
np.random.seed(20260622)

# Observed statistics
obs_chi2, _, _, _ = stats.chi2_contingency(pd.crosstab(greedy["region"], greedy["correct"]))
af_wrong = vce[(vce["region"] == "Africa") & (vce["correct"] == 0)]["vce"]
eu_wrong = vce[(vce["region"] == "Europe") & (vce["correct"] == 0)]["vce"]
obs_u, _ = stats.mannwhitneyu(af_wrong, eu_wrong, alternative='two-sided')

# Build qid-level mapping for valid permutation
qid_region = greedy.groupby("qid")["region"].first().reset_index()
qid_to_region = dict(zip(qid_region["qid"], qid_region["region"]))
qids = list(qid_to_region.keys())
regions = list(qid_to_region.values())

# Permutation distributions
perm_chi2 = np.zeros(N_PERM)
perm_u = np.zeros(N_PERM)

for i in range(N_PERM):
    perm_regions = np.random.permutation(regions)
    qid_perm = dict(zip(qids, perm_regions))
    
    g_perm = greedy.copy()
    g_perm["region"] = g_perm["qid"].map(qid_perm)
    crosstab_perm = pd.crosstab(g_perm["region"], g_perm["correct"])
    chi2_perm, _, _, _ = stats.chi2_contingency(crosstab_perm)
    perm_chi2[i] = chi2_perm
    
    v_perm = vce.copy()
    v_perm["region"] = v_perm["qid"].map(qid_perm)
    af_p = v_perm[(v_perm["region"] == "Africa") & (v_perm["correct"] == 0)]["vce"]
    eu_p = v_perm[(v_perm["region"] == "Europe") & (v_perm["correct"] == 0)]["vce"]
    if len(af_p) > 0 and len(eu_p) > 0:
        u_perm, _ = stats.mannwhitneyu(af_p, eu_p, alternative='two-sided')
    else:
        u_perm = 0
    perm_u[i] = u_perm

p_perm_chi2 = (np.sum(perm_chi2 >= obs_chi2) + 1) / (N_PERM + 1)
p_perm_u = (np.sum(perm_u >= obs_u) + 1) / (N_PERM + 1)

print(f"H1 Permutation test: observed chi2={obs_chi2:.3f}, p_perm={p_perm_chi2:.4f}")
print(f"H3 Permutation test: observed U={obs_u:.1f}, p_perm={p_perm_u:.4f}")

perm_results = {
    "observed_chi2": float(obs_chi2),
    "p_perm_chi2": float(p_perm_chi2),
    "observed_u": float(obs_u),
    "p_perm_u": float(p_perm_u),
    "n_perm": N_PERM,
}
with open(OUT / "permutation_test_results.json", "w") as f:
    json.dump(perm_results, f, indent=2)

# ============================================================================
# 3. NULL / EQUIVALENCE INTERPRETATION
# ============================================================================
print("\n" + "=" * 72)
print("3. NULL / EQUIVALENCE INTERPRETATION")
print("=" * 72)

# H3 observed effect and CI
af_wrong = vce[(vce["region"] == "Africa") & (vce["correct"] == 0)]["vce"]
eu_wrong = vce[(vce["region"] == "Europe") & (vce["correct"] == 0)]["vce"]

n1, n2 = len(af_wrong), len(eu_wrong)
m1, m2 = af_wrong.mean(), eu_wrong.mean()
v1, v2 = af_wrong.var(ddof=1), eu_wrong.var(ddof=1)
d = (m1 - m2) / np.sqrt(((n1-1)*v1 + (n2-1)*v2) / (n1+n2-2))
se_d = np.sqrt((n1+n2)/(n1*n2) + d**2/(2*(n1+n2)))

# 95% CI on d (non-central t approximation, using normal for simplicity given small n)
ci_low = d - 1.96 * se_d
ci_high = d + 1.96 * se_d

# Minimum detectable effect (MDE) for 80% power, alpha=0.05 two-sided
# Using formula for two-sample t-test
from scipy.stats import norm
z_alpha = norm.ppf(1 - 0.05/2)
z_beta = norm.ppf(0.80)
mde = (z_alpha + z_beta) * np.sqrt(v1/n1 + v2/n2)

print(f"H3 Observed Cohen's d: {d:.3f}")
print(f"95% CI on d: [{ci_low:.3f}, {ci_high:.3f}]")
print(f"MDE for 80% power (alpha=0.05): {mde:.3f}")
print(f"Power for d=0.30: {norm.cdf((np.sqrt(v1/n1 + v2/n2) * 0.30) / np.sqrt(v1/n1 + v2/n2) - z_alpha):.3f}")

# More precise power calculation using two-sample t-test power
from statsmodels.stats.power import tt_ind_solve_power
power_d30 = tt_ind_solve_power(effect_size=0.30, nobs1=n1, alpha=0.05, power=None, ratio=n2/n1, alternative='two-sided')
print(f"Precise power for d=0.30: {power_d30:.3f}")

# Achieved MDE at 80% power
achieved_mde = tt_ind_solve_power(effect_size=None, nobs1=n1, alpha=0.05, power=0.80, ratio=n2/n1, alternative='two-sided')
print(f"Achieved MDE at 80% power: {achieved_mde:.3f}")

null_results = {
    "h3_observed_d": float(d),
    "h3_ci_low": float(ci_low),
    "h3_ci_high": float(ci_high),
    "h3_mde_80pct": float(mde),
    "h3_power_d30": float(power_d30),
    "h3_achieved_mde_80pct": float(achieved_mde),
    "h3_n_africa": int(n1),
    "h3_n_europe": int(n2),
    "h3_mean_africa": float(m1),
    "h3_mean_europe": float(m2),
}
with open(OUT / "null_equivalence_interpretation.json", "w") as f:
    json.dump(null_results, f, indent=2)

# ============================================================================
# 4. MODEL DIAGNOSTICS (logit-normal LMM)
# ============================================================================
print("\n" + "=" * 72)
print("4. MODEL DIAGNOSTICS")
print("=" * 72)

v = vce.dropna(subset=["vce"]).copy()
c = v["vce"].clip(0.001, 0.999)
v["logit_c"] = np.log(c / (1 - c))
v["region"] = pd.Categorical(v["region"], categories=["Africa", "Europe"])
v["model"] = pd.Categorical(v["model"], categories=MODELS)
mf = smf.mixedlm("logit_c ~ region + model", v, groups=v["qid"]).fit(reml=True, method="cg", maxiter=5000)

# Residuals
residuals = mf.resid
fitted = mf.fittedvalues

# Basic diagnostics
from scipy.stats import shapiro, skew, kurtosis
shapiro_stat, shapiro_p = shapiro(residuals[:5000] if len(residuals) > 5000 else residuals)
resid_skew = float(skew(residuals))
resid_kurt = float(kurtosis(residuals))
resid_mean = float(np.mean(residuals))

# Check for influential qids
qid_counts = v["qid"].value_counts()
qid_var = float(mf.cov_re.iloc[0, 0])

# ICC-like estimate
total_var = float(np.var(v["logit_c"]))
icc = qid_var / (qid_var + np.var(residuals))

print(f"Residuals: mean={resid_mean:.4f}, skew={resid_skew:.3f}, kurtosis={resid_kurt:.3f}")
print(f"Shapiro-Wilk (n={min(len(residuals), 5000)}): W={shapiro_stat:.3f}, p={shapiro_p:.4f}")
print(f"qid variance: {qid_var:.3f}")
print(f"Total variance: {total_var:.3f}")
print(f"ICC-like estimate: {icc:.3f}")
print(f"Min qid count: {qid_counts.min()}, Max qid count: {qid_counts.max()}, Median: {qid_counts.median()}")

# Check for outliers in residuals
outlier_threshold = 3 * np.std(residuals)
n_outliers = np.sum(np.abs(residuals) > outlier_threshold)
print(f"Outliers (|resid| > 3*std): {n_outliers}")

# Variance homogeneity by region
af_resid = residuals[v["region"] == "Africa"]
eu_resid = residuals[v["region"] == "Europe"]
levene_stat, levene_p = stats.levene(af_resid, eu_resid, center='median')
print(f"Levene test (region): W={levene_stat:.3f}, p={levene_p:.4f}")

diagnostics = {
    "residual_mean": resid_mean,
    "residual_skew": resid_skew,
    "residual_kurtosis": resid_kurt,
    "shapiro_w": float(shapiro_stat),
    "shapiro_p": float(shapiro_p),
    "qid_variance": qid_var,
    "total_variance": total_var,
    "icc_estimate": icc,
    "min_qid_count": int(qid_counts.min()),
    "max_qid_count": int(qid_counts.max()),
    "median_qid_count": float(qid_counts.median()),
    "n_outliers_3std": int(n_outliers),
    "levene_w": float(levene_stat),
    "levene_p": float(levene_p),
    "n_total": int(len(v)),
}
with open(OUT / "model_diagnostics.json", "w") as f:
    json.dump(diagnostics, f, indent=2)

# ============================================================================
# 5. SOURCE-CONTROL SENSITIVITY: Descriptive comparison
# ============================================================================
print("\n" + "=" * 72)
print("5. SOURCE-CONTROL SENSITIVITY (DESCRIPTIVE)")
print("=" * 72)

# Load mixed-source data
mixed_csv = ROOT / "archive" / "experiments" / "mixed_source_2026-07-18" / "outputs" / "03_openrouter_outputs_mixed_180.csv"
mixed = pd.read_csv(mixed_csv)
mixed_vce = mixed[mixed["purpose"] == "vce"].copy()
mixed_greedy = mixed[mixed["purpose"] == "greedy"].copy()

# Mixed-source results (as reported in REMEDIATION_SUMMARY.md)
mixed_af_greedy = mixed_greedy[mixed_greedy["region"] == "Africa"]
mixed_eu_greedy = mixed_greedy[mixed_greedy["region"] == "Europe"]
mixed_af_acc = mixed_af_greedy["correct"].mean()
mixed_eu_acc = mixed_eu_greedy["correct"].mean()

mixed_af_wrong = mixed_vce[(mixed_vce["region"] == "Africa") & (mixed_vce["correct"] == 0)]
mixed_eu_wrong = mixed_vce[(mixed_vce["region"] == "Europe") & (mixed_vce["correct"] == 0)]
mixed_af_vce = mixed_af_wrong["vce"].mean() if len(mixed_af_wrong) > 0 else np.nan
mixed_eu_vce = mixed_eu_wrong["vce"].mean() if len(mixed_eu_wrong) > 0 else np.nan

# v18 source-controlled results
v18_af_greedy = greedy[greedy["region"] == "Africa"]
v18_eu_greedy = greedy[greedy["region"] == "Europe"]
v18_af_acc = v18_af_greedy["correct"].mean()
v18_eu_acc = v18_eu_greedy["correct"].mean()

v18_af_wrong = vce[(vce["region"] == "Africa") & (vce["correct"] == 0)]
v18_eu_wrong = vce[(vce["region"] == "Europe") & (vce["correct"] == 0)]
v18_af_vce = v18_af_wrong["vce"].mean()
v18_eu_vce = v18_eu_wrong["vce"].mean()

# Model overlap
v18_models = set(df["model"].unique())
mixed_models = set(mixed["model"].unique())
overlap_models = v18_models & mixed_models

print(f"v18 models: {sorted(v18_models)}")
print(f"mixed models: {sorted(mixed_models)}")
print(f"Overlap: {sorted(overlap_models)}")

print(f"\nMixed-source (source-confounded):")
print(f"  Accuracy: Af={mixed_af_acc:.3f} Eu={mixed_eu_acc:.3f}")
print(f"  Wrong-VCE: Af={mixed_af_vce:.3f} Eu={mixed_eu_vce:.3f} (n_af={len(mixed_af_wrong)}, n_eu={len(mixed_eu_wrong)})")

print(f"\nSource-controlled (v18):")
print(f"  Accuracy: Af={v18_af_acc:.3f} Eu={v18_eu_acc:.3f}")
print(f"  Wrong-VCE: Af={v18_af_vce:.3f} Eu={v18_eu_vce:.3f} (n_af={len(v18_af_wrong)}, n_eu={len(v18_eu_wrong)})")

print(f"\nIMPORTANT: These are BETWEEN-STUDY comparisons, not a within-study causal test.")
print(f"  - Different item sets (completely different 180 items)")
print(f"  - Different model panels (only {len(overlap_models)} overlap: {sorted(overlap_models)})")
print(f"  - Different pipelines (mixed-source had 5 models, v18 has 7)")
print(f"  - Mixed-source Africa items include 10 AfriMMLU items (92 rows)")
print(f"  - Any difference between conditions could reflect item/model differences, not just source mixing")

source_control = {
    "v18_models": sorted(v18_models),
    "mixed_models": sorted(mixed_models),
    "overlap_models": sorted(overlap_models),
    "n_overlap": len(overlap_models),
    "v18_accuracy_africa": float(v18_af_acc),
    "v18_accuracy_europe": float(v18_eu_acc),
    "v18_wrong_vce_africa": float(v18_af_vce),
    "v18_wrong_vce_europe": float(v18_eu_vce),
    "v18_n_wrong_africa": int(len(v18_af_wrong)),
    "v18_n_wrong_europe": int(len(v18_eu_wrong)),
    "mixed_accuracy_africa": float(mixed_af_acc),
    "mixed_accuracy_europe": float(mixed_eu_acc),
    "mixed_wrong_vce_africa": float(mixed_af_vce),
    "mixed_wrong_vce_europe": float(mixed_eu_vce),
    "mixed_n_wrong_africa": int(len(mixed_af_wrong)),
    "mixed_n_wrong_europe": int(len(mixed_eu_wrong)),
}
with open(OUT / "source_control_descriptive.json", "w") as f:
    json.dump(source_control, f, indent=2)

# ============================================================================
# 6. CATEGORY SENSITIVITY (constrained, Tier C)
# ============================================================================
print("\n" + "=" * 72)
print("6. CATEGORY SENSITIVITY")
print("=" * 72)

category_results = []
for cat in sorted(greedy["cat"].unique()):
    sub = greedy[greedy["cat"] == cat]
    if len(sub["region"].unique()) < 2:
        continue
    crosstab = pd.crosstab(sub["region"], sub["correct"])
    if crosstab.shape != (2, 2):
        continue
    chi2, p, _, _ = stats.chi2_contingency(crosstab)
    
    sub_vce = vce[vce["cat"] == cat]
    af_w = sub_vce[(sub_vce["region"] == "Africa") & (sub_vce["correct"] == 0)]
    eu_w = sub_vce[(sub_vce["region"] == "Europe") & (sub_vce["correct"] == 0)]
    if len(af_w) > 1 and len(eu_w) > 1:
        _, p_h3 = stats.mannwhitneyu(af_w["vce"], eu_w["vce"], alternative='two-sided')
    else:
        p_h3 = np.nan
    
    category_results.append({
        "category": cat,
        "n_africa": int((sub["region"] == "Africa").sum()),
        "n_europe": int((sub["region"] == "Europe").sum()),
        "acc_africa": float(sub[sub["region"] == "Africa"]["correct"].mean()),
        "acc_europe": float(sub[sub["region"] == "Europe"]["correct"].mean()),
        "chi2": float(chi2),
        "p_chi2": float(p),
        "h3_n_af_wrong": int(len(af_w)),
        "h3_n_eu_wrong": int(len(eu_w)),
        "h3_p": float(p_h3) if not np.isnan(p_h3) else None,
    })
    print(f"{cat}: n={len(sub)}, chi2={chi2:.3f} p={p:.3f}, H3 p={p_h3:.3f} if valid")

cat_df = pd.DataFrame(category_results)
cat_df.to_csv(OUT / "category_sensitivity.csv", index=False)

# Benjamini-Hochberg correction
pvals = cat_df["p_chi2"].dropna().values
n_tests = len(pvals)
if n_tests > 0:
    from statsmodels.stats.multitest import multipletests
    reject, pvals_corrected, _, _ = multipletests(pvals, alpha=0.05, method='fdr_bh')
    cat_df.loc[cat_df["p_chi2"].notna(), "p_chi2_bh"] = pvals_corrected
    print(f"\nBH-corrected p-values (accuracy):")
    for _, row in cat_df.iterrows():
        if pd.notna(row["p_chi2"]):
            print(f"  {row['category']}: p={row['p_chi2']:.3f} -> p_BH={row['p_chi2_bh']:.3f}")

print("\n" + "=" * 72)
print("ANALYSIS COMPLETE")
print("=" * 72)
print(f"All outputs saved to {OUT}")
