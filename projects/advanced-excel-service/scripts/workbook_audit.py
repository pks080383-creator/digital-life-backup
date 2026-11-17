#!/usr/bin/env python3
"""Pre-delivery structural QA for .xlsx/.xlsm workbooks; does not calculate formulas."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from openpyxl import load_workbook


def audit_workbook(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.suffix.lower() not in {".xlsx", ".xlsm"}:
        raise ValueError("Only .xlsx and .xlsm workbooks are supported.")

    # Read formulas rather than cached values. Formula calculation is performed by Excel,
    # not by openpyxl; this audit only flags literal Excel error values and formula presence.
    wb = load_workbook(path, read_only=True, data_only=False, keep_vba=path.suffix.lower() == ".xlsm")
    sheets: list[dict[str, Any]] = []
    total_formulas = 0
    total_error_cells = 0
    warnings: list[str] = []

    try:
        for ws in wb.worksheets:
            max_row = ws.max_row or 0
            max_col = ws.max_column or 0
            headers = [ws.cell(1, c).value for c in range(1, max_col + 1)] if max_row else []
            nonempty_headers = [str(v).strip() for v in headers if v is not None and str(v).strip()]
            duplicates = sorted({h for h in nonempty_headers if nonempty_headers.count(h) > 1})
            blank_header_columns = [i + 1 for i, v in enumerate(headers) if v is None or not str(v).strip()]
            formula_count = 0
            error_cells: list[str] = []
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str) and cell.value.startswith("="):
                        formula_count += 1
                    if cell.data_type == "e" or (
                        isinstance(cell.value, str)
                        and cell.value in {"#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A", "#NUM!", "#NULL!"}
                    ):
                        error_cells.append(cell.coordinate)
            total_formulas += formula_count
            total_error_cells += len(error_cells)
            if duplicates:
                warnings.append(f"{ws.title}: duplicate headers: {', '.join(duplicates)}")
            if blank_header_columns:
                warnings.append(f"{ws.title}: blank header columns: {blank_header_columns}")
            if error_cells:
                warnings.append(f"{ws.title}: error values found in {len(error_cells)} cell(s)")
            sheets.append({
                "sheet": ws.title,
                "rows_reported_by_excel": max_row,
                "columns_reported_by_excel": max_col,
                "formula_count": formula_count,
                "duplicate_headers": duplicates,
                "blank_header_columns": blank_header_columns,
                "error_cells": error_cells[:100],
                "error_cell_count": len(error_cells),
            })
    finally:
        wb.close()

    if not sheets:
        warnings.append("Workbook contains no worksheets.")
    return {
        "file": path.name,
        "extension": path.suffix.lower(),
        "sheet_count": len(sheets),
        "formula_count": total_formulas,
        "error_cell_count": total_error_cells,
        "sheets": sheets,
        "warnings": warnings,
        "status": "REVIEW_REQUIRED" if warnings else "STRUCTURE_CHECK_PASSED",
        "limitations": [
            "This is a structural pre-check, not a correctness guarantee.",
            "openpyxl does not calculate formulas; recalculate and inspect in Excel.",
            "Macro-enabled files are read for inspection only; macros are not executed.",
            "Large or unusual workbooks may need manual inspection.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--output", type=Path, help="Optional JSON report destination")
    args = parser.parse_args()
    report = audit_workbook(args.workbook)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 1 if report["status"] == "REVIEW_REQUIRED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
