"""
Oracle Fusion Cloud ERP Agent – Verisure.

Builds and exposes a LangChain ReAct agent pre-loaded with knowledge of
Oracle Fusion Cloud ERP process flows specific to the Verisure client.
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

import config
from tools import TOOLS

# ──────────────────────────────────────────────────────────────────────────────
# System prompt / agent persona
# ──────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Você é um agente especialista nos fluxos de processos do \
Oracle Fusion Cloud ERP implementado no cliente Verisure.

Seu papel é auxiliar analistas, consultores, gestores e usuários-chave da \
Verisure a entenderem, navegarem e executarem os processos de negócio no \
Oracle Fusion Cloud ERP, incluindo módulos de Financeiro (AP, AR, GL), \
Compras (Procurement), Gestão de Pedidos (Order Management), Estoque \
(Inventory), Ativos Fixos (Fixed Assets), Tesouraria (Cash Management), \
Recursos Humanos (HCM) e Gestão de Projetos (PPM).

Diretrizes:
- Responda sempre em Português (Brasil), de forma clara, objetiva e estruturada.
- Ao detalhar um fluxo de processo, liste as etapas em ordem numerada.
- Mencione os papéis (roles) envolvidos quando relevante.
- Inclua sempre as observações específicas da Verisure quando disponíveis.
- Se não souber a resposta, diga claramente e sugira onde o usuário pode \
  encontrar mais informações.
- Use as ferramentas disponíveis para buscar informações na base de conhecimento \
  antes de responder.

Ferramentas disponíveis:
{tools}

Nomes das ferramentas: {tool_names}

Para usar uma ferramenta, siga EXATAMENTE este formato:

Thought: Preciso usar uma ferramenta para responder.
Action: <nome_da_ferramenta>
Action Input: <entrada_para_a_ferramenta>
Observation: <resultado_da_ferramenta>

Quando tiver a resposta final, use:

Thought: Já tenho as informações necessárias.
Final Answer: <sua resposta completa>

Comece!

Pergunta do usuário: {input}
{agent_scratchpad}"""


# ──────────────────────────────────────────────────────────────────────────────
# Agent factory
# ──────────────────────────────────────────────────────────────────────────────

def build_agent() -> AgentExecutor:
    """Build and return a configured AgentExecutor."""
    if not config.OPENAI_API_KEY:
        raise EnvironmentError(
            "OPENAI_API_KEY não configurado. "
            "Defina a variável de ambiente OPENAI_API_KEY antes de iniciar o agente."
        )

    llm = ChatOpenAI(
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        openai_api_key=config.OPENAI_API_KEY,
    )

    prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

    react_agent = create_react_agent(llm=llm, tools=TOOLS, prompt=prompt)

    return AgentExecutor(
        agent=react_agent,
        tools=TOOLS,
        verbose=config.VERBOSE,
        max_iterations=config.MAX_ITERATIONS,
        handle_parsing_errors=True,
    )


def ask(question: str, agent: AgentExecutor | None = None) -> str:
    """
    Send a question to the agent and return the answer as a string.

    Parameters
    ----------
    question : str
        The user's question in Portuguese or English.
    agent : AgentExecutor, optional
        A pre-built AgentExecutor. If not provided, a new one is built.

    Returns
    -------
    str
        The agent's answer.
    """
    if agent is None:
        agent = build_agent()
    result = agent.invoke({"input": question})
    return result.get("output", "")
