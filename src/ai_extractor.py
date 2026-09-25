import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


# Load the API key from .env
load_dotenv()


class InvoiceItem(BaseModel):
    """One line item from an invoice."""

    item_number: Optional[int] = None
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


class InvoiceData(BaseModel):
    """Structured invoice data returned by the AI model."""

    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    payment_terms: Optional[str] = None
    po_number: Optional[str] = None
    currency: Optional[str] = None

    supplier_name: Optional[str] = None
    supplier_gstin: Optional[str] = None

    customer_name: Optional[str] = None
    customer_gstin: Optional[str] = None

    items: list[InvoiceItem] = Field(default_factory=list)

    subtotal: Optional[float] = None
    gst: Optional[float] = None
    total: Optional[float] = None


def extract_invoice_with_ai(invoice_text: str) -> InvoiceData:
    """Send invoice text to Gemini and return structured invoice data."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY was not found in .env")

    client = genai.Client(api_key=api_key)

    prompt = f"""
Extract the invoice information from the text below.

Rules:
- Extract only information explicitly present in the document.
- Do not invent missing values.
- Use null when a field is not present.
- Convert monetary values to numbers without commas or currency symbols.
- Preserve invoice dates as they appear.
- Extract every invoice line item.
- Extract supplier and customer information separately.

Invoice text:
----------------
{invoice_text}
----------------
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InvoiceData,
        ),
    )

    if response.parsed is None:
        raise RuntimeError("Gemini did not return structured invoice data.")

    return response.parsed