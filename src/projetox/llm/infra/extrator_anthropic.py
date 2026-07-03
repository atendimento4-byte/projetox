from __future__ import annotations

import json
import os

from anthropic import Anthropic

from projetox.compartilhado.erros import ErroAplicacao, Resultado
from projetox.llm.dominio.entidades import ResumoAtendimento
from projetox.llm.dominio.interfaces import IExtratorLLM

_PROMPT = """Voce e um assistente especializado em analisar transcricoes de atendimentos tecnicos.

Extraia as seguintes informacoes da transcricao fornecida e retorne APENAS
um objeto JSON valido (sem markdown, sem texto adicional) com exatamente
estes campos:

- "resumo": resumo conciso do atendimento (2-3 frases)
- "problema": problema relatado pelo cliente
- "solucao": solucao aplicada pelo tecnico
- "equipamentos": lista de equipamentos envolvidos
- "cliente": nome do cliente ou empresa
- "tipo_atendimento": tipo (suporte, instalacao, manutencao, configuracao, etc.)
- "observacoes": observacoes relevantes adicionais
- "acoes_pendentes": lista de acoes que ainda precisam ser realizadas

Se algum campo nao for encontrado, use string vazia ou lista vazia.

Transcricao:
{transcricao}"""


class ExtratorAnthropic(IExtratorLLM):
    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self._cliente: Anthropic | None = None

    def _obter_cliente(self) -> Anthropic:
        if self._cliente is None:
            self._cliente = Anthropic(api_key=self._api_key)
        return self._cliente

    def extrair_resumo(
        self,
        transcricao: str,
    ) -> Resultado[ResumoAtendimento, ErroAplicacao]:
        try:
            cliente = self._obter_cliente()
            prompt = _PROMPT.format(transcricao=transcricao)
            resposta = cliente.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )
            conteudo = resposta.content[0].text
            dados = json.loads(conteudo)
            return Resultado.sucesso(
                ResumoAtendimento(
                    resumo=dados.get("resumo", ""),
                    problema=dados.get("problema", ""),
                    solucao=dados.get("solucao", ""),
                    equipamentos=dados.get("equipamentos", []),
                    cliente=dados.get("cliente", ""),
                    tipo_atendimento=dados.get("tipo_atendimento", ""),
                    observacoes=dados.get("observacoes", ""),
                    acoes_pendentes=dados.get("acoes_pendentes", []),
                ),
            )
        except Exception as exc:
            return Resultado.falha_com_erro(
                ErroAplicacao(
                    mensagem=f"Erro ao extrair resumo com Anthropic: {exc}",
                    causa=exc,
                ),
            )
