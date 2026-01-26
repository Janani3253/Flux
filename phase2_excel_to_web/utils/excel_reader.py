import pandas as pd
from pathlib import Path

EXCEL_PATH = Path("data/output/invoices_with_oem.xlsx")


def read_login_data():
    df = pd.read_excel(EXCEL_PATH)
    return df.to_dict(orient="records")
