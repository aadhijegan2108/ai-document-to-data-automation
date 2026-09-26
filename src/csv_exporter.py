import csv
from pathlib import Path
from typing import Any


def export_invoice_to_csv(
    invoice: dict[str, Any],
    output_path: Path,
) -> None:
    """Export validated invoice data to a CSV file."""

    fieldnames = [
        "invoice_number",
        "invoice_date",
        "due_date",
        "payment_terms",
        "po_number",
        "currency",
        "supplier_name",
        "supplier_gstin",
        "customer_name",
        "customer_gstin",
        "item_number",
        "description",
        "quantity",
        "unit_price",
        "amount",
        "subtotal",
        "gst",
        "total",
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        items = invoice.get("items", [])

        for item in items:
            writer.writerow(
                {
                    "invoice_number": invoice.get("invoice_number"),
                    "invoice_date": invoice.get("invoice_date"),
                    "due_date": invoice.get("due_date"),
                    "payment_terms": invoice.get("payment_terms"),
                    "po_number": invoice.get("po_number"),
                    "currency": invoice.get("currency"),
                    "supplier_name": invoice.get("supplier_name"),
                    "supplier_gstin": invoice.get("supplier_gstin"),
                    "customer_name": invoice.get("customer_name"),
                    "customer_gstin": invoice.get("customer_gstin"),
                    "item_number": item.get("item_number"),
                    "description": item.get("description"),
                    "quantity": item.get("quantity"),
                    "unit_price": item.get("unit_price"),
                    "amount": item.get("amount"),
                    "subtotal": invoice.get("subtotal"),
                    "gst": invoice.get("gst"),
                    "total": invoice.get("total"),
                }
            )