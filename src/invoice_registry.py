import json
from pathlib import Path
from typing import Any


def create_invoice_key(invoice: dict[str, Any]) -> str:
    """Create a unique key using supplier GSTIN and invoice number."""

    supplier_gstin = str(invoice.get("supplier_gstin") or "").strip().upper()
    invoice_number = str(invoice.get("invoice_number") or "").strip().upper()

    if not supplier_gstin or not invoice_number:
        raise ValueError(
            "Cannot create duplicate key: supplier GSTIN or invoice number is missing."
        )

    return f"{supplier_gstin}|{invoice_number}"


def load_registry(registry_path: Path) -> dict[str, Any]:
    """Load the processed invoice registry."""

    if not registry_path.exists():
        return {}

    try:
        with registry_path.open(
            "r",
            encoding="utf-8",
        ) as registry_file:
            data = json.load(registry_file)

        if not isinstance(data, dict):
            return {}

        return data

    except (json.JSONDecodeError, OSError):
        return {}


def save_registry(
    registry_path: Path,
    registry: dict[str, Any],
) -> None:
    """Save the processed invoice registry."""

    registry_path.parent.mkdir(parents=True, exist_ok=True)

    with registry_path.open(
        "w",
        encoding="utf-8",
    ) as registry_file:
        json.dump(
            registry,
            registry_file,
            indent=4,
            ensure_ascii=False,
        )


def is_duplicate_invoice(
    invoice: dict[str, Any],
    registry_path: Path,
) -> bool:
    """Check whether an invoice has already been processed."""

    invoice_key = create_invoice_key(invoice)
    registry = load_registry(registry_path)

    return invoice_key in registry


def register_invoice(
    invoice: dict[str, Any],
    pdf_name: str,
    registry_path: Path,
) -> None:
    """Register a successfully processed invoice."""

    invoice_key = create_invoice_key(invoice)
    registry = load_registry(registry_path)

    registry[invoice_key] = {
        "invoice_number": invoice.get("invoice_number"),
        "supplier_gstin": invoice.get("supplier_gstin"),
        "supplier_name": invoice.get("supplier_name"),
        "pdf_name": pdf_name,
    }

    save_registry(
        registry_path,
        registry,
    )