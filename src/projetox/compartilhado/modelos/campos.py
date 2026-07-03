from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AtendimentoFrontmatter:
    cliente: str
    data: str
    chamado: str
    status: str
    tecnico: str
    equipamentos: list[str]
    solucao: str
    tags: list[str]


@dataclass(frozen=True)
class ClienteFrontmatter:
    empresa: str
    cnpj: str
    contato: str
    email: str
    endereco: str
    ultimo_atendimento: str
    tags: list[str]


@dataclass(frozen=True)
class EquipamentoFrontmatter:
    categoria: str
    marca: str
    modelo: str
    fabricante: str
    tags: list[str]


@dataclass(frozen=True)
class ProcedimentoFrontmatter:
    categoria: str
    equipamento: str
    tempo_estimado: str
    dificuldade: str
    tags: list[str]


@dataclass(frozen=True)
class SolucaoFrontmatter:
    problema: str
    causa: str
    solucao: str
    equipamento: str
    frequencia: str
    tags: list[str]
