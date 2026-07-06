"""Testes para o domínio de aprovação."""
from __future__ import annotations

from projetox.aprovacao.dominio.entidades import AcaoPendente


class TestAcaoPendente:
    def test_criar_acao_pendente(self) -> None:
        acao = AcaoPendente(
            id="act-001",
            tipo="transcricao",
            titulo="Transcrever audio",
            descricao="Audio da sessao 123",
            dados={"sessao_id": "123"},
            urgencia="alta",
        )
        assert acao.id == "act-001"
        assert acao.tipo == "transcricao"
        assert acao.status == "pendente"
        assert acao.urgencia == "alta"

    def test_acao_padrao_urgencia_media(self) -> None:
        acao = AcaoPendente(
            id="act-002",
            tipo="salvamento",
            titulo="Salvar nota",
            descricao="",
            dados={},
        )
        assert acao.urgencia == "baixa"

    def test_aprovar_acao(self) -> None:
        acao = AcaoPendente(
            id="act-003", tipo="email", titulo="Enviar email", descricao="", dados={},
        )
        acao.status = "aprovada"
        assert acao.status == "aprovada"

    def test_rejeitar_acao(self) -> None:
        acao = AcaoPendente(
            id="act-004", tipo="email", titulo="Enviar email", descricao="", dados={},
        )
        acao.status = "rejeitada"
        assert acao.status == "rejeitada"
