import pdfplumber
import re


class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pdf = None
        self._full_text = None
        self._buyer_section = None

    # ---------------- PDF LIFECYCLE ----------------
    def open(self):
        self.pdf = pdfplumber.open(self.pdf_path)
        return self

    def close(self):
        if self.pdf:
            self.pdf.close()

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ---------------- COMMON HELPERS ----------------
    def get_full_text(self) -> str:
        if self._full_text is None:
            text = ""
            for page in self.pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            self._full_text = text
        return self._full_text

    def get_buyer_section(self) -> str:
        if self._buyer_section is None:
            full_text = self.get_full_text()
            section = ""

            match = re.search(r"Buyer\s*\(Bill\s*to\)", full_text, re.IGNORECASE)
            if match:
                section = full_text[match.end():]

            section = re.split(
                r"\bSl\b|\bDescription\b|\bGoods\b",
                section,
                flags=re.IGNORECASE
            )[0]

            self._buyer_section = section

        return self._buyer_section

    # ---------------- HEADER FIELDS ----------------
    def get_invoice_number(self) -> str:
        text = self.get_full_text()
        m = re.search(r"\b[A-Z]{2,}-[A-Z]{2,}-\d{3,}\b", text)
        return m.group(0) if m else "Not Found"

    def get_invoice_date(self) -> str:
        text = self.get_full_text()
        m = re.search(
            r"\b\d{2}-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{2,4}\b",
            text,
            re.IGNORECASE,
        )
        if m:
            return m.group(0)

        m = re.search(r"\b\d{2}-\d{2}-\d{4}\b", text)
        return m.group(0) if m else "Not Found"

    # ---------------- BODY FIELDS ----------------
    def get_company_name_only(self) -> str:
        page = self.pdf.pages[0]
        chars = page.chars

        bold_lines = {}
        for ch in sorted(chars, key=lambda c: (c["top"], c["x0"])):
            font = ch.get("fontname", "").lower()
            if "bold" in font and "italic" not in font:
                top = round(ch["top"], 0)
                bold_lines.setdefault(top, []).append(ch)

        for top in sorted(bold_lines):
            line = bold_lines[top]
            if min(c["x0"] for c in line) < 50:
                text = "".join(c["text"] for c in sorted(line, key=lambda x: x["x0"]))
                if "invoice" not in text.lower() and "tax" not in text.lower():
                    return text.strip()

        return "Not Found"

    # --------- CHANGED: ACCOUNT TYPE ----------
    def get_account_type(self) -> str:
        lines = [l.strip() for l in self.get_buyer_section().splitlines() if l.strip()]
        if not lines:
            return "Not Found"

        line = lines[0]
        line = re.split(
            r"Dispatched|Through|Destination|Via",
            line,
            flags=re.IGNORECASE
        )[0]

        return line.strip()

    # buyer name
    def get_buyer_name(self) -> str:
        lines = [l.strip() for l in self.get_buyer_section().splitlines() if l.strip()]
        for line in lines:
            clean = line.replace(",", "")
            if re.fullmatch(r"[A-Z][A-Z\.]+", clean):
                return clean
        return "Not Found"

    # mobile number
    def get_mobile_number(self) -> str:
        match = re.search(r"\b\d{10}\b", self.get_buyer_section())
        return match.group() if match else "Not Found"

    # --------- CHANGED: MODEL NAME ----------
    def get_model_name(self) -> str:
        text = self.get_buyer_section()
        candidates = re.findall(r"\b[A-Z]{3,10}\b", text)

        blacklist = {
            "DESTINATION", "DISPATCHED", "THROUGH",
            "STATE", "NAME", "CODE", "ACCOUNT", "BUYER", "MOB"
        }

        filtered = [w for w in candidates if w not in blacklist]
        return filtered[0] if filtered else "Not Found"

    # state name
    def get_state_name(self) -> str:
        match = re.search(
            r"State\s*Name\s*:\s*([A-Za-z ]+)",
            self.get_buyer_section(),
            re.IGNORECASE
        )
        return match.group(1).strip() if match else "Not Found"

    # state code
    def get_state_code(self) -> str:
        match = re.search(r"Code\s*:\s*(\d+)", self.get_buyer_section())
        return match.group(1) if match else "Not Found"

    # total amount
    def get_total_amount(self) -> str:
        match = re.search(r"₹\s?([\d,]+\.\d{2})", self.get_full_text())
        return match.group(1) if match else "Not Found"

    # description of goods
    def get_description_of_goods(self) -> str:
        text = self.get_full_text()
        for line in text.splitlines():
            line = line.strip()
            if line and line[0].isdigit():
                line = re.sub(r"^\d+\s+", "", line)
                parts = re.split(r"\b\d{8}\b", line)
                return parts[0].strip()
        return "Not Found"

    # item code
    def get_item_code(self) -> str:
        text = self.get_full_text()
        match = re.search(r"\b\d{8}\b", text)
        return match.group(0) if match else "Not Found"

    # ---------------- FINAL OUTPUT ----------------
    def get_company_name(self) -> str:
        if not self.pdf:
            self.open()

        return (
            "Invoice Number | Invoice Date | Mode / Terms of Payment | Seller Name | "
            "Buyer Name | Buyer Mobile | Product / Model | State | State Code | "
            "OEM / Description | Total Invoice Amount | Item Code\n"
            f"{self.get_invoice_number()} | {self.get_invoice_date()} | "
            f"{self.get_account_type()} | {self.get_company_name_only()} | "
            f"{self.get_buyer_name()} | {self.get_mobile_number()} | "
            f"{self.get_model_name()} | {self.get_state_name()} | "
            f"{self.get_state_code()} | {self.get_description_of_goods()} | "
            f"{self.get_total_amount()} | {self.get_item_code()}"
        )