from pathlib import Path

from ai_extractor import extract_invoice_with_ai
from csv_exporter import export_invoice_to_csv
from excel_exporter import export_invoice_to_excel
from invoice_parser import validate_invoice
from invoice_registry import (
    is_duplicate_invoice,
    register_invoice,
)
from logger import setup_logger
from main import extract_text_from_pdf


def process_invoice(
    pdf_path: Path,
    output_dir: Path,
    registry_path: Path,
    logger,
) -> str:
    """Process one PDF invoice and export valid, non-duplicate results."""

    logger.info(f"Processing invoice: {pdf_path.name}")

    try:
        # Step 1: Extract text from the PDF.
        logger.info(f"Extracting text from: {pdf_path.name}")
        invoice_text = extract_text_from_pdf(pdf_path)

        # Step 2: Extract structured invoice data using Gemini.
        logger.info(f"Sending invoice to Gemini: {pdf_path.name}")
        invoice = extract_invoice_with_ai(invoice_text)

        # Step 3: Convert the Pydantic object to a dictionary.
        invoice_dict = invoice.model_dump()

        # Step 4: Check whether this invoice was already processed.
        try:
            duplicate = is_duplicate_invoice(
                invoice_dict,
                registry_path,
            )
        except ValueError as exc:
            logger.warning(
                f"Duplicate check skipped for {pdf_path.name}: {exc}"
            )
            duplicate = False

        if duplicate:
            logger.warning(
                f"Duplicate invoice detected: {pdf_path.name}"
            )
            return "duplicate"

        # Step 5: Validate the extracted invoice.
        logger.info(f"Validating invoice: {pdf_path.name}")
        errors = validate_invoice(invoice_dict)

        if errors:
            logger.error(f"Validation failed: {pdf_path.name}")

            for error in errors:
                logger.error(f"{pdf_path.name}: {error}")

            return "failed"

        logger.info(f"Validation passed: {pdf_path.name}")

        # Step 6: Create output filenames using the PDF filename.
        csv_path = output_dir / f"{pdf_path.stem}.csv"
        excel_path = output_dir / f"{pdf_path.stem}.xlsx"

        # Step 7: Export validated invoice to CSV.
        export_invoice_to_csv(
            invoice_dict,
            csv_path,
        )

        logger.info(f"CSV export successful: {csv_path.name}")

        # Step 8: Export validated invoice to Excel.
        export_invoice_to_excel(
            invoice_dict,
            excel_path,
        )

        logger.info(f"Excel export successful: {excel_path.name}")

        # Step 9: Register the invoice only after successful processing.
        register_invoice(
            invoice_dict,
            pdf_path.name,
            registry_path,
        )

        logger.info(
            f"Invoice registered successfully: {pdf_path.name}"
        )

        return "success"

    except Exception as exc:
        error_message = str(exc)

        logger.exception(
            f"Processing failed: {pdf_path.name} | {error_message}"
        )

        return "failed"


def main() -> None:
    """Process all PDF invoices in the input directory."""

    project_root = Path(__file__).resolve().parents[1]

    input_dir = project_root / "input"
    output_dir = project_root / "output"
    registry_path = project_root / "data" / "invoice_registry.json"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Set up application logging.
    logger = setup_logger(project_root)

    logger.info("=" * 60)
    logger.info("BATCH INVOICE PROCESSING STARTED")
    logger.info("=" * 60)

    # Find all PDF files in the input folder.
    pdf_files = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    if not pdf_files:
        logger.warning(f"No PDF invoices found in: {input_dir}")

        print(f"No PDF invoices found in: {input_dir}")
        return

    logger.info(f"Found {len(pdf_files)} PDF invoice(s)")

    successful = 0
    failed = 0
    duplicates = 0

    for pdf_path in pdf_files:
        status = process_invoice(
            pdf_path,
            output_dir,
            registry_path,
            logger,
        )

        if status == "success":
            successful += 1

        elif status == "duplicate":
            duplicates += 1

        else:
            failed += 1

    logger.info("=" * 60)
    logger.info("BATCH INVOICE PROCESSING COMPLETED")
    logger.info(
        f"Summary | Total: {len(pdf_files)} | "
        f"Successful: {successful} | "
        f"Duplicates: {duplicates} | "
        f"Failed: {failed}"
    )
    logger.info("=" * 60)

    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total invoices : {len(pdf_files)}")
    print(f"Successful     : {successful}")
    print(f"Duplicates     : {duplicates}")
    print(f"Failed         : {failed}")
    print(f"Output folder  : {output_dir}")
    print(f"Registry file  : {registry_path}")
    print(
        f"Log file       : "
        f"{project_root / 'logs' / 'invoice_processing.log'}"
    )


if __name__ == "__main__":
    main()