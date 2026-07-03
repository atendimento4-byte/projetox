from __future__ import annotations

from abc import ABC, abstractmethod

from projetox.compartilhado.erros.resultado import Resultado
from projetox.llm.dominio.entidades import ResumoAtendimento


class IRepositorioNotas(ABC):
    @abstractmethod
    def salvar_atendimento(
        self, resumo: ResumoAtendimento,
    ) -> Resultado[str, Exception]: ...

    @abstractmethod
    def salvar_cliente(
        self, nome: str, resumo: ResumoAtendimento,
    ) -> Resultado[str, Exception]: ...
