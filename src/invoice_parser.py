import re
from typing import Any


def extract_invoice_fields(text: str) -> dict[str, Any]:
    """Extract basic invoice fields from raw PDF text."""

    def find(pattern: str) -> str | None:
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    invoice = {
        "invoice_number": find(r"Invoice No\.\s*(?:\n)?([A-Z0-9-]+)"),
        "invoice_date": find(r"Invoice Date\s*(?:\n)?([0-9A-Za-z-]+)"),
        "due_date": find(r"Due Date\s*(?:\n)?([0-9A-Za-z-]+)"),
        "payment_terms": find(r"Payment Terms\s*(?:\n)?([A-Za-z0-9 ]+)"),
        "po_number": find(r"PO No\.\s*(?:\n)?([A-Z0-9-]+)"),
        "currency": find(r"Currency\s*(?:\n)?([A-Z]+)"),
        "supplier_gstin": find(r"GSTIN:\s*([A-Z0-9]+)"),
        "subtotal": find(r"Subtotal\s*\n?\s*([\d,]+\.\d{2})"),
        "gst": find(r"GST \(18%\)\s*\n?\s*([\d,]+\.\d{2})"),
        "total": find(r"(?mi)^\s*Total\s*$\s*([\d,]+\.\d{2})"),
    }

    # The first GSTIN belongs to the supplier.
    invoice["supplier_gstin"] = invoice["supplier_gstin"]

    # Convert money fields to numbers.
    for key in ("subtotal", "gst", "total"):
        if invoice[key]:
            invoice[key] = float(invoice[key].replace(",", ""))

    return invoice

def validate_invoice(invoice: dict[str, Any]) -> list[str]:
    """Validate extracted invoice data and return any errors."""
    errors: list[str] = []

    subtotal = invoice.get("subtotal")
    gst = invoice.get("gst")
    total = invoice.get("total")
    items = invoice.get("items", [])

    # Check required invoice totals.
    if subtotal is None:
        errors.append("Subtotal is missing.")

    if gst is None:
        errors.append("GST is missing.")

    if total is None:
        errors.append("Total is missing.")

    # Check each line item:
    # quantity × unit price should equal the item amount.
    item_amounts: list[float] = []

    for index, item in enumerate(items, start=1):
        quantity = item.get("quantity")
        unit_price = item.get("unit_price")
        amount = item.get("amount")

        if quantity is None or unit_price is None or amount is None:
            continue

        expected_amount = round(quantity * unit_price, 2)

        if round(amount, 2) != expected_amount:
            errors.append(
                f"Item {index} mismatch: expected {expected_amount:.2f}, "
                f"but extracted {amount:.2f}."
            )

        item_amounts.append(amount)

    # Check that the sum of line items equals the subtotal.
    if subtotal is not None and item_amounts:
        expected_subtotal = round(sum(item_amounts), 2)

        if round(subtotal, 2) != expected_subtotal:
            errors.append(
                f"Subtotal mismatch: expected {expected_subtotal:.2f}, "
                f"but extracted {subtotal:.2f}."
            )

    # Check subtotal + GST = total.
    if all(value is not None for value in (subtotal, gst, total)):
        expected_total = round(subtotal + gst, 2)

        if round(total, 2) != expected_total:
            errors.append(
                f"Total mismatch: expected {expected_total:.2f}, "
                f"but extracted {total:.2f}."
            )

    return errors