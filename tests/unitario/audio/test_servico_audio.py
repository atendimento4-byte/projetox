"""Testes unitários para o serviço de áudio."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from projetox.audio.dominio.interfaces import IGravador


class TestServicoAudio:
    def test_iniciar_gravacao(self) -> None:
        gravador = MagicMock(spec=IGravador)
        from projetox.audio.aplicacao.servico_audio import (
            ServicoAudio,
        )

        servico = ServicoAudio(gravador)
        caminho = servico.iniciar_gravacao("sessao-001")
        assert caminho is not None
        assert "sessao-001" in str(caminho)
        gravador.iniciar.assert_called_once()

    def test_parar_gravacao_retorna_caminho(self) -> None:
        gravador = MagicMock(spec=IGravador)
        gravador.parar.return_value = Path("/tmp/audio.wav")
        from projetox.audio.aplicacao.servico_audio import (
            ServicoAudio,
        )

        servico = ServicoAudio(gravador)
        resultado = servico.parar_gravacao("sessao-001")
        assert resultado == Path("/tmp/audio.wav")

    def test_pausar_retomar_gravacao(self) -> None:
        gravador = MagicMock(spec=IGravador)
        from projetox.audio.aplicacao.servico_audio import (
            ServicoAudio,
        )

        servico = ServicoAudio(gravador)
        servico.pausar_gravacao()
        gravador.pausar.assert_called_once()
        servico.retomar_gravacao()
        gravador.retomar.assert_called_once()

    def test_esta_gravando(self) -> None:
        gravador = MagicMock(spec=IGravador)
        gravador.esta_gravando.return_value = True
        from projetox.audio.aplicacao.servico_audio import (
            ServicoAudio,
        )

        servico = ServicoAudio(gravador)
        assert servico.esta_gravando()

    def test_esta_pausado(self) -> None:
        gravador = MagicMock(spec=IGravador)
        gravador.esta_pausado.return_value = True
        from projetox.audio.aplicacao.servico_audio import (
            ServicoAudio,
        )

        servico = ServicoAudio(gravador)
        assert servico.esta_pausado()
