import { Link, useLocation } from "react-router-dom"

const arquivosExemplo = [
  { id: 1, titulo: "Introdução ao Psydian" },
  { id: 2, titulo: "Ideias de funcionalidades" },
  { id: 3, titulo: "Anotações de reunião" },
]

export function Sidebar() {
  const location = useLocation()

  return (
    <aside className="bg-bg-secondary border-r border-white/5 flex flex-col overflow-y-auto">
      <div className="p-3 text-text-muted text-xs font-semibold uppercase tracking-wider">
        Arquivos
      </div>

      {arquivosExemplo.map((arquivo) => {
        const estaAtivo = location.pathname === `/editor/${arquivo.id}`

        return (
          <Link
            key={arquivo.id}
            to={`/editor/${arquivo.id}`}
            className={`px-3 py-2 text-sm truncate transition-colors hover:bg-bg-surface
              ${estaAtivo
                ? "bg-bg-surface text-text-primary border-l-2 border-accent-neon"
                : "text-text-muted"
              }`}
          >
            {arquivo.titulo}
          </Link>
        )
      })}
    </aside>
  )
}