from __future__ import annotations

from abc import ABC, abstractmethod

from projetox.compartilhado.erros import ErroAplicacao, Resultado
from projetox.llm.dominio.entidades import ResumoAtendimento


class IExtratorLLM(ABC):
    @abstractmethod
    def extrair_resumo(
        self,
        transcricao: str,
    ) -> Resultado[ResumoAtendimento, ErroAplicacao]: ...
