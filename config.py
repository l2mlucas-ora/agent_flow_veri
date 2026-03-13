"""
Configuration module for the Verisure Oracle Fusion Cloud ERP Agent.
Loads settings from environment variables / .env file.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file if present
load_dotenv()


def _require_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set. "
            "Copy .env.example to .env and fill in your values."
        )
    return value


# OpenAI settings
OPENAI_API_KEY: str = _require_env("OPENAI_API_KEY")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))

# Persistence
VECTORSTORE_DIR: Path = Path(os.getenv("VECTORSTORE_DIR", "./vectorstore"))

# Agent identity
AGENT_NAME = "Verisure Oracle Fusion ERP Expert"
AGENT_DESCRIPTION = (
    "Especialista nos fluxos de processos do Oracle Fusion Cloud ERP da Verisure. "
    "Auxilia equipes de negócio e TI a entender, executar e otimizar os processos "
    "de Finanças, Suprimentos, Projetos e Recursos Humanos no sistema."
)
