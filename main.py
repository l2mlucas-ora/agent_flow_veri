"""
CLI entrypoint for the Oracle Fusion Cloud ERP Agent – Verisure.

Usage:
    python main.py
    python main.py "Quais são as etapas do processo de fechamento mensal?"
"""

import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from agent import ask, build_agent

console = Console()

BANNER = """
# 🔒 Agente Oracle Fusion Cloud ERP – Verisure

Bem-vindo! Sou especialista nos fluxos de processos do Oracle Fusion Cloud ERP
implementado na Verisure. Pergunte sobre qualquer processo de negócio.

Digite **sair** ou **exit** para encerrar.
"""


def run_interactive() -> None:
    """Run an interactive question-answer loop."""
    console.print(Markdown(BANNER))

    try:
        agent = build_agent()
    except EnvironmentError as exc:
        console.print(f"[bold red]Erro de configuração:[/bold red] {exc}")
        sys.exit(1)

    while True:
        try:
            question = Prompt.ask("\n[bold cyan]Você[/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Encerrando o agente. Até logo![/yellow]")
            break

        if not question:
            continue

        if question.lower() in {"sair", "exit", "quit"}:
            console.print("[yellow]Encerrando o agente. Até logo![/yellow]")
            break

        console.print("\n[bold green]Agente:[/bold green] Processando...\n")
        try:
            answer = ask(question, agent=agent)
            console.print(Panel(Markdown(answer), title="Resposta", border_style="green"))
        except Exception as exc:  # noqa: BLE001
            console.print(f"[bold red]Erro ao processar a pergunta:[/bold red] {exc}")


def run_single_question(question: str) -> None:
    """Answer a single question and exit."""
    try:
        answer = ask(question)
        console.print(Panel(Markdown(answer), title="Resposta", border_style="green"))
    except EnvironmentError as exc:
        console.print(f"[bold red]Erro de configuração:[/bold red] {exc}")
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[bold red]Erro ao processar a pergunta:[/bold red] {exc}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_single_question(" ".join(sys.argv[1:]))
    else:
        run_interactive()
