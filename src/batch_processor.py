from pathlib import Path

from ai_extractor import extract_invoice_with_ai
from csv_exporter import export_invoice_to_csv
from excel_exporter import export_invoice_to_excel
from invoice_parser import validate_invoice
from main import extract_text_from_pdf


def process_invoice(
    pdf_path: Path,
    output_dir: Path,
) -> tuple[bool, list[str]]:
    """Process one PDF invoice and export valid results."""

    try:
        print("\n" + "=" * 60)
        print(f"PROCESSING: {pdf_path.name}")
        print("=" * 60)

        # Step 1: Extract text from the PDF.
        invoice_text = extract_text_from_pdf(pdf_path)

        # Step 2: Extract structured invoice data using Gemini.
        invoice = extract_invoice_with_ai(invoice_text)

        # Step 3: Convert the Pydantic object to a dictionary.
        invoice_dict = invoice.model_dump()

        # Step 4: Validate the extracted invoice.
        errors = validate_invoice(invoice_dict)

        if errors:
            print("❌ Validation failed")

            for error in errors:
                print(f"- {error}")

            return False, errors

        print("✅ Validation passed")

        # Step 5: Create output filenames using the PDF filename.
        csv_path = output_dir / f"{pdf_path.stem}.csv"
        excel_path = output_dir / f"{pdf_path.stem}.xlsx"

        # Step 6: Export validated invoice to CSV.
        export_invoice_to_csv(
            invoice_dict,
            csv_path,
        )

        print(f"✅ CSV exported: {csv_path.name}")

        # Step 7: Export validated invoice to Excel.
        export_invoice_to_excel(
            invoice_dict,
            excel_path,
        )

        print(f"✅ Excel exported: {excel_path.name}")

        return True, []

    except Exception as exc:
        error_message = str(exc)

        print(f"❌ Processing failed: {error_message}")

        return False, [error_message]


def main() -> None:
    """Process all PDF invoices in the input directory."""

    project_root = Path(__file__).resolve().parents[1]

    input_dir = project_root / "input"
    output_dir = project_root / "output"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all PDF files in the input folder.
    pdf_files = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    if not pdf_files:
        print(f"No PDF invoices found in: {input_dir}")
        return

    print("========================================")
    print("BATCH INVOICE PROCESSING")
    print("========================================")
    print(f"Found {len(pdf_files)} PDF invoice(s)")

    successful = 0
    failed = 0

    for pdf_path in pdf_files:
        success, _errors = process_invoice(
            pdf_path,
            output_dir,
        )

        if success:
            successful += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total invoices : {len(pdf_files)}")
    print(f"Successful     : {successful}")
    print(f"Failed         : {failed}")
    print(f"Output folder  : {output_dir}")


if __name__ == "__main__":
    main()