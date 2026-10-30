"""Reproducible verification of the paper's confidence LMM and Table 2 ECE/Brier/AUROC.

Ground truth: data/raw/03_openrouter_outputs_v18_correct.csv
(byte-identical to Kaggle dataset abrahamsunday123/afriknow-v18-inputs).

Read-only. Prints paper-claimed vs data-computed side by side and writes
evidence CSVs to evidence/. This is the SAME code pushed to the Kaggle kernel
so the cloud run and local run agree.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "raw" / "03_openrouter_outputs_v18_correct.csv"
EVID = ROOT / "results" / "reports"
EVID.mkdir(parents=True, exist_ok=True)

# Model display keys used in the paper (Table 2 / Table 4 order)
MODEL_KEY = {
    "claude-sonnet-4.6": "Claude",
    "deepseek-v3.2": "DeepSeek",
    "gemini-2.5-flash-lite": "Gemini",
    "gemma-4-31b": "Gemma",
    "gpt-4o-mini": "GPT-4o",
    "gpt41-nano": "GPT-4.1n",
    "llama-3.3-70b": "Llama",
}

df = pd.read_csv(CSV)
greedy = df[df["purpose"] == "greedy"].copy()
vce = df[df["purpose"] == "vce"].copy()

print("=" * 72)
print("DATA SHAPE")
print("=" * 72)
print(f"rows={len(df)} greedy={len(greedy)} vce={len(vce)} "
      f"vce_nonnull={vce['vce'].notna().sum()}")


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


# ---------------------------------------------------------------------------
# TABLE 2: ECE (Af / Eu / all), Brier, AUROC per model
# ---------------------------------------------------------------------------
print("\n" + "=" * 72)
print("TABLE 2  VCE calibration per model  (ECE 10 equal-width bins)")
print("=" * 72)
PAPER_TAB2 = {
    # key: (ECE_Af, ECE_Eu, ECE_all, Brier, AUROC)
    "Claude":   (0.086, 0.059, 0.064, 0.065, 0.841),
    "DeepSeek": (0.082, 0.030, 0.053, 0.081, 0.757),
    "Gemini":   (0.090, 0.101, 0.093, 0.112, 0.674),
    "Gemma":    (0.132, 0.139, 0.136, 0.135, 0.594),
    "GPT-4o":   (0.037, 0.079, 0.054, 0.120, 0.732),
    "GPT-4.1n": (0.051, 0.123, 0.086, 0.173, 0.610),
    "Llama":    (0.063, 0.102, 0.082, 0.113, 0.710),
}
tab2_rows = []
hdr = f"{'Model':9s} {'ECE_Af':>7s} {'ECE_Eu':>7s} {'ECE_all':>7s} {'Brier':>7s} {'AUROC':>7s}   vs PAPER"
print(hdr)
for raw, key in MODEL_KEY.items():
    sub = vce[vce["model"] == raw]
    af = sub[sub["region"] == "Africa"]
    eu = sub[sub["region"] == "Europe"]
    ece_af = compute_ece(af["vce"], af["correct"])
    ece_eu = compute_ece(eu["vce"], eu["correct"])
    ece_all = compute_ece(sub["vce"], sub["correct"])
    br = brier(sub["vce"], sub["correct"])
    au = roc_auc_score(sub["correct"], sub["vce"])
    p = PAPER_TAB2[key]
    flag = ""
    got = (round(ece_af, 3), round(ece_eu, 3), round(ece_all, 3), round(br, 3), round(au, 3))
    for g, pv in zip(got, p):
        if abs(g - pv) > 0.001:
            flag = "  <-- MISMATCH"
            break
    print(f"{key:9s} {ece_af:7.3f} {ece_eu:7.3f} {ece_all:7.3f} {br:7.3f} {au:7.3f}"
          f"   paper={p}{flag}")
    tab2_rows.append({
        "model": key, "ece_af": ece_af, "ece_eu": ece_eu, "ece_all": ece_all,
        "brier": br, "auroc": au,
        "paper_ece_af": p[0], "paper_ece_eu": p[1], "paper_ece_all": p[2],
        "paper_brier": p[3], "paper_auroc": p[4],
    })
pd.DataFrame(tab2_rows).to_csv(EVID / "table2_ece_verified.csv", index=False)

# pooled
v = vce.dropna(subset=["vce"])
pooled_ece = compute_ece(v["vce"], v["correct"])
pooled_brier = brier(v["vce"], v["correct"])
pooled_auroc = roc_auc_score(v["correct"], v["vce"])
print(f"\nPOOLED  ECE={pooled_ece:.4f} (paper 0.048)  "
      f"Brier={pooled_brier:.4f} (paper 0.114)  "
      f"AUROC={pooled_auroc:.4f} (paper 0.679)")
avg_percel = np.mean([r["ece_all"] for r in tab2_rows])
print(f"avg of per-model ECE = {avg_percel:.4f} (paper 0.081)")

# ---------------------------------------------------------------------------
# CONFIDENCE LMM: logit(C) ~ region + model + (1|qid)
# ---------------------------------------------------------------------------
print("\n" + "=" * 72)
print("CONFIDENCE LMM  logit(C) ~ region + model + (1|qid)")
print("=" * 72)
lmm = v.copy()
# Paper spec (exact reproduction): clip epsilon = 0.001, REML fit.
# Verified 2026-07-18: reproduces Intercept 2.342, region[Europe] +0.152,
# Gemma +4.049, Llama +2.728, qid Var 1.297 to 3 decimals.
c = lmm["vce"].clip(0.001, 0.999)
lmm["logit_c"] = np.log(c / (1 - c))
lmm["region"] = pd.Categorical(lmm["region"], categories=["Africa", "Europe"])
lmm["model"] = pd.Categorical(
    lmm["model"],
    categories=["claude-sonnet-4.6", "deepseek-v3.2", "gemini-2.5-flash-lite",
                "gemma-4-31b", "gpt-4o-mini", "gpt41-nano", "llama-3.3-70b"],
)
md = smf.mixedlm("logit_c ~ region + model", lmm, groups=lmm["qid"])
mf = md.fit(reml=True, method="cg", maxiter=5000)
print(mf.summary())
conf_rows = []
for name in mf.params.index:
    conf_rows.append({
        "term": name, "coef": mf.params[name],
        "se": mf.bse.get(name, np.nan), "p": mf.pvalues.get(name, np.nan),
    })
conf_rows.append({"term": "qid Var", "coef": float(mf.cov_re.iloc[0, 0]),
                  "se": np.nan, "p": np.nan})
pd.DataFrame(conf_rows).to_csv(EVID / "confidence_lmm_verified.csv", index=False)

PAPER_LMM = {
    "Intercept": 2.342, "region[T.Europe]": 0.152,
    "model[T.gemma-4-31b]": 4.049, "model[T.llama-3.3-70b]": 2.728,
    "qid Var": 1.297,
}
print("\nPAPER vs COMPUTED (confidence LMM):")
for term, pv in PAPER_LMM.items():
    if term == "qid Var":
        got = float(mf.cov_re.iloc[0, 0])
    else:
        got = mf.params.get(term, np.nan)
    flag = "" if abs(got - pv) <= 0.01 else "  <-- MISMATCH"
    print(f"  {term:24s} paper={pv:+.3f}  computed={got:+.3f}{flag}")

# ---------------------------------------------------------------------------
# ACCURACY marginal logit with cluster-robust SE
# ---------------------------------------------------------------------------
print("\n" + "=" * 72)
print("ACCURACY  logit  correct ~ region + model  (cluster SE by qid)")
print("=" * 72)
acc = greedy.copy()
acc["region"] = pd.Categorical(acc["region"], categories=["Africa", "Europe"])
acc["model"] = pd.Categorical(
    acc["model"],
    categories=["claude-sonnet-4.6", "deepseek-v3.2", "gemini-2.5-flash-lite",
                "gemma-4-31b", "gpt-4o-mini", "gpt41-nano", "llama-3.3-70b"],
)
ma = smf.glm("correct ~ region + model", acc, family=sm.families.Binomial()).fit(
    cov_type="cluster", cov_kwds={"groups": acc["qid"]})
print(ma.summary())

result = {
    "pooled_ece": pooled_ece, "pooled_brier": pooled_brier,
    "pooled_auroc": pooled_auroc, "avg_per_model_ece": avg_percel,
    "n_vce": int(len(v)), "n_greedy": int(len(greedy)),
}
(EVID / "summary.json").write_text(json.dumps(result, indent=2))
print("\nEvidence written to", EVID)
