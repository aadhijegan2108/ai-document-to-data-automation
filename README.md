# AI Document to Data Automation

## Problem

Businesses often receive information through PDFs and emails and manually
copy the information into spreadsheets or other systems.

This project explores how AI and automation can convert unstructured
business documents into structured, usable data.

## Planned Workflow

PDF / Document

↓

Text Extraction

↓

AI Data Extraction

↓

Duplicate Detection

↓

Validation

↓

Structured Data

↓

Excel / CSV

## Current Version

V0.9 - Duplicate Invoice Detection

## Current Workflow

PDF Invoice

↓

PDF Text Extraction

↓

AI Structured Invoice Extraction

↓

Duplicate Detection

↓

Invoice Validation

↓

CSV / Excel Export

↓

Logging

## V0.2 - PDF Extraction and Validation

- Read PDF invoices using PyPDF
- Extract invoice fields
- Extract financial values
- Convert monetary values to numbers
- Validate subtotal + GST = total
- Detect extraction errors

## V0.3 - Gemini AI Structured Extraction

- Extract structured invoice data using Gemini
- Use structured AI output for invoice fields
- Extract supplier and customer information separately
- Extract invoice line items
- Convert AI output into structured invoice data

## V0.4 - Automated Validation Tests

- Test valid invoices
- Test incorrect line-item amounts
- Test incorrect subtotals
- Test incorrect invoice totals
- Verify that invoice validation detects extraction errors automatically

## V0.5 - CSV Export

- Export validated AI-extracted invoice data to CSV
- One row generated per invoice line item
- Includes invoice, supplier, customer, item, subtotal, GST, and total fields
- CSV export occurs only after invoice validation passes
- Tested successfully with Sample_Invoice_AI_Test.pdf

## V0.6 - Excel Export

- Export validated AI-extracted invoice data to Excel
- Create separate `Invoice Summary` and `Line Items` worksheets
- Preserve invoice, supplier, customer, financial, and line-item data
- Automatically adjust column widths
- Excel export occurs only after invoice validation passes
- Tested successfully with Sample_Invoice_AI_Test.pdf

## V0.7 - Batch Invoice Processing

- Automatically detect all PDF invoices in the input directory
- Process multiple invoices in a single run
- Apply Gemini structured extraction to each invoice
- Validate each invoice independently
- Export valid invoices to CSV and Excel
- Report successful and failed invoice counts
- Tested successfully with 3 PDF invoices

## V0.8 - Error Handling and Logging

- Added centralized application logging
- Record PDF extraction, AI extraction, validation, and export steps
- Record validation failures and unexpected processing errors
- Continue batch processing when an individual invoice fails
- Store processing history in `logs/invoice_processing.log`
- Tested with both valid and intentionally corrupted PDF input

## V0.9 - Duplicate Invoice Detection

- Added invoice registry for previously processed invoices
- Detect duplicates using supplier GSTIN and invoice number
- Skip duplicate invoices before validation and export
- Register invoices only after successful validation and export
- Track duplicate invoices separately from failed invoices
- Store the registry in `data/invoice_registry.json`
- Tested successfully by processing the same invoice twice

## Technology

- Python
- PyPDF
- Gemini AI / LLM
- Pydantic
- Structured data
- CSV
- Excel
- openpyxl
- Logging
- Automation

## Project Goal

Build a practical automation that reduces manual document-processing
work and can eventually be tested with real businesses.

## Development Approach

Learn → Build → Test → Document → GitHub → Portfolio → Customer feedback

## Status

🚧 Under active development

## Future Development

- V1.0 - Complete end-to-end document automation
- Support for broader document workflows
- Improved error handling and reporting
- Additional document types
- User-facing automation interface
