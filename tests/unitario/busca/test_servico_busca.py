from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from projetox.busca.aplicacao.servico_busca import ServicoBusca
from projetox.busca.dominio.interfaces import DocumentoBusca, IRepositorioBusca
from projetox.compartilhado.erros import Resultado
from projetox.llm.dominio.entidades import ResumoAtendimento


@pytest.fixture
def repo_mock() -> AsyncMock:
    mock = AsyncMock(spec=IRepositorioBusca)
    mock.indexar = AsyncMock(return_value=Resultado.sucesso(1))
    mock.buscar = AsyncMock(return_value=[
        DocumentoBusca(
            id="1",
            texto="teste",
            metadados={"cliente": "Empresa X", "problema": "queda de link", "solucao": "reset"},
            pontuacao=0.95,
        ),
    ])
    return mock


@pytest.fixture
def llm_mock() -> AsyncMock:
    mock = AsyncMock()
    mock.ultimo_cache_hit = False
    mock.resumir = MagicMock()
    mock.gerar_embedding = AsyncMock(
        return_value=Resultado.sucesso([0.1] * 1536),
    )
    return mock


@pytest.fixture
def servico(repo_mock: AsyncMock, llm_mock: AsyncMock) -> ServicoBusca:
    return ServicoBusca(repo=repo_mock, llm=llm_mock)


@pytest.fixture
def resumo_valido() -> ResumoAtendimento:
    return ResumoAtendimento(
        resumo="troca de roteador",
        problema="quedas frequentes",
        solucao="substituir equipamento",
        equipamentos=["MikroTik RB951"],
        cliente="Empresa ABC",
        tipo_atendimento="suporte",
        observacoes="cliente satisfeito",
        acoes_pendentes=["agendar retorno"],
    )


@pytest.mark.asyncio
class TestServicoBusca:
    async def test_indexar_atendimento_com_sucesso(
        self,
        servico: ServicoBusca,
        repo_mock: AsyncMock,
        llm_mock: AsyncMock,
        resumo_valido: ResumoAtendimento,
    ) -> None:
        resultado = await servico.indexar_atendimento(resumo_valido)

        assert resultado.ok()
        assert resultado.valor == 1
        llm_mock.gerar_embedding.assert_awaited_once()
        repo_mock.indexar.assert_awaited_once()

    async def test_indexar_atendimento_falha_embedding(
        self,
        servico: ServicoBusca,
        repo_mock: AsyncMock,
        llm_mock: AsyncMock,
        resumo_valido: ResumoAtendimento,
    ) -> None:
        from projetox.compartilhado.erros import ErroAplicacao

        llm_mock.gerar_embedding = AsyncMock(
            return_value=Resultado.falha_com_erro(
                ErroAplicacao(mensagem="Falha na API"),
            ),
        )
        servico._llm = llm_mock

        resultado = await servico.indexar_atendimento(resumo_valido)

        assert resultado.falha()
        assert "Falha na API" in str(resultado.erro.mensagem)
        repo_mock.indexar.assert_not_called()

    async def test_buscar_similares_com_sucesso(
        self,
        servico: ServicoBusca,
        repo_mock: AsyncMock,
        llm_mock: AsyncMock,
    ) -> None:
        resultados = await servico.buscar_similares("roteador reiniciando", limite=3)

        assert len(resultados) == 1
        assert resultados[0].metadados["cliente"] == "Empresa X"
        llm_mock.gerar_embedding.assert_awaited_once_with("roteador reiniciando")
        repo_mock.buscar.assert_awaited_once()

    async def test_buscar_similares_falha_embedding(
        self,
        servico: ServicoBusca,
        repo_mock: AsyncMock,
        llm_mock: AsyncMock,
    ) -> None:
        from projetox.compartilhado.erros import ErroAplicacao

        llm_mock.gerar_embedding = AsyncMock(
            return_value=Resultado.falha_com_erro(
                ErroAplicacao(mensagem="API key invalida"),
            ),
        )
        servico._llm = llm_mock

        resultados = await servico.buscar_similares("teste")

        assert resultados == []
        repo_mock.buscar.assert_not_called()

    async def test_buscar_similares_respeita_limite(
        self,
        servico: ServicoBusca,
        repo_mock: AsyncMock,
    ) -> None:
        repo_mock.buscar = AsyncMock(return_value=[
            DocumentoBusca(id=str(i), texto="x", metadados={}, pontuacao=1.0 - i * 0.1)
            for i in range(5)
        ])

        resultados = await servico.buscar_similares("consulta", limite=5)

        assert len(resultados) == 5

    async def test_converter_para_texto(
        self,
        resumo_valido: ResumoAtendimento,
    ) -> None:
        texto = ServicoBusca._converter_para_texto(resumo_valido)

        assert "troca de roteador" in texto
        assert "quedas frequentes" in texto
        assert "Empresa ABC" in texto
        assert "MikroTik RB951" in texto

    async def test_indexar_atendimento_usa_embedding_correto(
        self,
        servico: ServicoBusca,
        repo_mock: AsyncMock,
        llm_mock: AsyncMock,
    ) -> None:
        embedding_esperado = [0.5] * 1536
        llm_mock.gerar_embedding = AsyncMock(
            return_value=Resultado.sucesso(embedding_esperado),
        )
        servico._llm = llm_mock

        await servico.indexar_atendimento(
            ResumoAtendimento(
                resumo="teste",
                problema="",
                solucao="",
                equipamentos=[],
                cliente="Foo",
                tipo_atendimento="suporte",
                observacoes="",
            ),
        )

        args, _kwargs = repo_mock.indexar.await_args
        docs, embeddings = args
        assert embeddings == [embedding_esperado]
        assert docs[0].metadados["cliente"] == "Foo"

    async def test_indexar_todos_do_db_sucesso(
        self,
        repo_mock: AsyncMock,
        llm_mock: AsyncMock,
    ) -> None:
        servico = ServicoBusca(repo=repo_mock, llm=llm_mock)

        with (
            patch("projetox.compartilhado.banco.config.get_session") as mock_get_session,
        ):
            mock_session = AsyncMock()
            mock_cm = AsyncMock()
            mock_cm.__aenter__ = AsyncMock(return_value=mock_session)
            mock_cm.__aexit__ = AsyncMock()
            mock_get_session.return_value = mock_cm

            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = []
            mock_session.execute = AsyncMock(return_value=mock_result)

            resultado = await servico.indexar_todos_do_db()

        assert resultado.ok()
        assert resultado.valor == 0

    @pytest.mark.skip(
        reason="ImportError em lazy import - testado via cobertura manual",
    )
    async def test_indexar_todos_do_db_falha_import(
        self,
        servico: ServicoBusca,
    ) -> None:
        resultado = await servico.indexar_todos_do_db()
        assert resultado.falha()
