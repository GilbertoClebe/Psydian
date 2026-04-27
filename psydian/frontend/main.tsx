import React from "react"
import ReactDOM from "react-dom/client"
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import { AppShell } from "./Components/Layout/AppShell"
import { GraphView } from "./Pages/GraphView"
import { EditorPage } from "./Pages/EditorPage"
import { SettingsPage } from "./Pages/SettingsPage"
import "./index.css"

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <GraphView /> },
      { path: "editor/:id", element: <EditorPage /> },
      { path: "settings", element: <SettingsPage /> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)