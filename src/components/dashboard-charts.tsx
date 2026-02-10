import { useMemo } from "react"
import { SalesOverviewChart } from "@/components/charts/sales-overview-chart"
import { StatusOverviewChart } from "@/components/charts/status-overview-chart"
import { format } from "date-fns"

interface DashboardChartsProps {
  data: any[]
}

export function DashboardCharts({ data }: DashboardChartsProps) {
  
  const salesChartData = useMemo(() => {
    // Initialize all 12 months with 0
    const allMonths = Array.from({ length: 12 }, (_, i) => {
      const d = new Date(new Date().getFullYear(), i, 1)
      return { 
        name: format(d, 'MMM'), 
        _monthIndex: i 
      }
    })

    const grouped = allMonths.reduce((acc, curr) => {
      acc[curr.name] = { ...curr }
      return acc
    }, {} as Record<string, any>)

    if (data && data.length > 0) {
      data.forEach(curr => {
        const date = new Date(curr.invoiceDate)
        const month = format(date, 'MMM')
        
        // Only aggregating for months that match our buckets (should be all)
        if (grouped[month]) {
          // Calculate by count of invoices per seller, not total amount
          grouped[month][curr.seller] = (grouped[month][curr.seller] || 0) + 1
        }
      })
    }

    return Object.values(grouped)
        .sort((a: any, b: any) => a._monthIndex - b._monthIndex)
        .map((item: any) => {
          const { _monthIndex, ...rest } = item
          return rest
        }) as any[]
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
      <SalesOverviewChart data={salesChartData} />
      <StatusOverviewChart data={statusChartData} />
    </div>
  )
}
