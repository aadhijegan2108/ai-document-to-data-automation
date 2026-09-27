import sys
import tempfile
import unittest
from pathlib import Path


# Allow Python to import modules from the src folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from invoice_registry import (
    create_invoice_key,
    is_duplicate_invoice,
    load_registry,
    register_invoice,
)


class TestInvoiceRegistry(unittest.TestCase):

    def setUp(self):
        self.invoice = {
            "invoice_number": "INV-2026-1045",
            "supplier_gstin": "33ABCDE1234F1Z5",
            "supplier_name": "SAMPLE INDUSTRIAL SUPPLIES",
        }

    def test_create_invoice_key(self):
        key = create_invoice_key(self.invoice)

        self.assertEqual(
            key,
            "33ABCDE1234F1Z5|INV-2026-1045",
        )

    def test_new_invoice_is_not_duplicate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "invoice_registry.json"

            result = is_duplicate_invoice(
                self.invoice,
                registry_path,
            )

            self.assertFalse(result)

    def test_registered_invoice_is_duplicate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "invoice_registry.json"

            register_invoice(
                self.invoice,
                "Sample_Invoice_AI_Test.pdf",
                registry_path,
            )

            result = is_duplicate_invoice(
                self.invoice,
                registry_path,
            )

            self.assertTrue(result)

    def test_registry_is_saved_correctly(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            registry_path = Path(temp_dir) / "invoice_registry.json"

            register_invoice(
                self.invoice,
                "Sample_Invoice_AI_Test.pdf",
                registry_path,
            )

            registry = load_registry(registry_path)

            key = "33ABCDE1234F1Z5|INV-2026-1045"

            self.assertIn(key, registry)

            self.assertEqual(
                registry[key]["invoice_number"],
                "INV-2026-1045",
            )

            self.assertEqual(
                registry[key]["supplier_gstin"],
                "33ABCDE1234F1Z5",
            )

            self.assertEqual(
                registry[key]["pdf_name"],
                "Sample_Invoice_AI_Test.pdf",
            )


if __name__ == "__main__":
    unittest.main()