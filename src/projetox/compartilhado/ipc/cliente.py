from __future__ import annotations

import json
import socket
from dataclasses import asdict
from typing import Any

from projetox.compartilhado.ipc.protocolo import MensagemIPC, RespostaIpc

PIPE_NAME = r"\\.\pipe\projetox"
TCP_HOST = "127.0.0.1"
TCP_PORT = 8790
TIMEOUT_SEGUNDOS = 10
TAMANHO_MAX_MSG = 65536

try:
    import pywintypes
    import win32file
    import win32pipe

    _TEM_WIN32PIPE = True
except ImportError:
    _TEM_WIN32PIPE = False


_MSG_DAEMON_OFFLINE = "Daemon nao esta rodando"


class ErroConexaoError(Exception):
    pass


class ClienteIPC:
    def __init__(self) -> None:
        self._timeout = TIMEOUT_SEGUNDOS

    def enviar_comando(
        self, metodo: str, params: dict[str, Any] | None = None,
    ) -> RespostaIpc:
        mensagem = MensagemIPC(metodo=metodo, params=params or {})

        if _TEM_WIN32PIPE:
            return self._enviar_named_pipe(mensagem)

        return self._enviar_tcp(mensagem)

    def _enviar_tcp(self, mensagem: MensagemIPC) -> RespostaIpc:
        try:
            with socket.create_connection(
                (TCP_HOST, TCP_PORT),
                timeout=self._timeout,
            ) as conn:
                dados = json.dumps(asdict(mensagem), ensure_ascii=False).encode("utf-8")
                conn.sendall(dados)
                resposta_bytes = conn.recv(TAMANHO_MAX_MSG)
        except (TimeoutError, ConnectionRefusedError, OSError) as exc:
            raise ErroConexaoError(_MSG_DAEMON_OFFLINE) from exc

        return self._parse_resposta(mensagem.id, resposta_bytes)

    def _enviar_named_pipe(self, mensagem: MensagemIPC) -> RespostaIpc:

        try:
            handle = win32file.CreateFile(
                PIPE_NAME,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None,
            )
            win32pipe.SetNamedPipeHandleState(
                handle,
                win32pipe.PIPE_READMODE_MESSAGE,
                None,
                None,
            )
            dados = json.dumps(asdict(mensagem), ensure_ascii=False).encode("utf-8")
            win32file.WriteFile(handle, dados)
            resposta_bytes, _ = win32file.ReadFile(handle, TAMANHO_MAX_MSG)
            win32file.CloseHandle(handle)
        except pywintypes.error as exc:
            raise ErroConexaoError(_MSG_DAEMON_OFFLINE) from exc

        return self._parse_resposta(mensagem.id, resposta_bytes)

    @staticmethod
    def _parse_resposta(id_esperado: str, dados: bytes) -> RespostaIpc:
        try:
            obj = json.loads(dados.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            return RespostaIpc(
                id=id_esperado, sucesso=False, erro=f"Resposta invalida: {exc}",
            )

        return RespostaIpc(
            id=obj.get("id", id_esperado),
            sucesso=obj.get("sucesso", False),
            dados=obj.get("dados"),
            erro=obj.get("erro"),
        )
