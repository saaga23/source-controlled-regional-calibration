# Environment

- **Python:** ≥ 3.9 required; this release was verified on **3.12.3/3.12.4 (Windows)**.
- **Dependencies:** `requirements.txt` (analysis + tests; `openai` only for fresh inference).
- **OS:** no OS-specific code in the analysis path; the release was verified on Windows 10 (PowerShell 5.1). Linux/macOS should work with the standard commands; if you verify on another OS, note it in an issue.
- **No credentials needed** for analysis/tests; `.env.example` documents the one variable needed for fresh inference.
- Reproduction entry points: README §15; the audit trail format is documented in `scripts/primary/05_audit_trail.py`.
