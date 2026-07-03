from __future__ import annotations

import threading
from pathlib import Path

import sounddevice as sd
import soundfile as sf

from projetox.audio.dominio.interfaces import IGravador


class GravadorSounddevice(IGravador):
    def __init__(self, samplerate: int = 44100, channels: int = 1) -> None:
        self.samplerate = samplerate
        self.channels = channels
        self._gravando: bool = False
        self._arquivo_atual: Path | None = None
        self._arquivo: sf.SoundFile | None = None
        self._thread: threading.Thread | None = None
        self._stream: sd.InputStream | None = None

    def _callback(self, indata, _frames, _time_info, _status) -> None:
        if self._arquivo is not None:
            self._arquivo.write(indata)

    def iniciar(self, path: Path) -> None:
        if self._gravando:
            msg = "Ja existe uma gravacao em andamento"
            raise RuntimeError(msg)

        path.parent.mkdir(parents=True, exist_ok=True)
        self._arquivo = sf.SoundFile(
            str(path),
            mode="w",
            samplerate=self.samplerate,
            channels=self.channels,
            subtype="PCM_16",
        )
        self._arquivo_atual = path
        self._gravando = True

        self._stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self._callback,
        )
        self._stream.start()

    def parar(self) -> Path:
        if not self._gravando or self._arquivo_atual is None:
            msg = "Nenhuma gravacao em andamento"
            raise RuntimeError(msg)

        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        if self._arquivo is not None:
            self._arquivo.close()
            self._arquivo = None

        path = self._arquivo_atual
        self._gravando = False
        self._arquivo_atual = None
        return path

    def esta_gravando(self) -> bool:
        return self._gravando
