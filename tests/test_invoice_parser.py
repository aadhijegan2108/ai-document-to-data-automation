import sys
import unittest
from pathlib import Path


# Allow Python to import modules from the src folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from invoice_parser import validate_invoice


class TestInvoiceValidation(unittest.TestCase):

    def setUp(self):
        self.valid_invoice = {
            "subtotal": 29500.0,
            "gst": 5310.0,
            "total": 34810.0,
            "items": [
                {
                    "quantity": 4.0,
                    "unit_price": 4500.0,
                    "amount": 18000.0,
                },
                {
                    "quantity": 4.0,
                    "unit_price": 850.0,
                    "amount": 3400.0,
                },
                {
                    "quantity": 6.0,
                    "unit_price": 650.0,
                    "amount": 3900.0,
                },
                {
                    "quantity": 10.0,
                    "unit_price": 420.0,
                    "amount": 4200.0,
                },
            ],
        }

    def test_valid_invoice(self):
        errors = validate_invoice(self.valid_invoice)

        self.assertEqual(errors, [])

    def test_wrong_line_item_amount(self):
        invoice = self.valid_invoice.copy()
        invoice["items"] = [dict(item) for item in self.valid_invoice["items"]]

        invoice["items"][0]["amount"] = 19000.0

        errors = validate_invoice(invoice)

        self.assertTrue(any("Item 1 mismatch" in error for error in errors))

    def test_wrong_subtotal(self):
        invoice = self.valid_invoice.copy()
        invoice["subtotal"] = 30000.0

        errors = validate_invoice(invoice)

        self.assertTrue(
            any("Subtotal mismatch" in error for error in errors)
        )

    def test_wrong_total(self):
        invoice = self.valid_invoice.copy()
        invoice["total"] = 35000.0

        errors = validate_invoice(invoice)

        self.assertTrue(
            any("Total mismatch" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()