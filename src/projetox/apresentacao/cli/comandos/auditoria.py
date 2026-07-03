import typer
from rich.console import Console
from rich.table import Table

from projetox.auditoria.aplicacao.servico_auditoria import ServicoAuditoria

app = typer.Typer(name="auditoria", help="Consultar log de auditoria")
console = Console()

_servico = ServicoAuditoria()


@app.callback(invoke_without_command=True)
def listar(
    ctx: typer.Context,
    limite: int = typer.Option(20, "--limite", "-l", help="Numero de registros"),
) -> None:
    if ctx.invoked_subcommand is not None:
        return

    registros = _servico.listar(limite=limite)

    if not registros:
        console.print("[bold yellow]Nenhum registro de auditoria encontrado.[/]")
        raise typer.Exit(code=0)

    table = Table(title=f"Auditoria (ultimos {len(registros)} registros)")
    table.add_column("ID", style="dim")
    table.add_column("Acao")
    table.add_column("Usuario")
    table.add_column("Sessao")
    table.add_column("Data")

    for r in reversed(registros):
        table.add_row(
            r.id[:8],
            r.acao,
            r.usuario,
            r.sessao_id[:8] if r.sessao_id else "-",
            r.criado_em.strftime("%H:%M:%S"),
        )

    console.print(table)
