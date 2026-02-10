import { useMemo } from "react"
import { InvoiceByBrandChart } from "@/components/charts/invoice-by-brand-chart"
import { StatusOverviewChart } from "@/components/charts/status-overview-chart"
import { format } from "date-fns"

interface DashboardChartsProps {
  data: any[]
}

export function DashboardCharts({ data }: DashboardChartsProps) {
  
  const salesChartData = useMemo(() => {
    // Hardcoded OEM list to ensure consistent ordering and presence
    const OEMS = ["MRF", "Bridgestone", "Ceat", "Apollo", "Michelin"]

    const counts: Record<string, number> = {}
    if (data && data.length > 0) {
      data.forEach((curr) => {
        const oem = curr.oem || (curr.seller && String(curr.seller).split(" ")[0]) || "Unknown"
        counts[oem] = (counts[oem] || 0) + 1
      })
    }

    return OEMS.map((oem) => ({ name: oem, count: counts[oem] || 0 }))
  }, [data])

  const statusChartData = useMemo(() => {
    const counts = {
      success: 0,
      pending: 0,
      failed: 0,
    }

    if (data && data.length > 0) {
      data.forEach((curr) => {
        const status = curr.status.toLowerCase() as keyof typeof counts
        if (counts[status] !== undefined) {
          counts[status]++
        }
      })
    }

    return [
      { status: "success", count: counts.success, fill: "#00B765" },
      { status: "pending", count: counts.pending, fill: "orange" },
      { status: "failed", count: counts.failed, fill: "red" },
    ]
  }, [data])

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <InvoiceByBrandChart data={salesChartData} />
      <StatusOverviewChart data={statusChartData} />
    </div>
  )
}
