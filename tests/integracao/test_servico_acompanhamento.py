"""Testes para o serviço de acompanhamento (repositório em memória)."""
from __future__ import annotations

import pytest

from projetox.acompanhamento.aplicacao.servico_acompanhamento import (
    ServicoAcompanhamento,
)
from projetox.acompanhamento.infra.repositorio_memoria import (
    RepositorioSessaoMemoria,
)


@pytest.fixture
def servico() -> ServicoAcompanhamento:
    return ServicoAcompanhamento(RepositorioSessaoMemoria())


@pytest.mark.asyncio
async def test_iniciar_sessao(servico: ServicoAcompanhamento) -> None:
    sessao = await servico.iniciar(
        chamado="12345", cliente="Empresa Teste", tecnico="João", tipo="suporte",
    )
    assert sessao.chamado == "12345"
    assert sessao.cliente == "Empresa Teste"
    assert sessao.status == "active"


@pytest.mark.asyncio
async def test_status_sem_sessao(servico: ServicoAcompanhamento) -> None:
    resultado = await servico.status()
    assert resultado is None


@pytest.mark.asyncio
async def test_finalizar_sessao(servico: ServicoAcompanhamento) -> None:
    await servico.iniciar("999", "Cliente", "", "suporte")
    finalizada = await servico.finalizar()
    assert finalizada is not None
    assert finalizada.status == "completed"


@pytest.mark.asyncio
async def test_finalizar_sem_sessao(servico: ServicoAcompanhamento) -> None:
    resultado = await servico.finalizar()
    assert resultado is None


@pytest.mark.asyncio
async def test_status_apos_finalizar(servico: ServicoAcompanhamento) -> None:
    await servico.iniciar("111", "Teste", "", "suporte")
    await servico.finalizar()
    status = await servico.status()
    assert status is None
