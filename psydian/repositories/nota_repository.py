from __future__ import annotations

from datetime import date
from pathlib import Path

import frontmatter

from psydian.models.nota import NotaMetadata

class NoteRepository:
    def __init__(self, vault_path: Path) -> None :
        self.notas_path = vault_path / "notas"
        self.notas_path.mkdir(parents=True, exist_ok=True)
        
    def _path_de(self, titulo: str) -> Path :
        slug = titulo.lower().replace(" ", "-")
        return self.notas_path / f"{slug}.md"
    
    def salvar(self, metadata: NotaMetadata, conteudo: str = "") -> Path :
        meta_atualizada = metadata.model_copy(update={"modificado_em": date.today()})
        
        post = frontmatter.Post(
            content = conteudo,
            **meta_atualizada.model_dump(mode="json"),
        )
        
        caminho = self._path_de(metadata.titulo)
        caminho.write_text(frontmatter.dumps(post), encoding="utf-8")
        return caminho
    
    def ler(self, titulo: str) -> tuple[NotaMetadata, str] :
        caminho = self._path_de(titulo)
        
        if not caminho.exists() :
            raise FileNotFoundError(f"Nota não encontrada: {titulo}")
        
        post = frontmatter.load(str(caminho))
        metadata = NotaMetadata(**post.metadata)
        
        return metadata, post.content
    
    def listar(self) -> list[NotaMetadata] :
        notas = []
        for arquivo in self.notas_path.glob("*.md") :
            post = frontmatter.load(str(arquivo))
            notas.append(NotaMetadata(**post.metadata))
        return notas
    
    def deletar(self, titulo: str) -> None :
        caminho = self._path_de(titulo)
        if caminho.exists() :
            caminho.unlink()
        else :
            raise FileNotFoundError(f"Arquivo não encontrado")
            
