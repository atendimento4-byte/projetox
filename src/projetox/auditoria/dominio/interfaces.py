from abc import ABC, abstractmethod

from projetox.auditoria.dominio.entidades import RegistroAuditoria


class IRegistroAuditoria(ABC):
    @abstractmethod
    def registrar(self, registro: RegistroAuditoria) -> None: ...

    @abstractmethod
    def listar(self, limite: int = 50) -> list[RegistroAuditoria]: ...
