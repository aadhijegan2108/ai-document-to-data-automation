import json
from pathlib import Path

from ai_extractor import extract_invoice_with_ai
from csv_exporter import export_invoice_to_csv
from excel_exporter import export_invoice_to_excel
from invoice_parser import validate_invoice
from main import extract_text_from_pdf


def main() -> None:
    """Extract invoice text, send it to Gemini, validate, and export valid data."""

    project_root = Path(__file__).resolve().parents[1]
    pdf_path = project_root / "input" / "Sample_Invoice_AI_Test.pdf"
    csv_path = project_root / "output" / "validated_invoice.csv"
    excel_path = project_root / "output" / "validated_invoice.xlsx"

    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}")
        return

    try:
        # Step 1: Read the PDF and extract its text.
        invoice_text = extract_text_from_pdf(pdf_path)

        # Step 2: Send the invoice text to Gemini.
        invoice = extract_invoice_with_ai(invoice_text)

        # Step 3: Convert the Pydantic object to a normal dictionary.
        invoice_dict = invoice.model_dump()

        print("========================================")
        print("AI STRUCTURED INVOICE DATA")
        print("========================================")

        print(
            json.dumps(
                invoice_dict,
                indent=4,
                ensure_ascii=False,
            )
        )

        # Step 4: Validate the AI-extracted invoice.
        errors = validate_invoice(invoice_dict)

        print("\n========================================")
        print("AI VALIDATION")
        print("========================================")

        if errors:
            print("❌ AI invoice validation failed")

            for error in errors:
                print(f"- {error}")

        else:
            print("✅ AI invoice validation passed")

            # Step 5: Export the validated invoice to CSV.
            export_invoice_to_csv(
                invoice_dict,
                csv_path,
            )

            print("\n========================================")
            print("CSV EXPORT")
            print("========================================")
            print(f"✅ CSV exported successfully: {csv_path}")

            # Step 6: Export the validated invoice to Excel.
            export_invoice_to_excel(
                invoice_dict,
                excel_path,
            )

            print("\n========================================")
            print("EXCEL EXPORT")
            print("========================================")
            print(f"✅ Excel exported successfully: {excel_path}")

    except Exception as exc:
        print(f"ERROR: AI invoice extraction failed: {exc}")


if __name__ == "__main__":
    main()