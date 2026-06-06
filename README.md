# Restaurant LLC Formation Skill

An agent skill for forming restaurant, cafe, boba, food-service, and hospitality LLCs and tracking the permits needed to open a location.

The workflow is California-first, but the package structure is designed so an agent can replace California-specific steps with the official requirements for another state, city, or county.

## What It Generates

- Intake summary and missing-items list
- Formation execution checklist
- Operating agreement draft outline
- Initial resolutions
- Membership ledger and capital contribution CSVs
- Restaurant permit checklist
- Banking/accounting handoff
- Closing binder index
- Government portal account tracker

## Typical Workflow

1. Create an intake JSON from `assets/intake-template.json` or `assets/templates/intake-questionnaire.md`.
2. Generate the package:

```bash
python3 scripts/generate_package.py --generate examples/sample-intake.json --out /tmp/sample-restaurant-llc-package
```

3. Verify current official sources before filing or advising on deadlines and fees.
4. Execute filings and permits with explicit user confirmation before final submit/payment.
5. Archive filed documents, receipts, approvals, permit certificates, and renewal dates.

## Install as an Agent Skill

One-line install from GitHub:

```bash
git clone https://github.com/umeteagroup/form-restaurant-llc.git /tmp/form-restaurant-llc && /tmp/form-restaurant-llc/setup all
```

Install for one host:

```bash
git clone https://github.com/umeteagroup/form-restaurant-llc.git /tmp/form-restaurant-llc && /tmp/form-restaurant-llc/setup codex
git clone https://github.com/umeteagroup/form-restaurant-llc.git /tmp/form-restaurant-llc && /tmp/form-restaurant-llc/setup claude
git clone https://github.com/umeteagroup/form-restaurant-llc.git /tmp/form-restaurant-llc && /tmp/form-restaurant-llc/setup openclaw
git clone https://github.com/umeteagroup/form-restaurant-llc.git /tmp/form-restaurant-llc && /tmp/form-restaurant-llc/setup hermes
```

Run the lightweight setup script:

```bash
./setup codex
```

Supported hosts:

```bash
./setup codex
./setup claude
./setup openclaw
./setup hermes
./setup all
```

Default install targets:

| Host | Target |
| --- | --- |
| Codex | `~/.agents/skills/form-restaurant-llc` |
| Claude Code | `~/.claude/skills/form-restaurant-llc` |
| OpenClaw | `~/.openclaw/skills/form-restaurant-llc` |
| Hermes | `~/.hermes/skills/form-restaurant-llc` |

Override targets with `CODEX_SKILLS_DIR`, `CLAUDE_SKILLS_DIR`, `OPENCLAW_SKILLS_DIR`, or `HERMES_SKILLS_DIR`.

For Codex UI metadata, see `agents/openai.yaml`.

## License

Recommended: Apache-2.0 for explicit patent protection and corporate-friendly contribution terms. MIT is also compatible with broad commercial reuse but does not include the same explicit patent grant.

## Model Guidance

Use a high-reasoning model for official-source interpretation, legal/tax/permit sequencing, portal submissions, payment gates, and final review. A faster model is fine for mechanical package generation from validated intake.

## Privacy and Open Source Safety

Do not commit live company packages, government downloads, receipts, screenshots, sensitive intake, credentials, payment data, or personal identity records. The `.gitignore` excludes `projects/` and common generated evidence folders by default.

This skill is an execution aid, not legal or tax advice. Attorney, CPA, permit expediter, landlord, and agency confirmation may be required.
