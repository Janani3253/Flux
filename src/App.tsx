
import * as React from "react"
import { useState, useMemo, useEffect } from "react"
import { AppSidebar } from "@/components/app-sidebar"
import {
  SidebarInset,
  SidebarProvider,
} from "@/components/ui/sidebar"
import { AppHeader } from "@/components/app-header"
import { DashboardHeader } from "@/components/dashboard-header" 
import { DashboardStats } from "@/components/dashboard-stats" 
import { DashboardCharts } from "@/components/dashboard-charts" 
import { DashboardInvoiceTable } from "@/components/dashboard-invoice-table"
import type { DateRange } from "react-day-picker"
import { addDays, startOfMonth, endOfMonth, subMonths, startOfYear, isWithinInterval, startOfDay, endOfDay, startOfWeek, endOfWeek } from "date-fns"
import { generateInvoices } from "@/lib/data"

export default function App() {
  const [period, setPeriod] = useState("today")
  // Default to this month
  const [date, setDate] = useState<DateRange | undefined>({
    from: startOfDay(new Date()),
    to: endOfDay(new Date()),
  })
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState<string | null>(null)

  const invoices = useMemo(() => generateInvoices(), [])

  useEffect(() => {
    const today = new Date()
    if (period === "today") {
      setDate({ from: startOfDay(today), to: endOfDay(today) })
    } else if (period === "this-week") {
      setDate({ from: startOfWeek(today), to: endOfWeek(today) })
    } else if (period === "this-month") {
      setDate({ from: startOfMonth(today), to: endOfMonth(today) })
    } else if (period === "last-month") {
      const lastMonth = subMonths(today, 1)
      setDate({ from: startOfMonth(lastMonth), to: endOfMonth(lastMonth) })
    } else if (period === "this-year") {
      setDate({ from: startOfYear(today), to: endOfDay(today) })
    }
  }, [period])

  const filteredInvoices = useMemo(() => {
    return invoices.filter((invoice) => {
      const matchesSearch = 
        searchQuery === "" ||
        invoice.buyer.toLowerCase().includes(searchQuery.toLowerCase()) ||
        invoice.seller.toLowerCase().includes(searchQuery.toLowerCase()) ||
        invoice.invoiceNumber.toLowerCase().includes(searchQuery.toLowerCase())
      
      let matchesDate = true
      if (date?.from && date?.to) {
        const invoiceDate = new Date(invoice.invoiceDate)
        matchesDate = isWithinInterval(invoiceDate, { start: date.from, end: date.to })
      }
      const matchesStatus = !statusFilter || invoice.status === statusFilter
      
      return matchesSearch && matchesDate && matchesStatus
    })
  }, [invoices, searchQuery, date, statusFilter])


  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset className="overflow-x-hidden">
        <AppHeader searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
        <div className="flex flex-1 flex-col gap-4 p-4">
          <DashboardHeader 
            period={period} 
            setPeriod={setPeriod} 
            date={date} 
            setDate={setDate} 
          />
          <DashboardStats data={filteredInvoices} onFilterStatus={setStatusFilter} activeStatus={statusFilter} />
          <DashboardCharts data={filteredInvoices} />
          <DashboardInvoiceTable data={filteredInvoices} />
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}