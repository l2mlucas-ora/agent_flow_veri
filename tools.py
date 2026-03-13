"""
LangChain tools for the Verisure Oracle Fusion Cloud ERP Agent.

Each tool exposes a specific capability to query the process-flow knowledge base.
"""

from __future__ import annotations

from typing import Any

from langchain.tools import tool

from knowledge_base.oracle_processes import (
    get_all_modules,
    get_all_sub_modules,
    get_process_by_id,
    get_processes_by_module,
    search_processes,
)


def _format_flow(flow: dict[str, Any], verbose: bool = False) -> str:
    """Return a human-readable string representation of a process flow."""
    lines: list[str] = [
        f"### {flow['name']}",
        f"**ID:** {flow['id']}",
        f"**Módulo:** {flow['module']} › {flow['sub_module']}",
        f"**Descrição:** {flow['description']}",
        f"**Gatilho:** {flow['trigger']}",
    ]

    if verbose:
        lines.append("\n**Etapas:**")
        for step in flow["steps"]:
            lines.append(f"  {step}")

        lines.append(f"\n**Papéis envolvidos:** {', '.join(flow['roles'])}")
        lines.append(
            f"**Pontos de integração:** {', '.join(flow['integration_points'])}"
        )

        if flow.get("verisure_notes"):
            lines.append(f"\n**Notas Verisure:** {flow['verisure_notes']}")

    return "\n".join(lines)


@tool
def list_erp_modules() -> str:
    """
    Lists all Oracle Fusion Cloud ERP modules available in the Verisure knowledge base.
    Use this to discover which ERP areas are covered before drilling down.
    """
    modules = get_all_modules()
    sub_modules = get_all_sub_modules()
    return (
        f"Módulos ERP disponíveis ({len(modules)}):\n"
        + "\n".join(f"  • {m}" for m in modules)
        + f"\n\nSub-módulos ({len(sub_modules)}):\n"
        + "\n".join(f"  • {s}" for s in sub_modules)
    )


@tool
def list_processes_in_module(module_name: str) -> str:
    """
    Lists all process flows within a specific Oracle Fusion ERP module for Verisure.
    Provide the module name (e.g., 'Financials', 'Procurement', 'Supply Chain',
    'Project Portfolio Management', 'Human Capital Management').
    """
    flows = get_processes_by_module(module_name)
    if not flows:
        modules = get_all_modules()
        return (
            f"Nenhum processo encontrado para o módulo '{module_name}'. "
            f"Módulos disponíveis: {', '.join(modules)}."
        )

    lines = [f"Processos no módulo '{module_name}' ({len(flows)}):"]
    for flow in flows:
        lines.append(f"  • [{flow['id']}] {flow['name']} ({flow['sub_module']})")
    return "\n".join(lines)


@tool
def get_process_details(process_id: str) -> str:
    """
    Returns the full details (steps, roles, integrations, Verisure notes) of a
    specific Oracle Fusion ERP process flow identified by its ID.
    Example IDs: 'fi-ap-01', 'scm-po-01', 'hcm-py-01'.
    Use list_processes_in_module or search_erp_processes first to discover IDs.
    """
    flow = get_process_by_id(process_id)
    if not flow:
        return (
            f"Processo com ID '{process_id}' não encontrado. "
            "Use list_erp_modules ou search_erp_processes para descobrir IDs válidos."
        )
    return _format_flow(flow, verbose=True)


@tool
def search_erp_processes(query: str) -> str:
    """
    Searches Verisure's Oracle Fusion ERP process flows using keywords.
    Returns the most relevant processes ranked by relevance.
    Useful when you know a topic but not the exact module or process ID.
    Example queries: 'pagamento fornecedor', 'fechamento contábil', 'folha pagamento',
    'estoque alarme', 'admissão colaborador'.
    """
    flows = search_processes(query)
    if not flows:
        return f"Nenhum processo encontrado para a busca: '{query}'."

    # Return top 5 results with brief summary
    top = flows[:5]
    lines = [f"Processos encontrados para '{query}' (top {len(top)}):"]
    for flow in top:
        lines.append(f"\n{_format_flow(flow, verbose=False)}")
    return "\n".join(lines)


@tool
def get_process_steps(process_id: str) -> str:
    """
    Returns only the ordered step-by-step instructions for executing a specific
    Oracle Fusion ERP process at Verisure.
    Useful when a user wants a quick 'how to execute' guide.
    """
    flow = get_process_by_id(process_id)
    if not flow:
        return f"Processo '{process_id}' não encontrado."

    lines = [f"**{flow['name']}** – Passo a Passo:\n"]
    lines.extend(flow["steps"])
    return "\n".join(lines)


@tool
def get_process_roles(process_id: str) -> str:
    """
    Returns the Oracle roles and job functions involved in a specific ERP process.
    Useful for understanding who is responsible for each step.
    """
    flow = get_process_by_id(process_id)
    if not flow:
        return f"Processo '{process_id}' não encontrado."

    roles = flow["roles"]
    lines = [
        f"**{flow['name']}** – Papéis e Responsabilidades:\n",
        f"Papéis envolvidos: {', '.join(roles)}",
        "",
        "Notas de responsabilidades:",
    ]
    for step in flow["steps"]:
        lines.append(f"  {step}")
    return "\n".join(lines)


@tool
def get_verisure_config_notes(process_id: str) -> str:
    """
    Returns Verisure-specific configuration notes and business rules for a given
    Oracle Fusion ERP process. These notes reflect how Oracle is configured and
    used specifically at Verisure (policies, thresholds, local adaptations).
    """
    flow = get_process_by_id(process_id)
    if not flow:
        return f"Processo '{process_id}' não encontrado."

    notes = flow.get("verisure_notes", "")
    if not notes:
        return f"Não há notas específicas da Verisure para o processo '{process_id}'."

    return (
        f"**{flow['name']}** – Configurações e Regras de Negócio da Verisure:\n\n"
        + notes
    )


@tool
def list_all_processes() -> str:
    """
    Returns a complete index of all Oracle Fusion ERP process flows available
    in the Verisure knowledge base, organized by module.
    """
    from knowledge_base.oracle_processes import PROCESS_FLOWS

    by_module: dict[str, list[str]] = {}
    for flow in PROCESS_FLOWS:
        mod = flow["module"]
        by_module.setdefault(mod, [])
        by_module[mod].append(f"  [{flow['id']}] {flow['name']}")

    lines = ["**Índice Completo de Processos Oracle Fusion ERP – Verisure**\n"]
    for module in sorted(by_module.keys()):
        lines.append(f"\n📌 {module}")
        lines.extend(by_module[module])

    return "\n".join(lines)


ALL_TOOLS = [
    list_erp_modules,
    list_processes_in_module,
    get_process_details,
    search_erp_processes,
    get_process_steps,
    get_process_roles,
    get_verisure_config_notes,
    list_all_processes,
]
