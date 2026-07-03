from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Resultado[T, E]:
    valor: T | None = None
    erro: E | None = None

    def ok(self) -> bool:
        return self.erro is None

    def falha(self) -> bool:
        return self.erro is not None

    @classmethod
    def sucesso(cls, valor: T) -> Resultado[T, E]:
        return cls(valor=valor, erro=None)

    @classmethod
    def falha_com_erro(cls, erro: E) -> Resultado[T, E]:
        return cls(valor=None, erro=erro)
