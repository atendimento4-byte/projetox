from __future__ import annotations

from datetime import datetime

from projetox.aprovacao.dominio.entidades import AcaoPendente
from projetox.aprovacao.dominio.interfaces import IRepositorioAprovacao
from projetox.compartilhado.erros.resultado import Resultado


class ServicoAprovacao:

    def __init__(self, repositorio: IRepositorioAprovacao) -> None:
        self._repositorio = repositorio

    def adicionar_acao(
        self,
        tipo: str,
        titulo: str,
        descricao: str,
        dados: dict,
        urgencia: str = "baixa",
    ) -> AcaoPendente:
        acao = AcaoPendente(
            tipo=tipo,
            titulo=titulo,
            descricao=descricao,
            dados=dados,
            urgencia=urgencia,
            criada_em=datetime.now(),
        )
        self._repositorio.adicionar(acao)
        return acao

    def listar(self) -> list[AcaoPendente]:
        return self._repositorio.listar_pendentes()

    def aprovar(self, id: str) -> Resultado[str, str]:
        if self._repositorio.aprovar(id):
            acao = self._repositorio.obter(id)
            return Resultado.sucesso(f"Acao '{acao.titulo}' aprovada.")
        return Resultado.falha_com_erro(
            f"Acao com id '{id}' nao encontrada ou ja processada.",
        )

    def rejeitar(self, id: str) -> Resultado[str, str]:
        if self._repositorio.rejeitar(id):
            acao = self._repositorio.obter(id)
            return Resultado.sucesso(f"Acao '{acao.titulo}' rejeitada.")
        return Resultado.falha_com_erro(
            f"Acao com id '{id}' nao encontrada ou ja processada.",
        )
