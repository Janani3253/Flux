import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import type { DateRange } from "react-day-picker"
import { DatePickerWithRange } from "@/components/date-range-picker"

interface DashboardHeaderProps {
  period: string
  setPeriod: (period: string) => void
  date: DateRange | undefined
  setDate: (date: DateRange | undefined) => void
}

export function DashboardHeader({ period, setPeriod, date, setDate }: DashboardHeaderProps) {

  return (
    <div className="flex items-center justify-between">
      <h2 className="text-2xl font-bold tracking-tight">Dashboard</h2>
      <div className="flex items-center gap-2">
        {period === "custom" && <DatePickerWithRange date={date} setDate={setDate} />}
        <Select value={period} onValueChange={(value) => value && setPeriod(value)}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Select period" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="today">Today</SelectItem>
            <SelectItem value="this-week">This Week</SelectItem>
            <SelectItem value="this-month">This Month</SelectItem>
            <SelectItem value="last-month">Last Month</SelectItem>
            <SelectItem value="this-year">This Year</SelectItem>
            <SelectItem value="custom">Custom</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  )
}
