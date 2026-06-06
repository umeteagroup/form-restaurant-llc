#!/usr/bin/env python3
"""Generate a California restaurant LLC formation package from intake JSON."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from string import Template


ROOT = Path(__file__).resolve().parents[1]
INTAKE_TEMPLATE = ROOT / "assets" / "intake-template.json"


def text(value, fallback="TBD"):
    if value is None:
        return fallback
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        return ", ".join(cleaned) if cleaned else fallback
    value = str(value).strip()
    return value if value else fallback


def money(value):
    return text(value, "")


def load_intake(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def render(template: str, **values) -> str:
    return Template(template).safe_substitute(**values)


def company_values(data: dict) -> dict:
    company = data.get("company", {})
    brand = data.get("brand", {})
    owners = data.get("owners", [])
    locations = data.get("locations", [])
    filing_roles = data.get("filing_roles", {})
    first_owner = owners[0] if owners else {}
    first_location = locations[0] if locations else {}
    alcohol_applies = any(bool(location.get("serves_alcohol")) for location in locations)
    abc_status = "Not started" if alcohol_applies else "Not applicable"
    abc_note = "Alcohol sales indicated; confirm ABC license type." if alcohol_applies else "No alcohol sales per intake."
    return {
        "legal_name": text(company.get("legal_name")),
        "state": text(company.get("state"), "California"),
        "entity_type": text(company.get("entity_type"), "LLC"),
        "management": text(company.get("management")),
        "business_purpose": text(company.get("business_purpose")),
        "principal_office_address": text(company.get("principal_office_address")),
        "mailing_address": text(company.get("mailing_address")),
        "registered_agent_name": text(company.get("registered_agent_name")),
        "registered_agent_address": text(company.get("registered_agent_address")),
        "desired_effective_date": text(company.get("desired_effective_date")),
        "tax_classification_preference": text(company.get("tax_classification_preference")),
        "public_brand_name": text(brand.get("public_brand_name")),
        "needs_dba": text(brand.get("needs_dba")),
        "first_owner_name": text(first_owner.get("name")),
        "first_owner_role": text(first_owner.get("role")),
        "first_owner_ownership": text(first_owner.get("ownership_percent")),
        "first_location_address": text(first_location.get("address")),
        "first_location_city": text(first_location.get("city")),
        "first_location_county": text(first_location.get("county")),
        "abc_status": abc_status,
        "abc_note": abc_note,
        "organizer_filer_name": text(filing_roles.get("organizer_filer_name")),
        "manager_authorized_signer_name": text(filing_roles.get("manager_authorized_signer_name")),
        "ein_responsible_party_name": text(filing_roles.get("ein_responsible_party_name")),
        "authority_confirmation": text(filing_roles.get("authority_confirmation")),
        "registered_agent_consent": text(filing_roles.get("registered_agent_consent")),
        "owner_count": str(len(owners)),
        "location_count": str(len(locations)),
        "notes": text(data.get("notes"), ""),
    }


def collect_missing(data: dict) -> list[str]:
    missing = []
    required = [
        ("company.legal_name", data.get("company", {}).get("legal_name")),
        ("company.management", data.get("company", {}).get("management")),
        ("company.principal_office_address", data.get("company", {}).get("principal_office_address")),
        ("company.registered_agent_name", data.get("company", {}).get("registered_agent_name")),
        ("company.registered_agent_address", data.get("company", {}).get("registered_agent_address")),
        ("brand.public_brand_name", data.get("brand", {}).get("public_brand_name")),
    ]
    for key, value in required:
        if not text(value, ""):
            missing.append(key)
    owners = data.get("owners", [])
    if not owners:
        missing.append("owners[0]")
    for idx, owner in enumerate(owners):
        for field in ("name", "ownership_percent", "capital_contribution_cash"):
            if not text(owner.get(field), ""):
                missing.append(f"owners[{idx}].{field}")
    locations = data.get("locations", [])
    if not locations:
        missing.append("locations[0]")
    for idx, location in enumerate(locations):
        for field in ("address", "city", "county"):
            if not text(location.get(field), ""):
                missing.append(f"locations[{idx}].{field}")
    return missing


def markdown_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None identified."


def location_lines(data: dict) -> str:
    lines = []
    for idx, location in enumerate(data.get("locations", []), start=1):
        lines.append(
            f"{idx}. {text(location.get('store_name'), 'Store')} - "
            f"{text(location.get('address'))}, {text(location.get('city'))}, "
            f"{text(location.get('county'))}; alcohol: {text(location.get('serves_alcohol'))}; "
            f"employees: {text(location.get('has_employees'))}"
        )
    return "\n".join(lines) if lines else "1. TBD"


README = """
# $legal_name Formation Package

This package contains editable drafts and execution checklists for forming and launching a California restaurant LLC.

## Next Actions

1. Review `01-intake-summary.md` and complete anything listed in `02-missing-items.md`.
2. Have an attorney review `04-operating-agreement-draft.md` before signature.
3. Have a CPA confirm tax classification, FTB obligations, and any S-corp or partnership questions.
4. File or confirm CA SOS, IRS, FTB, CDTFA, city, county health, ABC, payroll, insurance, bank, and lease items using `03-formation-execution-checklist.md`.
5. Move approved filings and signed documents into the closing binder listed in `10-closing-binder-index.md`.

This package is a drafting and execution aid, not final legal or tax advice.
"""

INTAKE_SUMMARY = """
# Intake Summary

## Company

- Legal name: $legal_name
- Entity type: $state $entity_type
- Management: $management
- Purpose: $business_purpose
- Principal office: $principal_office_address
- Mailing address: $mailing_address
- Registered agent: $registered_agent_name
- Registered agent address: $registered_agent_address
- Desired effective date: $desired_effective_date
- Tax classification preference: $tax_classification_preference

## Brand

- Public brand name: $public_brand_name
- DBA needed: $needs_dba

## Locations

$locations

## Counts

- Owners: $owner_count
- Locations: $location_count

## Notes

$notes
"""

CHECKLIST = """
# Formation Execution Checklist

| Step | Owner | Status | Evidence / File | Notes |
| --- | --- | --- | --- | --- |
| Confirm entity structure and legal name | Founder / Attorney | Prepared | `11-pre-filing-checklist.md` | Confirm exact legal name and structure before filing. |
| File CA SOS Articles of Organization | Authorized organizer | Not started | Filed LLC-1 | Verify current SOS fee and form. |
| Save filed copy and entity number | Authorized organizer | Not started | | Needed for EIN, bank, and Statement of Information. |
| Sign operating agreement | Members / Attorney | Not started | Signed operating agreement | Attorney review recommended. |
| Adopt initial resolutions | Members / Managers | Not started | Signed resolutions | Authorize bank, tax, permits, leases. |
| Apply for IRS EIN | Responsible party | Not started | EIN CP 575 | Apply after state entity exists. |
| File CA Statement of Information | Authorized filer | Not started | Filed LLC-12 | Due within 90 days, then biennially. |
| Pay or calendar CA FTB annual tax | CPA / Founder | Not started | FTB 3522/payment | Verify due date and first-year treatment. |
| Register CDTFA seller's permit | Founder / CPA | Not started | Seller's permit | Add each location/sub-location as needed. |
| Apply for city business license | Ops | Not started | City license | One per applicable city. |
| Apply for health permit / plan check | Ops / Permit expediter | Not started | Health permit | County/city specific. |
| Apply for ABC license if alcohol applies | Ops / ABC consultant | $abc_status | ABC license | $abc_note |
| Set up payroll and workers' comp if employees | Ops / Payroll provider | Not started | Payroll account, WC policy | Required before employees work. |
| Open bank account | Manager / Authorized signer | Not started | Bank confirmation | Bring EIN, filed LLC docs, operating agreement, resolutions. |
| Assemble closing binder | Ops | Not started | Binder index | Save final approved docs and renewal dates. |
"""

OPERATING_AGREEMENT = """
# Operating Agreement Draft

## $legal_name

This draft is for review by the members, attorney, and CPA. Do not sign until reviewed for the actual ownership, management, tax, and operating arrangement.

## 1. Formation

$legal_name is intended to be a $state limited liability company formed for $business_purpose and related lawful activities.

## 2. Principal Office and Agent

- Principal office: $principal_office_address
- Registered agent: $registered_agent_name
- Registered agent address: $registered_agent_address

## 3. Management

The company is expected to be $management. The members should confirm manager authority, spending limits, lease authority, hiring authority, debt authority, bank signers, and emergency operating authority.

## 4. Members and Contributions

Member names, ownership percentages, and contributions are listed in `06-membership-ledger.csv` and `07-capital-contributions.csv`.

## 5. Tax Matters

Tax classification preference: $tax_classification_preference. CPA must confirm federal and California tax treatment, annual filings, FTB annual tax, and any election deadlines.

## 6. Transfers and Buy-Sell Terms

Add attorney-reviewed terms for transfer restrictions, right of first refusal, death/disability, deadlock, forced sale, member exit, valuation, and dispute resolution.

## 7. Restaurant Operations

Add operating rules for brand ownership, store opening approvals, leases, equipment, payroll, food safety, alcohol compliance, delivery platforms, accounting, and related-party transactions.

## 8. Signatures

Each member should sign after final legal review.
"""

RESOLUTIONS = """
# Initial Company Resolutions

## $legal_name

The undersigned members/managers approve the following actions, subject to final legal and tax review:

1. Form and operate $legal_name as a $state $entity_type.
2. Authorize filing of formation documents and required state statements.
3. Authorize applying for an EIN with the IRS.
4. Authorize registration with California FTB and CDTFA as applicable.
5. Authorize applications for city business licenses, health permits, ABC licenses if applicable, payroll accounts, insurance, and related operating permits.
6. Authorize opening one or more business bank accounts.
7. Authorize designated managers/signers to negotiate and sign leases, vendor agreements, POS agreements, delivery platform agreements, and professional service agreements within approved limits.
8. Approve preparation and attorney review of the operating agreement, membership ledger, and capital contribution schedule.

## Signature

Name: ______________________________

Title: ______________________________

Date: _______________________________
"""

PERMITS = """
# Restaurant Permit Checklist

## Locations

$locations

## Per-Location Permit Tracker

| Location | Permit / Registration | Agency | Status | Notes |
| --- | --- | --- | --- | --- |
| Each | City business license | City | Not started | Confirm city rules and zoning. |
| Each | Food facility permit / plan check | County or city health department | Not started | Menu, floor plan, equipment, inspection dependencies. |
| Each | Seller's permit location/sub-location | CDTFA | Not started | Required for taxable sales. |
| Each | ABC license | California ABC | Not applicable | Required only if alcohol is served. |
| Each | Sign permit | City | Not started | If exterior signs are planned. |
| Each | Fire inspection | Fire department | Not started | Often needed before opening. |
| Each | Grease / wastewater approvals | City or utility | Not started | Depends on kitchen and local requirements. |
| Each | Payroll / workers' compensation | EDD, payroll provider, carrier | Not started | Required if employees work. |
"""

BANKING = """
# Banking and Accounting Handoff

## Company

- Legal name: $legal_name
- EIN: TBD
- State entity number: TBD
- Principal office: $principal_office_address
- Management: $management

## Bring to Bank

- Filed Articles of Organization
- EIN confirmation letter
- Operating agreement
- Initial resolutions authorizing bank account and signers
- IDs for authorized signers
- Business license or lease, if requested

## Accounting Setup

- Confirm tax classification with CPA.
- Calendar FTB annual tax and annual return.
- Set up chart of accounts for restaurant operations.
- Track store-level sales, COGS, labor, rent, fees, delivery platform commissions, tips, sales tax, gift cards, and owner draws/distributions.
- Confirm POS, payroll, and sales tax reporting integration.
"""

CLOSING = """
# Closing Binder Index

## Formation

- Pre-filing checklist
- Filed Articles of Organization
- Statement of Information
- EIN confirmation letter
- Operating agreement
- Initial resolutions
- Membership ledger
- Capital contribution schedule

## Tax and Registrations

- FTB payment records and tax calendar
- CDTFA seller's permit and login details record
- Payroll registration if applicable
- CPA handoff notes

## Restaurant Operations

- City business license
- Health permit / inspection records
- ABC license if applicable
- Lease and amendments
- Insurance certificates
- Workers' compensation policy if applicable
- Food safety manager certificate and food handler records

## Renewal Calendar

Add renewal dates and responsible owner for each permit, insurance policy, tax filing, lease option, and license.
"""

POST_FORMATION = """
# Post-Formation Missing Files and Registration Plan

Company: $legal_name

EIN: TBD

CA SOS entity number: TBD

Store: $first_location_address

Principal office: $principal_office_address

## Completed and Archived

- TBD

## Still Missing / Next Government Files

| Priority | File / Registration | Responsible Site | Status | Notes |
| --- | --- | --- | --- | --- |
| 1 | CA SOS official formation documents | CA SOS bizfile | Not started | Articles, acknowledgment, welcome letter, receipt. |
| 2 | EIN evidence | IRS | Not started | CP575 preferred; success page acceptable if CP575 unavailable. |
| 3 | CA Statement of Information | CA SOS bizfile | Not started | Initial statement after formation. |
| 4 | CDTFA seller's permit | CDTFA online registration | Not started | Required for taxable retail sales. |
| 5 | City business license | City portal | Not started | Submit application, pay invoice, save final certificate. |
| 6 | County food facility / health permit | County/city environmental health | Not started | Plan check and inspection may be required. |
| 7 | California FTB annual LLC tax payment record | FTB Web Pay or Form 3522 | Not started | Confirm with CPA. |
| 8 | Payroll tax accounts | EDD / payroll provider | Not started | Required before W-2 employees start working. |
| 9 | Workers' compensation policy | Insurance broker | Not started | Required if employees are working in California. |
| 10 | Bank account confirmation | Bank | Not started | Use filed docs, EIN, operating agreement, resolutions, signer IDs. |

## Submission Records

Add one subsection per filing/payment with confirmation numbers, dates, evidence files, and next steps.
"""

PORTAL_TRACKER = """
# Government Portal Account Tracker

Company: $legal_name

EIN: TBD

CA SOS Entity No.: TBD

Use this tracker to record portal access without storing passwords. Store passwords, recovery codes, MFA seeds, and temporary credentials only in the approved password manager.

## Account Rules

- Use a company-controlled email whenever possible.
- Turn on MFA / two-factor authentication where available.
- Save official PDFs, receipts, permits, certificates, and confirmation pages into the company package.
- Record who created the account and who has admin access.
- Use external Chrome/Safari when a government portal download is blocked.

## Portal Accounts

| Portal | Purpose | URL | Account Email / Username | MFA | Owner | Status | Files to Download |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CA SOS bizfile Online | Articles, Statement of Information, receipts | https://bizfileonline.sos.ca.gov/ |  |  |  | Not started | Filed articles, acknowledgments, receipts, statements |
| IRS EIN Online | EIN assignment | https://sa.www4.irs.gov/applyein/ | No reusable account | N/A |  | Not started | EIN assignment page, CP575 or 147C if needed |
| CDTFA Online Services | Seller's permit, sales tax account, returns, payments | https://www.cdtfa.ca.gov/services/registration.htm |  |  |  | Not started | Seller's permit, account confirmation, correspondence |
| FTB MyFTB / Web Pay for Businesses | CA LLC annual tax and tax payments | https://www.ftb.ca.gov/pay/business.html |  |  |  | Not started | Web Pay confirmation, Form 3522 proof, tax notices |
| EDD e-Services for Business | Payroll tax account | https://edd.ca.gov/Payroll_Taxes/e-Services_for_Business.htm |  |  |  | Not started | Payroll account confirmation, filings |
| City Business License | City business license |  |  |  |  | Not started | Application confirmation, payment receipt, license certificate |
| County Health Portal | Food facility permit / plan check |  |  |  |  | Not started | Plan check application, health permit, inspection records |
| Insurance Broker / Carrier Portal | General liability and workers' comp |  |  |  |  | Not started | COI, workers' comp policy, renewal docs |
| Bank Online Portal | Business checking and treasury |  |  |  |  | Not started | Account opening confirmation, bank letter, statements |

## Download Naming Convention

- `official-ca-sos-downloads/01-articles-of-organization-filed.pdf`
- `official-ca-sos-downloads/02-business-entity-filing-acknowledgment.pdf`
- `official-irs-downloads/01-ein-assignment-success-page-print.pdf`
- `cdtfa/01-sellers-permit.pdf`
- `<city>-business-license/01-application-review-before-submit.png`
- `<city>-business-license/02-application-submitted-confirmation.md`
- `<city>-business-license/03-payment-receipt.md`
- `<city>-business-license/04-business-license-certificate.pdf`
- `<county>-health-permit/01-plan-check-application.pdf`
- `<county>-health-permit/02-health-permit.pdf`
- `ftb/01-annual-tax-payment-confirmation.pdf`
- `edd-payroll/01-edd-account-confirmation.pdf`
- `insurance/01-workers-comp-policy.pdf`
- `banking/01-bank-account-confirmation.pdf`
"""

PREFILING = """
# Pre-Filing Checklist

## Company

- Legal name to file: `$legal_name`
- State: $state
- Entity type: $entity_type
- Management: $management
- Business purpose: $business_purpose
- Principal office: $principal_office_address
- Mailing address: $mailing_address
- Registered agent: $registered_agent_name
- Registered agent address: $registered_agent_address
- Owner/member: $first_owner_name, $first_owner_ownership
- Brand / DBA: $public_brand_name
- Store address: $first_location_address
- Store city/county: $first_location_city, $first_location_county

## Required Confirmations Before CA SOS Filing

- Confirm exact legal name capitalization and spacing.
- Confirm the registered agent agrees to serve and can receive legal mail at the registered agent address.
- Confirm who will act as organizer/filer for the Articles of Organization.
- Confirm who will be manager or authorized signer for the LLC.
- Confirm owner/member and ownership percentage.
- Confirm CPA treatment, especially if the owner/member is a corporation, trust, foreign person, or another entity.

## Confirmed Authority

- Authority confirmation: $authority_confirmation
- Registered agent consent: $registered_agent_consent

## Official Filing Checkpoints

- CA SOS Articles of Organization: verify current filing fee and submit through bizfile when ready.
- CA SOS Statement of Information: due within 90 days of initial registration and every two years thereafter.
- IRS EIN: apply after the LLC is formed with California. The responsible party generally must be an individual in control of the entity or an authorized representative with the responsible party's SSN/ITIN.
- FTB annual tax: California LLCs organized or doing business in California generally owe annual LLC tax. Calendar the first-year due date based on the SOS filing date.
- CDTFA seller's permit: needed for taxable food/beverage sales and store-level location setup.
- City/county permits: verify city business license and county health permit based on store address.
- ABC license: $abc_note
- Payroll/workers' compensation: required path if employees are expected.

## Filing Sequence

1. Resolve the open items below.
2. Search/confirm LLC name availability.
3. File CA SOS Articles of Organization.
4. Save filed copy and California entity/file number.
5. Apply for EIN.
6. Prepare and sign operating agreement and initial resolutions.
7. File initial Statement of Information within 90 days.
8. Calendar FTB annual tax and Form 568 obligations with CPA.
9. Start CDTFA seller's permit, city business license, county health permit, payroll/workers' comp, insurance, and bank account setup.

## Open Items

- Organizer/filer name: $organizer_filer_name
- Manager/authorized signer name: $manager_authorized_signer_name
- Responsible party for EIN: $ein_responsible_party_name
- CPA confirmation: Pending
- Attorney review: Pending
"""


def write_csvs(data: dict, out: Path):
    owners = data.get("owners", [])
    with (out / "06-membership-ledger.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["member_name", "role", "ownership_percent", "address", "email", "authorized_signer"])
        for owner in owners:
            writer.writerow([
                text(owner.get("name"), ""),
                text(owner.get("role"), ""),
                text(owner.get("ownership_percent"), ""),
                text(owner.get("address"), ""),
                text(owner.get("email"), ""),
                text(owner.get("manager_or_authorized_signer"), ""),
            ])
    with (out / "07-capital-contributions.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["member_name", "cash_contribution", "non_cash_contribution", "notes"])
        for owner in owners:
            writer.writerow([
                text(owner.get("name"), ""),
                money(owner.get("capital_contribution_cash")),
                text(owner.get("capital_contribution_non_cash"), ""),
                "",
            ])


def generate(intake_path: Path, out: Path):
    data = load_intake(intake_path)
    values = company_values(data)
    values["locations"] = location_lines(data)
    out.mkdir(parents=True, exist_ok=True)

    write(out / "00-readme-next-actions.md", render(README, **values))
    write(out / "01-intake-summary.md", render(INTAKE_SUMMARY, **values))
    write(out / "02-missing-items.md", "# Missing Items\n\n" + markdown_list(collect_missing(data)))
    write(out / "03-formation-execution-checklist.md", render(CHECKLIST, **values))
    write(out / "04-operating-agreement-draft.md", render(OPERATING_AGREEMENT, **values))
    write(out / "05-initial-resolutions.md", render(RESOLUTIONS, **values))
    write_csvs(data, out)
    write(out / "08-restaurant-permit-checklist.md", render(PERMITS, **values))
    write(out / "09-banking-accounting-handoff.md", render(BANKING, **values))
    write(out / "10-closing-binder-index.md", render(CLOSING, **values))
    write(out / "11-pre-filing-checklist.md", render(PREFILING, **values))
    write(out / "24-post-formation-missing-files-and-registration-plan.md", render(POST_FORMATION, **values))
    write(out / "25-government-portal-account-tracker.md", render(PORTAL_TRACKER, **values))
    for folder in [
        "official-ca-sos-downloads",
        "official-irs-downloads",
        "company-records",
        "cdtfa",
        "city-business-license",
        "county-health-permit",
        "ftb",
        "edd-payroll",
        "insurance",
        "banking",
    ]:
        (out / folder).mkdir(exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--init-intake", type=Path, help="Path to write a blank intake JSON")
    group.add_argument("--generate", type=Path, help="Completed intake JSON to generate from")
    parser.add_argument("--out", type=Path, help="Output folder for generated package")
    args = parser.parse_args()

    if args.init_intake:
        args.init_intake.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(INTAKE_TEMPLATE, args.init_intake)
        print(f"Wrote intake template: {args.init_intake}")
        return

    if not args.out:
        parser.error("--out is required with --generate")
    generate(args.generate, args.out)
    print(f"Wrote formation package: {args.out}")


if __name__ == "__main__":
    main()
