from __future__ import annotations

import json
import socket
from collections.abc import Callable
from contextlib import suppress
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

try:
    import pywintypes
    import win32file
    import win32pipe

    _TEM_WIN32PIPE = True
except ImportError:
    _TEM_WIN32PIPE = False


PIPE_NAME = r"\\.\pipe\projetox"
TCP_HOST = "127.0.0.1"
TCP_PORT = 8790
TAMANHO_MAX_MSG = 65536


def _serializar(valor: Any) -> Any:
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, Path):
        return str(valor)
    if is_dataclass(valor):
        return asdict(valor)
    if isinstance(valor, Exception):
        return str(valor)
    return valor


def _para_json(resposta: dict) -> bytes:
    return json.dumps(resposta, default=_serializar, ensure_ascii=False).encode("utf-8")


class ServidorIPC:
    def __init__(self) -> None:
        self._handlers: dict[str, Callable[..., Any]] = {}
        self._rodando = False
        self._socket: socket.socket | None = None
        self._pipe_handle: Any = None

    def registrar(self, metodo: str, handler: Callable[..., Any]) -> None:
        self._handlers[metodo] = handler

    def iniciar(self) -> None:
        self._rodando = True
        transporte = "tcp" if not _TEM_WIN32PIPE else "named_pipe"
        logger.info("ipc.servidor.iniciando", transporte=transporte)

        if _TEM_WIN32PIPE:
            self._iniciar_named_pipe()
        else:
            self._iniciar_tcp()

    def _iniciar_tcp(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((TCP_HOST, TCP_PORT))
        self._socket.listen(5)
        self._socket.settimeout(1.0)
        logger.info("ipc.servidor.tcp.ouvindo", host=TCP_HOST, porta=TCP_PORT)

        while self._rodando:
            try:
                conn, _addr = self._socket.accept()
            except TimeoutError:
                continue
            except OSError:
                break

            try:
                with conn:
                    dados = conn.recv(TAMANHO_MAX_MSG)
                    if not dados:
                        continue
                    resposta = self._processar(dados)
                    conn.sendall(resposta)
            except Exception:
                logger.exception("ipc.servidor.erro_conexao")
                with suppress(Exception):
                    conn.close()

    def _iniciar_named_pipe(self) -> None:

        while self._rodando:
            try:
                self._pipe_handle = win32pipe.CreateNamedPipe(
                    PIPE_NAME,
                    win32pipe.PIPE_ACCESS_DUPLEX,
                    win32pipe.PIPE_TYPE_MESSAGE
                    | win32pipe.PIPE_READMODE_MESSAGE
                    | win32pipe.PIPE_WAIT,
                    1,
                    TAMANHO_MAX_MSG,
                    TAMANHO_MAX_MSG,
                    0,
                    None,
                )
                logger.info("ipc.servidor.pipe.aguardando")
                win32pipe.ConnectNamedPipe(self._pipe_handle, None)
                dados, _ = win32file.ReadFile(self._pipe_handle, TAMANHO_MAX_MSG)
                resposta = self._processar(dados)
                win32file.WriteFile(self._pipe_handle, resposta)
                win32pipe.DisconnectNamedPipe(self._pipe_handle)
            except pywintypes.error:
                break
            except Exception:
                logger.exception("ipc.servidor.erro_pipe")

    def _processar(self, dados: bytes) -> bytes:
        try:
            mensagem = json.loads(dados.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            logger.warning("ipc.servidor.json_invalido", dados=dados[:200])
            return _para_json(
                {"id": "", "sucesso": False, "erro": "JSON invalido"},
            )

        id_msg = mensagem.get("id", "")
        metodo = mensagem.get("metodo", "")
        params = mensagem.get("params", {})

        logger.info("ipc.servidor.chamada", metodo=metodo, id=id_msg)

        handler = self._handlers.get(metodo)
        if handler is None:
            logger.warning("ipc.servidor.metodo_nao_encontrado", metodo=metodo)
            return _para_json(
                {
                    "id": id_msg,
                    "sucesso": False,
                    "erro": f"Metodo nao encontrado: {metodo}",
                },
            )

        try:
            resultado = handler(**params) if isinstance(params, dict) else handler(params)
            return _para_json({"id": id_msg, "sucesso": True, "dados": resultado})
        except Exception as exc:
            logger.exception("ipc.servidor.erro_handler", metodo=metodo, erro=str(exc))
            return _para_json({"id": id_msg, "sucesso": False, "erro": str(exc)})

    def parar(self) -> None:
        self._rodando = False
        if _TEM_WIN32PIPE and self._pipe_handle is not None:
            with suppress(Exception):
                win32pipe.DisconnectNamedPipe(self._pipe_handle)
        if self._socket is not None:
            with suppress(OSError):
                self._socket.close()
        logger.info("ipc.servidor.parado")
