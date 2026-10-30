# Contributing

Thank you for helping make this audit more reliable. Three rules keep the science intact:

1. **Frozen data stays frozen.** `data/raw/` and `data/curated/` are hash-pinned (`reproducibility/hashes/`, tests enforce the canonical hashes). Never edit them; analyses read, they never write.
2. **Every claim needs a path.** If a README or docs statement reports a number, it must be re-derivable by a committed script from the raw CSV (see `docs/results/RESULTS.md` for the verification trail pattern).
3. **Report failures honestly.** A reproduction failure is a bug report, not an embarrassment.

## Development setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python -m pytest tests/ -q
```

## Pull requests

- New analyses → add tests; keep scripts read-only over `data/`.
- Documentation fixes → welcome, including typos; keep the honest-reporting conventions (nulls are nulls, not equivalence).
- Do not include credentials, personal paths, or model-output dumps in PRs.
