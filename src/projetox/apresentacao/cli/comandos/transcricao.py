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


_SUESTOES = [
    ("nao encontrado", "Verifique se o caminho do arquivo esta correto e tente novamente"),
    ("muito curto", "Gravacao precisa ter pelo menos 1 segundo de audio com fala"),
    ("autenticacao", "Confirme se a variavel OPENAI_API_KEY esta configurada corretamente"),
    ("limite de requisicoes", "Aguarde alguns segundos e tente novamente"),
    ("tempo limite", "Verifique sua conexao de internet e tente novamente"),
    ("corrompido", "Use um arquivo WAV valido. Converta o audio antes de tentar novamente"),
    ("vazia", "O arquivo de audio pode nao conter fala inteligivel. Grave novamente"),
    ("muito pequeno", "O arquivo de audio parece estar vazio ou corrompido"),
    ("inesperado", "Tente novamente. Se o erro persistir, contate o suporte"),
]


def _sugerir_acao(mensagem: str) -> str | None:
    msg = mensagem.lower()
    for padrao, sugestao in _SUESTOES:
        if padrao in msg:
            return sugestao
    return None

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
        mensagem = resultado.erro.mensagem
        sugestao = _sugerir_acao(mensagem)
        console.print(f"[bold red]Erro:[/] {mensagem}")
        if sugestao:
            console.print(f"[bold yellow]Sugestao:[/] {sugestao}")
        raise typer.Exit(code=1)
    console.print("[bold green]Transcricao concluida![/]")
    console.print(resultado.valor)
