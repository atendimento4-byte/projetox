from __future__ import annotations

from enum import StrEnum


class TipoNota(StrEnum):
    ATENDIMENTO = "atendimento"
    CLIENTE = "cliente"
    EQUIPAMENTO = "equipamento"
    PROCEDIMENTO = "procedimento"
    SOLUCAO = "solucao"
