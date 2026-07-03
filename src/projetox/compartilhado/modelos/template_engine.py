from __future__ import annotations

from pathlib import Path
from string import Template

from projetox.compartilhado.modelos.tipos_nota import TipoNota

_VAULT_PADRAO = "C:\\Users\\v2admin\\Documents\\Obisidian\\ProjetoX"


class TemplateEngine:
    def __init__(self, vault_path: str | Path = _VAULT_PADRAO) -> None:
        self.vault_path = Path(vault_path)

    def _caminho_template(self, tipo: TipoNota) -> Path:
        mapa = {
            TipoNota.ATENDIMENTO: "Modelo - Nota de Atendimento.md",
            TipoNota.CLIENTE: "Modelo - Nota de Cliente.md",
            TipoNota.EQUIPAMENTO: "Modelo - Nota de Equipamento.md",
            TipoNota.PROCEDIMENTO: "Modelo - Nota de Procedimento.md",
            TipoNota.SOLUCAO: "Modelo - Nota de Solucao.md",
        }
        return self.vault_path / "Modelos" / mapa[tipo]

    def carregar_template(self, tipo: TipoNota) -> str:
        caminho = self._caminho_template(tipo)
        return caminho.read_text(encoding="utf-8")

    def preencher(self, template: str, dados: dict[str, str]) -> str:
        return Template(template).safe_substitute(**dados)

    def gerar_nome_arquivo(self, tipo: TipoNota, dados: dict[str, str]) -> str:
        padroes = {
            TipoNota.ATENDIMENTO: Template("Atendimento - $data - $cliente - $resumo.md"),
            TipoNota.CLIENTE: Template("$nome.md"),
            TipoNota.EQUIPAMENTO: Template("$modelo.md"),
            TipoNota.PROCEDIMENTO: Template("$nome.md"),
            TipoNota.SOLUCAO: Template("Problema - $problema - $solucao.md"),
        }
        return padroes[tipo].safe_substitute(**dados)

    def criar_nota(
        self, tipo: TipoNota, dados: dict[str, str], destino: str | Path | None = None,
    ) -> Path:
        template = self.carregar_template(tipo)
        conteudo = self.preencher(template, dados)
        nome = self.gerar_nome_arquivo(tipo, dados)
        caminho_destino = Path(destino) if destino else self.vault_path / "Notas"
        caminho_destino.mkdir(parents=True, exist_ok=True)
        arquivo = caminho_destino / nome
        arquivo.write_text(conteudo, encoding="utf-8")
        return arquivo
