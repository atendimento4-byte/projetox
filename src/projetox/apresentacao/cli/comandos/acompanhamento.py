import asyncio

import typer
from rich.console import Console
from rich.text import Text

from projetox.acompanhamento.aplicacao.servico_acompanhamento import (
    ServicoAcompanhamento,
)
from projetox.acompanhamento.infra.repositorio_memoria import (
    RepositorioSessaoMemoria,
)
from projetox.audio.aplicacao.servico_audio import ServicoAudio
from projetox.audio.infra.gravador_sounddevice import GravadorSounddevice

app = typer.Typer(name="acompanhamento", help="Gerenciar acompanhamentos")
gravar_app = typer.Typer(name="gravar", help="Gerenciar gravacao de audio")
console = Console()

_servico = ServicoAcompanhamento(RepositorioSessaoMemoria())
_servico_audio = ServicoAudio(GravadorSounddevice())


def _indicador_gravacao() -> Text:
    if _servico_audio.esta_gravando():
        return Text("[GRAVANDO]", style="bold red")
    return Text("[PARADO]", style="bold white")


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


@gravar_app.command("iniciar")
def iniciar_gravacao():
    sessao = asyncio.run(_servico.status())
    if sessao is None:
        console.print("[bold yellow]Nenhum acompanhamento em andamento.[/]")
        raise typer.Exit(code=1)

    if _servico_audio.esta_gravando():
        console.print("[bold yellow]Gravacao ja esta em andamento.[/]")
        raise typer.Exit(code=1)

    confirm = typer.confirm("Confirmar inicio de gravacao?", default=False)
    if not confirm:
        console.print("[bold yellow]Gravacao cancelada.[/]")
        return

    caminho = _servico_audio.iniciar_gravacao(sessao.id)
    console.print(f"[bold green]Gravacao iniciada![/]  {_indicador_gravacao()}")
    console.print(f"  Arquivo: {caminho}")


@gravar_app.command()
def parar():
    if not _servico_audio.esta_gravando():
        console.print("[bold yellow]Nenhuma gravacao em andamento.[/]")
        raise typer.Exit(code=1)

    caminho = _servico_audio.parar_gravacao("")
    console.print(f"[bold green]Gravacao finalizada![/]  {_indicador_gravacao()}")
    console.print(f"  Arquivo: {caminho}")


app.add_typer(gravar_app)
