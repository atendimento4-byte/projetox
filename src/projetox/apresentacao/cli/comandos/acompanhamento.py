import asyncio

import typer
from rich.console import Console

from projetox.acompanhamento.aplicacao.servico_acompanhamento import (
    ServicoAcompanhamento,
)
from projetox.acompanhamento.infra.repositorio_memoria import (
    RepositorioSessaoMemoria,
)

app = typer.Typer(name="acompanhamento", help="Gerenciar acompanhamentos")
console = Console()

_servico = ServicoAcompanhamento(RepositorioSessaoMemoria())


@app.command()
def iniciar(
    chamado: str = typer.Argument(help="Número do chamado"),
    cliente: str = typer.Argument(help="Nome do cliente"),
    tecnico: str = typer.Option(None, help="Nome do técnico responsável"),
    tipo: str = typer.Option("suporte", help="Tipo de atendimento"),
):
    sessao = asyncio.run(
        _servico.iniciar(
            chamado=chamado,
            cliente=cliente,
            tecnico=tecnico or "",
            tipo=tipo,
        ),
    )
    console.print("[bold green]Acompanhamento iniciado![/]")
    console.print(f"  Chamado: {sessao.chamado}")
    console.print(f"  Cliente: {sessao.cliente}")
    if sessao.tecnico:
        console.print(f"  Técnico: {sessao.tecnico}")
    console.print(f"  Tipo:    {sessao.tipo}")


@app.command()
def finalizar():
    sessao = asyncio.run(_servico.finalizar())
    if sessao is None:
        console.print("[bold yellow]Nenhum acompanhamento em andamento.[/]")
        raise typer.Exit(code=1)
    console.print(f"[bold green]Acompanhamento {sessao.chamado} finalizado![/]")


@app.command()
def status():
    sessao = asyncio.run(_servico.status())
    if sessao is None:
        console.print("[bold yellow]Nenhum acompanhamento em andamento.[/]")
        return
    console.print("[bold]Acompanhamento atual:[/]")
    console.print(f"  Chamado: {sessao.chamado}")
    console.print(f"  Cliente: {sessao.cliente}")
    console.print(f"  Técnico: {sessao.tecnico or '—'}")
    console.print(f"  Tipo:    {sessao.tipo}")
    console.print(f"  Status:  {sessao.status}")
