from __future__ import annotations

import asyncio
import signal
import sys
from dataclasses import asdict
from pathlib import Path

import structlog

from projetox.acompanhamento.aplicacao.servico_acompanhamento import (
    ServicoAcompanhamento,
)
from projetox.acompanhamento.infra.repositorio_memoria import (
    RepositorioSessaoMemoria,
)
from projetox.aprovacao.aplicacao.servico_aprovacao import ServicoAprovacao
from projetox.aprovacao.infra.repositorio_memoria import (
    RepositorioAprovacaoMemoria,
)
from projetox.audio.aplicacao.servico_audio import ServicoAudio
from projetox.audio.infra.gravador_sounddevice import GravadorSounddevice
from projetox.auditoria.aplicacao.servico_auditoria import ServicoAuditoria
from projetox.compartilhado.erros.resultado import Resultado
from projetox.compartilhado.ipc import servidor
from projetox.compartilhado.ipc.servidor import ServidorIPC
from projetox.llm.aplicacao.servico_llm import ServicoLLM
from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.llm.infra.extrator_nvidia import ExtratorNVIDIA
from projetox.memoria.aplicacao.servico_memoria import ServicoMemoria
from projetox.memoria.infra.repositorio_obsidian import (
    RepositorioNotasObsidian,
)
from projetox.transcricao.aplicacao.servico_transcricao import (
    ServicoTranscricao,
)
from projetox.transcricao.infra.transcritor_whisper import TranscritorWhisper

logger = structlog.get_logger(__name__)


def _serializar_sessao(sessao: object) -> dict | None:
    if sessao is None:
        return None
    return asdict(sessao)


def _serializar_resultado(resultado: object) -> dict:
    if isinstance(resultado, Resultado):
        if resultado.ok():
            return {"sucesso": True, "valor": resultado.valor}
        return {"sucesso": False, "erro": str(resultado.erro)}
    return {"sucesso": True, "valor": resultado}


def _serializar_para_lista(itens: list) -> list[dict]:
    return [asdict(i) for i in itens]


def _criar_servicos() -> dict:
    repo_sessao = RepositorioSessaoMemoria()
    return {
        "acompanhamento": ServicoAcompanhamento(repo_sessao),
        "audio": ServicoAudio(GravadorSounddevice()),
        "memoria": ServicoMemoria(RepositorioNotasObsidian()),
        "transcricao": ServicoTranscricao(TranscritorWhisper()),
        "llm": ServicoLLM(ExtratorNVIDIA()),
        "aprovacao": ServicoAprovacao(RepositorioAprovacaoMemoria()),
        "auditoria": ServicoAuditoria(),
    }


def _registrar_handlers(srv: ServidorIPC, s: dict) -> None:
    srv.registrar(
        "acompanhamento.iniciar",
        lambda c, cl, te="", ti="suporte": _serializar_sessao(
            asyncio.run(s["acompanhamento"].iniciar(chamado=c, cliente=cl, tecnico=te, tipo=ti)),
        ),
    )
    srv.registrar(
        "acompanhamento.finalizar",
        lambda: _serializar_sessao(asyncio.run(s["acompanhamento"].finalizar())),
    )
    srv.registrar(
        "acompanhamento.status",
        lambda: _serializar_sessao(asyncio.run(s["acompanhamento"].status())),
    )

    srv.registrar(
        "audio.gravar.iniciar",
        lambda sessao_id: {"caminho": str(s["audio"].iniciar_gravacao(sessao_id))},
    )
    srv.registrar(
        "audio.gravar.parar",
        lambda sessao_id="": {"caminho": str(s["audio"].parar_gravacao(sessao_id))},
    )
    srv.registrar(
        "audio.gravar.pausar",
        lambda: s["audio"].pausar_gravacao() or {},
    )
    srv.registrar(
        "audio.gravar.retomar",
        lambda: s["audio"].retomar_gravacao() or {},
    )
    srv.registrar(
        "audio.status",
        lambda: {
            "gravando": s["audio"].esta_gravando(),
            "pausado": s["audio"].esta_pausado(),
        },
    )

    def _transcrever(caminho: str) -> dict:
        resultado = s["transcricao"].transcrever(Path(caminho))
        if resultado.ok():
            return {"texto": resultado.valor}
        return {"erro": str(resultado.erro)}

    srv.registrar("transcricao.transcrever", _transcrever)

    def _resumir(transcricao: str) -> dict:
        resultado = s["llm"].resumir(transcricao)
        if resultado.ok():
            return asdict(resultado.valor)
        return {"erro": str(resultado.erro)}

    srv.registrar("llm.resumir", _resumir)

    def _salvar(resumo: dict) -> dict:
        resumo_obj = ResumoAtendimento(**resumo)
        resultado = s["memoria"].salvar(resumo_obj)
        if resultado.ok():
            return {"mensagem": resultado.valor}
        return {"erro": str(resultado.erro)}

    srv.registrar("memoria.salvar", _salvar)

    srv.registrar(
        "aprovacao.listar",
        lambda: _serializar_para_lista(s["aprovacao"].listar()),
    )

    srv.registrar(
        "aprovacao.adicionar",
        lambda tipo, titulo, descricao="", dados=None, urgencia="baixa": asdict(
            s["aprovacao"].adicionar_acao(
                tipo=tipo, titulo=titulo, descricao=descricao,
                dados=dados or {}, urgencia=urgencia,
            ),
        ),
    )

    def _aprovar(id: str) -> dict:
        return _serializar_resultado(s["aprovacao"].aprovar(id))

    srv.registrar("aprovacao.aprovar", _aprovar)

    def _rejeitar(id: str) -> dict:
        return _serializar_resultado(s["aprovacao"].rejeitar(id))

    srv.registrar("aprovacao.rejeitar", _rejeitar)

    srv.registrar(
        "auditoria.listar",
        lambda limite=50: _serializar_para_lista(s["auditoria"].listar(limite=limite)),
    )


def _registrar_sinais(srv: ServidorIPC) -> None:
    def sinal_parar(signum: int, _frame: object) -> None:
        logger.info("daemon.parando", signal=signum)
        srv.parar()
        sys.exit(0)

    signal.signal(signal.SIGINT, sinal_parar)
    signal.signal(signal.SIGTERM, sinal_parar)


def main() -> None:
    logger.info("daemon.iniciando")

    servicos = _criar_servicos()
    sv = ServidorIPC()
    _registrar_handlers(sv, servicos)
    _registrar_sinais(sv)

    logger.info("daemon.inicializado", handlers=list(sv._handlers.keys()))
    sv.iniciar()
