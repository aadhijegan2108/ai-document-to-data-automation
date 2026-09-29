import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import MagicMock, patch


# Allow Python to import modules from the src folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from batch_processor import process_batch
from config import create_config
from processing_result import ProcessingResult, ProcessingStatus


class TestBatchProcessor(unittest.TestCase):

    def test_empty_input_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir)

            config = create_config()

            config = replace(
                config,
                input_dir=input_dir,
            )

            logger = MagicMock()

            results = process_batch(
                config,
                logger,
            )

            self.assertEqual(
                results,
                [],
            )

    @patch("batch_processor.process_invoice")
    def test_processes_all_pdf_files(
        self,
        mock_process_invoice,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir)

            pdf_a = input_dir / "invoice_a.pdf"
            pdf_b = input_dir / "invoice_b.pdf"

            txt_file = input_dir / "notes.txt"

            pdf_a.write_bytes(b"test")
            pdf_b.write_bytes(b"test")
            txt_file.write_text(
                "This is not a PDF invoice.",
                encoding="utf-8",
            )

            config = create_config()

            config = replace(
                config,
                input_dir=input_dir,
            )

            logger = MagicMock()

            result_a = ProcessingResult(
                filename="invoice_a.pdf",
                status=ProcessingStatus.SUCCESS,
                message="Processed successfully.",
            )

            result_b = ProcessingResult(
                filename="invoice_b.pdf",
                status=ProcessingStatus.DUPLICATE,
                message="Invoice was already processed.",
            )

            mock_process_invoice.side_effect = [
                result_a,
                result_b,
            ]

            results = process_batch(
                config,
                logger,
            )

            self.assertEqual(
                results,
                [result_a, result_b],
            )

            self.assertEqual(
                mock_process_invoice.call_count,
                2,
            )

            first_call = mock_process_invoice.call_args_list[0]
            second_call = mock_process_invoice.call_args_list[1]

            self.assertEqual(
                first_call.args[0],
                pdf_a,
            )

            self.assertEqual(
                second_call.args[0],
                pdf_b,
            )

            self.assertEqual(
                first_call.args[1],
                config,
            )

            self.assertEqual(
                first_call.args[2],
                logger,
            )

    @patch("batch_processor.process_invoice")
    def test_processes_pdf_files_in_sorted_order(
        self,
        mock_process_invoice,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir)

            pdf_c = input_dir / "invoice_c.pdf"
            pdf_a = input_dir / "invoice_a.pdf"
            pdf_b = input_dir / "invoice_b.pdf"

            for pdf_file in [pdf_c, pdf_a, pdf_b]:
                pdf_file.write_bytes(b"test")

            config = create_config()

            config = replace(
                config,
                input_dir=input_dir,
            )

            logger = MagicMock()

            mock_process_invoice.side_effect = [
                ProcessingResult(
                    filename="invoice_a.pdf",
                    status=ProcessingStatus.SUCCESS,
                ),
                ProcessingResult(
                    filename="invoice_b.pdf",
                    status=ProcessingStatus.SUCCESS,
                ),
                ProcessingResult(
                    filename="invoice_c.pdf",
                    status=ProcessingStatus.SUCCESS,
                ),
            ]

            results = process_batch(
                config,
                logger,
            )

            filenames = [
                result.filename
                for result in results
            ]

            self.assertEqual(
                filenames,
                [
                    "invoice_a.pdf",
                    "invoice_b.pdf",
                    "invoice_c.pdf",
                ],
            )

    @patch("batch_processor.process_invoice")
    def test_returns_mixed_processing_results(
        self,
        mock_process_invoice,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir)

            pdf_a = input_dir / "invoice_a.pdf"
            pdf_b = input_dir / "invoice_b.pdf"
            pdf_c = input_dir / "invoice_c.pdf"

            for pdf_file in [pdf_a, pdf_b, pdf_c]:
                pdf_file.write_bytes(b"test")

            config = create_config()

            config = replace(
                config,
                input_dir=input_dir,
            )

            logger = MagicMock()

            success_result = ProcessingResult(
                filename="invoice_a.pdf",
                status=ProcessingStatus.SUCCESS,
            )

            duplicate_result = ProcessingResult(
                filename="invoice_b.pdf",
                status=ProcessingStatus.DUPLICATE,
            )

            failed_result = ProcessingResult(
                filename="invoice_c.pdf",
                status=ProcessingStatus.PROCESSING_ERROR,
                errors=["Test processing error"],
            )

            mock_process_invoice.side_effect = [
                success_result,
                duplicate_result,
                failed_result,
            ]

            results = process_batch(
                config,
                logger,
            )

            self.assertEqual(
                results,
                [
                    success_result,
                    duplicate_result,
                    failed_result,
                ],
            )

            self.assertEqual(
                results[0].status,
                ProcessingStatus.SUCCESS,
            )

            self.assertEqual(
                results[1].status,
                ProcessingStatus.DUPLICATE,
            )

            self.assertEqual(
                results[2].status,
                ProcessingStatus.PROCESSING_ERROR,
            )


if __name__ == "__main__":
    unittest.main()