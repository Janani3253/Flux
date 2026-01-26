from openpyxl import Workbook
from phase1_pdf_to_excel.utils.pdf_extractor import PDFExtractor
from config.settings import OUTPUT_DIR


def extract_company_to_excel(pdf_path: str, output_filename: str = "invoice_data.xlsx"):
    """Extract invoice data from PDF and save to Excel."""
    with PDFExtractor(pdf_path) as extractor:
        company_name = extractor.get_company_name()

    print(f"Extracted data:\n{company_name}")

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice Data"

    # -------- CORRECT EXCEL WRITING --------
    lines = company_name.splitlines()

    headers = lines[0].split(" | ")
    values = lines[1].split(" | ")

    ws.append(headers)   
    ws.append(values)    
    # --------------------------------------

    # Save to output directory
    output_path = OUTPUT_DIR / output_filename
    wb.save(output_path)

    print(f"Data saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <path-to-pdf>")
        sys.exit(1)

    extract_company_to_excel(sys.argv[1])
