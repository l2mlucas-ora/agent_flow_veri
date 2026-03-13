"""
Configuration for the Oracle Fusion Cloud ERP Agent - Verisure.
Reads settings from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI / LLM
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o")
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0"))

# Agent behaviour
MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
VERBOSE: bool = os.getenv("VERBOSE", "false").lower() == "true"
