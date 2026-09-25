import json
from pathlib import Path

from ai_extractor import extract_invoice_with_ai
from main import extract_text_from_pdf


def main() -> None:
    """Extract invoice text and send it to Gemini."""

    project_root = Path(__file__).resolve().parents[1]
    pdf_path = project_root / "input" / "Sample_Invoice_AI_Test.pdf"

    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}")
        return

    try:
        # Read the PDF using our existing PDF extraction function.
        invoice_text = extract_text_from_pdf(pdf_path)

        # Send the extracted text to Gemini.
        invoice = extract_invoice_with_ai(invoice_text)

        print("========================================")
        print("AI STRUCTURED INVOICE DATA")
        print("========================================")

        print(
            json.dumps(
                invoice.model_dump(),
                indent=4,
                ensure_ascii=False,
            )
        )

    except Exception as exc:
        print(f"ERROR: AI invoice extraction failed: {exc}")


if __name__ == "__main__":
    main()