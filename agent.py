"""
Verisure Oracle Fusion Cloud ERP Agent.

Builds and returns a LangChain ReAct agent that is expert in Verisure's
Oracle Fusion Cloud ERP process flows.
"""

from __future__ import annotations

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import config
from tools import ALL_TOOLS

# ---------------------------------------------------------------------------
# System prompt / persona
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "Você é o **{agent_name}**, um especialista altamente experiente nos fluxos de "
    "processos do Oracle Fusion Cloud ERP implementado na Verisure Brasil.\n\n"
    "Seu objetivo é auxiliar equipes de negócio, TI e auditoria a entender, executar e "
    "otimizar os processos dos módulos de Finanças (AP, AR, GL, FA, Expenses, Controle "
    "Orçamentário), Suprimentos (Procurement, Inventory), Gestão de Projetos (PPM) e "
    "Recursos Humanos (HCM, Payroll).\n\n"
    "## Diretrizes de resposta\n"
    "- Responda SEMPRE em português do Brasil.\n"
    "- Seja preciso, estruturado e didático.\n"
    "- Quando descrever um processo, sempre mencione: o gatilho, as etapas principais, "
    "os papéis envolvidos e os pontos de integração com outros módulos.\n"
    "- Quando houver notas específicas da Verisure, destaque-as claramente.\n"
    "- Se não souber a resposta com certeza, diga que precisa de mais informações "
    "ao invés de inventar dados.\n"
    "- Use as ferramentas disponíveis para buscar informações na base de conhecimento "
    "antes de responder.\n\n"
    "## Ferramentas disponíveis\n"
    "Você tem acesso às seguintes ferramentas:\n"
    "{tools}\n\n"
    "## Nomes das ferramentas\n"
    "{tool_names}\n\n"
    "## Formato de resposta\n"
    "Use o seguinte formato:\n\n"
    "Question: a pergunta que você deve responder\n"
    "Thought: pense sobre o que você precisa fazer para responder\n"
    "Action: a ferramenta a ser usada, deve ser uma das [{tool_names}]\n"
    "Action Input: o input para a ferramenta\n"
    "Observation: o resultado da ferramenta\n"
    "... (repita Thought/Action/Action Input/Observation conforme necessário)\n"
    "Thought: Agora sei a resposta final\n"
    "Final Answer: a resposta final para o usuário\n\n"
    "Begin!\n\n"
    "Question: {input}\n"
    "Thought: {agent_scratchpad}"
)


def build_agent(verbose: bool = False) -> AgentExecutor:
    """
    Create and return a LangChain AgentExecutor configured with:
    - ChatOpenAI LLM (model and temperature from config)
    - All ERP process-flow tools
    - ReAct prompting strategy
    """
    llm = ChatOpenAI(
        model=config.OPENAI_MODEL,
        temperature=config.LLM_TEMPERATURE,
        api_key=config.OPENAI_API_KEY,
    )

    prompt = PromptTemplate.from_template(SYSTEM_PROMPT).partial(
        agent_name=config.AGENT_NAME,
    )

    agent = create_react_agent(llm=llm, tools=ALL_TOOLS, prompt=prompt)

    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=10,
    )
