
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


# Allow Python to import modules from the src folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from invoice_processor import process_invoice
from config import create_config
from processing_result import ProcessingStatus


class TestProcessInvoice(unittest.TestCase):

    def setUp(self):
        self.config = create_config()

        self.logger = MagicMock()

        self.invoice_path = Path("test_invoice.pdf")

        self.invoice_data = {
            "invoice_number": "INV-001",
            "supplier_gstin": "33TESTGSTIN1Z5",
            "supplier_name": "Test Supplier",
            "subtotal": 1000.0,
            "gst": 180.0,
            "total": 1180.0,
            "items": [
                {
                    "item_number": 1,
                    "description": "Test Item",
                    "quantity": 2.0,
                    "unit_price": 500.0,
                    "amount": 1000.0,
                }
            ],
        }

    @patch("invoice_processor.extract_invoice_with_ai")
    @patch("invoice_processor.validate_invoice")
    @patch("invoice_processor.is_duplicate_invoice")
    @patch("invoice_processor.export_invoice_to_csv")
    @patch("invoice_processor.export_invoice_to_excel")
    @patch("invoice_processor.register_invoice")
    @patch("invoice_processor.extract_text_from_pdf")
    def test_success(
        self,
        mock_extract_text,
        mock_register,
        mock_excel_export,
        mock_csv_export,
        mock_duplicate_check,
        mock_validate,
        mock_ai_extract,
    ):
        mock_extract_text.return_value = "invoice text"

        mock_invoice = MagicMock()
        mock_invoice.model_dump.return_value = self.invoice_data

        mock_ai_extract.return_value = mock_invoice
        mock_duplicate_check.return_value = False
        mock_validate.return_value = []

        result = process_invoice(
            self.invoice_path,
            self.config,
            self.logger,
        )

        self.assertEqual(
            result.status,
            ProcessingStatus.SUCCESS,
        )

        self.assertEqual(
            result.filename,
            "test_invoice.pdf",
        )

        self.assertEqual(
            result.errors,
            [],
        )

        mock_csv_export.assert_called_once()
        mock_excel_export.assert_called_once()
        mock_register.assert_called_once()

    @patch("invoice_processor.validate_invoice")
    @patch("invoice_processor.is_duplicate_invoice")
    @patch("invoice_processor.extract_invoice_with_ai")
    @patch("invoice_processor.extract_text_from_pdf")
    def test_duplicate(
        self,
        mock_extract_text,
        mock_ai_extract,
        mock_duplicate_check,
        mock_validate,
    ):
        mock_extract_text.return_value = "invoice text"

        mock_invoice = MagicMock()
        mock_invoice.model_dump.return_value = self.invoice_data

        mock_ai_extract.return_value = mock_invoice
        mock_duplicate_check.return_value = True

        result = process_invoice(
            self.invoice_path,
            self.config,
            self.logger,
        )

        self.assertEqual(
            result.status,
            ProcessingStatus.DUPLICATE,
        )

        self.assertEqual(
            result.message,
            "Invoice was already processed.",
        )

        mock_validate.assert_not_called()

    @patch("invoice_processor.is_duplicate_invoice")
    @patch("invoice_processor.extract_invoice_with_ai")
    @patch("invoice_processor.extract_text_from_pdf")
    @patch("invoice_processor.validate_invoice")
    def test_validation_failed(
        self,
        mock_validate,
        mock_extract_text,
        mock_ai_extract,
        mock_duplicate_check,
    ):
        mock_extract_text.return_value = "invoice text"

        mock_invoice = MagicMock()
        mock_invoice.model_dump.return_value = self.invoice_data

        mock_ai_extract.return_value = mock_invoice
        mock_duplicate_check.return_value = False

        validation_errors = [
            "Total mismatch",
        ]

        mock_validate.return_value = validation_errors

        result = process_invoice(
            self.invoice_path,
            self.config,
            self.logger,
        )

        self.assertEqual(
            result.status,
            ProcessingStatus.VALIDATION_FAILED,
        )

        self.assertEqual(
            result.message,
            "Invoice validation failed.",
        )

        self.assertEqual(
            result.errors,
            validation_errors,
        )

    @patch("invoice_processor.extract_invoice_with_ai")
    @patch("invoice_processor.extract_text_from_pdf")
    def test_processing_error(
        self,
        mock_extract_text,
        mock_ai_extract,
    ):
        mock_extract_text.side_effect = RuntimeError(
            "PDF extraction failed"
        )

        result = process_invoice(
            self.invoice_path,
            self.config,
            self.logger,
        )

        self.assertEqual(
            result.status,
            ProcessingStatus.PROCESSING_ERROR,
        )

        self.assertEqual(
            result.message,
            "Invoice processing failed.",
        )

        self.assertEqual(
            result.errors,
            ["PDF extraction failed"],
        )


if __name__ == "__main__":
    unittest.main()
