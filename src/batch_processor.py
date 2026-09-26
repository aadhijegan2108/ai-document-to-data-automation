from pathlib import Path

from ai_extractor import extract_invoice_with_ai
from csv_exporter import export_invoice_to_csv
from excel_exporter import export_invoice_to_excel
from invoice_parser import validate_invoice
from logger import setup_logger
from main import extract_text_from_pdf


def process_invoice(
    pdf_path: Path,
    output_dir: Path,
    logger,
) -> tuple[bool, list[str]]:
    """Process one PDF invoice and export valid results."""

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

        # Step 4: Validate the extracted invoice.
        logger.info(f"Validating invoice: {pdf_path.name}")
        errors = validate_invoice(invoice_dict)

        if errors:
            logger.error(f"Validation failed: {pdf_path.name}")

            for error in errors:
                logger.error(f"{pdf_path.name}: {error}")

            return False, errors

        logger.info(f"Validation passed: {pdf_path.name}")

        # Step 5: Create output filenames using the PDF filename.
        csv_path = output_dir / f"{pdf_path.stem}.csv"
        excel_path = output_dir / f"{pdf_path.stem}.xlsx"

        # Step 6: Export validated invoice to CSV.
        export_invoice_to_csv(
            invoice_dict,
            csv_path,
        )

        logger.info(f"CSV export successful: {csv_path.name}")

        # Step 7: Export validated invoice to Excel.
        export_invoice_to_excel(
            invoice_dict,
            excel_path,
        )

        logger.info(f"Excel export successful: {excel_path.name}")

        return True, []

    except Exception as exc:
        error_message = str(exc)

        logger.exception(
            f"Processing failed: {pdf_path.name} | {error_message}"
        )

        return False, [error_message]


def main() -> None:
    """Process all PDF invoices in the input directory."""

    project_root = Path(__file__).resolve().parents[1]

    input_dir = project_root / "input"
    output_dir = project_root / "output"

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

    for pdf_path in pdf_files:
        success, _errors = process_invoice(
            pdf_path,
            output_dir,
            logger,
        )

        if success:
            successful += 1
        else:
            failed += 1

    logger.info("=" * 60)
    logger.info("BATCH INVOICE PROCESSING COMPLETED")
    logger.info(
        f"Summary | Total: {len(pdf_files)} | "
        f"Successful: {successful} | Failed: {failed}"
    )
    logger.info("=" * 60)

    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total invoices : {len(pdf_files)}")
    print(f"Successful     : {successful}")
    print(f"Failed         : {failed}")
    print(f"Output folder  : {output_dir}")
    print(f"Log file       : {project_root / 'logs' / 'invoice_processing.log'}")


if __name__ == "__main__":
    main()