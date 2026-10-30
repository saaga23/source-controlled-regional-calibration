# Security Policy

## Scope

This repository contains research code that processes public benchmark data and recorded model outputs. It has no user accounts, no network services, and stores no secrets.

## Reporting

- **Vulnerabilities** (e.g., code execution via crafted input files): open a GitHub security advisory or contact the owner privately — do not open a public issue with exploit details.
- **Data/privacy concerns** (e.g., you believe an item contains problematic content): open an issue describing the item ID; the frozen dataset is versioned so corrections produce a new version rather than silent edits.

## Handling of secrets

- API keys are read from environment variables only (`OPENROUTER_API_KEY`); `.env` is git-ignored; `.env.example` documents the variable names without values.
- The test suite includes a secret-pattern scan; do not weaken it.
