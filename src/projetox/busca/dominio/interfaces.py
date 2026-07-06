from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from projetox.compartilhado.erros import ErroInfraestrutura, Resultado


@dataclass
class DocumentoBusca:
    id: str
    texto: str
    metadados: dict
    pontuacao: float = 0.0


class IRepositorioBusca(ABC):
    @abstractmethod
    async def indexar(
        self, docs: list[DocumentoBusca], embeddings: list[list[float]],
    ) -> Resultado[int, ErroInfraestrutura]: ...

    @abstractmethod
    async def buscar(
        self, vetor_consulta: list[float], limite: int = 5,
    ) -> list[DocumentoBusca]: ...

    @abstractmethod
    async def remover(self, id: str) -> bool: ...

    @abstractmethod
    async def limpar(self) -> None: ...
