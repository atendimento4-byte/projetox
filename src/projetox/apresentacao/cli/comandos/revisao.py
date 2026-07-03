from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.memoria.aplicacao.servico_memoria import ServicoMemoria
from projetox.memoria.infra.repositorio_obsidian import RepositorioNotasObsidian

app = typer.Typer(name="revisar", help="Revisar e editar resumo do atendimento")
console = Console()

_servico_memoria = ServicoMemoria(RepositorioNotasObsidian())

_ARQUIVO_OPTS = typer.Option(None, "--arquivo", "-a", help="Caminho do arquivo JSON com o resumo")
_RESUMO_OPTS = typer.Option(None, "--resumo", "-r", help="JSON do resumo do atendimento")


def _carregar_resumo(
    arquivo: Path | None,
    resumo_json: str | None,
) -> ResumoAtendimento:
    if arquivo:
        with open(arquivo, encoding="utf-8") as f:
            dados = json.load(f)
    elif resumo_json:
        dados = json.loads(resumo_json)
    else:
        console.print("[bold yellow]Forneca --arquivo ou --resumo com o JSON do resumo.[/]")
        raise typer.Exit(code=1)
    return ResumoAtendimento(**dados)


def _editar_campo(nome: str, valor_atual: str, multiline: bool = False) -> str:
    exibicao = valor_atual if valor_atual else "(vazio)"
    console.print(f"\n[bold cyan]{nome}:[/] {exibicao}")
    if multiline:
        console.print("[dim]Digite o texto (Enter confirma):[/]")
        novo = typer.prompt("Novo valor (Enter mantem atual)", default="", show_default=False)
        if not novo:
            return valor_atual
        return novo
    novo = typer.prompt("Novo valor (Enter mantem atual)", default="", show_default=False)
    if not novo:
        return valor_atual
    return novo


def _editar_lista(nome: str, valor_atual: list[str]) -> list[str]:
    atual = ", ".join(valor_atual) if valor_atual else "(vazio)"
    console.print(f"\n[bold cyan]{nome}:[/] {atual}")
    novo = typer.prompt(
        "Novos valores separados por virgula (Enter mantem atual)",
        default="",
        show_default=False,
    )
    if not novo:
        return valor_atual
    return [item.strip() for item in novo.split(",") if item.strip()]


def _exibir_preview(resumo: ResumoAtendimento) -> None:
    tabela = Table(title="Resumo Editado", show_lines=True)
    tabela.add_column("Campo", style="bold cyan")
    tabela.add_column("Valor")

    tabela.add_row("Resumo", resumo.resumo)
    tabela.add_row("Problema", resumo.problema)
    tabela.add_row("Solucao", resumo.solucao)
    tabela.add_row("Equipamentos", ", ".join(resumo.equipamentos) if resumo.equipamentos else "-")
    tabela.add_row("Cliente", resumo.cliente)
    tabela.add_row("Tipo", resumo.tipo_atendimento)
    tabela.add_row("Observacoes", resumo.observacoes)
    tabela.add_row(
        "Acoes Pendentes",
        "\n".join(f"- {a}" for a in resumo.acoes_pendentes) if resumo.acoes_pendentes else "-",
    )

    console.print(tabela)


@app.callback(invoke_without_command=True)
def revisar(
    ctx: typer.Context,
    arquivo: Path | None = _ARQUIVO_OPTS,
    resumo: str | None = _RESUMO_OPTS,
) -> None:
    """Revisar e editar manualmente o resumo do atendimento antes de salvar."""
    if ctx.invoked_subcommand is not None:
        return

    resumo_obj = _carregar_resumo(arquivo, resumo)

    console.print("\n[bold]=== Revisao do Resumo ===[/]")
    console.print("[dim]Deixe em branco para manter o valor atual.[/]")

    while True:
        resumo_obj.resumo = _editar_campo("Resumo", resumo_obj.resumo, multiline=True)
        resumo_obj.problema = _editar_campo("Problema", resumo_obj.problema)
        resumo_obj.solucao = _editar_campo("Solucao", resumo_obj.solucao)
        resumo_obj.equipamentos = _editar_lista("Equipamentos", resumo_obj.equipamentos)
        resumo_obj.observacoes = _editar_campo(
            "Observacoes", resumo_obj.observacoes, multiline=True,
        )

        console.print("\n[bold]=== Preview do Resumo Editado ===[/]")
        _exibir_preview(resumo_obj)

        acao = typer.prompt(
            "\n[E]ditar novamente, [C]onfirmar salvar no Obsidian, [X]ancelar",
            default="C",
            show_default=False,
        )
        acao = acao.strip().upper()

        if acao == "E":
            continue
        if acao == "X":
            console.print("[bold yellow]Operacao cancelada.[/]")
            raise typer.Exit(code=0)
        if acao == "C":
            break
        console.print("[bold red]Opcao invalida. Use E, C ou X.[/]")

    confirmar = typer.confirm("\nSalvar no Obsidian?", default=False)
    if not confirmar:
        console.print("[bold yellow]Operacao cancelada.[/]")
        raise typer.Exit(code=0)

    resultado = _servico_memoria.salvar(resumo_obj)
    if resultado.falha():
        console.print(f"[bold red]Erro ao salvar:[/] {resultado.erro}")
        raise typer.Exit(code=1)

    console.print("[bold green]Resumo salvo com sucesso no Obsidian![/]")
    console.print(f"  {resultado.valor}")
