"""Dataset loading and validation for AfriKnow GM-only v3."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

EXPECTED_N_TOTAL = 180
EXPECTED_N_AFRICA = 90
EXPECTED_N_EUROPE = 90
EXPECTED_DIFFICULTY = "medium"
EXPECTED_LANGUAGE = "en"
CURATED_SHA256 = "fc07491b188ca2017b15ef93b6c1a9fd5066007362ea5c4e944f60443a52ef52"
RAW_SHA256 = "1915a77c02ff1f08a87f8b2950f2e2c5e3041a353f7e26f456dd700543a6807d"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_items(path: Path) -> dict:
    """Load the curated 180-item JSON and return the top-level dict."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_items(data: dict) -> list[str]:
    """Return a list of validation failures (empty list == valid)."""
    errors = []
    items = data.get("items", [])
    if data.get("n_total") != EXPECTED_N_TOTAL or len(items) != EXPECTED_N_TOTAL:
        errors.append(f"expected {EXPECTED_N_TOTAL} items, found {len(items)}")
    regions = [i["region"] for i in items]
    if regions.count("Africa") != EXPECTED_N_AFRICA:
        errors.append(f"expected {EXPECTED_N_AFRICA} Africa items, found {regions.count('Africa')}")
    if regions.count("Europe") != EXPECTED_N_EUROPE:
        errors.append(f"expected {EXPECTED_N_EUROPE} Europe items, found {regions.count('Europe')}")
    ids = [i["id"] for i in items]
    if len(set(ids)) != len(ids):
        errors.append("duplicate item ids")
    qtexts = [i["q"].strip().lower() for i in items]
    if len(set(qtexts)) != len(qtexts):
        errors.append("duplicate question texts")
    for i in items:
        if i["diff"] != EXPECTED_DIFFICULTY:
            errors.append(f"{i['id']}: difficulty {i['diff']!r}")
            break
        if i["lang"] != EXPECTED_LANGUAGE:
            errors.append(f"{i['id']}: language {i['lang']!r}")
            break
        if len(i["ch"]) != 4:
            errors.append(f"{i['id']}: {len(i['ch'])} options")
            break
        if not (0 <= i["a"] <= 3):
            errors.append(f"{i['id']}: gold index {i['a']!r}")
            break
        if any(v in (None, "") for v in (i["q"], i["id"])):
            errors.append(f"{i['id']}: missing field value")
            break
    if not (data.get("gm_only_core", False) or all(i.get("gm_only", False) for i in items)):
        errors.append("gm_only flags not set")
    return errors
