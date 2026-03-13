"""
LangChain tools for the Oracle Fusion Cloud ERP Agent – Verisure.

Each tool queries the in-memory knowledge base and returns structured text
that the agent uses to compose its answers.
"""

import json
from langchain.tools import tool

from knowledge_base import MODULE_DESCRIPTIONS, PROCESS_FLOWS


# ──────────────────────────────────────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────────────────────────────────────

def _format_process(proc: dict) -> str:
    """Return a human-readable representation of a process flow."""
    steps = "\n".join(proc["steps"])
    roles = ", ".join(proc["roles"])
    return (
        f"[{proc['id']}] {proc['name']}\n"
        f"Módulo: {proc['module']}\n"
        f"Descrição: {proc['description']}\n\n"
        f"Etapas:\n{steps}\n\n"
        f"Papéis envolvidos: {roles}\n\n"
        f"Notas Verisure: {proc['notes']}"
    )


# ──────────────────────────────────────────────────────────────────────────────
# Tools
# ──────────────────────────────────────────────────────────────────────────────

@tool
def list_modules() -> str:
    """
    Lista todos os módulos do Oracle Fusion Cloud ERP implementados na Verisure,
    com uma breve descrição de cada módulo.
    Use esta ferramenta quando o usuário quiser saber quais módulos estão disponíveis.
    """
    lines = []
    for module, description in MODULE_DESCRIPTIONS.items():
        lines.append(f"• {module}: {description}")
    return "\n\n".join(lines)


@tool
def list_processes_by_module(module_name: str) -> str:
    """
    Lista todos os fluxos de processo disponíveis para um módulo específico do
    Oracle Fusion Cloud ERP na Verisure.
    O parâmetro module_name deve ser um dos nomes de módulo reconhecidos, por exemplo:
    'Accounts Payable', 'Accounts Receivable', 'General Ledger', 'Procurement',
    'Order Management', 'Inventory Management', 'Fixed Assets', 'Cash Management',
    'Human Capital Management', 'Project Portfolio Management'.
    """
    matched = [p for p in PROCESS_FLOWS if p["module"].lower() == module_name.strip().lower()]
    if not matched:
        available = ", ".join(MODULE_DESCRIPTIONS.keys())
        return (
            f"Nenhum processo encontrado para o módulo '{module_name}'. "
            f"Módulos disponíveis: {available}."
        )
    lines = [f"Processos no módulo '{matched[0]['module']}':"]
    for proc in matched:
        lines.append(f"  [{proc['id']}] {proc['name']} – {proc['description']}")
    return "\n".join(lines)


@tool
def get_process_detail(process_id: str) -> str:
    """
    Retorna os detalhes completos de um fluxo de processo específico, incluindo
    todas as etapas, papéis envolvidos e notas específicas da Verisure.
    O parâmetro process_id deve ser o ID do processo, por exemplo: 'AP-001',
    'AR-001', 'GL-001', 'PO-001', 'OM-001', 'INV-001', 'FA-001', 'CM-001',
    'HCM-001', 'HCM-002', 'PPM-001'.
    """
    proc = next((p for p in PROCESS_FLOWS if p["id"].upper() == process_id.strip().upper()), None)
    if not proc:
        ids = ", ".join(p["id"] for p in PROCESS_FLOWS)
        return (
            f"Processo '{process_id}' não encontrado. "
            f"IDs disponíveis: {ids}."
        )
    return _format_process(proc)


@tool
def search_processes(query: str) -> str:
    """
    Busca fluxos de processo que contenham a palavra ou frase informada no nome,
    descrição, etapas ou notas. Útil para encontrar processos por tema, por exemplo:
    'pagamento', 'fatura', 'instalação', 'cobrança', 'depreciação'.
    """
    query_lower = query.strip().lower()
    results = []
    for proc in PROCESS_FLOWS:
        searchable = " ".join([
            proc["name"],
            proc["description"],
            " ".join(proc["steps"]),
            proc["notes"],
        ]).lower()
        if query_lower in searchable:
            results.append(proc)

    if not results:
        return f"Nenhum processo encontrado para a busca: '{query}'."

    lines = [f"Processos encontrados para '{query}':"]
    for proc in results:
        lines.append(f"  [{proc['id']}] {proc['name']} (Módulo: {proc['module']})")
    return "\n".join(lines)


@tool
def list_all_processes() -> str:
    """
    Lista todos os fluxos de processo disponíveis na base de conhecimento,
    agrupados por módulo do Oracle Fusion Cloud ERP.
    """
    grouped: dict[str, list[dict]] = {}
    for proc in PROCESS_FLOWS:
        grouped.setdefault(proc["module"], []).append(proc)

    lines = ["Todos os fluxos de processo Oracle Fusion Cloud ERP – Verisure:\n"]
    for module, processes in grouped.items():
        lines.append(f"📦 {module}")
        for proc in processes:
            lines.append(f"   [{proc['id']}] {proc['name']}")
        lines.append("")
    return "\n".join(lines)


@tool
def get_roles_for_process(process_id: str) -> str:
    """
    Retorna os papéis (roles) do Oracle Fusion Cloud envolvidos em um determinado
    fluxo de processo. Útil para questões sobre responsabilidades e segregação de funções.
    O parâmetro process_id deve ser o ID do processo, por exemplo: 'AP-001'.
    """
    proc = next((p for p in PROCESS_FLOWS if p["id"].upper() == process_id.strip().upper()), None)
    if not proc:
        ids = ", ".join(p["id"] for p in PROCESS_FLOWS)
        return f"Processo '{process_id}' não encontrado. IDs disponíveis: {ids}."
    roles = "\n".join(f"  • {r}" for r in proc["roles"])
    return (
        f"Papéis envolvidos no processo [{proc['id']}] {proc['name']}:\n{roles}"
    )


# Exported list of all tools for the agent
TOOLS = [
    list_modules,
    list_processes_by_module,
    get_process_detail,
    search_processes,
    list_all_processes,
    get_roles_for_process,
]
