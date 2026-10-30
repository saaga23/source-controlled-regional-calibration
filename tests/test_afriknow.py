"""Test suite for the source-controlled regional calibration repository.

Run: pytest tests/ -q  (or python -m pytest tests/)

Test classes map to the reproducibility requirements:
- TestDatasetIntegrity: counts, balance, duplicates, schema (dataset docs §5)
- TestMetrics: metric implementations against hand-computed fixtures
- TestAgainstRawData: headline published numbers recomputed from the raw CSV
- TestSecrets: no credentials committed
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from afriknow_calib import dataset as ds  # noqa: E402
from afriknow_calib import metrics as M  # noqa: E402

CSV = REPO / "data" / "raw" / "03_openrouter_outputs_v18_correct.csv"
CURATED = REPO / "data" / "curated" / "02_gm_only_180_items.json"


# ---------------------------------------------------------------- dataset ---
class TestDatasetIntegrity:
    def test_curated_file_exists(self):
        assert CURATED.exists(), "curated 180-item JSON missing"

    def test_row_counts_and_balance(self):
        d = ds.load_items(CURATED)
        assert d["n_total"] == 180
        assert d["n_africa"] == 90 and d["n_europe"] == 90
        assert len(d["items"]) == 180

    def test_validation_passes(self):
        d = ds.load_items(CURATED)
        assert ds.validate_items(d) == [], f"validation errors: {ds.validate_items(d)}"

    def test_curated_hash_matches_canonical(self):
        assert ds.sha256_of(CURATED) == ds.CURATED_SHA256, "curated dataset hash changed"

    def test_raw_csv_hash_matches_canonical(self):
        assert ds.sha256_of(CSV) == ds.RAW_SHA256, "raw CSV hash changed"

    def test_region_balance_in_raw(self):
        df = pd.read_csv(CSV)
        assert df["region"].value_counts().to_dict() == {"Africa": 1260, "Europe": 1260}

    def test_flagged_us_history_split(self):
        d = ds.load_items(CURATED)
        us = [i for i in d["items"] if i["cat"] == "high_school_us_history"]
        assert len(us) == 12
        regions = [i["region"] for i in us]
        assert regions.count("Africa") == 6 and regions.count("Europe") == 6


# ---------------------------------------------------------------- metrics ---
class TestMetrics:
    def test_parse_vce_basic(self):
        # fixtures mirror real model outputs (a bare integer, possibly with trailing text)
        assert M.parse_vce("85") == 0.85
        assert M.parse_vce("85\n\nConfidence is high because the training data covers this.") == 0.85
        assert M.parse_vce("0") == 0.0
        assert M.parse_vce("The answer is D. Confidence: 72") == 0.72

    def test_parse_vce_rejects_invalid(self):
        assert M.parse_vce("no numbers here") is None
        assert M.parse_vce("150") is None
        assert M.parse_vce(None) is None

    def test_parse_letter(self):
        assert M.parse_letter("B. Some text") == "B"
        assert M.parse_letter("Answer: d") == "D"  # normalized to uppercase

    def test_accuracy(self):
        assert M.accuracy(np.array(["A", "B", "C"]), np.array(["A", "B", "A"])) == pytest.approx(2 / 3)

    def test_ece_perfect_calibration(self):
        # 100 predictions at confidence 0.8 with exactly 80% correct -> ECE 0 in that bin
        conf = np.full(100, 0.8)
        correct = np.array([1] * 80 + [0] * 20)
        assert M.expected_calibration_error(conf, correct) == pytest.approx(0.0, abs=1e-9)

    def test_ece_overconfidence_fixture(self):
        # hand-computed: 10 preds at 0.9, 4 correct -> |0.4-0.9| * 1 = 0.5
        conf = np.full(10, 0.9)
        correct = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0])
        assert M.expected_calibration_error(conf, correct) == pytest.approx(0.5)

    def test_ece_equal_mass_runs(self):
        rng = np.random.default_rng(0)
        conf = rng.random(500)
        correct = (rng.random(500) < conf).astype(float)
        v = M.expected_calibration_error(conf, correct, n_bins=15, strategy="mass")
        assert 0 <= v <= 1

    def test_brier(self):
        assert M.brier_score(np.array([1.0, 0.0]), np.array([1, 0])) == pytest.approx(0.0)
        assert M.brier_score(np.array([0.5, 0.5]), np.array([1, 0])) == pytest.approx(0.25)

    def test_chr_denominator_is_high_confidence_set(self):
        # 3 high-conf predictions (2 wrong) -> CHR = 2/3; the 1 low-conf wrong answer is excluded
        conf = np.array([0.9, 0.8, 0.7, 0.5])
        correct = np.array([0, 0, 1, 0])
        chr_val, n = M.calibration_hit_rate(conf, correct, tau=0.70)
        assert n == 3
        assert chr_val == pytest.approx(2 / 3)

    def test_cohens_d_sign(self):
        a = np.array([0.9, 0.95, 0.85, 0.92])
        b = np.array([0.5, 0.55, 0.45, 0.52])
        assert M.cohens_d(a, b) > 3  # strongly positive
        assert M.cohens_d(b, a) < -3


# ----------------------------------------------------- against raw data ----
class TestAgainstRawData:
    @pytest.fixture(scope="class")
    def df(self):
        return pd.read_csv(CSV)

    @pytest.fixture(scope="class")
    def split(self, df):
        greedy = df[df["purpose"] == "greedy"]
        vce = df[df["purpose"] == "vce"]
        return greedy, vce

    def test_shape(self, df):
        assert len(df) == 2520
        assert df["model"].nunique() == 7

    def test_h1_accuracy(self, split):
        greedy, _ = split
        af = greedy[greedy["region"] == "Africa"]
        eu = greedy[greedy["region"] == "Europe"]
        assert (af["correct"].sum(), len(af)) == (551, 630)
        assert (eu["correct"].sum(), len(eu)) == (539, 630)
        assert M.accuracy(af["pred"], af["correct_letter"]) == pytest.approx(551 / 630)

    def test_h3_wrong_answer_vce(self, split):
        _, vce = split
        waf = vce[(vce["region"] == "Africa") & (vce["correct"] == 0)]["vce"]
        weu = vce[(vce["region"] == "Europe") & (vce["correct"] == 0)]["vce"]
        assert len(waf) == 79 and len(weu) == 91
        assert waf.mean() == pytest.approx(0.761, abs=0.0005)
        assert weu.mean() == pytest.approx(0.832, abs=0.0005)
        d = M.cohens_d(waf.values, weu.values)
        assert d == pytest.approx(-0.317, abs=0.01)

    def test_chr(self, split):
        _, vce = split
        af = vce[vce["region"] == "Africa"]
        eu = vce[vce["region"] == "Europe"]
        chr_af, n_af = M.calibration_hit_rate(af["vce"], af["correct"], tau=0.70)
        chr_eu, n_eu = M.calibration_hit_rate(eu["vce"], eu["correct"], tau=0.70)
        assert n_af == 601 and n_eu == 609
        assert chr_af == pytest.approx(0.105, abs=0.0005)
        assert chr_eu == pytest.approx(0.136, abs=0.0005)
        assert chr_af / chr_eu == pytest.approx(0.769, abs=0.001)

    def test_pooled_calibration(self, split):
        _, vce = split
        v = vce.dropna(subset=["vce"])
        assert M.expected_calibration_error(v["vce"], v["correct"]) == pytest.approx(0.048, abs=0.0005)
        assert M.brier_score(v["vce"], v["correct"]) == pytest.approx(0.114, abs=0.0005)
        from sklearn.metrics import roc_auc_score

        assert roc_auc_score(v["correct"], v["vce"]) == pytest.approx(0.679, abs=0.0005)

    def test_run_quality(self, df):
        assert df["cost_usd"].sum() == pytest.approx(0.6556, abs=0.0001)
        assert df["input_tokens"].sum() + df["output_tokens"].sum() == 4_448_016
        assert df["vce"].notna().sum() == 1260

    def test_permutation_results_frozen(self):
        import json

        p = REPO / "results" / "reports" / "permutation_audit_results.json"
        if not p.exists():
            pytest.skip("permutation rerun output not present")
        r = json.loads(p.read_text())
        assert r["corrected_p_perm_chi2"] == pytest.approx(0.677, abs=0.005)
        assert r["corrected_p_perm_u"] == pytest.approx(0.726, abs=0.005)
        assert r["seed"] == 20260622 and r["n_perm"] == 10000


# ---------------------------------------------------------------- secrets ---
class TestSecrets:
    def test_no_env_file(self):
        assert not (REPO / ".env").exists(), "remove .env before publishing"

    def test_no_key_patterns_in_repo_files(self):
        import re

        # realistic secret shapes, not bare substrings ( scanners legitimately name patterns )
        shapes = [
            re.compile(r"sk-[A-Za-z0-9]{20,}"),        # OpenAI-style key
            re.compile(r"ghp_[A-Za-z0-9]{30,}"),        # GitHub PAT
            re.compile(r"AKIA[A-Z0-9]{16}"),            # AWS access key
            re.compile(r"OPENROUTER_API_KEY\s*=\s*\S+"),  # assigned value (not .env.example)
        ]
        for p in REPO.rglob("*"):
            if p.is_file() and p.suffix in {".py", ".md", ".json", ".csv", ".yaml", ".txt", ".cff"}:
                text = p.read_text(errors="ignore")
                for rx in shapes:
                    if p.name == ".env.example" and rx.pattern.startswith("OPENROUTER"):
                        continue
                    if rx.search(text):
                        pytest.fail(f"possible secret pattern {rx.pattern!r} in {p}")
