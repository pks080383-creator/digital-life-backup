# Advanced Excel Service — Automation Foundation

This project is isolated from Tallwater Revenue. It uses **n8n on the owner's existing computer** for workflow orchestration and GitHub for version control. Grok Bot is not used.

## Current scope

- Capture and normalize inbound enquiries through an n8n webhook.
- Capture order requests and place them in a human-approval state.
- Audit submitted .xlsx/.xlsm workbooks for common delivery risks using Python.
- Keep customer communication and final file delivery behind an explicit human approval step.

## Zero-cost operating model

- GitHub Free for source control.
- Self-hosted n8n on the existing computer (runs only while that computer is on and connected).
- Python + openpyxl for workbook QA.
- Existing Gmail account for customer communication after OAuth is configured.
- No paid hosting, paid APIs, ads, or new subscriptions before the first paid order.

## Project layout

- `n8n/workflows/`: importable starter workflows.
- `scripts/workbook_audit.py`: local workbook QA utility.
- `tests/`: tests for the QA utility.
- `docs/`: setup, operating controls, and launch checklist.

## Important current status

These files are a **version-controlled build foundation**, not a claim that n8n is already installed or running. Import the workflows only after n8n is installed locally and tested. The webhook workflows validate and normalize incoming data; they do not silently send sales emails, take payments, or deliver customer files.

## Quick start

1. Install Python 3 and n8n locally (see `docs/LOCAL-SETUP.md`).
2. Install Python dependency: `python -m pip install -r projects/advanced-excel-service/requirements.txt`.
3. Run tests: `python -m unittest discover -s projects/advanced-excel-service/tests -v`.
4. Import the two JSON files from `n8n/workflows` into n8n.
5. Configure webhook URLs and test with dummy data only.
6. Configure Gmail OAuth only when ready; keep live sending disabled until a test and explicit approval.

## First commercial objective

Get one paid pilot customer. Start with one tightly scoped outcome (cleaning a workbook, fixing a formula, or building a simple management dashboard). Do not promise fully unattended delivery until the complete local workflow has passed end-to-end tests.
