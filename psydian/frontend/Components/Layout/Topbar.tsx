export function Topbar() {
  return (
    <header
      style={{ gridColumn: "1 / -1" }}
      className="bg-bg-secondary border-b border-white/10 flex items-center px-4"
    >
      <span className="text-accent-glow font-bold text-sm tracking-widest">
        PSYDIAN
      </span>
    </header>
  )
}