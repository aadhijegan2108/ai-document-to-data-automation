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
from pdf_extractor import extract_text_from_pdf
from processing_result import ProcessingResult, ProcessingStatus


def process_invoice(
    pdf_path: Path,
    output_dir: Path,
    registry_path: Path,
    logger,
) -> ProcessingResult:
    """Process one PDF invoice and return a structured result."""

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
            message = "Invoice was already processed."

            logger.warning(
                f"Duplicate invoice detected: {pdf_path.name}"
            )

            return ProcessingResult(
                filename=pdf_path.name,
                status=ProcessingStatus.DUPLICATE,
                message=message,
            )

        # Step 5: Validate the extracted invoice.
        logger.info(f"Validating invoice: {pdf_path.name}")
        errors = validate_invoice(invoice_dict)

        if errors:
            logger.error(
                f"Validation failed: {pdf_path.name}"
            )

            for error in errors:
                logger.error(
                    f"{pdf_path.name}: {error}"
                )

            return ProcessingResult(
                filename=pdf_path.name,
                status=ProcessingStatus.VALIDATION_FAILED,
                message="Invoice validation failed.",
                errors=errors,
            )

        logger.info(
            f"Validation passed: {pdf_path.name}"
        )

        # Step 6: Create output filenames.
        csv_path = output_dir / f"{pdf_path.stem}.csv"
        excel_path = output_dir / f"{pdf_path.stem}.xlsx"

        # Step 7: Export validated invoice to CSV.
        export_invoice_to_csv(
            invoice_dict,
            csv_path,
        )

        logger.info(
            f"CSV export successful: {csv_path.name}"
        )

        # Step 8: Export validated invoice to Excel.
        export_invoice_to_excel(
            invoice_dict,
            excel_path,
        )

        logger.info(
            f"Excel export successful: {excel_path.name}"
        )

        # Step 9: Register the invoice after successful processing.
        register_invoice(
            invoice_dict,
            pdf_path.name,
            registry_path,
        )

        logger.info(
            f"Invoice registered successfully: {pdf_path.name}"
        )

        return ProcessingResult(
            filename=pdf_path.name,
            status=ProcessingStatus.SUCCESS,
            message="Invoice processed and exported successfully.",
        )

    except Exception as exc:
        error_message = str(exc)

        logger.exception(
            f"Processing failed: {pdf_path.name} | {error_message}"
        )

        return ProcessingResult(
            filename=pdf_path.name,
            status=ProcessingStatus.PROCESSING_ERROR,
            message="Invoice processing failed.",
            errors=[error_message],
        )


def main() -> None:
    """Process all PDF invoices in the input directory."""

    project_root = Path(__file__).resolve().parents[1]

    input_dir = project_root / "input"
    output_dir = project_root / "output"
    registry_path = project_root / "data" / "invoice_registry.json"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = setup_logger(project_root)

    logger.info("=" * 60)
    logger.info("BATCH INVOICE PROCESSING STARTED")
    logger.info("=" * 60)

    pdf_files = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() == ".pdf"
    )

    if not pdf_files:
        logger.warning(
            f"No PDF invoices found in: {input_dir}"
        )

        print(f"No PDF invoices found in: {input_dir}")
        return

    logger.info(
        f"Found {len(pdf_files)} PDF invoice(s)"
    )

    results: list[ProcessingResult] = []

    for pdf_path in pdf_files:
        result = process_invoice(
            pdf_path,
            output_dir,
            registry_path,
            logger,
        )

        results.append(result)

    successful = sum(
        result.status == ProcessingStatus.SUCCESS
        for result in results
    )

    duplicates = sum(
        result.status == ProcessingStatus.DUPLICATE
        for result in results
    )

    validation_failed = sum(
        result.status == ProcessingStatus.VALIDATION_FAILED
        for result in results
    )

    processing_errors = sum(
        result.status == ProcessingStatus.PROCESSING_ERROR
        for result in results
    )

    failed = validation_failed + processing_errors

    logger.info("=" * 60)
    logger.info("BATCH INVOICE PROCESSING COMPLETED")
    logger.info(
        f"Summary | Total: {len(results)} | "
        f"Successful: {successful} | "
        f"Duplicates: {duplicates} | "
        f"Validation Failed: {validation_failed} | "
        f"Processing Errors: {processing_errors}"
    )
    logger.info("=" * 60)

    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total invoices        : {len(results)}")
    print(f"Successful            : {successful}")
    print(f"Duplicates            : {duplicates}")
    print(f"Validation failures   : {validation_failed}")
    print(f"Processing errors     : {processing_errors}")
    print(f"Total failed          : {failed}")
    print(f"Output folder         : {output_dir}")
    print(f"Registry file         : {registry_path}")
    print(
        f"Log file              : "
        f"{project_root / 'logs' / 'invoice_processing.log'}"
    )

    # Display individual non-success results.
    for result in results:
        if result.status != ProcessingStatus.SUCCESS:
            print(
                f"\n{result.status.value.upper()}: "
                f"{result.filename}"
            )
            print(f"Message: {result.message}")

            for error in result.errors:
                print(f"- {error}")


if __name__ == "__main__":
    main()