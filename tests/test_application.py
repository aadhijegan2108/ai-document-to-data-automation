import sys
import tempfile
import unittest
from dataclasses import replace
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

    @patch("application.setup_logger")
    @patch("application.process_batch")
    def test_application_passes_config_and_logger(
        self,
        mock_process_batch,
        mock_setup_logger,
    ):
        config = create_config()

        mock_logger = mock_setup_logger.return_value

        mock_process_batch.return_value = []

        results, summary = run_application(config)

        self.assertEqual(
            results,
            [],
        )

        self.assertEqual(
            summary.total,
            0,
        )

        mock_setup_logger.assert_called_once_with(
            config,
        )

        mock_process_batch.assert_called_once_with(
            config,
            mock_logger,
        )

    @patch("application.setup_logger")
    @patch("application.process_batch")
    def test_application_creates_required_directories(
        self,
        mock_process_batch,
        mock_setup_logger,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            config = create_config()

            config = replace(
                config,
                project_root=project_root,
                output_dir=project_root / "output",
                data_dir=project_root / "data",
            )

            mock_process_batch.return_value = []

            run_application(config)

            self.assertTrue(
                config.output_dir.exists()
            )

            self.assertTrue(
                config.output_dir.is_dir()
            )

            self.assertTrue(
                config.data_dir.exists()
            )

            self.assertTrue(
                config.data_dir.is_dir()
            )


if __name__ == "__main__":
    unittest.main()