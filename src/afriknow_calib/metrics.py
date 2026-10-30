"""Metric implementations for the source-controlled calibration audit.

Reference implementations used by the test suite. The paper's published
numbers were produced by scripts/verification/verify_v18_lmm_ece.py; this
module mirrors those definitions so tests can assert against the raw data.
"""
from __future__ import annotations

import re
from typing import Optional

import numpy as np


def parse_vce(text: str) -> Optional[float]:
    """Parse a verbalized confidence as the first 0-100 integer -> probability in [0,1].

    Mirrors the runner's regex: first integer in the text; must be in 0..100.
    Returns None when no valid integer is found (parse failure).
    """
    if text is None:
        return None
    m = re.search(r"\d+", str(text))
    if not m:
        return None
    val = int(m.group())
    if not (0 <= val <= 100):
        return None
    return val / 100.0


def parse_letter(text: str) -> Optional[str]:
    """Parse the predicted option letter: first A-D (case-insensitive) in the text."""
    if text is None:
        return None
    m = re.search(r"\b([A-Da-d])\b", str(text).strip())
    return m.group(1).upper() if m else None


def accuracy(pred: np.ndarray, gold: np.ndarray) -> float:
    """Share of predictions equal to gold."""
    pred = np.asarray(pred)
    gold = np.asarray(gold)
    if len(pred) == 0:
        raise ValueError("empty input")
    return float(np.mean(pred == gold))


def expected_calibration_error(conf: np.ndarray, correct: np.ndarray, n_bins: int = 10, strategy: str = "width") -> float:
    """ECE with equal-width or equal-mass bins over [0, 1].

    Matches scripts/verification/verify_v18_lmm_ece.py: equal-width bins use
    half-open intervals (lo, hi] with the lowest bin closed at 0.
    """
    c = np.asarray(conf, dtype=float)
    r = np.asarray(correct, dtype=float)
    if len(c) != len(r) or len(c) == 0:
        raise ValueError("conf/correct must be same non-zero length")
    if strategy == "width":
        edges = np.linspace(0.0, 1.0, n_bins + 1)
        edges[0] -= 1e-9
        edges[-1] += 1e-9
        ece = 0.0
        # Mirror scripts/verification/verify_v18_lmm_ece.py exactly:
        # first bin is closed at 0, all bins are (lo, hi].
        for lo, hi in zip(edges[:-1], edges[1:]):
            mask = (c > lo) & (c <= hi)
            if mask.sum() == 0:
                continue
            ece += (mask.sum() / len(c)) * abs(r[mask].mean() - c[mask].mean())
        return float(ece)
    elif strategy == "mass":
        qs = np.quantile(c, np.linspace(0, 1, n_bins + 1))
        qs[0] -= 1e-9
        qs[-1] += 1e-9
        bins = np.clip(np.searchsorted(qs[1:-1], c, side="right"), 0, n_bins - 1)
    else:
        raise ValueError("strategy must be 'width' or 'mass'")
    ece = 0.0
    for b in range(n_bins):
        mask = bins == b
        if mask.sum() == 0:
            continue
        ece += (mask.sum() / len(c)) * abs(r[mask].mean() - c[mask].mean())
    return float(ece)


def brier_score(conf: np.ndarray, correct: np.ndarray) -> float:
    """Mean squared error of confidence against the correctness indicator."""
    c = np.asarray(conf, dtype=float)
    r = np.asarray(correct, dtype=float)
    if len(c) != len(r) or len(c) == 0:
        raise ValueError("conf/correct must be same non-zero length")
    return float(np.mean((c - r) ** 2))


def calibration_hit_rate(conf: np.ndarray, correct: np.ndarray, tau: float = 0.70) -> tuple[float, int]:
    """Fraction wrong among predictions with confidence >= tau.

    Returns (CHR, n_high_confidence). Denominator is the set of predictions
    with conf >= tau (NOT the set of wrong answers).
    """
    c = np.asarray(conf, dtype=float)
    r = np.asarray(correct, dtype=float)
    if len(c) != len(r) or len(c) == 0:
        raise ValueError("conf/correct must be same non-zero length")
    hi = c >= tau
    n_hi = int(hi.sum())
    if n_hi == 0:
        return float("nan"), 0
    return float(np.mean(r[hi] == 0)), n_hi


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """Cohen's d for two independent samples (pooled-SD denominator).

    The parametric CI around this value assumes independent observations and
    is reported as descriptive only in the manuscript (item clustering).
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) < 2 or len(b) < 2:
        raise ValueError("both groups need >= 2 observations")
    na, nb = len(a), len(b)
    pooled_sd = np.sqrt(((na - 1) * a.std(ddof=1) ** 2 + (nb - 1) * b.std(ddof=1) ** 2) / (na + nb - 2))
    if pooled_sd == 0:
        return 0.0
    return float((a.mean() - b.mean()) / pooled_sd)
