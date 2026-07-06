"""Testes unitários para o domínio de acompanhamento."""
from __future__ import annotations

from datetime import datetime

from projetox.acompanhamento.dominio.entidades import SessaoAcompanhamento


class TestSessaoAcompanhamento:
    def test_criar_sessao_com_valores_padrao(self) -> None:
        sessao = SessaoAcompanhamento()
        assert sessao.id == ""
        assert sessao.status == "active"
        assert sessao.tipo == "suporte"
        assert isinstance(sessao.iniciado_em, datetime)
        assert sessao.finalizado_em is None

    def test_criar_sessao_com_dados(self) -> None:
        sessao = SessaoAcompanhamento(
            id="abc-123",
            chamado="99999",
            cliente="Empresa XYZ",
            tecnico="João",
            tipo="instalacao",
        )
        assert sessao.id == "abc-123"
        assert sessao.chamado == "99999"
        assert sessao.cliente == "Empresa XYZ"
        assert sessao.tecnico == "João"
        assert sessao.tipo == "instalacao"

    def test_finalizar_sessao(self) -> None:
        sessao = SessaoAcompanhamento(id="abc-123")
        sessao.status = "completed"
        sessao.finalizado_em = datetime.now()
        assert sessao.status == "completed"
        assert sessao.finalizado_em is not None

    def test_sessao_str_repr(self) -> None:
        sessao = SessaoAcompanhamento(
            chamado="123", cliente="Teste", status="active",
        )
        assert "chamado=123" in str(sessao) or "123" in str(sessao)
