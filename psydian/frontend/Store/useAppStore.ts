import { create } from "zustand"

interface AppStore {
  arquivoSelecionadoId: number | null
  isPainelIAAberto: boolean
  setArquivoSelecionado: (id: number | null) => void
  togglePainelIA: () => void
}

export const useAppStore = create<AppStore>((set) => ({
  arquivoSelecionadoId: null,
  isPainelIAAberto: false,
  setArquivoSelecionado: (id) => set({ arquivoSelecionadoId: id }),
  togglePainelIA: () => set((estado) => ({
    isPainelIAAberto: !estado.isPainelIAAberto
  })),
}))