from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class AcaoPendente:
    tipo: str
    titulo: str
    descricao: str
    dados: dict
    urgencia: str = "baixa"
    id: str = field(default_factory=lambda: str(uuid4()))
    criada_em: datetime = field(default_factory=datetime.now)
    status: str = "pendente"
