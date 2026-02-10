
import { subDays, format } from "date-fns"

export const generateInvoices = () => {
  const statuses = ["Success", "Pending", "Failed"]
  const sellers = ["MRF Tyres Ltd", "Bridgestone India", "Ceat Ltd", "Apollo Tyres", "Michelin India"]
  
  return Array.from({ length: 300 }).map((_, i) => {
    // Generate dates within the last 365 days for realistic data
    const date = subDays(new Date(), Math.floor(Math.random() * 365))
    
    return {
      invoiceNumber: `INV-${String(i + 1).padStart(3, "0")}`,
      invoiceDate: date.toISOString(), // Store as ISO string for easier parsing
      invoiceDateDisplay: format(date, "yyyy-MM-dd"),
      modeTerms: "Credit 30 Days",
      seller: sellers[i % sellers.length],
      buyer: `Buyer ${i + 1}`,
      mobile: `+91 9${String(i).padStart(9, "0")}`,
      product: "Tyre Product",
      state: "Tamil Nadu",
      stateCode: "33",
      oem: sellers[i % sellers.length].split(" ")[0],
      totalAmount: Math.floor(Math.random() * 10000 + 1000), 
      totalAmountDisplay: `₹${(Math.random() * 10000 + 1000).toFixed(0)}`,
      itemCode: `ITEM-${i + 1}`,
      qty: Math.floor(Math.random() * 5) + 1,
      rate: "₹2,000",
      status: statuses[i % statuses.length],
      error: statuses[i % statuses.length] === "Failed" ? "Network Error" : "-",
      processedDate: format(date, "yyyy-MM-dd HH:mm a"),
    }
  })
}

export const salesData = [
  { month: "January", mrf: 186, bridgestone: 80, ceat: 100, apollo: 150 },
  { month: "February", mrf: 305, bridgestone: 200, ceat: 150, apollo: 220 },
  { month: "March", mrf: 237, bridgestone: 120, ceat: 180, apollo: 190 },
  { month: "April", mrf: 73, bridgestone: 190, ceat: 120, apollo: 130 },
  { month: "May", mrf: 209, bridgestone: 130, ceat: 140, apollo: 160 },
  { month: "June", mrf: 214, bridgestone: 140, ceat: 160, apollo: 180 },
  { month: "July", mrf: 186, bridgestone: 80, ceat: 100, apollo: 150 },
  { month: "August", mrf: 305, bridgestone: 200, ceat: 150, apollo: 220 },
  { month: "September", mrf: 237, bridgestone: 120, ceat: 180, apollo: 190 },
  { month: "October", mrf: 73, bridgestone: 190, ceat: 120, apollo: 130 },
  { month: "November", mrf: 209, bridgestone: 130, ceat: 140, apollo: 160 },
  { month: "December", mrf: 214, bridgestone: 140, ceat: 160, apollo: 180 },
]
