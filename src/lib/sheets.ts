export async function fetchInvoicesCsv(spreadsheetIdOrUrl: string, sheetName = "Sheet1") {
  // Accept either a full published CSV URL, a spreadsheet id, or a published `e` id (starts with 2PACX-)
  const trimmed = String(spreadsheetIdOrUrl || "").trim()
  const isUrl = /^https?:\/\//i.test(trimmed)
  let url: string

  if (isUrl) {
    url = trimmed
    console.log("Fetching sheet from provided URL:", url);
  } else if (/^2PACX-/i.test(trimmed)) {
    // Published /d/e/ IDs (the 'e' token) — construct a published CSV URL (assume gid=0)
    url = `https://docs.google.com/spreadsheets/d/e/${trimmed}/pub?gid=0&single=true&output=csv`
    console.log("Fetching sheet from published e/id:", url);
} else {
    // Normal spreadsheet id
    url = `https://docs.google.com/spreadsheets/d/${trimmed}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent(
      sheetName
    )}`
    console.log("Fetching sheet from spreadsheet ID:", url);
  }

  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`Failed to fetch sheet from ${url}: ${res.status} ${res.statusText}`)
  }

  const text = await res.text()
  const rows = text.split("\n").filter((r) => r.trim() !== "")
  if (!rows.length) return []

  // Basic CSV line parser that handles quoted fields
  const parseLine = (line: string) => {
    const result: string[] = []
    let cur = ""
    let inQuotes = false
    for (let i = 0; i < line.length; i++) {
      const ch = line[i]
      if (ch === '"') {
        if (inQuotes && line[i + 1] === '"') {
          cur += '"'
          i++
        } else {
          inQuotes = !inQuotes
        }
      } else if (ch === "," && !inQuotes) {
        result.push(cur)
        cur = ""
      } else {
        cur += ch
      }
    }
    result.push(cur)
    return result
  }

  const headers = parseLine(rows[0]).map((h) => h.trim())
  const data = rows.slice(1).map((r) => {
    const cols = parseLine(r)
    const obj: Record<string, string> = {}
    headers.forEach((h, i) => (obj[h] = (cols[i] ?? "").trim()))
    return obj
  })

  // Map CSV columns to invoice shape (best-effort by header names)
  return data.map((row) => ({
    invoiceNumber: row["Invoice Number"] || "",
    invoiceDate: row["Invoice Date"] || "",
    modeTerms: row["Mode / Terms of Payment"] || "",
    seller: row["Seller Name"] || "",
    buyer: row["Buyer Name"] || "",
    mobile: row["Buyer Mobile"] || "",
    product: row["Product / Model"] || "",
    state: row["State"] || "",
    stateCode: row["State Code"] || "",
    oem: row["OEM"] || "",
    totalAmount: Number(row["Total Invoice Amount"].replace(/[^0-9.-]+/g, "") || "0") || 0,
    itemCode: row["Item Code"] || "",
    qty: Number(row["Quantity"] || "0") || 0,
    rate: row["Rate"] || "",
    status: row["Status"] || "Pending",
    error: row["Error"] || "",
    processedDate: row["Processed Date"] || "",
  }))
}
