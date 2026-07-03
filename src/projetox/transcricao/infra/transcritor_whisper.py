from __future__ import annotations

import os
from pathlib import Path
from typing import NoReturn

import soundfile as sf
import structlog
from openai import (
    APIError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

from projetox.compartilhado.erros import ErroTranscricao, Resultado
from projetox.transcricao.dominio.interfaces import ITranscritor

logger = structlog.get_logger(__name__)

_DURACAO_MINIMA_SEGUNDOS = 1.0


class _ErroTranscricaoEx(BaseException):
    def __init__(self, erro: ErroTranscricao) -> None:
        self.erro = erro


class TranscritorWhisper(ITranscritor):
    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._cliente: OpenAI | None = None
        self._caminho_atual: Path | None = None

    def _obter_cliente(self) -> OpenAI:
        if self._cliente is None:
            self._cliente = OpenAI(api_key=self._api_key)
        return self._cliente

    def _falhar(self, msg: str, causa: Exception | None = None) -> NoReturn:
        raise _ErroTranscricaoEx(ErroTranscricao(mensagem=msg, causa=causa))

    def _log_e_falhar(self, log_ref: str, msg: str, causa: Exception | None = None) -> NoReturn:
        logger.exception(log_ref, caminho=str(self._caminho_atual), erro=str(causa))
        raise _ErroTranscricaoEx(ErroTranscricao(mensagem=msg, causa=causa))

    def _validar_audio(self, caminho: Path) -> None:
        try:
            with sf.SoundFile(caminho) as f:
                duracao = f.frames / f.samplerate
        except FileNotFoundError:
            self._log_e_falhar("arquivo_nao_encontrado", f"Arquivo nao encontrado: {caminho}")
        except sf.SoundFileError as exc:
            self._log_e_falhar(
                "audio_corrompido",
                "Arquivo de audio corrompido ou em formato nao suportado",
                exc,
            )

        if duracao < _DURACAO_MINIMA_SEGUNDOS:
            logger.warning("audio_muito_curto", caminho=str(caminho), duracao_segundos=duracao)
            self._falhar(f"Audio muito curto ({duracao:.1f}s). Minimo: 1s")

    def _transcrever_api(self, caminho: Path) -> str:
        cliente = self._obter_cliente()
        with open(caminho, "rb") as arquivo:
            resposta = cliente.audio.transcriptions.create(model="whisper-1", file=arquivo)
        texto = resposta.text
        if not texto or not texto.strip():
            self._log_e_falhar("resposta_vazia_api",
                               "API retornou transcricao vazia. Verifique se ha fala no audio")
        return texto

    def _tratar_erro_api(self, exc: Exception, caminho: Path) -> Resultado[str, ErroTranscricao]:
        mapa: dict[type, tuple[str, str]] = {
            FileNotFoundError: ("arquivo_nao_encontrado", f"Arquivo nao encontrado: {caminho}"),
            AuthenticationError: ("erro_autenticacao_api",
                                  "Falha de autenticacao. Verifique a chave OPENAI_API_KEY"),
            RateLimitError: ("limite_taxa_api",
                             "Limite de requisicoes da API excedido. Aguarde e tente novamente"),
            APITimeoutError: ("timeout_api",
                              "Tempo limite excedido. Verifique sua conexao de internet"),
        }
        tipo = type(exc)
        if tipo in mapa:
            log_ref, msg = mapa[tipo]
            logger.exception(log_ref, erro=str(exc))
            return Resultado.falha_com_erro(ErroTranscricao(mensagem=msg, causa=exc))

        if isinstance(exc, APIError):
            logger.exception("erro_api_openai", status_code=exc.status_code, erro=str(exc))
            return Resultado.falha_com_erro(
                ErroTranscricao(mensagem=f"Erro na API OpenAI (status {exc.status_code})", causa=exc),  # noqa: E501
            )

        logger.exception("erro_inesperado", caminho=str(caminho))
        return Resultado.falha_com_erro(
            ErroTranscricao(mensagem=f"Erro inesperado ao transcrever audio: {exc}", causa=exc),
        )

    def transcrever(self, caminho_audio: Path) -> Resultado[str, ErroTranscricao]:
        self._caminho_atual = caminho_audio

        try:
            self._validar_audio(caminho_audio)
            texto = self._transcrever_api(caminho_audio)
            logger.info("transcricao_concluida", caminho=str(caminho_audio))
            return Resultado.sucesso(texto)
        except _ErroTranscricaoEx as exc:
            return Resultado.falha_com_erro(exc.erro)
        except Exception as exc:
            return self._tratar_erro_api(exc, caminho_audio)
