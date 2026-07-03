from __future__ import annotations

import asyncio

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from projetox.acompanhamento.aplicacao.servico_acompanhamento import (
    ServicoAcompanhamento,
)
from projetox.acompanhamento.infra.repositorio_memoria import (
    RepositorioSessaoMemoria,
)
from projetox.compartilhado.cache import CacheMemoria
from projetox.llm.aplicacao.servico_llm import ServicoLLM
from projetox.llm.infra.extrator_anthropic import ExtratorAnthropic
from projetox.transcricao.aplicacao.servico_transcricao import ServicoTranscricao
from projetox.transcricao.infra.transcritor_whisper import TranscritorWhisper

app = typer.Typer(name="resumir", help="Gerar resumo estruturado de atendimento")
console = Console()

_servico_acompanhamento = ServicoAcompanhamento(RepositorioSessaoMemoria())
_servico_transcricao = ServicoTranscricao(TranscritorWhisper())
_cache = CacheMemoria()
_servico_llm = ServicoLLM(ExtratorAnthropic(), cache=_cache)


def _exibir_resumo(resumo):
    tabela = Table(title="Resumo do Atendimento", show_lines=True)
    tabela.add_column("Campo", style="bold cyan")
    tabela.add_column("Valor")

    tabela.add_row("Resumo", resumo.resumo)
    tabela.add_row("Problema", resumo.problema)
    tabela.add_row("Solucao", resumo.solucao)
    tabela.add_row("Equipamentos", ", ".join(resumo.equipamentos) if resumo.equipamentos else "-")
    tabela.add_row("Cliente", resumo.cliente)
    tabela.add_row("Tipo", resumo.tipo_atendimento)
    tabela.add_row("Observacoes", resumo.observacoes)
    tabela.add_row(
        "Acoes Pendentes",
        "\n".join(f"- {a}" for a in resumo.acoes_pendentes) if resumo.acoes_pendentes else "-",
    )

    console.print(tabela)


@app.callback(invoke_without_command=True)
def resumir(
    ctx: typer.Context,
    texto: str | None = typer.Option(
        None, "--texto", "-t", help="Texto da transcricao para resumir",
    ),
    no_cache: bool = typer.Option(
        False, "--no-cache", help="Ignorar cache de respostas LLM",
    ),
):
    if ctx.invoked_subcommand is not None:
        return

    transcricao: str | None = texto

    if not transcricao:
        sessao = asyncio.run(_servico_acompanhamento.status())
        if sessao is None:
            console.print(
                "[bold yellow]Nenhum acompanhamento em andamento "
                "e nenhum --texto fornecido.[/]",
            )
            raise typer.Exit(code=1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Transcrevendo ultimo audio...", total=None)
            resultado_transcricao = _servico_transcricao.transcrever_ultimo_audio(
                sessao.id,
            )

        if resultado_transcricao.falha():
            console.print(
                f"[bold red]Erro na transcricao:[/] {resultado_transcricao.erro.mensagem}",
            )
            raise typer.Exit(code=1)

        transcricao = resultado_transcricao.valor

    servico = _servico_llm if not no_cache else ServicoLLM(ExtratorAnthropic())

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Extraindo pontos-chave e gerando resumo...", total=None)
        resultado = servico.resumir(transcricao)

    if resultado.falha():
        console.print(f"[bold red]Erro ao gerar resumo:[/] {resultado.erro.mensagem}")
        raise typer.Exit(code=1)

    cache_label = " [dim](cache)[/]" if servico.ultimo_cache_hit else ""
    console.print(f"[bold green]Resumo gerado com sucesso![/]{cache_label}")
    _exibir_resumo(resultado.valor)
