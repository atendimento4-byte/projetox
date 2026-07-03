from abc import ABC, abstractmethod
from pathlib import Path


class IGravador(ABC):
    @abstractmethod
    def iniciar(self, path: Path) -> None: ...

    @abstractmethod
    def parar(self) -> Path: ...

    @abstractmethod
    def pausar(self) -> None: ...

    @abstractmethod
    def retomar(self) -> None: ...

    @abstractmethod
    def esta_pausado(self) -> bool: ...

    @abstractmethod
    def esta_gravando(self) -> bool: ...
