"""
Tests for tool functions exposed to the LangChain agent.

These tests invoke the tool's underlying Python function (via .invoke())
without calling any LLM, so no OpenAI key is needed.
"""

import pytest

from tools import (
    get_process_detail,
    get_roles_for_process,
    list_all_processes,
    list_modules,
    list_processes_by_module,
    search_processes,
)


class TestListModules:
    def test_returns_all_known_modules(self):
        result = list_modules.invoke({})
        assert "Accounts Payable" in result
        assert "Accounts Receivable" in result
        assert "General Ledger" in result
        assert "Procurement" in result
        assert "Human Capital Management" in result

    def test_result_is_non_empty_string(self):
        result = list_modules.invoke({})
        assert isinstance(result, str)
        assert len(result) > 0


class TestListProcessesByModule:
    def test_accounts_payable_lists_ap001(self):
        result = list_processes_by_module.invoke({"module_name": "Accounts Payable"})
        assert "AP-001" in result
        assert "AP-002" in result

    def test_unknown_module_returns_helpful_message(self):
        result = list_processes_by_module.invoke({"module_name": "Nonexistent Module"})
        assert "Nenhum processo encontrado" in result

    def test_hcm_module(self):
        result = list_processes_by_module.invoke({"module_name": "Human Capital Management"})
        assert "HCM-001" in result
        assert "HCM-002" in result


class TestGetProcessDetail:
    def test_ap001_detail_contains_steps(self):
        result = get_process_detail.invoke({"process_id": "AP-001"})
        assert "AP-001" in result
        assert "Processamento de Faturas" in result
        assert "Etapas:" in result

    def test_gl001_detail_contains_verisure_notes(self):
        result = get_process_detail.invoke({"process_id": "GL-001"})
        assert "Verisure" in result
        assert "fechamento" in result.lower()

    def test_unknown_process_returns_helpful_message(self):
        result = get_process_detail.invoke({"process_id": "XX-999"})
        assert "não encontrado" in result

    def test_all_known_processes_are_retrievable(self):
        known_ids = [
            "AP-001", "AP-002", "AR-001", "AR-002", "GL-001",
            "PO-001", "PO-002", "OM-001", "INV-001", "FA-001",
            "CM-001", "HCM-001", "HCM-002", "PPM-001",
        ]
        for pid in known_ids:
            result = get_process_detail.invoke({"process_id": pid})
            assert pid in result, f"Process {pid} detail not found in result"


class TestSearchProcesses:
    def test_search_pagamento_returns_results(self):
        result = search_processes.invoke({"query": "pagamento"})
        assert "Processos encontrados" in result

    def test_search_instalacao_returns_results(self):
        result = search_processes.invoke({"query": "instala"})
        assert "Processos encontrados" in result

    def test_search_unknown_returns_message(self):
        result = search_processes.invoke({"query": "xyzabc123notfound"})
        assert "Nenhum processo encontrado" in result

    def test_search_fatura_contains_ap_processes(self):
        result = search_processes.invoke({"query": "fatura"})
        assert "AP-001" in result or "AR-001" in result


class TestListAllProcesses:
    def test_contains_all_module_groups(self):
        result = list_all_processes.invoke({})
        modules = [
            "Accounts Payable",
            "Accounts Receivable",
            "General Ledger",
            "Procurement",
            "Order Management",
        ]
        for module in modules:
            assert module in result, f"Module '{module}' not found in list_all_processes result"

    def test_contains_all_known_ids(self):
        result = list_all_processes.invoke({})
        for pid in ["AP-001", "GL-001", "HCM-001", "PPM-001"]:
            assert pid in result


class TestGetRolesForProcess:
    def test_ap001_roles(self):
        result = get_roles_for_process.invoke({"process_id": "AP-001"})
        assert "AP Invoice Processor" in result

    def test_hcm002_roles(self):
        result = get_roles_for_process.invoke({"process_id": "HCM-002"})
        assert "Payroll Specialist" in result

    def test_unknown_process_returns_message(self):
        result = get_roles_for_process.invoke({"process_id": "ZZ-000"})
        assert "não encontrado" in result
