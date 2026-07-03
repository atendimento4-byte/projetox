"""Testes unitários para o domínio de LLM (entidades)."""
from __future__ import annotations

from projetox.llm.dominio.entidades import ResumoAtendimento


class TestResumoAtendimento:
    def test_criar_resumo_completo(self) -> None:
        resumo = ResumoAtendimento(
            resumo="troca de roteador",
            problema="quedas frequentes",
            solucao="substituir equipamento",
            equipamentos=["MikroTik RB951"],
            cliente="Empresa ABC",
            tipo_atendimento="suporte",
            observacoes="cliente satisfeito",
            acoes_pendentes=["agendar retorno"],
        )
        assert resumo.resumo == "troca de roteador"
        assert "MikroTik RB951" in resumo.equipamentos
        assert resumo.cliente == "Empresa ABC"

    def test_criar_resumo_minimo(self) -> None:
        resumo = ResumoAtendimento(
            resumo="teste",
            problema="",
            solucao="",
            equipamentos=[],
            cliente="",
            tipo_atendimento="suporte",
            observacoes="",
            acoes_pendentes=[],
        )
        assert resumo.resumo == "teste"
        assert resumo.equipamentos == []

    def test_resumo_sem_equipamentos(self) -> None:
        resumo = ResumoAtendimento(
            resumo="atendimento simples",
            problema="senha perdida",
            solucao="reset de fabrica",
            equipamentos=[],
            cliente="Joao",
            tipo_atendimento="suporte",
            observacoes="",
            acoes_pendentes=[],
        )
        assert len(resumo.equipamentos) == 0
