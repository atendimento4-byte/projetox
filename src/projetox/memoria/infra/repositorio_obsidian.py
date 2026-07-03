from __future__ import annotations

from pathlib import Path

from projetox.compartilhado.erros.resultado import Resultado
from projetox.compartilhado.modelos.template_engine import TemplateEngine
from projetox.compartilhado.modelos.tipos_nota import TipoNota
from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.memoria.dominio.interfaces import IRepositorioNotas

_VAULT_PADRAO = "C:\\Users\\v2admin\\Documents\\Obisidian\\ProjetoX"


class RepositorioNotasObsidian(IRepositorioNotas):
    def __init__(self, vault_path: str = _VAULT_PADRAO) -> None:
        self.engine = TemplateEngine(vault_path)
        self.vault_path = Path(vault_path)

    def salvar_atendimento(
        self, resumo: ResumoAtendimento,
    ) -> Resultado[str, Exception]:
        try:
            dados = {
                "cliente": resumo.cliente,
                "data": "2026-07-03",
                "chamado": "",
                "status": "Resolvido",
                "tecnico": "",
                "equipamentos": ", ".join(resumo.equipamentos),
                "solucao": resumo.solucao,
                "tags": "atendimento",
                "resumo": resumo.resumo,
                "problema": resumo.problema,
                "solucao_texto": resumo.solucao,
                "configuracoes": "",
                "equipamentos_lista": "\n".join(
                    f"- {e}" for e in resumo.equipamentos
                ),
                "observacoes": resumo.observacoes,
            }
            template = self.engine.carregar_template(TipoNota.ATENDIMENTO)
            conteudo = self.engine.preencher(template, dados)
            nome = (
                f"Atendimento - {dados['data']} - {resumo.cliente}"
                f" - {resumo.resumo[:30]}.md"
            )
            caminho = (
                self.vault_path / "Atendimentos" / "2026" / nome
            )
            caminho.parent.mkdir(parents=True, exist_ok=True)
            caminho.write_text(conteudo, encoding="utf-8")
            return Resultado.sucesso(str(caminho))
        except Exception as e:
            return Resultado.falha(e)

    def salvar_cliente(
        self, nome: str, resumo: ResumoAtendimento,
    ) -> Resultado[str, Exception]:
        try:
            dados = {
                "empresa": nome,
                "cnpj": "",
                "contato": "",
                "email": "",
                "endereco": "",
                "ultimo_atendimento": "2026-07-03",
                "tags": "cliente",
                "equipamentos_lista": "\n".join(
                    f"- [[{e}]]" for e in resumo.equipamentos
                ),
                "historico_atendimentos": (
                    f"- [[Atendimento - 2026-07-03 - {nome}"
                    f" - {resumo.resumo[:30]}]]"
                ),
                "observacoes": resumo.observacoes,
            }
            template = self.engine.carregar_template(TipoNota.CLIENTE)
            conteudo = self.engine.preencher(template, dados)
            caminho = self.vault_path / "Clientes" / f"{nome}.md"
            caminho.parent.mkdir(parents=True, exist_ok=True)
            caminho.write_text(conteudo, encoding="utf-8")
            return Resultado.sucesso(str(caminho))
        except Exception as e:
            return Resultado.falha(e)
