"""Testes para o protocolo IPC."""
from __future__ import annotations

from projetox.compartilhado.ipc.protocolo import MensagemIPC, RespostaIpc


class TestMensagemIPC:
    def test_criar_mensagem(self) -> None:
        msg = MensagemIPC(
            id="msg-001",
            metodo="acompanhamento.status",
            params={},
        )
        assert msg.id == "msg-001"
        assert msg.metodo == "acompanhamento.status"
        assert msg.params == {}

    def test_mensagem_com_parametros(self) -> None:
        msg = MensagemIPC(
            id="msg-002",
            metodo="acompanhamento.iniciar",
            params={"chamado": "123", "cliente": "ABC"},
        )
        assert msg.params["chamado"] == "123"


class TestRespostaIpc:
    def test_resposta_sucesso(self) -> None:
        resp = RespostaIpc(id="msg-001", sucesso=True, dados={"status": "active"})
        assert resp.sucesso
        assert resp.dados == {"status": "active"}
        assert resp.erro is None

    def test_resposta_erro(self) -> None:
        resp = RespostaIpc(
            id="msg-001", sucesso=False, erro="Metodo nao encontrado"
        )
        assert not resp.sucesso
        assert resp.erro == "Metodo nao encontrado"

    def test_resposta_sem_dados(self) -> None:
        resp = RespostaIpc(id="msg-001", sucesso=True)
        assert resp.sucesso
        assert resp.dados is None
