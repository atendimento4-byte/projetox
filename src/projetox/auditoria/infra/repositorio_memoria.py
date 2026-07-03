from collections import deque
from uuid import uuid4

from projetox.auditoria.dominio.entidades import RegistroAuditoria
from projetox.auditoria.dominio.interfaces import IRegistroAuditoria


class RepositorioAuditoriaMemoria(IRegistroAuditoria):
    def __init__(self) -> None:
        self._dados: deque[RegistroAuditoria] = deque(maxlen=1000)

    def registrar(self, registro: RegistroAuditoria) -> None:
        registro.id = str(uuid4())
        self._dados.append(registro)

    def listar(self, limite: int = 50) -> list[RegistroAuditoria]:
        return list(self._dados)[-limite:]
