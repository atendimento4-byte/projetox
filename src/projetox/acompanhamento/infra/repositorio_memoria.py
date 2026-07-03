from datetime import datetime
from uuid import uuid4

from projetox.acompanhamento.dominio.entidades import SessaoAcompanhamento
from projetox.acompanhamento.dominio.interfaces_repositorio import (
    IRepositorioSessao,
)


class RepositorioSessaoMemoria(IRepositorioSessao):
    def __init__(self) -> None:
        self._dados: dict[str, SessaoAcompanhamento] = {}

    async def criar(self, sessao: SessaoAcompanhamento) -> SessaoAcompanhamento:
        sessao.id = str(uuid4())
        self._dados[sessao.id] = sessao
        return sessao

    async def obter_ativa(self) -> SessaoAcompanhamento | None:
        for s in self._dados.values():
            if s.status == "active":
                return s
        return None

    async def finalizar(self, id_sessao: str) -> SessaoAcompanhamento | None:
        sessao = self._dados.get(id_sessao)
        if sessao is None:
            return None
        sessao.status = "completed"
        sessao.finalizado_em = datetime.now()
        return sessao
