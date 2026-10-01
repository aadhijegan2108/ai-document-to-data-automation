from pathlib import Path

from ai_extractor import extract_invoice_with_ai
from config import AppConfig
from csv_exporter import export_invoice_to_csv
from excel_exporter import export_invoice_to_excel
from invoice_parser import validate_invoice
from invoice_registry import (
    is_duplicate_invoice,
    register_invoice,
)
from pdf_extractor import extract_text_from_pdf
from processing_result import ProcessingResult, ProcessingStatus
from invoice_processor import process_invoice

def process_batch(
    config: AppConfig,
    logger,
) -> list[ProcessingResult]:
    """Process all PDF invoices in the configured input directory."""

    pdf_files = sorted(
        path
        for path in config.input_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() == ".pdf"
    )

    if not pdf_files:
        logger.warning(
            f"No PDF invoices found in: "
            f"{config.input_dir}"
        )

        return []

    logger.info(
        f"Found {len(pdf_files)} PDF invoice(s)"
    )

    results: list[ProcessingResult] = []

    for pdf_path in pdf_files:
        result = process_invoice(
            pdf_path,
            config,
            logger,
        )

        results.append(result)

    return results