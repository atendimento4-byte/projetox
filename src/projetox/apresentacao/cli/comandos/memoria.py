from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.table import Table

from projetox.acompanhamento.aplicacao.servico_acompanhamento import (
    ServicoAcompanhamento,
)
from projetox.acompanhamento.infra.repositorio_memoria import (
    RepositorioSessaoMemoria,
)
from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.memoria.aplicacao.servico_memoria import ServicoMemoria
from projetox.memoria.infra.repositorio_obsidian import (
    RepositorioNotasObsidian,
)

app = typer.Typer(name="salvar", help="Salvar conhecimento no Obsidian")
console = Console()

_servico_memoria = ServicoMemoria(RepositorioNotasObsidian())
_servico_acompanhamento = ServicoAcompanhamento(RepositorioSessaoMemoria())


@app.callback(invoke_without_command=True)
def salvar(
    ctx: typer.Context,
    resumo: str | None = typer.Option(
        None, "--resumo", "-r", help="JSON do resumo do atendimento",
    ),
) -> None:
    """Salvar resumo do atendimento no vault do Obsidian."""
    if ctx.invoked_subcommand is not None:
        return

    if not resumo:
        sessao = _servico_acompanhamento.status()
        if sessao is None:
            console.print("[bold yellow]Nenhum resumo disponivel.[/]")
            console.print("Use: projetox salvar --resumo '{\"resumo\":...}'")
            raise typer.Exit(code=1)
        console.print("[bold yellow]Resumo em memoria nao implementado.[/]")
        raise typer.Exit(code=1)

    try:
        dados = json.loads(resumo)
    except json.JSONDecodeError:
        console.print("[bold red]Resumo deve ser um JSON valido.[/]")
        raise typer.Exit(code=1) from None

    resumo_obj = ResumoAtendimento(**dados)

    console.print("\n[bold]Preview do salvamento:[/]")
    table = Table(show_header=False)
    table.add_row("Cliente", resumo_obj.cliente)
    table.add_row("Resumo", resumo_obj.resumo[:80] + "...")
    table.add_row("Equipamentos", ", ".join(resumo_obj.equipamentos))
    console.print(table)

    confirmar = typer.confirm("Salvar no Obsidian?", default=False)
    if not confirmar:
        console.print("[bold yellow]Operacao cancelada.[/]")
        raise typer.Exit(code=0)

    resultado = _servico_memoria.salvar(resumo_obj)
    if resultado.falha():
        console.print(
            f"[bold red]Erro ao salvar:[/] {resultado.erro}",
        )
        raise typer.Exit(code=1)

    console.print("[bold green]Salvo com sucesso![/]")
    console.print(f"  {resultado.valor}")
