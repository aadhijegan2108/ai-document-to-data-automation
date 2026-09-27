import sys
import unittest
from pathlib import Path


# Allow Python to import modules from the src folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from processing_result import ProcessingResult, ProcessingStatus


class TestProcessingResult(unittest.TestCase):

    def test_success_status(self):
        result = ProcessingResult(
            filename="invoice.pdf",
            status=ProcessingStatus.SUCCESS,
            message="Invoice processed successfully.",
        )

        self.assertEqual(
            result.status,
            ProcessingStatus.SUCCESS,
        )

        self.assertTrue(result.is_success)

    def test_duplicate_status(self):
        result = ProcessingResult(
            filename="invoice.pdf",
            status=ProcessingStatus.DUPLICATE,
            message="Invoice was already processed.",
        )

        self.assertEqual(
            result.status,
            ProcessingStatus.DUPLICATE,
        )

        self.assertFalse(result.is_success)

    def test_validation_failed_status(self):
        result = ProcessingResult(
            filename="invoice.pdf",
            status=ProcessingStatus.VALIDATION_FAILED,
            message="Invoice validation failed.",
            errors=["Total mismatch"],
        )

        self.assertEqual(
            result.status,
            ProcessingStatus.VALIDATION_FAILED,
        )

        self.assertFalse(result.is_success)

        self.assertEqual(
            result.errors,
            ["Total mismatch"],
        )

    def test_processing_error_status(self):
        result = ProcessingResult(
            filename="invoice.pdf",
            status=ProcessingStatus.PROCESSING_ERROR,
            message="Invoice processing failed.",
            errors=["PDF could not be read"],
        )

        self.assertEqual(
            result.status,
            ProcessingStatus.PROCESSING_ERROR,
        )

        self.assertFalse(result.is_success)

        self.assertEqual(
            result.errors,
            ["PDF could not be read"],
        )


if __name__ == "__main__":
    unittest.main()