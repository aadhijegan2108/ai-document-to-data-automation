import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch


# Allow Python to import modules from the src folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from main import main
from processing_result import ProcessingResult, ProcessingStatus


class TestMain(unittest.TestCase):

    @patch("main.run_application")
    def test_main_reports_successful_batch(
        self,
        mock_run_application,
    ):
        expected_result = ProcessingResult(
            filename="test_invoice.pdf",
            status=ProcessingStatus.SUCCESS,
            message="Invoice processed successfully.",
        )

        mock_summary = type(
            "MockSummary",
            (),
            {
                "total": 1,
                "successful": 1,
                "duplicates": 0,
                "validation_failed": 0,
                "processing_errors": 0,
                "failed": 0,
            },
        )()

        mock_run_application.return_value = (
            [expected_result],
            mock_summary,
        )

        with patch(
            "sys.stdout",
            new_callable=StringIO,
        ) as mock_stdout:

            main()

        output = mock_stdout.getvalue()

        self.assertIn(
            "BATCH PROCESSING COMPLETE",
            output,
        )

        self.assertIn(
            "Total invoices        : 1",
            output,
        )

        self.assertIn(
            "Successful            : 1",
            output,
        )

        self.assertIn(
            "Total failed          : 0",
            output,
        )

        mock_run_application.assert_called_once()

    @patch("main.run_application")
    def test_main_reports_non_success_result(
        self,
        mock_run_application,
    ):
        expected_result = ProcessingResult(
            filename="invalid_invoice.pdf",
            status=ProcessingStatus.VALIDATION_FAILED,
            message="Invoice validation failed.",
            errors=[
                "Invoice total does not match subtotal + GST."
            ],
        )

        mock_summary = type(
            "MockSummary",
            (),
            {
                "total": 1,
                "successful": 0,
                "duplicates": 0,
                "validation_failed": 1,
                "processing_errors": 0,
                "failed": 1,
            },
        )()

        mock_run_application.return_value = (
            [expected_result],
            mock_summary,
        )

        with patch(
            "sys.stdout",
            new_callable=StringIO,
        ) as mock_stdout:

            main()

        output = mock_stdout.getvalue()

        self.assertIn(
            "VALIDATION_FAILED: invalid_invoice.pdf",
            output,
        )

        self.assertIn(
            "Message: Invoice validation failed.",
            output,
        )

        self.assertIn(
            "Invoice total does not match subtotal + GST.",
            output,
        )

        self.assertIn(
            "Validation failures   : 1",
            output,
        )

        self.assertIn(
            "Total failed          : 1",
            output,
        )

        mock_run_application.assert_called_once()


if __name__ == "__main__":
    unittest.main()