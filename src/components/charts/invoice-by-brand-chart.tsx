import * as React from "react"
import { Bar, BarChart, XAxis } from "recharts"

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,

} from "@/components/ui/chart"



interface InvoiceByBrandChartProps {
  data: Record<string, string | number>[]
}

export function InvoiceByBrandChart({ data }: InvoiceByBrandChartProps) {
  // Dynamically generate chart config based on data keys
  const chartConfig = React.useMemo(() => {
    if (!data || data.length === 0) return {} as ChartConfig

    // Get all unique keys (sellers) from all data objects, excluding "name"
    const allKeys = new Set<string>()
    data.forEach(item => {
      Object.keys(item).forEach(key => {
        if (key !== "name") {
          allKeys.add(key)
        }
      })
    })

    const config: ChartConfig = {}
    
    Array.from(allKeys).forEach((key) => {
      config[key] = {
        label: key.charAt(0).toUpperCase() + key.slice(1),
        color: "#0470FD",
      }
    })
    
    return config
  }, [data])

  if (!data || data.length === 0) {
      return (
        <Card>
            <CardHeader>
                <CardTitle>Invoice by Brand</CardTitle>
            </CardHeader>
             <CardContent>
                 <div className="flex items-center justify-center h-[300px] text-muted-foreground">
                     No data available
                 </div>
             </CardContent>
        </Card>
      )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Invoice by Brand</CardTitle>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="aspect-auto h-[200px] w-full">
          <BarChart accessibilityLayer data={data}>

            <XAxis
              dataKey="name"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              tickFormatter={(value) => String(value)}
            />
            <ChartTooltip content={<ChartTooltipContent hideLabel />} />

            {Object.keys(chartConfig).map((key, index) => {
               const isTop = index === Object.keys(chartConfig).length - 1
               const radius: [number, number, number, number] = isTop ? [4, 4, 0, 0] : [0, 0, 0, 0]
               
               return (
                 <Bar
                   key={key}
                   dataKey={key}
                   stackId="a"
                   fill="#0470FD"
                   radius={radius}
                   barSize={20}
                   className=""
                 />
               )
            })}
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
