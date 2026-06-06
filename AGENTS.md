# Agent Guidance

This repository contains an agent skill for restaurant LLC formation and permit execution.

## Model Routing

- Use a high-reasoning model for official-source interpretation, legal/tax/permit sequencing, government portal submissions, payment gates, and final status review.
- Use a faster model only for mechanical drafting from already-reviewed intake or for regenerating package files.
- If a filing, tax, or permit requirement is uncertain or jurisdiction-specific, verify the current official source before acting.
- If model outputs conflict on a legal, tax, filing, or permit decision, stop and route the question to the user, attorney, CPA, or permit specialist.

## Safety Rules

- Do not store SSNs, full DOBs, passwords, MFA codes, payment card data, bank logins, or ID images in repo files.
- Do not commit live company packages under `projects/`.
- Before final submit, payment, signature, certification, or government attestation, ask the user for explicit action-time confirmation.
- Keep generated examples sanitized and generic.

## Public Repo Hygiene

- Main content should be in English.
- Keep real portal receipts, government PDFs, screenshots, and client/company data out of git.
- Prefer editable Markdown, CSV, and JSON templates over binary documents.

## Host Compatibility

- Codex: install under `~/.agents/skills/form-restaurant-llc`; Codex UI metadata lives in `agents/openai.yaml`.
- Claude Code: install under `~/.claude/skills/form-restaurant-llc`.
- OpenClaw: install under `~/.openclaw/skills/form-restaurant-llc`.
- Hermes: install under `~/.hermes/skills/form-restaurant-llc`.
- Use `./setup all` to symlink the current checkout into all four default locations.
