from __future__ import annotations

from datetime import datetime
from pathlib import Path

from projetox.audio.dominio.interfaces import IGravador


class ServicoAudio:
    def __init__(self, gravador: IGravador, base_dir: Path | None = None) -> None:
        self.gravador = gravador
        self.base_dir = base_dir or Path("dados/audio")

    def _caminho_arquivo(self, sessao_id: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.base_dir / sessao_id / f"{timestamp}.wav"

    def iniciar_gravacao(self, sessao_id: str) -> Path:
        caminho = self._caminho_arquivo(sessao_id)
        self.gravador.iniciar(caminho)
        return caminho

    def parar_gravacao(self, _sessao_id: str) -> Path:
        return self.gravador.parar()

    def esta_gravando(self) -> bool:
        return self.gravador.esta_gravando()
