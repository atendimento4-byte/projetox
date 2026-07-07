from __future__ import annotations

import asyncio

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from projetox.busca.aplicacao.servico_busca import ServicoBusca
from projetox.busca.infra.qdrant_repo import QdrantRepositorioBusca
from projetox.compartilhado.cache import CacheMemoria
from projetox.llm.aplicacao.servico_llm import ServicoLLM
from projetox.llm.infra.extrator_nvidia import ExtratorNVIDIA

app = typer.Typer(name="busca", help="Busca semantica em atendimentos")
console = Console()

_repo = QdrantRepositorioBusca()
_cache = CacheMemoria()
_llm = ServicoLLM(ExtratorNVIDIA(), cache=_cache)
_servico = ServicoBusca(repo=_repo, llm=_llm)


@app.callback(invoke_without_command=True)
def buscar(
    ctx: typer.Context,
    consulta: str = typer.Argument(
        None, help="Texto da consulta para busca semantica",
    ),
    limite: int = typer.Option(5, "--limite", "-l", help="Numero maximo de resultados"),
):
    """Busca semantica em atendimentos anteriores."""
    if ctx.invoked_subcommand is not None:
        return

    if not consulta:
        console.print("[bold yellow]Forneca um texto de consulta.[/]")
        console.print("  Exemplo: projetox busca \"roteador reiniciando\"")
        raise typer.Exit(code=1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Buscando atendimentos similares...", total=None)
        resultados = asyncio.run(_servico.buscar_similares(consulta, limite=limite))

    if not resultados:
        console.print("[bold yellow]Nenhum resultado encontrado.[/]")
        return

    tabela = Table(title=f"Resultados da busca: {consulta}")
    tabela.add_column("Score", style="cyan", justify="right")
    tabela.add_column("Cliente", style="green")
    tabela.add_column("Problema")
    tabela.add_column("Solucao")

    for doc in resultados:
        tabela.add_row(
            f"{doc.pontuacao:.3f}",
            doc.metadados.get("cliente", "-"),
            doc.metadados.get("problema", "-"),
            doc.metadados.get("solucao", "-"),
        )

    console.print(tabela)


@app.command()
def indexar():
    """Indexa todos os atendimentos do banco de dados."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Indexando atendimentos do banco...", total=None)
        resultado = asyncio.run(_servico.indexar_todos_do_db())

    if resultado.falha():
        console.print(f"[bold red]Erro ao indexar:[/] {resultado.erro.mensagem}")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Indexacao concluida![/] {resultado.valor} atendimentos indexados.")
