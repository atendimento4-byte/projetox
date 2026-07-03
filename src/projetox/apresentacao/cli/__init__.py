import typer

from projetox.apresentacao.cli.comandos.acompanhamento import app as acompanhamento_app
from projetox.apresentacao.cli.comandos.aprovacao import app as pendentes_app
from projetox.apresentacao.cli.comandos.auditoria import app as auditoria_app
from projetox.apresentacao.cli.comandos.llm import app as resumir_app
from projetox.apresentacao.cli.comandos.memoria import app as salvar_app
from projetox.apresentacao.cli.comandos.revisao import app as revisar_app
from projetox.apresentacao.cli.comandos.transcricao import app as transcrever_app

app = typer.Typer(
    name="projetox",
    help="Assistente inteligente para fluxo de atendimentos",
    no_args_is_help=True,
)

app.add_typer(acompanhamento_app, name="acompanhamento", help="Gerenciar acompanhamentos")
app.add_typer(transcrever_app, name="transcrever", help="Transcrever audio gravado")
app.add_typer(resumir_app, name="resumir", help="Gerar resumo estruturado de atendimento")
app.add_typer(revisar_app, name="revisar", help="Revisar e editar resumo antes de salvar")
app.add_typer(salvar_app, name="salvar", help="Salvar conhecimento no Obsidian")
app.add_typer(pendentes_app, name="pendentes", help="Gerenciar acoes pendentes de aprovacao")
app.add_typer(auditoria_app, name="auditoria", help="Consultar log de auditoria")

if __name__ == "__main__":
    app()
