import sys
import unittest
from pathlib import Path


# Allow Python to import modules from the src folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from batch_reporter import BatchSummary, create_batch_summary
from processing_result import ProcessingResult, ProcessingStatus


class TestBatchReporter(unittest.TestCase):

    def test_empty_batch(self):
        summary = create_batch_summary([])

        self.assertIsInstance(summary, BatchSummary)
        self.assertEqual(summary.total, 0)
        self.assertEqual(summary.successful, 0)
        self.assertEqual(summary.duplicates, 0)
        self.assertEqual(summary.validation_failed, 0)
        self.assertEqual(summary.processing_errors, 0)
        self.assertEqual(summary.failed, 0)

    def test_mixed_batch(self):
        results = [
            ProcessingResult(
                filename="invoice_001.pdf",
                status=ProcessingStatus.SUCCESS,
            ),
            ProcessingResult(
                filename="invoice_002.pdf",
                status=ProcessingStatus.SUCCESS,
            ),
            ProcessingResult(
                filename="invoice_003.pdf",
                status=ProcessingStatus.DUPLICATE,
            ),
            ProcessingResult(
                filename="invoice_004.pdf",
                status=ProcessingStatus.VALIDATION_FAILED,
                errors=["Total mismatch"],
            ),
            ProcessingResult(
                filename="invoice_005.pdf",
                status=ProcessingStatus.PROCESSING_ERROR,
                errors=["PDF could not be read"],
            ),
        ]

        summary = create_batch_summary(results)

        self.assertEqual(summary.total, 5)
        self.assertEqual(summary.successful, 2)
        self.assertEqual(summary.duplicates, 1)
        self.assertEqual(summary.validation_failed, 1)
        self.assertEqual(summary.processing_errors, 1)
        self.assertEqual(summary.failed, 2)

    def test_all_successful(self):
        results = [
            ProcessingResult(
                filename="invoice_001.pdf",
                status=ProcessingStatus.SUCCESS,
            ),
            ProcessingResult(
                filename="invoice_002.pdf",
                status=ProcessingStatus.SUCCESS,
            ),
        ]

        summary = create_batch_summary(results)

        self.assertEqual(summary.total, 2)
        self.assertEqual(summary.successful, 2)
        self.assertEqual(summary.duplicates, 0)
        self.assertEqual(summary.failed, 0)

    def test_all_duplicates(self):
        results = [
            ProcessingResult(
                filename="invoice_001.pdf",
                status=ProcessingStatus.DUPLICATE,
            ),
            ProcessingResult(
                filename="invoice_002.pdf",
                status=ProcessingStatus.DUPLICATE,
            ),
        ]

        summary = create_batch_summary(results)

        self.assertEqual(summary.total, 2)
        self.assertEqual(summary.successful, 0)
        self.assertEqual(summary.duplicates, 2)
        self.assertEqual(summary.failed, 0)


if __name__ == "__main__":
    unittest.main()