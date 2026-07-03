from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RegistroAuditoria:
    id: str = ""
    acao: str = ""
    usuario: str = ""
    sessao_id: str | None = None
    detalhes: dict = field(default_factory=dict)
    criado_em: datetime = field(default_factory=datetime.now)
