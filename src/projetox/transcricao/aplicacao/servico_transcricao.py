from __future__ import annotations

from pathlib import Path

from projetox.compartilhado.erros import ErroTranscricao, Resultado
from projetox.transcricao.dominio.interfaces import ITranscritor

_TAMANHO_MINIMO_BYTES = 1024
_EXTENSAO_WAV = ".wav"


class ServicoTranscricao:
    def __init__(self, transcritor: ITranscritor) -> None:
        self._transcritor = transcritor

    def _validar_arquivo(self, caminho: Path) -> Resultado[None, ErroTranscricao]:
        if not caminho.exists():
            return Resultado.falha_com_erro(
                ErroTranscricao(
                    mensagem=f"Arquivo nao encontrado: {caminho}",
                ),
            )

        if caminho.suffix.lower() != _EXTENSAO_WAV:
            return Resultado.falha_com_erro(
                ErroTranscricao(
                    mensagem=f"Formato invalido: {caminho.suffix}. Use apenas .wav",
                ),
            )

        if caminho.stat().st_size < _TAMANHO_MINIMO_BYTES:
            return Resultado.falha_com_erro(
                ErroTranscricao(
                    mensagem=f"Arquivo muito pequeno ({caminho.stat().st_size}B). Minimo: 1KB",
                ),
            )

        return Resultado.sucesso(None)

    def transcrever(self, caminho: Path) -> Resultado[str, ErroTranscricao]:
        validacao = self._validar_arquivo(caminho)
        if validacao.falha():
            return Resultado.falha_com_erro(validacao.erro)
        return self._transcritor.transcrever(caminho)

    def transcrever_ultimo_audio(
        self,
        sessao_id: str,
        base_dir: Path | None = None,
    ) -> Resultado[str, ErroTranscricao]:
        diretorio = (base_dir or Path("dados/audio")) / sessao_id
        if not diretorio.exists():
            return Resultado.falha_com_erro(
                ErroTranscricao(
                    mensagem=f"Nenhum audio encontrado para sessao {sessao_id}",
                ),
            )
        audios = sorted(
            diretorio.glob("*.wav"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not audios:
            return Resultado.falha_com_erro(
                ErroTranscricao(
                    mensagem=f"Nenhum arquivo WAV encontrado em {diretorio}",
                ),
            )
        return self._transcritor.transcrever(audios[0])
