from __future__ import annotations

from projetox.compartilhado.erros.resultado import Resultado
from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.memoria.dominio.interfaces import IRepositorioNotas


class ServicoMemoria:
    def __init__(self, repo: IRepositorioNotas) -> None:
        self.repo = repo

    def salvar(
        self, resumo: ResumoAtendimento,
    ) -> Resultado[str, Exception]:
        resultado = self.repo.salvar_atendimento(resumo)
        if resultado.falha():
            return resultado

        self.repo.salvar_cliente(resumo.cliente, resumo)

        return Resultado.sucesso(
            f"Notas salvas em: {resultado.valor}",
        )
