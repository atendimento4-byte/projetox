from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from projetox.compartilhado.erros import ErroTranscricao, Resultado


class ITranscritor(ABC):
    @abstractmethod
    def transcrever(self, caminho_audio: Path) -> Resultado[str, ErroTranscricao]:
        ...
