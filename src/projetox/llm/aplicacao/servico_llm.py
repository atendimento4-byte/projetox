from __future__ import annotations

from projetox.compartilhado.erros import ErroAplicacao, Resultado
from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.llm.dominio.interfaces import IExtratorLLM


class ServicoLLM:
    def __init__(self, extrator: IExtratorLLM) -> None:
        self._extrator = extrator

    def resumir(self, transcricao: str) -> Resultado[ResumoAtendimento, ErroAplicacao]:
        if not transcricao.strip():
            return Resultado.falha_com_erro(
                ErroAplicacao(mensagem="Transcricao vazia para gerar resumo"),
            )
        return self._extrator.extrair_resumo(transcricao)
