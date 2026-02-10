import { SidebarTrigger } from "@/components/ui/sidebar"
import { Search } from "lucide-react"
import { Separator } from "@/components/ui/separator"
import { Input } from "@/components/ui/input"

interface AppHeaderProps {
  searchQuery: string
  setSearchQuery: (query: string) => void
}

export function AppHeader({ searchQuery, setSearchQuery }: AppHeaderProps) {
  return (
    <header className="flex sticky top-0 bg-background h-16 shrink-0 items-center gap-2 border-b px-4">
      <SidebarTrigger className="-ml-1" />
      <Separator orientation="vertical" className="mr-2 h-4" />
      <div className="relative w-full max-w-sm">
        <Search className="absolute left-2 top-2 h-4 w-4 text-muted-foreground pointer-events-none" />
        <Input 
          type="search" 
          placeholder="Search..." 
          className="pl-8 h-8" 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>
    </header>
  )
}
