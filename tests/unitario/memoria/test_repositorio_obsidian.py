"""Testes para o módulo de memória (Obsidian)."""
from __future__ import annotations

from pathlib import Path

from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.memoria.infra.repositorio_obsidian import (
    RepositorioNotasObsidian,
)


class TestRepositorioNotasObsidian:
    def test_vault_path_padrao_contem_obisidian(self) -> None:
        repo = RepositorioNotasObsidian()
        assert "Obisidian" in str(repo.vault_path)

    def test_vault_path_personalizado(self) -> None:
        repo = RepositorioNotasObsidian(vault_path="C:\\tmp\\vault")
        assert "tmp" in str(repo.vault_path)

    def test_salvar_atendimento_em_temp_dir(self, tmp_path: Path) -> None:
        from unittest.mock import patch as _patch

        with _patch(
            "projetox.memoria.infra.repositorio_obsidian.TemplateEngine.carregar_template",
            return_value="# Cliente: $cliente - Resumo: $resumo",
        ):
            vault = tmp_path / "Vault"
            vault.mkdir(parents=True)
            repo = RepositorioNotasObsidian(vault_path=str(vault))
            resumo = ResumoAtendimento(
                resumo="teste",
                problema="queda de link",
                solucao="reiniciar",
                equipamentos=["RB951"],
                cliente="Empresa X",
                tipo_atendimento="suporte",
                observacoes="ok",
            )
            resultado = repo.salvar_atendimento(resumo)
            assert resultado.ok()
            assert resultado.valor is not None
            caminho_gerado = Path(resultado.valor)
            assert caminho_gerado.exists()
            conteudo = caminho_gerado.read_text(encoding="utf-8")
            assert "Empresa X" in conteudo

    def test_salvar_cliente_em_temp_dir(self, tmp_path: Path) -> None:
        from unittest.mock import patch as _patch

        with _patch(
            "projetox.memoria.infra.repositorio_obsidian.TemplateEngine.carregar_template",
            return_value="# Cliente: $empresa - Resumo: $resumo",
        ):
            vault = tmp_path / "Vault"
            vault.mkdir(parents=True)
            repo = RepositorioNotasObsidian(vault_path=str(vault))
            resumo = ResumoAtendimento(
                resumo="teste",
                problema="lentidao",
                solucao="otimizar",
                equipamentos=["Server"],
                cliente="Cliente Teste",
                tipo_atendimento="suporte",
                observacoes="",
            )
            resultado = repo.salvar_cliente("Cliente Teste", resumo)
            assert resultado.ok()
            assert resultado.valor is not None
            caminho = Path(resultado.valor)
            assert "Cliente Teste" in caminho.name
            assert caminho.exists()


class TestServicoMemoria:
    def test_servico_cria_sem_erro(self) -> None:
        from projetox.memoria.aplicacao.servico_memoria import (
            ServicoMemoria,
        )

        servico = ServicoMemoria(RepositorioNotasObsidian())
        assert servico is not None
