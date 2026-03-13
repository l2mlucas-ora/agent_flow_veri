"""Knowledge base package for Oracle Fusion Cloud ERP process flows."""

from .oracle_processes import PROCESS_FLOWS, get_all_modules, get_process_by_id

__all__ = ["PROCESS_FLOWS", "get_all_modules", "get_process_by_id"]
