
import { format } from "date-fns"
import { fetchInvoicesCsv } from "./sheets"


export async function loadInvoices() {
  // If VITE_SHEET_ID is provided, try to fetch published CSV from Google Sheets
  const sheetId = (import.meta.env as any).VITE_SHEET_ID
  const sheetName = (import.meta.env as any).VITE_SHEET_NAME || "Sheet1"

  if (sheetId) {
    try {
      const rows = await fetchInvoicesCsv(sheetId, sheetName)
      // Normalize fields and ensure invoiceDate is ISO when possible
      return rows.map((r: any) => ({
        invoiceNumber: r.invoiceNumber || "",
        invoiceDate: format(new Date(r.invoiceDate || Date.now()), "yyyy-MM-dd"),
        modeTerms: r.modeTerms || "",
        seller: r.seller || "",
        buyer: r.buyer || "",
        mobile: r.mobile || "",
        product: r.product || "",
        state: r.state || "",
        stateCode: r.stateCode || "",
        oem: r.oem || (r.seller ? String(r.seller).split(" ")[0] : ""),
        totalAmount: r.totalAmount || 0,
        totalAmountDisplay: r.totalAmountDisplay || `₹${r.totalAmount || 0}`,
        itemCode: r.itemCode || "",
        qty: r.qty || 0,
        rate: r.rate || "",
        status: r.status || "Pending",
        error: r.error || "",
        processedDate: format(new Date(r.processedDate || Date.now()), "yyyy-MM-dd"),
      }))
    } catch (err) {
      console.warn("Failed to load sheet, falling back to mock invoices:", err)
    }
  }

}

