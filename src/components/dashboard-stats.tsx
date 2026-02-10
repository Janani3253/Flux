import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { FileText, CheckCircle, Clock, AlertCircle } from "lucide-react"

interface DashboardStatsProps {
  data: any[] // Using any[] for now, ideal to share type
  onFilterStatus?: (status: string | null) => void
  activeStatus?: string | null
}

export function DashboardStats({ data, onFilterStatus, activeStatus }: DashboardStatsProps) {
  const total = data.length
  const success = data.filter(i => i.status === "Success").length
  const pending = data.filter(i => i.status === "Pending").length
  const failed = data.filter(i => i.status === "Failed").length

  const toggleStatus = (status: string | null) => {
    if (!onFilterStatus) return
    if (activeStatus === status) {
      onFilterStatus(null)
    } else {
      onFilterStatus(status)
    }
  }

  const cardClass = (status?: string | null) =>
    `cursor-pointer hover:shadow-sm ${activeStatus === status ? "ring-2 ring-offset-1 ring-indigo-200" : ""}`

  return (
    <div className="grid auto-rows-min gap-4 md:grid-cols-4">
      <Card onClick={() => toggleStatus(null)} className={cardClass(null)}>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Total Invoices
          </CardTitle>
          <FileText className="h-4 w-4 text-[#0470FD]" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{total}</div>
        </CardContent>
      </Card>
      <Card onClick={() => toggleStatus("Success")} className={cardClass("Success")}>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Success
          </CardTitle>
          <CheckCircle className="h-4 w-4 text-green-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{success}</div>
        </CardContent>
      </Card>
      <Card onClick={() => toggleStatus("Pending")} className={cardClass("Pending")}>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Pending</CardTitle>
          <Clock className="h-4 w-4 text-orange-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{pending}</div>
        </CardContent>
      </Card>
      <Card onClick={() => toggleStatus("Failed")} className={cardClass("Failed")}>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Failed
          </CardTitle>
          <AlertCircle className="h-4 w-4 text-red-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{failed}</div>
        </CardContent>
      </Card>
    </div>
  )
}
