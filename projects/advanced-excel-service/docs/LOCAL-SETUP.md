# Local setup

## Before installing

The previous environment audit found no running n8n instance and no confirmed local Docker access. This GitHub connection cannot install software on the physical computer or inspect its current desktop. Confirm the computer has Windows 10/11, a supported Node.js LTS runtime, Python 3, and a stable internet connection before proceeding.

## Recommended zero-cost route

1. Install a current Node.js LTS release from the official Node.js website.
2. Open PowerShell and verify:
   ```powershell
   node --version
   npm --version
   python --version
   ```
3. Install n8n locally:
   ```powershell
   npm install -g n8n
   ```
4. Start it:
   ```powershell
   n8n
   ```
5. Open the local URL printed by n8n (normally `http://localhost:5678`) and create the local owner account.
6. Keep the computer awake and online whenever workflows must run. Local hosting is free in hosting cost, but it is not always-on if the PC is off, asleep, or disconnected.

Do not expose port 5678 directly to the public internet. Use n8n's documented secure access method if remote webhook access is later required. Do not put credentials or API keys in GitHub.

## Python workbook QA

From the repository root:
```powershell
python -m pip install -r projects/advanced-excel-service/requirements.txt
python projects/advanced-excel-service/scripts/workbook_audit.py "C:\path\to\sample.xlsx" --output "audit-report.json"
python -m unittest discover -s projects/advanced-excel-service/tests -v
``

## Import workflows

In n8n, use **Import from File** and select each JSON file in `n8n/workflows`. Activate only after testing with dummy enquiries. These starter workflows use webhook triggers and need no external account credentials.

## Gmail connection

Connect Gmail through n8n's supported OAuth credential flow. Do not paste an app password or OAuth secret into workflow JSON or commit it to GitHub. Start with draft creation or a test mailbox; enable customer-facing sends only after reviewing the exact message and recipient.
