import { Outlet } from "react-router-dom"
import { Sidebar } from "./Sidebar"
import { Topbar } from "./Topbar"

export function AppShell() {
  return (
    <div
      className="h-screen w-screen overflow-hidden"
      style={{
        display: "grid",
        gridTemplateRows: "48px 1fr",
        gridTemplateColumns: "240px 1fr",
      }}
    >
      <Topbar />
      <Sidebar />
      <main className="bg-bg-primary overflow-hidden">
        <Outlet />
      </main>
    </div>
  )
}