"""Verify EVERY cell of paper Table 4 (mixed-effects) against verified specs.

Accuracy: marginal logit, cluster SE by qid.
Confidence: logit(clip 0.001) LMM, REML, cg.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "raw" / "03_openrouter_outputs_v18_correct.csv"
df = pd.read_csv(CSV)

cats = ["claude-sonnet-4.6", "deepseek-v3.2", "gemini-2.5-flash-lite",
        "gemma-4-31b", "gpt-4o-mini", "gpt41-nano", "llama-3.3-70b"]
KEY = {"deepseek-v3.2": "DeepSeek", "gemini-2.5-flash-lite": "Gemini",
       "gemma-4-31b": "Gemma", "gpt-4o-mini": "GPT-4o", "gpt41-nano": "GPT-4.1n",
       "llama-3.3-70b": "Llama"}

# ---- Accuracy ----
g = df[df["purpose"] == "greedy"].copy()
g["region"] = pd.Categorical(g["region"], categories=["Africa", "Europe"])
g["model"] = pd.Categorical(g["model"], categories=cats)
ma = smf.glm("correct ~ region + model", g, family=sm.families.Binomial()).fit(
    cov_type="cluster", cov_kwds={"groups": g["qid"]})

PAPER_ACC = {
    "Intercept": (2.346, 0.321, 7.30), "region[T.Europe]": (-0.165, 0.360, -0.46),
    "model[T.deepseek-v3.2]": (-0.063, 0.211, -0.30),
    "model[T.gemini-2.5-flash-lite]": (-0.236, 0.238, -0.99),
    "model[T.gemma-4-31b]": (-0.340, 0.228, -1.49),
    "model[T.gpt-4o-mini]": (-0.526, 0.224, -2.35),
    "model[T.gpt41-nano]": (-0.976, 0.260, -3.76),
    "model[T.llama-3.3-70b]": (-0.436, 0.232, -1.88),
}
print("=== ACCURACY LMM (paper vs computed: coef, se, z) ===")
for t, (pc, ps, pz) in PAPER_ACC.items():
    c, s, z = ma.params[t], ma.bse[t], ma.tvalues[t]
    fl = "" if abs(c - pc) < 0.005 and abs(s - ps) < 0.005 and abs(z - pz) < 0.05 else "  <-- MISMATCH"
    print(f"  {t:32s} paper=({pc:+.3f},{ps:.3f},{pz:+.2f}) got=({c:+.3f},{s:.3f},{z:+.2f}){fl}")

# ---- Confidence ----
v = df[df["purpose"] == "vce"].dropna(subset=["vce"]).copy()
c_ = v["vce"].clip(0.001, 0.999)
v["logit_c"] = np.log(c_ / (1 - c_))
v["region"] = pd.Categorical(v["region"], categories=["Africa", "Europe"])
v["model"] = pd.Categorical(v["model"], categories=cats)
mf = smf.mixedlm("logit_c ~ region + model", v, groups=v["qid"]).fit(
    reml=True, method="cg", maxiter=5000)

PAPER_CONF = {
    "Intercept": (2.342, 0.166, 14.07), "region[T.Europe]": (0.152, 0.188, 0.81),
    "model[T.deepseek-v3.2]": (-0.140, 0.153, -0.91),
    "model[T.gemini-2.5-flash-lite]": (0.372, 0.153, 2.44),
    "model[T.gemma-4-31b]": (4.049, 0.153, 26.53),
    "model[T.gpt-4o-mini]": (-0.484, 0.153, -3.17),
    "model[T.gpt41-nano]": (-0.093, 0.153, -0.61),
    "model[T.llama-3.3-70b]": (2.728, 0.153, 17.88),
}
print("\n=== CONFIDENCE LMM (paper vs computed: coef, se, z) ===")
for t, (pc, ps, pz) in PAPER_CONF.items():
    c, s, z = mf.params[t], mf.bse[t], mf.tvalues[t]
    fl = "" if abs(c - pc) < 0.005 and abs(s - ps) < 0.005 and abs(z - pz) < 0.05 else "  <-- MISMATCH"
    print(f"  {t:32s} paper=({pc:+.3f},{ps:.3f},{pz:+.2f}) got=({c:+.3f},{s:.3f},{z:+.2f}){fl}")
print(f"  qid Var                          paper=1.297  got={float(mf.cov_re.iloc[0,0]):.3f}")
