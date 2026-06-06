---
name: form-restaurant-llc
description: Use when forming a U.S. restaurant, cafe, boba, food service, hospitality, or store-level LLC; generating formation packets; coordinating Secretary of State, EIN, tax, seller's permit, city license, health permit, alcohol, payroll, insurance, and bank setup; or archiving government receipts, approvals, permits, and closing-binder records. Optimized for California first, with official-source verification before jurisdiction-specific advice.
---

# Form Restaurant LLC

## Core Rules

- Treat this as a drafting and execution workflow, not final legal or tax advice.
- Verify current official sources before relying on filing fees, deadlines, forms, BOI rules, permit requirements, or portal behavior.
- Prefer official sources: Secretary of State, IRS, state tax agencies, seller's permit agencies, city licensing, health department, alcohol authority, payroll agency, and workers' compensation authority.
- Ask for explicit user confirmation before submitting anything on government, tax, bank, landlord, payroll, or permit portals.
- Ask again at action time before final submit/payment/certification, even if the user approved the plan earlier.
- Never store SSNs, full DOBs, passwords, payment card details, CVVs, bank logins, MFA codes, recovery codes, or personal ID images in chat or package files.
- If the user will publish or commit the repo, exclude live company packages, portal receipts, government downloads, screenshots, and intake files containing real parties.

## Model Guidance

- Use a high-reasoning model for legal/tax/permit sequencing, portal submissions, official-source interpretation, and final review gates.
- A faster model is acceptable for mechanical package generation from already-validated intake.
- If two models disagree on a filing or permit decision, stop, cite the official-source issue, and ask the user to route to counsel/CPA/permit specialist.

## Workflow

1. **Scope the entity**
   - Confirm state, county/city, restaurant concept, number of locations, whether there is a parent/store LLC structure, alcohol sales, employees, outside investors, franchising, and non-U.S. owners.
   - If the user is forming outside California, keep the packet structure but replace California-specific steps with current official state/local requirements.

2. **Collect intake**
   - Prefer `assets/templates/intake-questionnaire.md` for owner-friendly intake. Ask the user to fill it in, or create a project-specific copy and fill it collaboratively.
   - Convert the completed Markdown questionnaire into the JSON shape in `assets/intake-template.json` before running the package generator.
   - Keep `assets/intake-form/index.html` as an optional experimental intake form only when the user explicitly wants a browser form.
   - Ask only for missing material facts. Do not require SSNs, full dates of birth, passport images, or other sensitive identity data in chat unless the user explicitly wants a local private worksheet.
   - If users provide partial details, generate the package with placeholders and a missing-items list.

3. **Generate the file package**
   - Run `scripts/generate_package.py --init-intake <path>` to create a blank intake JSON.
   - Run `scripts/generate_package.py --generate <intake.json> --out <folder>` to generate the formation package.
   - The generated package should include drafts and CSVs suitable for review, completion, and handoff.

4. **Guide execution**
   - Use `references/california-restaurant-llc.md` for filing sequence, official-source checkpoints, and restaurant-specific permits.
   - Use `references/execution-sop.md` when actually operating portals, filing forms, paying fees, downloading documents, naming files, or updating statuses.
   - Track each step as: `Not started`, `Prepared`, `Submitted / pending review`, `Paid / pending approval`, `Approved / archived`, `Blocked`, or `Not applicable`.
   - For each permit, capture agency, portal URL, account owner, submission date, confirmation number, amount paid, status, evidence file, and renewal date if available.

5. **Build the closing binder**
   - After formation, assemble filed/approved items, signed internal documents, tax registrations, permits, insurance, lease documents, and banking records.
   - Use `references/cpa-sample-closing-binder-map.md` as a structural reference for documents commonly delivered by CPA-supported formations.
   - Treat in-app browser filing portals as review/verification tools when downloads are unreliable. For official PDFs, use browser network response capture, browser print-to-PDF, an external browser, or a user-provided downloaded file path, then archive and QA the files in the closing binder.
   - If a government portal opens a PDF inside the browser viewer but download is unreliable, first try saving the network response body to the target file. If that captures only the viewer HTML, use the browser's PDF/print view to export a rendered PDF, keep a screenshot as evidence, and label the file notes honestly.
   - Keep a separate `missing-and-follow-up.md` for incomplete filings, professional review items, and renewal deadlines.

## CDTFA Seller's Permit Notes

- CDTFA may show the application confirmation as "submitted and being processed" while the status page already lists a new Sales and Use Tax account and an approved Seller's Permit.
- Capture all three records when available: application confirmation number, Sales and Use Tax account number, and Seller's Permit/location ID.
- After permit approval, verify whether the account appears on the CDTFA Home page. If Home still says the user has no account access, record that as a follow-up rather than treating it as a failed permit.
- Save correspondence messages separately from the permit PDF, especially application notifications and account setup notices.

## City Business License Notes

- City portals may accept an application first, then email a payment-due notice later. Track application confirmation, account number/PIN if provided, payment receipt, and final certificate separately.
- Do not expose temporary portal passwords in chat or non-sensitive records. Save a screenshot only if needed and label it sensitive.
- After payment, many cities still require zoning/planning review before issuing the actual license certificate.

## Health Permit Notes

- Do not assume one county's checklist applies to another county or city.
- Before plan check or food facility permit submission, gather menu, floor plan, equipment list, lease/buildout status, prior tenant facts, food safety manager records, water/ice/refrigeration/sinks/storage/wastewater details, and inspection dependencies.
- Track plan check, application submission, payment, inspection, permit issuance, renewal, and certificate download as separate milestones.

## Output Standards

Each generated package should be easy for a business owner, attorney, CPA, or operations manager to use. Prefer clear file names and one folder per company. Keep templates editable in Markdown/CSV/JSON unless the user asks for DOCX or PDF conversion.

Required generated files:

- `00-readme-next-actions.md`
- `01-intake-summary.md`
- `02-missing-items.md`
- `03-formation-execution-checklist.md`
- `04-operating-agreement-draft.md`
- `05-initial-resolutions.md`
- `06-membership-ledger.csv`
- `07-capital-contributions.csv`
- `08-restaurant-permit-checklist.md`
- `09-banking-accounting-handoff.md`
- `10-closing-binder-index.md`
- `11-pre-filing-checklist.md`
- `24-post-formation-missing-files-and-registration-plan.md`
- `25-government-portal-account-tracker.md`

Recommended execution folders:

- `official-ca-sos-downloads/`
- `official-irs-downloads/`
- `cdtfa/`
- `<city>-business-license/`
- `<county>-health-permit/`
- `ftb/`
- `edd-payroll/`
- `insurance/`
- `banking/`

## Decision Points

Flag these decisions before generating final drafts:

- Single LLC vs parent LLC plus separate store LLCs.
- Member-managed vs manager-managed.
- Tax classification and possible S-corp election.
- DBA/fictitious business name if brand differs from legal name.
- Seller's permit setup for each location.
- Health permit by county/city.
- Alcohol license type if selling beer, wine, or liquor.
- Payroll, workers' compensation, and employment compliance if hiring.
- Investor, franchise, IP, licensing, or cross-state expansion issues.

## Bundled Resources

- `assets/intake-template.json`: fillable intake file.
- `assets/templates/intake-questionnaire.md`: primary Markdown intake questionnaire.
- `assets/intake-form/index.html`: optional local browser form that exports intake JSON without uploading data.
- `assets/templates/`: standalone editable templates for teams that want to work manually.
- `scripts/generate_package.py`: deterministic generator for package drafts.
- `references/california-restaurant-llc.md`: California restaurant LLC execution reference.
- `references/execution-sop.md`: reusable execution SOP distilled from a completed restaurant LLC pilot.
- `references/cpa-sample-closing-binder-map.md`: CPA sample-derived map of approved filing documents, EIN, LLC-12, operating agreement, and ledger expectations.
