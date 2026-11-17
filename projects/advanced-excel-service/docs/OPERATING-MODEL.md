# Sales and fulfillment operating model

## Initial service menu

Keep the first offer narrow and easy to demonstrate:

1. **Excel cleanup:** remove duplicates, standardize dates/text, repair layout, and provide a before/after note.
2. **Formula repair:** diagnose and fix broken or slow formulas, with a short explanation.
3. **Dashboard/MIS:** create a simple KPI summary and refreshable reporting view.

Treat prices as pilot quotes, not validated market rates. Confirm scope and effort before quoting. Do not offer unlimited revisions.

## Lead lifecycle

`NEW → QUALIFIED → SAMPLE/DEMO → QUOTE_SENT → WON/LOST`

Capture: name, business email, company, requested outcome, source, received time, consent/contact context, and status. Reject or manually review incomplete or suspicious submissions.

## Order lifecycle

`REQUESTED → SCOPE_CONFIRMED → PAYMENT_CONFIRMED → FILE_RECEIVED → QA → CUSTOMER_APPROVAL → DELIVERED → CLOSED`

Never mark an order paid based only on a customer message or screenshot. Verify payment in the receiving account. Keep original customer files unchanged; work on a copy.

## Fulfillment QA

- Confirm workbook opens and required sheets are present.
- Check blank or duplicate headers and formula error cells.
- Check row counts and obvious missing values.
- Confirm formulas, filters, formats, and charts still work after edits.
- Compare output with the agreed scope and test with sample records.
- Keep a short change log and final delivery note.

The included Python audit is a preliminary safety check, not a guarantee that a workbook is correct. It does not execute formulas or replace manual review in Excel.

## Human approval gates

- No unsolicited bulk outreach.
- No automatic customer email until Gmail OAuth is configured and the message is approved.
- No payment confirmation without checking the actual transaction.
- No final file delivery until QA and recipient are confirmed.
- Do not upload sensitive client workbooks to public repositories or unapproved AI tools.
