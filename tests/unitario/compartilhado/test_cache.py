"""Testes para o cache em memória."""
from __future__ import annotations

from projetox.compartilhado.cache import CacheMemoria


class TestCacheMemoria:
    def test_obter_valor_inexistente(self) -> None:
        cache = CacheMemoria()
        assert cache.obter("chave_qualquer") is None

    def test_definir_e_obter(self) -> None:
        cache = CacheMemoria()
        cache.definir("abc", "valor123")
        assert cache.obter("abc") == "valor123"

    def test_limpar_cache(self) -> None:
        cache = CacheMemoria()
        cache.definir("a", "1")
        cache.definir("b", "2")
        cache.limpar()
        assert cache.obter("a") is None
        assert cache.obter("b") is None

    def test_estatisticas_iniciais(self) -> None:
        cache = CacheMemoria()
        stats = cache.estatisticas()
        assert stats["total"] == 0
        assert stats["hit_rate"] == 0.0

    def test_hit_rate_parcial(self) -> None:
        cache = CacheMemoria()
        cache.definir("existe", "valor")
        cache.obter("existe")  # hit
        cache.obter("existe")  # hit
        cache.obter("nao_existe")  # miss
        stats = cache.estatisticas()
        assert stats["total"] == 3
        assert stats["hit_rate"] == 2 / 3

    def test_max_itens_respeitado(self) -> None:
        cache = CacheMemoria(max_itens=3)
        for i in range(5):
            cache.definir(f"chave_{i}", f"valor_{i}")
        stats = cache.estatisticas()
        assert stats["total"] <= 3
