from __future__ import annotations

from projetox.aprovacao.dominio.entidades import AcaoPendente
from projetox.aprovacao.dominio.interfaces import IRepositorioAprovacao


class RepositorioAprovacaoMemoria(IRepositorioAprovacao):

    def __init__(self) -> None:
        self._acoes: dict[str, AcaoPendente] = {}

    def adicionar(self, acao: AcaoPendente) -> None:
        self._acoes[acao.id] = acao

    def listar_pendentes(self) -> list[AcaoPendente]:
        return [a for a in self._acoes.values() if a.status == "pendente"]

    def aprovar(self, id: str) -> bool:
        acao = self._acoes.get(id)
        if acao is None or acao.status != "pendente":
            return False
        acao.status = "aprovada"
        return True

    def rejeitar(self, id: str) -> bool:
        acao = self._acoes.get(id)
        if acao is None or acao.status != "pendente":
            return False
        acao.status = "rejeitada"
        return True

    def obter(self, id: str) -> AcaoPendente | None:
        return self._acoes.get(id)
