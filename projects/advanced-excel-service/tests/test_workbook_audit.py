import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from scripts.workbook_audit import audit_workbook


class WorkbookAuditTests(unittest.TestCase):
    def test_clean_workbook(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "clean.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.append(["Name", "Amount"])
            ws.append(["Sample", 120])
            wb.save(path)
            result = audit_workbook(path)
            self.assertEqual(result["status"], "STRUCTURE_CHECK_PASSED")
            self.assertEqual(result["sheet_count"], 1)

    def test_duplicate_headers_are_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicate.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.append(["Name", "Name"])
            wb.save(path)
            result = audit_workbook(path)
            self.assertEqual(result["status"], "REVIEW_REQUIRED")
            self.assertEqual(result["sheets"][0]["duplicate_headers"], ["Name"])

    def test_wrong_extension_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "not_excel.csv"
            path.write_text("a,b\n1,2\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                audit_workbook(path)


if __name__ == "__main__":
    unittest.main()
