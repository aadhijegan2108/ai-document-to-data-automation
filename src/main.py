from pathlib import Path

from invoice_parser import extract_invoice_fields, validate_invoice
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from all pages of a PDF."""
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"\n--- Page {page_number} ---\n{text}")

    return "\n".join(pages)


def main() -> None:
    """Read the sample invoice, extract data, and validate it."""
    project_root = Path(__file__).resolve().parents[1]
    pdf_path = project_root / "input" / "Sample_Invoice_AI_Test.pdf"

    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}")
        return

    try:
        # Step 1: Extract raw text from the PDF.
        raw_text = extract_text_from_pdf(pdf_path)

        # Step 2: Convert raw text into structured invoice data.
        invoice = extract_invoice_fields(raw_text)

        # Step 3: Validate the extracted data.
        errors = validate_invoice(invoice)

        print("========================================")
        print("STRUCTURED INVOICE DATA")
        print("========================================")

        for key, value in invoice.items():
            print(f"{key}: {value}")

        print("\n========================================")
        print("VALIDATION")
        print("========================================")

        if errors:
            print("❌ Validation failed")

            for error in errors:
                print(f"- {error}")
        else:
            print("✅ Validation passed")

    except Exception as exc:
        print(f"ERROR: Could not process PDF: {exc}")


if __name__ == "__main__":
    main()