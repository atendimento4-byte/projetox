import typer
from rich.console import Console

app = typer.Typer(name="acompanhamento", help="Gerenciar acompanhamentos")
console = Console()

_state: dict = {"atual": None}


@app.command()
def iniciar(
    chamado: str = typer.Argument(help="Número do chamado"),
    cliente: str = typer.Argument(help="Nome do cliente"),
    tecnico: str = typer.Option(None, help="Nome do técnico responsável"),
    tipo: str = typer.Option("suporte", help="Tipo de atendimento"),
):
    _state["atual"] = {
        "chamado": chamado,
        "cliente": cliente,
        "tecnico": tecnico,
        "tipo": tipo,
        "status": "em_andamento",
    }
    console.print("[bold green]Acompanhamento iniciado![/]")
    console.print(f"  Chamado: {chamado}")
    console.print(f"  Cliente: {cliente}")
    if tecnico:
        console.print(f"  Técnico: {tecnico}")
    console.print(f"  Tipo:    {tipo}")


@app.command()
def finalizar():
    if _state["atual"] is None:
        console.print("[bold yellow]Nenhum acompanhamento em andamento.[/]")
        raise typer.Exit(code=1)
    _state["atual"]["status"] = "finalizado"
    chamado = _state["atual"]["chamado"]
    console.print(f"[bold green]Acompanhamento {chamado} finalizado![/]")
    _state["atual"] = None


@app.command()
def status():
    if _state["atual"] is None:
        console.print("[bold yellow]Nenhum acompanhamento em andamento.[/]")
        return
    console.print("[bold]Acompanhamento atual:[/]")
    console.print(f"  Chamado: {_state['atual']['chamado']}")
    console.print(f"  Cliente: {_state['atual']['cliente']}")
    console.print(f"  Técnico: {_state['atual'].get('tecnico', '—')}")
    console.print(f"  Tipo:    {_state['atual']['tipo']}")
    console.print(f"  Status:  {_state['atual']['status']}")
