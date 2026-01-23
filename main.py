from openpyxl import Workbook
from phase1_pdf_to_excel.utils.pdf_extractor import PDFExtractor
from config.settings import OUTPUT_DIR


def extract_company_to_excel(pdf_path: str, output_filename: str = "invoice_data.xlsx"):
    """Extract company name from PDF and save to Excel."""
    # Extract company name from PDF using context manager
    with PDFExtractor(pdf_path) as extractor:
        company_name = extractor.get_company_name()

    print(f"Extracted company name: {company_name}")

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice Data"

    # Add headers and data
    ws["A1"] = "Company Name"
    ws["A2"] = company_name

    # Save to output directory
    output_path = OUTPUT_DIR / output_filename
    wb.save(output_path)

    print(f"Data saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    pdf_path = "/location/to/pdf"
    extract_company_to_excel(pdf_path)