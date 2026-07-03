from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from projetox.acompanhamento.aplicacao.servico_acompanhamento import (
    ServicoAcompanhamento,
)
from projetox.acompanhamento.infra.repositorio_memoria import (
    RepositorioSessaoMemoria,
)
from projetox.transcricao.aplicacao.servico_transcricao import ServicoTranscricao
from projetox.transcricao.infra.transcritor_whisper import TranscritorWhisper

app = typer.Typer(name="transcrever", help="Transcrever audio gravado")
console = Console()

_servico_acompanhamento = ServicoAcompanhamento(RepositorioSessaoMemoria())
_servico_transcricao = ServicoTranscricao(TranscritorWhisper())

_ARQUIVO_OPTS = typer.Option(None, "--arquivo", "-a", help="Caminho do arquivo WAV")


@app.callback(invoke_without_command=True)
def transcrever(
    ctx: typer.Context,
    arquivo: Path | None = _ARQUIVO_OPTS,
):
    if ctx.invoked_subcommand is not None:
        return

    if not arquivo:
        sessao = asyncio.run(_servico_acompanhamento.status())
        if sessao is None:
            console.print("[bold yellow]Nenhum acompanhamento em andamento.[/]")
            raise typer.Exit(code=1)

    descricao = (
        "Transcrevendo audio..."
        if arquivo
        else "Transcrevendo ultimo audio..."
    )
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task(descricao, total=None)
        resultado = (
            _servico_transcricao.transcrever(arquivo)
            if arquivo
            else _servico_transcricao.transcrever_ultimo_audio(sessao.id)
        )

    if resultado.falha():
        console.print(f"[bold red]Erro:[/] {resultado.erro.mensagem}")
        raise typer.Exit(code=1)
    console.print("[bold green]Transcricao concluida![/]")
    console.print(resultado.valor)
