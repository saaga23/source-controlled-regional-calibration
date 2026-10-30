#!/usr/bin/env python3
"""
Corrected permutation test for AfriKnow.
Permutes region labels at the qid level (keeping all 7 model observations together).
"""
import pandas as pd
import numpy as np
from scipy import stats
import json

np.random.seed(20260622)
N_PERM = 10000

# Portable root resolution (refactored from a hardcoded machine path; logic unchanged)
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "raw" / "03_openrouter_outputs_v18_correct.csv"
OUT = ROOT / "results" / "reports"

df = pd.read_csv(CSV)
greedy = df[df["purpose"] == "greedy"].copy()
vce = df[df["purpose"] == "vce"].copy()

# Observed statistics
obs_chi2, _, _, _ = stats.chi2_contingency(pd.crosstab(greedy["region"], greedy["correct"]))
af_wrong = vce[(vce["region"] == "Africa") & (vce["correct"] == 0)]["vce"].values
eu_wrong = vce[(vce["region"] == "Europe") & (vce["correct"] == 0)]["vce"].values
obs_u, _ = stats.mannwhitneyu(af_wrong, eu_wrong, alternative='two-sided')

print(f"Observed chi2: {obs_chi2:.4f}")
print(f"Observed U: {obs_u:.1f}")

# Build qid-level structures
qid_region = greedy.groupby("qid")["region"].first().reset_index()
qids = qid_region["qid"].values
regions = qid_region["region"].values
n_qids = len(qids)

# Pre-build arrays for greedy and vce
greedy_qid = greedy["qid"].values
greedy_correct = greedy["correct"].values
vce_qid = vce["qid"].values
vce_correct = vce["correct"].values
vce_vce = vce["vce"].values

# Maps for fast lookup
qid_to_idx = {qid: i for i, qid in enumerate(qids)}

perm_chi2 = np.zeros(N_PERM)
perm_u = np.zeros(N_PERM)

for i in range(N_PERM):
    perm_regions = np.random.permutation(regions)
    
    # H1: accuracy chi2
    g_perm_regions = perm_regions[[qid_to_idx[q] for q in greedy_qid]]
    af_mask = g_perm_regions == "Africa"
    eu_mask = g_perm_regions == "Europe"
    af_acc = greedy_correct[af_mask].sum()
    af_n = af_mask.sum()
    eu_acc = greedy_correct[eu_mask].sum()
    eu_n = eu_mask.sum()
    # Build 2x2 table: rows=region, cols=correct (0/1)
    table = np.array([[af_n - af_acc, af_acc], [eu_n - eu_acc, eu_acc]])
    chi2_perm, _, _, _ = stats.chi2_contingency(table)
    perm_chi2[i] = chi2_perm
    
    # H3: wrong-answer MWU
    v_perm_regions = perm_regions[[qid_to_idx[q] for q in vce_qid]]
    af_p_mask = (v_perm_regions == "Africa") & (vce_correct == 0)
    eu_p_mask = (v_perm_regions == "Europe") & (vce_correct == 0)
    af_p = vce_vce[af_p_mask]
    eu_p = vce_vce[eu_p_mask]
    if len(af_p) > 0 and len(eu_p) > 0:
        u_perm, _ = stats.mannwhitneyu(af_p, eu_p, alternative='two-sided')
    else:
        u_perm = 0
    perm_u[i] = u_perm

p_perm_chi2 = (np.sum(perm_chi2 >= obs_chi2) + 1) / (N_PERM + 1)
p_perm_u = (np.sum(perm_u >= obs_u) + 1) / (N_PERM + 1)

print(f"\nCORRECTED qid-level permutation:")
print(f"H1 p_perm: {p_perm_chi2:.4f}")
print(f"H3 p_perm: {p_perm_u:.4f}")

# Also compute WRONG current implementation for comparison
perm_chi2_wrong = np.zeros(N_PERM)
perm_u_wrong = np.zeros(N_PERM)
for i in range(N_PERM):
    g_perm = greedy.copy()
    g_perm["region"] = np.random.permutation(g_perm["region"].values)
    crosstab_perm = pd.crosstab(g_perm["region"], g_perm["correct"])
    chi2_perm, _, _, _ = stats.chi2_contingency(crosstab_perm)
    perm_chi2_wrong[i] = chi2_perm
    
    v_perm = vce.copy()
    v_perm["region"] = np.random.permutation(v_perm["region"].values)
    af_p = v_perm[(v_perm["region"] == "Africa") & (v_perm["correct"] == 0)]["vce"]
    eu_p = v_perm[(v_perm["region"] == "Europe") & (v_perm["correct"] == 0)]["vce"]
    if len(af_p) > 0 and len(eu_p) > 0:
        u_perm, _ = stats.mannwhitneyu(af_p, eu_p, alternative='two-sided')
    else:
        u_perm = 0
    perm_u_wrong[i] = u_perm

p_perm_chi2_wrong = (np.sum(perm_chi2_wrong >= obs_chi2) + 1) / (N_PERM + 1)
p_perm_u_wrong = (np.sum(perm_u_wrong >= obs_u) + 1) / (N_PERM + 1)

print(f"\nWRONG current implementation (row-level permutation):")
print(f"H1 p_perm: {p_perm_chi2_wrong:.4f}")
print(f"H3 p_perm: {p_perm_u_wrong:.4f}")

# Save results
results = {
    "observed_chi2": float(obs_chi2),
    "observed_u": float(obs_u),
    "corrected_p_perm_chi2": float(p_perm_chi2),
    "corrected_p_perm_u": float(p_perm_u),
    "wrong_p_perm_chi2": float(p_perm_chi2_wrong),
    "wrong_p_perm_u": float(p_perm_u_wrong),
    "n_perm": N_PERM,
    "seed": 20260622,
    "permutation_unit": "qid",
    "n_qids": int(n_qids),
    "n_africa_qids": int((regions == "Africa").sum()),
    "n_europe_qids": int((regions == "Europe").sum()),
}
with open(f"{OUT}/permutation_audit_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to {OUT}/permutation_audit_results.json")
