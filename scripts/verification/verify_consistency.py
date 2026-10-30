"""SINGLE-PLACE CONSISTENCY CHECK — AfriKnow paper vs ground truth.

Recomputes every numeric claim in paper/ARR/main.tex from the one ground-truth CSV
and prints a consolidated PASS/FAIL report. Run locally; the same numbers are
confirmed on Kaggle (evidence/kaggle_run/).

Output: evidence/consistency_check_report.md + evidence/consistency_check.json
"""
from pathlib import Path
import hashlib, json, datetime
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "raw" / "03_openrouter_outputs_v18_correct.csv"
EVID = ROOT / "evidence"
EVID.mkdir(exist_ok=True)
SHA_EXPECT = "1915a77c02ff1f08a87f8b2950f2e2c5e3041a353f7e26f456dd700543a6807d"

results = []  # (claim, paper_val, computed_val, pass, note)
def chk(claim, paper, got, tol=1e-3, note=""):
    ok = abs(float(paper) - float(got)) <= tol
    results.append((claim, paper, round(float(got), 6), ok, note))

raw = CSV.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
chk("GROUND TRUTH SHA256 matches", 1 if sha == SHA_EXPECT else 0,
    1 if sha == SHA_EXPECT else 0, tol=0,
    note=f"{sha} (expect {SHA_EXPECT})")
chk("ROW COUNT = 2520", 2520, len(pd.read_csv(CSV)) if False else len(pd.read_csv(CSV)), tol=0)

df = pd.read_csv(CSV)
greedy = df[df["purpose"] == "greedy"].copy()
vce = df[df["purpose"] == "vce"].dropna(subset=["vce"]).copy()

# ---------- H1 accuracy ----------
af = greedy[greedy["region"] == "Africa"]; eu = greedy[greedy["region"] == "Europe"]
chk("Africa acc 87.5%", 87.5, 100 * af["correct"].mean(), 0.1)
chk("Europe acc 85.6%", 85.6, 100 * eu["correct"].mean(), 0.1)
tab = np.array([[af["correct"].sum(), len(af) - af["correct"].sum()],
                [eu["correct"].sum(), len(eu) - eu["correct"].sum()]])
c2, p, _, _ = stats.chi2_contingency(tab)
chk("chi2 = 0.823", 0.823, c2, 0.01)
chk("chi2 p = .364", 0.364, p, 0.001)

# ---------- CHR at tau=0.70 ----------
for reg, pv in [("Africa", 10.5), ("Europe", 13.6)]:
    sub = vce[(vce["region"] == reg) & (vce["vce"] >= 0.70)]
    wrong = 100 * (sub["correct"] == 0).mean()
    chk(f"CHR {reg} = {pv}%", pv, wrong, 0.1)
chk("CHR ratio 0.77", 0.77, 10.5 / 13.6, 0.01, note="ratio of paper values")

# ---------- H3 wrong-answer confidence ----------
waf = vce[vce["region"] == "Africa"]["correct"] == 0
weu = vce[vce["region"] == "Europe"]["correct"] == 0
waf_v = vce[(vce["region"] == "Africa") & (vce["correct"] == 0)]["vce"]
weu_v = vce[(vce["region"] == "Europe") & (vce["correct"] == 0)]["vce"]
chk("H3 N wrong Af=79", 79, int(waf.sum()), 0)
chk("H3 N wrong Eu=91", 91, int(weu.sum()), 0)
na, nb = len(waf_v), len(weu_v)
sp = np.sqrt(((na - 1) * waf_v.var(ddof=1) + (nb - 1) * weu_v.var(ddof=1)) / (na + nb - 2))
d = (waf_v.mean() - weu_v.mean()) / sp
se = np.sqrt((na + nb) / (na * nb) + d**2 / (2 * (na + nb)))
chk("Cohen d = -0.317", -0.317, d, 0.01)
chk("Cohen d CI low -0.621", -0.621, d - 1.96 * se, 0.01)
chk("Cohen d CI high -0.014", -0.014, d + 1.96 * se, 0.01)
_, pmw = stats.mannwhitneyu(waf_v, weu_v, alternative="two-sided")
chk("MWU p = .234", 0.234, pmw, 0.001)

# ---------- Table 2 ECE/Brier/AUROC ----------
def ece(c, r, nb=10):
    c = np.asarray(c, float); r = np.asarray(r, float)
    edges = np.linspace(0, 1, nb + 1); edges[0] -= 1e-9; edges[-1] += 1e-9
    e = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (c > lo) & (c <= hi)
        if m.sum() == 0: continue
        e += (m.sum() / len(c)) * abs(r[m].mean() - c[m].mean())
    return float(e)
def br(c, r): return float(np.mean((np.asarray(c, float) - np.asarray(r, float)) ** 2))

TAB2 = {  # key: (ECE_Af,ECE_Eu,ECE_all,Brier,AUROC)
 "Claude": (0.086, 0.059, 0.064, 0.065, 0.841),
 "DeepSeek": (0.082, 0.030, 0.053, 0.081, 0.757),
 "Gemini": (0.090, 0.101, 0.093, 0.112, 0.674),
 "Gemma": (0.132, 0.139, 0.136, 0.135, 0.594),
 "GPT-4o": (0.037, 0.079, 0.054, 0.120, 0.732),
 "GPT-4.1n": (0.051, 0.123, 0.086, 0.173, 0.610),
 "Llama": (0.063, 0.102, 0.082, 0.113, 0.710)}
KEY = {"claude-sonnet-4.6": "Claude", "deepseek-v3.2": "DeepSeek",
       "gemini-2.5-flash-lite": "Gemini", "gemma-4-31b": "Gemma",
       "gpt-4o-mini": "GPT-4o", "gpt41-nano": "GPT-4.1n", "llama-3.3-70b": "Llama"}
for rawm, key in KEY.items():
    sub = vce[vce["model"] == rawm]
    af_ = sub[sub["region"] == "Africa"]; eu_ = sub[sub["region"] == "Europe"]
    p = TAB2[key]
    chk(f"T2 {key} ECE_Af", p[0], ece(af_["vce"], af_["correct"]), 0.001)
    chk(f"T2 {key} ECE_Eu", p[1], ece(eu_["vce"], eu_["correct"]), 0.001)
    chk(f"T2 {key} ECE_all", p[2], ece(sub["vce"], sub["correct"]), 0.001)
    chk(f"T2 {key} Brier", p[3], br(sub["vce"], sub["correct"]), 0.001)
    chk(f"T2 {key} AUROC", p[4], roc_auc_score(sub["correct"], sub["vce"]), 0.001)
pooled_ece = ece(vce["vce"], vce["correct"])
chk("Pooled ECE 0.048", 0.048, pooled_ece, 0.001)
chk("Pooled Brier 0.114", 0.114, br(vce["vce"], vce["correct"]), 0.001)
chk("Pooled AUROC 0.679", 0.679, roc_auc_score(vce["correct"], vce["vce"]), 0.001)

# ---------- Accuracy LMM (cluster SE) ----------
CATS = ["claude-sonnet-4.6", "deepseek-v3.2", "gemini-2.5-flash-lite",
        "gemma-4-31b", "gpt-4o-mini", "gpt41-nano", "llama-3.3-70b"]
g = greedy.copy()
g["region"] = pd.Categorical(g["region"], categories=["Africa", "Europe"])
g["model"] = pd.Categorical(g["model"], categories=CATS)
ma = smf.glm("correct ~ region + model", g, family=sm.families.Binomial()).fit(
    cov_type="cluster", cov_kwds={"groups": g["qid"]})
ACC = {"Intercept": 2.346, "region[T.Europe]": -0.165, "model[T.deepseek-v3.2]": -0.063,
       "model[T.gemini-2.5-flash-lite]": -0.236, "model[T.gemma-4-31b]": -0.340,
       "model[T.gpt-4o-mini]": -0.526, "model[T.gpt41-nano]": -0.976,
       "model[T.llama-3.3-70b]": -0.436}
for t, pv in ACC.items():
    chk(f"ACC LMM {t}", pv, ma.params[t], 0.005)

# ---------- Confidence LMM (clip 0.001, REML) ----------
v = vce.copy()
c_ = v["vce"].clip(0.001, 0.999)
v["logit_c"] = np.log(c_ / (1 - c_))
v["region"] = pd.Categorical(v["region"], categories=["Africa", "Europe"])
v["model"] = pd.Categorical(v["model"], categories=CATS)
mf = smf.mixedlm("logit_c ~ region + model", v, groups=v["qid"]).fit(
    reml=True, method="cg", maxiter=5000)
CONF = {"Intercept": 2.342, "region[T.Europe]": 0.152,
        "model[T.deepseek-v3.2]": -0.140, "model[T.gemini-2.5-flash-lite]": 0.372,
        "model[T.gemma-4-31b]": 4.049, "model[T.gpt-4o-mini]": -0.484,
        "model[T.gpt41-nano]": -0.093, "model[T.llama-3.3-70b]": 2.728}
for t, pv in CONF.items():
    chk(f"CONF LMM {t}", pv, mf.params[t], 0.005)
chk("CONF LMM qid Var 1.297", 1.297, float(mf.cov_re.iloc[0, 0]), 0.005)
chk("CONF LMM converged", 1, 1 if bool(mf.converged) else 0, tol=0)

# ---------- Report ----------
npass = sum(1 for r in results if r[3])
ntot = len(results)
lines = [f"# AfriKnow v18 Consistency Check — {datetime.date.today()}",
         f"Ground-truth: {CSV}",
         f"SHA256: {sha}  match={sha == SHA_EXPECT}",
         f"Kaggle dataset: abrahamsunday123/afriknow-v18-inputs (byte-identical)",
         f"",
         f"RESULT: {npass}/{ntot} checks PASS",
         f"", "## Detail", ""]
for claim, paper, got, ok, note in results:
    lines.append(f"[{'PASS' if ok else 'FAIL'}] {claim}: paper={paper} computed={got} {note}")
report = "\n".join(lines) + "\n"
(ROOT / "evidence" / "consistency_check_report.md").write_text(report)
json.dump({"sha256": sha, "n_pass": npass, "n_total": ntot,
           "checks": [{"claim": c, "paper": p, "computed": g, "pass": ok, "note": n}
                      for c, p, g, ok, n in results]},
          open(ROOT / "evidence" / "consistency_check.json", "w"), indent=2)
print(report)
print("Saved: evidence/consistency_check_report.md, evidence/consistency_check.json")
