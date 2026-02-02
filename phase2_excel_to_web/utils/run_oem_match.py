"""
Run OEM matching over invoice and OEM list Excel files.

Default behavior:
- Match OEMs in memory
- DO NOT generate output Excel

Optional:
- --save-excel → save matched result to Excel
- --run-tests  → trigger pytest (Playwright automation)
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import pytest

from phase2_excel_to_web.shared.runtime_store import RUNTIME_DATA

try:
    from phase2_excel_to_web.utils.oem_matcher import attach_credentials
except Exception as exc:
    print("Failed to import `attach_credentials`:", exc)
    raise


# ---------------- ARGUMENT PARSER ----------------
def parse_args():
    p = argparse.ArgumentParser(description="Run OEM matcher and optionally trigger Playwright automation.")
        
    

    p.add_argument( "--invoices",default="data/output/invoicedata_as_per_tool.xlsx",help="Path to invoices Excel file")
    p.add_argument("--oem",default="data/input/oem_list.xlsx",help="Path to OEM list Excel file")
    p.add_argument("--out",default="data/output/invoices_with_oem.xlsx",help="Output Excel file path")
    p.add_argument("--invoice-col",default="OEM / Description",help="Column in invoices containing OEM/raw text")
    p.add_argument("--oem-col",default="OEM",help="Column in OEM list with OEM names")
    p.add_argument("--fuzz",type=int,default=85,help="Fuzzy matching threshold (0-100)")
    p.add_argument("--debug",action="store_true",help="Print match scores and methods")
    p.add_argument("--save-excel",action="store_true",help="Save matched output to Excel")
    p.add_argument("--run-tests",action="store_true",help="Run Playwright pytest automation")

    return p.parse_args()


# ---------------- MAIN ----------------
def main(argv: list[str] | None = None) -> int:
    args = parse_args() if argv is None else parse_args()

    invoices_path = Path(args.invoices)
    oem_path = Path(args.oem)
    out_path = Path(args.out)

    if not invoices_path.exists():
        print(f"Invoices file not found: {invoices_path}")
        return 2

    if not oem_path.exists():
        print(f"OEM list file not found: {oem_path}")
        return 2

    # ---------------- LOAD EXCEL ----------------
    invoices = pd.read_excel(invoices_path)
    oem_df = pd.read_excel(oem_path)

    try:
        # ---------------- DEBUG OEM MATCH ----------------
        if args.debug:
            from phase2_excel_to_web.utils.oem_matcher import match_oem

            details = match_oem(
                invoices[args.invoice_col],
                oem_df[args.oem_col],
                fuzz_threshold=args.fuzz,
                return_details=True
            )

            print("\nMatch details:\n")
            print(invoices[[args.invoice_col]].join(details))

        # ---------------- OEM + CREDENTIAL ATTACH ----------------
        result = attach_credentials(
            invoices,
            oem_df,
            invoice_col=args.invoice_col,
            oem_col=args.oem_col,
            fuzz_threshold=args.fuzz
        )

    except Exception as exc:
        print("Error during attach_credentials:", exc)
        raise

    # ---------------- ENSURE STATUS / ERROR ----------------
    if "Status" not in result.columns:
        result["Status"] = ""

    if "Error" not in result.columns:
        result["Error"] = ""

    # ---------------- STORE FULL DATA IN RAM (EMULATOR STYLE) ----------------
    # Playwright WILL use username / URL from here
    RUNTIME_DATA["invoices"] = result.to_dict(orient="records")

    # ---------------- RUN PLAYWRIGHT ----------------
    if args.run_tests:
        print("\nRunning Playwright automation...\n")

        # pytest runs in SAME Python process → shared RAM
        pytest.main(["phase2_excel_to_web/tests", "-s"])

        # ---------------- WRITE BACK CLEAN EXCEL ----------------
        final_df = pd.DataFrame(RUNTIME_DATA["invoices"])

        #  REMOVE AUTOMATION-ONLY COLUMNS BEFORE SAVING
        DROP_COLUMNS = ["username", "URL", "matched_oem","OEM"]

        final_df = final_df.drop(
            columns=[c for c in DROP_COLUMNS if c in final_df.columns],
            errors="ignore"
        )

        final_df.to_excel(invoices_path, index=False)
        print("\nStatus / Error updated in Excel")

    unmatched = int(result["matched_oem"].isna().sum())
    print(f"\nOEM matching completed — Rows: {len(result)}, Unmatched: {unmatched}")

    return 0


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    raise SystemExit(main())
