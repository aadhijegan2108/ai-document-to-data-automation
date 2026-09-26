# AI Document to Data Automation

## Problem

Businesses often receive information through PDFs and emails and
manually copy the information into spreadsheets or other systems.

This project explores how AI and automation can convert unstructured
business documents into structured, usable data.

## Planned Workflow

PDF / Document
↓
Text Extraction
↓
AI Data Extraction
↓
Validation
↓
Structured Data
↓
Excel / CSV

## Current Version
## Current Version

V0.2 - PDF extraction, structured invoice parsing, and validation

## Current Workflow

PDF Invoice
↓
PDF Text Extraction
↓
Structured Invoice Parsing
↓
Invoice Validation

## V0.2 Features

- Read PDF invoices using PyPDF
- Extract invoice fields
- Extract financial values
- Convert monetary values to numbers
- Validate subtotal + GST = total
- Detect extraction errors

## Technology

- Python
- PDF processing
- AI / LLM
- Structured data
- Excel / CSV
- Automation

## Project Goal

Build a practical automation that reduces manual document-processing
work and can eventually be tested with real businesses.

## Development Approach

Learn → Build → Test → Document → GitHub → Portfolio → Customer feedback

## Status

🚧 Under 
### V0.5 - CSV Export

- Export validated AI-extracted invoice data to CSV
- One row generated per invoice line item
- Includes invoice, supplier, customer, item, subtotal, GST, and total fields
- CSV export occurs only after invoice validation passes
- Tested successfully with Sample_Invoice_AI_Test.pdf