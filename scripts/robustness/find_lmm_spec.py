"""Find the exact confidence-LMM specification that reproduces the paper's numbers.

Paper claims: Intercept 2.342, region[Europe] +0.152, Gemma +4.049,
Llama +2.728, qid Var 1.297.

We sweep candidate clip bounds and REML/ML to locate the spec (if any) that
reproduces those coefficients. Read-only.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "raw" / "03_openrouter_outputs_v18_correct.csv"

df = pd.read_csv(CSV)
vce = df[df["purpose"] == "vce"].dropna(subset=["vce"]).copy()
vce["region"] = pd.Categorical(vce["region"], categories=["Africa", "Europe"])
vce["model"] = pd.Categorical(
    vce["model"],
    categories=["claude-sonnet-4.6", "deepseek-v3.2", "gemini-2.5-flash-lite",
                "gemma-4-31b", "gpt-4o-mini", "gpt41-nano", "llama-3.3-70b"],
)

PAPER = {"Intercept": 2.342, "region[T.Europe]": 0.152,
         "model[T.gemma-4-31b]": 4.049, "model[T.llama-3.3-70b]": 2.728,
         "qidVar": 1.297}


def fit(clip_lo, clip_hi, reml):
    d = vce.copy()
    c = d["vce"].clip(clip_lo, clip_hi)
    d["logit_c"] = np.log(c / (1 - c))
    md = smf.mixedlm("logit_c ~ region + model", d, groups=d["qid"])
    try:
        m = md.fit(reml=reml, method="lbfgs", maxiter=3000)
    except Exception:
        return None
    return {
        "Intercept": m.params.get("Intercept", np.nan),
        "region[T.Europe]": m.params.get("region[T.Europe]", np.nan),
        "model[T.gemma-4-31b]": m.params.get("model[T.gemma-4-31b]", np.nan),
        "model[T.llama-3.3-70b]": m.params.get("model[T.llama-3.3-70b]", np.nan),
        "qidVar": float(m.cov_re.iloc[0, 0]),
    }


def score(got):
    if got is None:
        return 1e9
    return sum(abs(got[k] - PAPER[k]) for k in PAPER)


print(f"{'clip':>14s} {'reml':>5s}  {'Interc':>7s} {'regEu':>6s} "
      f"{'Gemma':>6s} {'Llama':>6s} {'qidVar':>6s}  {'dist':>7s}")
candidates = []
for lo, hi in [(0.005, 0.995), (0.01, 0.99), (0.02, 0.98), (0.025, 0.975),
               (0.001, 0.999), (1e-4, 1 - 1e-4), (1e-6, 1 - 1e-6)]:
    for reml in (True, False):
        got = fit(lo, hi, reml)
        s = score(got)
        candidates.append(((lo, hi, reml), got, s))
        if got:
            print(f"[{lo:.3f},{hi:.3f}] {str(reml):>5s}  "
                  f"{got['Intercept']:7.3f} {got['region[T.Europe]']:6.3f} "
                  f"{got['model[T.gemma-4-31b]']:6.3f} {got['model[T.llama-3.3-70b]']:6.3f} "
                  f"{got['qidVar']:6.3f}  {s:7.3f}")

best = min(candidates, key=lambda x: x[2])
print("\nBEST SPEC:", best[0], "dist=", round(best[2], 4))
print("PAPER    :", PAPER)
print("BEST GOT :", {k: round(v, 3) for k, v in best[1].items()})
