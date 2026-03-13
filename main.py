"""
CLI entrypoint for the Verisure Oracle Fusion Cloud ERP Agent.

Usage:
    python main.py                     # Interactive chat mode
    python main.py --query "..."       # Single-shot query mode
    python main.py --verbose           # Enable verbose ReAct tracing
    python main.py --list-modules      # List all ERP modules and processes
"""

from __future__ import annotations

import argparse
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

import config

console = Console()


def _print_welcome() -> None:
    console.print(
        Panel.fit(
            f"[bold cyan]{config.AGENT_NAME}[/bold cyan]\n\n"
            f"[dim]{config.AGENT_DESCRIPTION}[/dim]\n\n"
            "[yellow]Digite sua pergunta sobre os processos Oracle Fusion ERP da Verisure.[/yellow]\n"
            "[dim]Comandos especiais: 'sair' | 'exit' | 'quit' para encerrar • 'ajuda' para dicas[/dim]",
            title="[bold green]🔒 Verisure ERP Agent[/bold green]",
            border_style="green",
        )
    )


def _print_help() -> None:
    help_text = (
        "## Exemplos de perguntas\n\n"
        "- Como funciona o processo de contas a pagar na Verisure?\n"
        "- Quais são os passos para o fechamento contábil mensal?\n"
        "- Quem são os responsáveis pela aprovação de ordens de compra?\n"
        "- Como é feito o inventário de estoque de alarmes?\n"
        "- Quais módulos do Oracle ERP a Verisure utiliza?\n"
        "- Descreva o processo de admissão de um novo colaborador.\n"
        "- Quais são as regras específicas da Verisure para despesas de viagem?\n"
        "- Como funciona a folha de pagamento no Oracle HCM?\n"
    )
    console.print(Markdown(help_text))


def run_interactive(verbose: bool = False) -> None:
    """Run the agent in interactive conversation mode."""
    from agent import build_agent

    _print_welcome()

    agent_executor = build_agent(verbose=verbose)

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]Você[/bold green]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Encerrando...[/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() in {"sair", "exit", "quit", "q"}:
            console.print("[dim]Até logo! 👋[/dim]")
            break

        if user_input.lower() in {"ajuda", "help", "?"}:
            _print_help()
            continue

        try:
            with console.status("[bold yellow]Consultando base de conhecimento...[/bold yellow]"):
                result = agent_executor.invoke({"input": user_input})

            answer = result.get("output", "Sem resposta.")
            console.print("\n[bold cyan]Agente:[/bold cyan]")
            console.print(Markdown(answer))

        except Exception as exc:  # noqa: BLE001
            console.print(f"[bold red]Erro:[/bold red] {exc}")


def run_single_query(query: str, verbose: bool = False) -> None:
    """Execute a single query and print the result."""
    from agent import build_agent

    agent_executor = build_agent(verbose=verbose)

    try:
        result = agent_executor.invoke({"input": query})
        answer = result.get("output", "Sem resposta.")
        console.print(Markdown(answer))
    except Exception as exc:  # noqa: BLE001
        console.print(f"[bold red]Erro:[/bold red] {exc}")
        sys.exit(1)


def run_list_modules() -> None:
    """Print all modules and processes without invoking the LLM."""
    from tools import list_all_processes

    result = list_all_processes.invoke({})
    console.print(Markdown(result))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verisure Oracle Fusion Cloud ERP Expert Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--query",
        "-q",
        metavar="PERGUNTA",
        help="Execute uma única consulta e encerre.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Ative o modo verboso (exibe o raciocínio ReAct do agente).",
    )
    parser.add_argument(
        "--list-modules",
        action="store_true",
        help="Lista todos os módulos e processos disponíveis na base de conhecimento.",
    )

    args = parser.parse_args()

    if args.list_modules:
        run_list_modules()
        return

    if args.query:
        run_single_query(args.query, verbose=args.verbose)
        return

    run_interactive(verbose=args.verbose)


if __name__ == "__main__":
    main()
