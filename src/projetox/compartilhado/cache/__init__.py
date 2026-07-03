from __future__ import annotations

__all__ = ["CacheMemoria"]


class CacheMemoria:
    def __init__(self, max_itens: int = 100) -> None:
        self._cache: dict[str, str] = {}
        self._max = max_itens
        self._hits = 0
        self._total = 0

    def obter(self, chave: str) -> str | None:
        self._total += 1
        valor = self._cache.get(chave)
        if valor is not None:
            self._hits += 1
        return valor

    def definir(self, chave: str, valor: str) -> None:
        if len(self._cache) >= self._max:
            self._cache.pop(next(iter(self._cache)))
        self._cache[chave] = valor

    def limpar(self) -> None:
        self._cache.clear()
        self._hits = 0
        self._total = 0

    def estatisticas(self) -> dict:
        return {
            "total": self._total,
            "hit_rate": self._hits / self._total if self._total > 0 else 0.0,
        }
