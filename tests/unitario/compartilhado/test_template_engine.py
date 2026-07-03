"""Testes unitários para o motor de templates."""
from __future__ import annotations

from pathlib import Path

from projetox.compartilhado.modelos.tipos_nota import TipoNota


class TestTipoNota:
    def test_tipos_existem(self) -> None:
        assert TipoNota.ATENDIMENTO == "atendimento"
        assert TipoNota.CLIENTE == "cliente"
        assert TipoNota.EQUIPAMENTO == "equipamento"
        assert TipoNota.PROCEDIMENTO == "procedimento"
        assert TipoNota.SOLUCAO == "solucao"

    def test_tipo_nota_eh_string(self) -> None:
        assert isinstance(TipoNota.ATENDIMENTO, str)

    def test_todos_tipos(self) -> None:
        tipos = list(TipoNota)
        assert len(tipos) == 5


class TestTemplateEngine:
    def test_caminho_template_atendimento(self) -> None:
        from projetox.compartilhado.modelos.template_engine import (
            TemplateEngine,
        )

        engine = TemplateEngine()
        caminho = engine._caminho_template(TipoNota.ATENDIMENTO)
        assert "Modelo - Nota de Atendimento.md" in str(caminho)

    def test_caminho_template_cliente(self) -> None:
        from projetox.compartilhado.modelos.template_engine import (
            TemplateEngine,
        )

        engine = TemplateEngine()
        caminho = engine._caminho_template(TipoNota.CLIENTE)
        assert "Modelo - Nota de Cliente.md" in str(caminho)

    def test_preencher_placeholders(self) -> None:
        from projetox.compartilhado.modelos.template_engine import (
            TemplateEngine,
        )

        engine = TemplateEngine()
        template = "Cliente: $cliente - Data: $data"
        resultado = engine.preencher(template, {"cliente": "ABC", "data": "2026-07-03"})
        assert resultado == "Cliente: ABC - Data: 2026-07-03"

    def test_preencher_sem_placeholders(self) -> None:
        from projetox.compartilhado.modelos.template_engine import (
            TemplateEngine,
        )

        engine = TemplateEngine()
        resultado = engine.preencher("Texto fixo", {})
        assert resultado == "Texto fixo"

    def test_gerar_nome_atendimento(self) -> None:
        from projetox.compartilhado.modelos.template_engine import (
            TemplateEngine,
        )

        engine = TemplateEngine()
        nome = engine.gerar_nome_arquivo(
            TipoNota.ATENDIMENTO,
            {"data": "2026-07-03", "cliente": "ABC", "resumo": "Suporte"},
        )
        assert "Atendimento" in nome
        assert "2026-07-03" in nome

    def test_gerar_nome_cliente(self) -> None:
        from projetox.compartilhado.modelos.template_engine import (
            TemplateEngine,
        )

        engine = TemplateEngine()
        nome = engine.gerar_nome_arquivo(TipoNota.CLIENTE, {"nome": "Empresa"})
        assert nome == "Empresa.md"
