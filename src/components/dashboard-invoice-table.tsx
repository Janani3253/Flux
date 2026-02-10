import * as React from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Card,
  CardContent,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react"

// Generate 50 mock invoices
interface DashboardInvoiceTableProps {
  data: any[]
}

export function DashboardInvoiceTable({ data }: DashboardInvoiceTableProps) {
  const [page, setPage] = React.useState(1)
  const [rowsPerPage, setRowsPerPage] = React.useState(10)
  const [selectedRows, setSelectedRows] = React.useState<string[]>([])

  const totalPages = Math.ceil(data.length / rowsPerPage)
  
  const startIndex = (page - 1) * rowsPerPage
  const endIndex = startIndex + rowsPerPage
  const currentInvoices = data.slice(startIndex, endIndex)

  const handleSelectAll = (checked: boolean) => {
      const currentIds = currentInvoices.map(inv => inv.invoiceNumber)
      if (checked) {
          // Add visible rows to selection, avoiding duplicates
          setSelectedRows(prev => {
            const newSelection = new Set([...prev, ...currentIds])
            return Array.from(newSelection)
          })
      } else {
          // Remove visible rows from selection
          setSelectedRows(prev => prev.filter(id => !currentIds.includes(id)))
      }
  }

  const handleSelectRow = (invoiceNumber: string, checked: boolean) => {
      if (checked) {
          setSelectedRows(prev => [...prev, invoiceNumber])
      } else {
          setSelectedRows(prev => prev.filter(id => id !== invoiceNumber))
      }
  }

  return (
    <Card className="h-full overflow-hidden flex flex-col">
      <CardContent className="p-0 flex-1 overflow-auto">
          <Table className="min-w-[1200px]">
          <TableHeader className="bg-muted/50">
              <TableRow>
              <TableHead className="w-[40px]">
                  <Checkbox 
                    checked={currentInvoices.length > 0 && currentInvoices.every(inv => selectedRows.includes(inv.invoiceNumber))}
                    onCheckedChange={(checked) => handleSelectAll(!!checked)}
                  />
              </TableHead>
              <TableHead className="w-[100px]">Invoice No</TableHead>
              <TableHead>Invoice Date</TableHead>
              <TableHead>Mode/Terms</TableHead>
              <TableHead>Seller</TableHead>
              <TableHead>Buyer</TableHead>
              <TableHead>Mobile</TableHead>
              <TableHead>Product</TableHead>
              <TableHead>State</TableHead>
              <TableHead>State Code</TableHead>
              <TableHead>OEM</TableHead>
              <TableHead className="text-right">Total Amount</TableHead>
              <TableHead>Item Code</TableHead>
              <TableHead>Qty</TableHead>
              <TableHead>Rate</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Error</TableHead>
              <TableHead>Processed Date</TableHead>
              </TableRow>
          </TableHeader>
          <TableBody>
              {currentInvoices.map((invoice) => (
              <TableRow key={invoice.invoiceNumber}>
                  <TableCell>
                      <Checkbox 
                        checked={selectedRows.includes(invoice.invoiceNumber)}
                        onCheckedChange={(checked) => handleSelectRow(invoice.invoiceNumber, !!checked)}
                      />
                  </TableCell>
                  <TableCell className="font-medium">{invoice.invoiceNumber}</TableCell>
                  <TableCell>{invoice.invoiceDate}</TableCell>
                  <TableCell>{invoice.modeTerms}</TableCell>
                  <TableCell>{invoice.seller}</TableCell>
                  <TableCell>{invoice.buyer}</TableCell>
                  <TableCell>{invoice.mobile}</TableCell>
                  <TableCell>{invoice.product}</TableCell>
                  <TableCell>{invoice.state}</TableCell>
                  <TableCell>{invoice.stateCode}</TableCell>
                  <TableCell>{invoice.oem}</TableCell>
                  <TableCell className="text-right">{invoice.totalAmount}</TableCell>
                  <TableCell>{invoice.itemCode}</TableCell>
                  <TableCell>{invoice.qty}</TableCell>
                  <TableCell>{invoice.rate}</TableCell>
                  <TableCell>
                      <Badge variant={
                          invoice.status === "Success" ? "default" : 
                          invoice.status === "Pending" ? "secondary" : "destructive"
                      }
                      className={
                          invoice.status === "Success" ? "bg-chart-success hover:bg-chart-success/80 text-foreground" :
                          invoice.status === "Pending" ? "bg-chart-pending hover:bg-chart-pending/80 text-foreground" :
                          "bg-chart-failed hover:bg-chart-failed/80 text-foreground"
                      }
                      >
                          {invoice.status}
                      </Badge>
                  </TableCell>
                  <TableCell className="text-destructive font-medium text-xs max-w-[150px] truncate" title={invoice.error}>
                      {invoice.error}
                  </TableCell>
                  <TableCell className="whitespace-nowrap">{invoice.processedDate}</TableCell>
              </TableRow>
              ))}
          </TableBody>
          </Table>
      </CardContent>
      <div className="flex items-center justify-between px-4 py-4 border-t">
        <div className="flex-1 text-sm text-muted-foreground">
          {selectedRows.length} of {data.length} row(s) selected.
        </div>
        <div className="flex items-center space-x-6 lg:space-x-8">
          <div className="flex items-center space-x-2">
            <p className="text-sm font-medium">Rows per page</p>
            <Select
              value={`${rowsPerPage}`}
              onValueChange={(value) => {
                setRowsPerPage(Number(value))
                setPage(1) 
              }}
            >
              <SelectTrigger className="h-8 w-[70px]">
                <SelectValue placeholder={rowsPerPage} />
              </SelectTrigger>
              <SelectContent side="top">
                {[10, 20, 30, 40, 50].map((pageSize) => (
                  <SelectItem key={pageSize} value={`${pageSize}`}>
                    {pageSize}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex w-[100px] items-center justify-center text-sm font-medium">
            Page {page} of {totalPages}
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              className="hidden h-8 w-8 p-0 lg:flex"
              onClick={() => setPage(1)}
              disabled={page === 1}
            >
              <span className="sr-only">Go to first page</span>
              <ChevronsLeft className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              className="h-8 w-8 p-0"
              onClick={() => setPage(page - 1)}
              disabled={page === 1}
            >
              <span className="sr-only">Go to previous page</span>
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              className="h-8 w-8 p-0"
              onClick={() => setPage(page + 1)}
              disabled={page === totalPages}
            >
              <span className="sr-only">Go to next page</span>
              <ChevronRight className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              className="hidden h-8 w-8 p-0 lg:flex"
              onClick={() => setPage(totalPages)}
              disabled={page === totalPages}
            >
              <span className="sr-only">Go to last page</span>
              <ChevronsRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </Card>
  )
}
