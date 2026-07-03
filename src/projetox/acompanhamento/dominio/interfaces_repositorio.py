from abc import ABC, abstractmethod

from projetox.acompanhamento.dominio.entidades import SessaoAcompanhamento


class IRepositorioSessao(ABC):
    @abstractmethod
    async def criar(self, sessao: SessaoAcompanhamento) -> SessaoAcompanhamento: ...

    @abstractmethod
    async def obter_ativa(self) -> SessaoAcompanhamento | None: ...

    @abstractmethod
    async def finalizar(self, id_sessao: str) -> SessaoAcompanhamento | None: ...
