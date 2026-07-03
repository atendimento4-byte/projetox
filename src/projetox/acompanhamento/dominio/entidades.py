from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SessaoAcompanhamento:
    id: str = ""
    chamado: str = ""
    cliente: str = ""
    tecnico: str = ""
    tipo: str = "suporte"
    status: str = "active"
    iniciado_em: datetime = field(default_factory=datetime.now)
    finalizado_em: datetime | None = None
