import typer

from projetox.apresentacao.cli.comandos.acompanhamento import app as acompanhamento_app
from projetox.apresentacao.cli.comandos.transcricao import app as transcrever_app

app = typer.Typer(
    name="projetox",
    help="Assistente inteligente para fluxo de atendimentos",
    no_args_is_help=True,
)

app.add_typer(acompanhamento_app, name="acompanhamento", help="Gerenciar acompanhamentos")
app.add_typer(transcrever_app, name="transcrever", help="Transcrever audio gravado")

if __name__ == "__main__":
    app()
