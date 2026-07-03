from __future__ import annotations

from abc import ABC, abstractmethod

from projetox.aprovacao.dominio.entidades import AcaoPendente


class IRepositorioAprovacao(ABC):

    @abstractmethod
    def adicionar(self, acao: AcaoPendente) -> None: ...

    @abstractmethod
    def listar_pendentes(self) -> list[AcaoPendente]: ...

    @abstractmethod
    def aprovar(self, id: str) -> bool: ...

    @abstractmethod
    def rejeitar(self, id: str) -> bool: ...

    @abstractmethod
    def obter(self, id: str) -> AcaoPendente | None: ...
