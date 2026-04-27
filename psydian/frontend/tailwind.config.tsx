// tailwind.config.ts
export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: "#0d0d0f",
          secondary: "#141417",
          surface: "#1a1a1f",
        },
        accent: {
          neon: "#7c3aed",      // roxo principal
          glow: "#a78bfa",      // roxo claro p/ glow
          edge: "#06b6d4",      // ciano para arestas
        },
        text: {
          primary: "#f4f4f5",
          muted: "#71717a",
        },
      },
    },
  },
}