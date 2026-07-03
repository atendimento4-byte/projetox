from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ResumoAtendimento:
    resumo: str
    problema: str
    solucao: str
    equipamentos: list[str]
    cliente: str
    tipo_atendimento: str
    observacoes: str
    acoes_pendentes: list[str] = field(default_factory=list)
