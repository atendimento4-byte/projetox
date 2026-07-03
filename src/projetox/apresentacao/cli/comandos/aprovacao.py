from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from projetox.aprovacao.aplicacao.servico_aprovacao import ServicoAprovacao
from projetox.aprovacao.infra.repositorio_memoria import (
    RepositorioAprovacaoMemoria,
)

app = typer.Typer(name="pendentes", help="Gerenciar acoes pendentes de aprovacao")
console = Console()

_servico = ServicoAprovacao(RepositorioAprovacaoMemoria())


@app.callback(invoke_without_command=True)
def listar(ctx: typer.Context) -> None:
    """Listar acoes pendentes de aprovacao."""
    if ctx.invoked_subcommand is not None:
        return
    acoes = _servico.listar()
    if not acoes:
        console.print("[bold yellow]Nenhuma acao pendente.[/]")
        return

    table = Table(title="Acoes Pendentes", show_lines=True)
    table.add_column("ID", style="bold cyan", no_wrap=True)
    table.add_column("Tipo", style="bold")
    table.add_column("Titulo")
    table.add_column("Urgencia")
    table.add_column("Criada em")

    for acao in acoes:
        urgencia_style = {
            "alta": "bold red",
            "media": "bold yellow",
            "baixa": "bold green",
        }.get(acao.urgencia, "")
        table.add_row(
            acao.id[:8],
            acao.tipo,
            acao.titulo,
            f"[{urgencia_style}]{acao.urgencia}[/]",
            acao.criada_em.strftime("%d/%m/%Y %H:%M"),
        )

    console.print(table)


@app.command()
def aprovar(
    id: str = typer.Argument(help="ID da acao a aprovar"),
) -> None:
    """Aprovar uma acao pendente."""
    resultado = _servico.aprovar(id)
    if resultado.falha():
        console.print(f"[bold red]Erro:[/] {resultado.erro}")
        raise typer.Exit(code=1)
    console.print(f"[bold green]Sucesso:[/] {resultado.valor}")


@app.command()
def rejeitar(
    id: str = typer.Argument(help="ID da acao a rejeitar"),
) -> None:
    """Rejeitar uma acao pendente."""
    resultado = _servico.rejeitar(id)
    if resultado.falha():
        console.print(f"[bold red]Erro:[/] {resultado.erro}")
        raise typer.Exit(code=1)
    console.print(f"[bold green]Sucesso:[/] {resultado.valor}")
