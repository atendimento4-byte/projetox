"""Testes para o serviço de auditoria."""
from __future__ import annotations

from projetox.auditoria.aplicacao.servico_auditoria import (
    ServicoAuditoria,
)


class TestServicoAuditoria:
    def setup_method(self) -> None:
        # Reset singleton
        ServicoAuditoria._instancia = None

    def test_registrar_e_listar(self) -> None:
        servico = ServicoAuditoria()
        servico.registrar_acao(tipo="transcricao.concluida")
        registros = servico.listar()
        assert len(registros) == 1
        assert registros[0].acao == "transcricao.concluida"

    def test_listar_limitado(self) -> None:
        servico = ServicoAuditoria()
        for i in range(20):
            servico.registrar_acao(tipo=f"teste.{i}")
        todos = servico.listar()
        assert len(todos) == 20
        limitado = servico.listar(limite=5)
        assert len(limitado) == 5

    def test_registros_tem_timestamp(self) -> None:
        servico = ServicoAuditoria()
        servico.registrar_acao(tipo="teste")
        registro = servico.listar()[0]
        assert registro.criado_em is not None
