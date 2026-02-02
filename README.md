# Flux 

An end-to-end invoice automation pipeline that extracts data from PDF invoices, converts it to Excel, intelligently matches OEMs, and automates ERP Sales Invoice creation using Playwright.

---

##  Features

* **Phase 1: PDF Intelligence** – High-accuracy extraction of invoice metadata using `pdfplumber`.
* **Intelligent Matching** – Multi-layered OEM identification (Substring, Token, and Fuzzy matching via `RapidFuzz`).
* **Phase 2: ERP Automation** – Seamless data entry into ERPNext using Playwright with resilient, delay-aware navigation.
* **Robust Testing** – Comprehensive test suite for both data extraction and UI automation.

---

##  Installation

### Prerequisites

* Python **3.10 or higher**
* Google Chrome (Required for Playwright)
* Windows / Linux / macOS

### Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Agan-org/Flux.git](https://github.com/Agan-org/Flux.git)
    cd Flux
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install pdfplumber openpyxl pandas rapidfuzz pytest playwright
    ```

4.  **Install Playwright browser binaries:**
    ```bash
    playwright install
    ```

---

##  Project Structure

```text
FLUX-WORKING/
│
├── config/
│   ├── credentials.properties      # ERP credentials (username/password mapping)
│   └── settings.py                  # Global configuration & paths
│
├── data/
│   ├── input/                       # Input PDF invoices
│   ├── output/                      # Extracted Excel files
│   └── temp/                        # Runtime JSON files for automation
│       ├── login_tasks.json
│       └── playwright_tasks.json
│
├── phase1_pdf_to_excel/
│   ├── pages/
│   └── utils/
│       └── pdf_extractor.py         # PDF → structured Excel extraction
│
├── phase2_excel_to_web/
│   ├── pages/
│   │   ├── login_page.py            # ERP login automation (Playwright)
│   │   └── sales_invoice_page.py    # Sales Invoice form automation
│   │
│   ├── tests/
│   │   └── test_login.py            # End-to-end Playwright test
│   │
│   ├── utils/
│   │   ├── credential_loader.py     # Secure credential access
│   │   ├── oem_matcher.py            # OEM matching & normalization logic
│   │   ├── run_oem_match.py          # Phase-2 orchestration runner
│   │   └── conftest.py               #  Pytest + Playwright fixtures
│
├── tests/
│   └── test_pdf_extractor.py         # Phase-1 unit tests
│
├── venv/                             # Python virtual environment
│
├── .gitignore
├── main.py                           # Main entry point (PDF → Excel)
└── README.md


 Workflow Overview
Phase 1 – PDF to Excel

Extracts structured invoice data using pdfplumber and generates Excel output.

Captured fields:

Invoice Number & Date

Buyer Details

OEM / Item Description

Total Invoice Amount

State and Tax Information

Output location:

data/output/invoice_data.xlsx

Phase 2 – Excel to ERP Automation

Reads extracted Excel data and performs OEM matching using:

Substring & Token-based matching

Fuzzy matching (RapidFuzz)

Automates ERPNext Sales Invoice creation via Playwright.

 Usage
PDF Extraction

Place invoice PDFs inside:

data/input/


Run:

python main.py data/input/invoice.pdf


Output:

data/output/invoice_data.xlsx

OEM Matching & ERP Automation

Run the full automation pipeline:

python -m phase2_excel_to_web.utils.run_oem_match --debug --run-tests


Optional flags:

Flag	Description
--save-excel	Save matched Excel output
--debug	Show OEM match score & method
--run-tests	Execute Playwright automation
 Running Tests
Test Type	Command
Run all tests	pytest -v
PDF extraction only	pytest tests/test_pdf_extractor.py -v
Playwright automation only	pytest phase2_excel_to_web/tests -s

 Dependencies
Package	Purpose
pdfplumber	PDF text extraction
openpyxl	Excel file creation
pandas	Data processing
rapidfuzz	OEM fuzzy matching
playwright	Browser automation
pytest	Testing framework