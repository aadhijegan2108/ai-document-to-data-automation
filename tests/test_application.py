import sys
import unittest
from pathlib import Path
from unittest.mock import patch


# Allow Python to import modules from the src folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from application import run_application
from config import create_config
from processing_result import ProcessingResult, ProcessingStatus


class TestApplication(unittest.TestCase):

    def test_no_pdf_files_returns_empty_results(self):
        config = create_config()

        with patch(
            "application.process_batch",
            return_value=[],
        ):
            results, summary = run_application(config)

        self.assertEqual(
            results,
            [],
        )

        self.assertEqual(
            summary.total,
            0,
        )

        self.assertEqual(
            summary.successful,
            0,
        )

        self.assertEqual(
            summary.duplicates,
            0,
        )

        self.assertEqual(
            summary.failed,
            0,
        )

    @patch("application.process_batch")
    def test_application_processes_batch(
        self,
        mock_process_batch,
    ):
        config = create_config()

        expected_result = ProcessingResult(
            filename="test_invoice.pdf",
            status=ProcessingStatus.SUCCESS,
            message="Invoice processed successfully.",
        )

        mock_process_batch.return_value = [
            expected_result
        ]

        results, summary = run_application(config)

        self.assertEqual(
            results,
            [expected_result],
        )

        self.assertEqual(
            summary.total,
            1,
        )

        self.assertEqual(
            summary.successful,
            1,
        )

        self.assertEqual(
            summary.failed,
            0,
        )

        mock_process_batch.assert_called_once()

        call_args = mock_process_batch.call_args

        self.assertEqual(
            call_args.args[0],
            config,
        )


if __name__ == "__main__":
    unittest.main()