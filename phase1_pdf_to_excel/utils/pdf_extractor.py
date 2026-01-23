import pdfplumber


class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pdf = None

    def open(self):
        """Open PDF file."""
        self.pdf = pdfplumber.open(self.pdf_path)
        return self

    def close(self):
        """Close PDF file."""
        if self.pdf:
            self.pdf.close()

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_company_name(self) -> str:
        """Extract company name - bold text at top-left (second bold line)."""
        if not self.pdf:
            self.open()

        page = self.pdf.pages[0]
        chars = page.chars

        # Group bold (non-italic) characters by line
        bold_lines = {}
        for char in sorted(chars, key=lambda c: (c["top"], c["x0"])):
            font = char.get("fontname", "").lower()
            if "bold" in font and "italic" not in font:
                top = round(char["top"], 0)
                if top not in bold_lines:
                    bold_lines[top] = []
                bold_lines[top].append({"x0": char["x0"], "text": char["text"]})

        # Sort lines by vertical position
        sorted_lines = sorted(bold_lines.keys())

        # Company name is typically the second bold line at left margin
        for top in sorted_lines:
            chars_in_line = bold_lines[top]
            first_x = min(c["x0"] for c in chars_in_line)

            # Check if line starts at left margin (x0 < 50)
            if first_x < 50:
                text = "".join([c["text"] for c in sorted(chars_in_line, key=lambda x: x["x0"])])
                # Skip header lines (usually contain INVOICE, TAX, etc.)
                if "invoice" not in text.lower() and "tax" not in text.lower():
                    return text.strip()

        return ""