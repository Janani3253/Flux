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
import subprocess
import json
import os
import pandas as pd

try:
    from phase2_excel_to_web.utils.oem_matcher import attach_credentials
except Exception as exc:
    print("Failed to import `attach_credentials`:", exc)
    raise


# ---------------- ARGUMENT PARSER ----------------
def parse_args():
    p = argparse.ArgumentParser(description="Run OEM matcher and optionally trigger Playwright automation.")

    p.add_argument("--invoices", default="data/output/invoice_data.xlsx", help="Path to invoices Excel file")
    p.add_argument("--oem", default="data/input/oem_list.xlsx", help="Path to OEM list Excel file")
    p.add_argument("--out", default="data/output/invoices_with_oem.xlsx", help="Output Excel file path")
    p.add_argument("--invoice-col", default="OEM / Description", help="Column in invoices containing OEM/raw text")
    p.add_argument("--oem-col", default="OEM", help="Column in OEM list with OEM names")
    p.add_argument("--fuzz", type=int, default=85, help="Fuzzy matching threshold (0-100)")
    p.add_argument("--debug", action="store_true", help="Print match scores and methods")

    # optional flags
    p.add_argument("--save-excel", action="store_true", help="Save matched output to Excel")
    p.add_argument("--run-tests", action="store_true", help="Run Playwright pytest automation")

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

    invoices = pd.read_excel(invoices_path)
    oem_df = pd.read_excel(oem_path)

    try:
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

    # ---------------- SAVE EXCEL (OPTIONAL) ----------------
    if args.save_excel:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        result.to_excel(out_path, index=False)
        print(f"Excel saved to: {out_path}")

    # ---------------- PASS DATA TO PYTEST (JSON) ----------------
    temp_dir = Path("data/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)

   # --- ORIGINAL LOGIN TASKS (UNCHANGED) ---
    login_json = temp_dir / "login_tasks.json"
    result.to_json(login_json, orient="records", indent=2)
    os.environ["LOGIN_TASKS_FILE"] = str(login_json.resolve())

    # --- TEMP PLAYWRIGHT TASKS (HARD-CODED SAFE VALUES) ---

    # --- USE PREBUILT PLAYWRIGHT TASKS JSON ---
    playwright_json = temp_dir / "playwright_tasks.json"

    if not playwright_json.exists():
        raise FileNotFoundError(
            f"Playwright tasks JSON not found at {playwright_json}. "
            "You said this file is manually prepared."
        )

    os.environ["PLAYWRIGHT_TASKS_FILE"] = str(playwright_json.resolve())



    # ---------------- RUN AUTOMATION ----------------
    if args.run_tests:
        print("\nRunning Playwright automation...\n")
        subprocess.run(
            ["pytest", "phase2_excel_to_web/tests", "-s"],
            check=True
        )

    unmatched = int(result["matched_oem"].isna().sum())
    print(f"\nOEM matching completed — Rows: {len(result)}, Unmatched: {unmatched}")

    return 0


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    raise SystemExit(main())
