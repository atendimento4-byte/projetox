import typer

from projetox.apresentacao.cli.comandos.acompanhamento import app as acompanhamento_app

app = typer.Typer(
    name="projetox",
    help="Assistente inteligente para fluxo de atendimentos",
    no_args_is_help=True,
)

app.add_typer(acompanhamento_app, name="acompanhamento", help="Gerenciar acompanhamentos")

if __name__ == "__main__":
    app()
