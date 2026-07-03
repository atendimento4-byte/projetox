from __future__ import annotations

from pathlib import Path

from projetox.compartilhado.erros import ErroTranscricao, Resultado
from projetox.transcricao.dominio.interfaces import ITranscritor


class ServicoTranscricao:
    def __init__(self, transcritor: ITranscritor) -> None:
        self._transcritor = transcritor

    def transcrever(self, caminho: Path) -> Resultado[str, ErroTranscricao]:
        if not caminho.exists():
            return Resultado.falha_com_erro(
                ErroTranscricao(mensagem=f"Arquivo nao encontrado: {caminho}"),
            )
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
