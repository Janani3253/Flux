# Flux

A PDF to Excel extraction pipeline for processing invoice data.

## Installation

### Prerequisites

- Python 3.10 or higher

### Setup

1. Clone the repository:

```bash
git clone https://github.com/Agan-org/Flux.git
cd Flux
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install pdfplumber openpyxl pytest
```

## Project Structure

```
flux/
├── config/
│   └── settings.py          # Configuration and paths
├── data/
│   ├── input/                # Place PDF files here
│   └── output/               # Extracted Excel files
├── phase1_pdf_to_excel/
│   └── utils/
│       └── pdf_extractor.py  # PDF extraction logic
├── phase2_excel_to_web/      # Web pipeline (future)
├── tests/                    # Test files
└── main.py                   # Main entry point
```

## Usage

1. Place your PDF invoice in the `data/input/` directory.

2. Run the PDF extractor:

```bash
python main.py <path-to-pdf>
```

Example:

```bash
python main.py data/input/invoice.pdf
```

3. Find the output Excel file in `data/output/invoice_data.xlsx`.

## Running Tests

Run all tests:

```bash
pytest tests/ -v
```

Run a specific test:

```bash
pytest tests/test_pdf_extractor.py -v
```

## Dependencies

| Package | Purpose |
|---------|---------|
| pdfplumber | PDF text extraction |
| openpyxl | Excel file creation |
| pytest | Testing framework |