from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class MensagemIPC:
    id: str = field(default_factory=lambda: str(uuid4()))
    metodo: str = ""
    params: dict = field(default_factory=dict)


@dataclass
class RespostaIpc:
    id: str
    sucesso: bool
    dados: object | None = None
    erro: str | None = None
