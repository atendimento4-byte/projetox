"""Testes unitários para o sistema de erros compartilhado."""
from __future__ import annotations

from projetox.compartilhado.erros.hierarquia import (
    ErroAplicacao,
    ErroAplicacaoServico,
    ErroComunicacao,
    ErroConfiguracao,
    ErroDominio,
    ErroEntidadeNaoEncontrada,
    ErroInfraestrutura,
    ErroLLM,
    ErroPersistencia,
    ErroRegraNegocio,
    ErroTranscricao,
)
from projetox.compartilhado.erros.resultado import Resultado


class TestResultado:
    def test_sucesso(self) -> None:
        res = Resultado.sucesso(42)
        assert res.ok()
        assert not res.falha()
        assert res.valor == 42

    def test_falha(self) -> None:
        res = Resultado.falha_com_erro(ValueError("deu ruim"))
        assert not res.ok()
        assert res.falha()
        assert isinstance(res.erro, ValueError)

    def test_sucesso_com_string(self) -> None:
        res = Resultado.sucesso("ok")
        assert res.ok()
        assert res.valor == "ok"


class TestHierarquiaErros:
    def test_erro_aplicacao_base(self) -> None:
        erro = ErroAplicacao("msg")
        assert erro.mensagem == "msg"
        assert erro.causa is None

    def test_erro_dominio(self) -> None:
        erro = ErroDominio("regra violada")
        assert isinstance(erro, ErroAplicacao)

    def test_erro_regra_negocio(self) -> None:
        erro = ErroRegraNegocio("cliente invalido")
        assert isinstance(erro, ErroDominio)

    def test_erro_entidade_nao_encontrada(self) -> None:
        erro = ErroEntidadeNaoEncontrada("sessao nao encontrada")
        assert isinstance(erro, ErroDominio)

    def test_erro_aplicacao_servico(self) -> None:
        erro = ErroAplicacaoServico("falha no caso de uso")
        assert isinstance(erro, ErroAplicacao)

    def test_erro_infraestrutura(self) -> None:
        erro = ErroInfraestrutura("falha de rede")
        assert isinstance(erro, ErroAplicacao)

    def test_erro_persistencia(self) -> None:
        erro = ErroPersistencia("banco indisponivel")
        assert isinstance(erro, ErroInfraestrutura)

    def test_erro_comunicacao(self) -> None:
        erro = ErroComunicacao("API offline")
        assert isinstance(erro, ErroInfraestrutura)

    def test_erro_configuracao(self) -> None:
        erro = ErroConfiguracao("variavel faltando")
        assert isinstance(erro, ErroInfraestrutura)

    def test_erro_transcricao(self) -> None:
        erro = ErroTranscricao("audio corrompido")
        assert isinstance(erro, ErroInfraestrutura)

    def test_erro_llm(self) -> None:
        erro = ErroLLM("API key invalida")
        assert isinstance(erro, ErroInfraestrutura)

    def test_erro_com_causa(self) -> None:
        causa = ValueError("original")
        erro = ErroComunicacao("falha", causa=causa)
        assert erro.causa is causa

    def test_resultado_com_erro_hierarquia(self) -> None:
        erro = ErroRegraNegocio("teste")
        res = Resultado.falha_com_erro(erro)
        assert res.falha()
        assert isinstance(res.erro, ErroDominio)
