from __future__ import annotations

import os
from pathlib import Path

from openai import OpenAI

from projetox.compartilhado.erros import ErroTranscricao, Resultado
from projetox.transcricao.dominio.interfaces import ITranscritor


class TranscritorWhisper(ITranscritor):
    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._cliente: OpenAI | None = None

    def _obter_cliente(self) -> OpenAI:
        if self._cliente is None:
            self._cliente = OpenAI(api_key=self._api_key)
        return self._cliente

    def transcrever(self, caminho_audio: Path) -> Resultado[str, ErroTranscricao]:
        try:
            cliente = self._obter_cliente()
            with open(caminho_audio, "rb") as arquivo:
                resposta = cliente.audio.transcriptions.create(
                    model="whisper-1",
                    file=arquivo,
                )
            return Resultado.sucesso(resposta.text)
        except Exception as exc:
            return Resultado.falha_com_erro(
                ErroTranscricao(
                    mensagem=f"Erro ao transcrever audio: {exc}",
                    causa=exc,
                ),
            )
