"""
Unit tests for the Oracle Fusion Cloud ERP knowledge base and agent tools.

These tests validate the knowledge base data integrity, search functionality,
and tool outputs WITHOUT requiring a real OpenAI API key.
"""

from __future__ import annotations

import pytest

from knowledge_base.oracle_processes import (
    PROCESS_FLOWS,
    get_all_modules,
    get_all_sub_modules,
    get_process_by_id,
    get_processes_by_module,
    search_processes,
)


# ---------------------------------------------------------------------------
# Knowledge Base – Data Integrity
# ---------------------------------------------------------------------------


class TestKnowledgeBaseIntegrity:
    """Ensure the knowledge base is well-formed."""

    REQUIRED_FIELDS = {
        "id",
        "module",
        "sub_module",
        "name",
        "description",
        "trigger",
        "steps",
        "roles",
        "integration_points",
        "key_tables_views",
        "verisure_notes",
    }

    def test_process_flows_not_empty(self):
        assert len(PROCESS_FLOWS) > 0, "PROCESS_FLOWS should not be empty"

    def test_each_flow_has_required_fields(self):
        for flow in PROCESS_FLOWS:
            missing = self.REQUIRED_FIELDS - set(flow.keys())
            assert not missing, f"Flow '{flow.get('id')}' is missing fields: {missing}"

    def test_ids_are_unique(self):
        ids = [flow["id"] for flow in PROCESS_FLOWS]
        assert len(ids) == len(set(ids)), "Process IDs must be unique"

    def test_steps_are_non_empty_lists(self):
        for flow in PROCESS_FLOWS:
            assert isinstance(flow["steps"], list), f"Flow '{flow['id']}': steps must be a list"
            assert len(flow["steps"]) > 0, f"Flow '{flow['id']}': steps must not be empty"

    def test_roles_are_non_empty_lists(self):
        for flow in PROCESS_FLOWS:
            assert isinstance(flow["roles"], list), f"Flow '{flow['id']}': roles must be a list"
            assert len(flow["roles"]) > 0, f"Flow '{flow['id']}': roles must not be empty"

    def test_integration_points_are_non_empty_lists(self):
        for flow in PROCESS_FLOWS:
            assert isinstance(flow["integration_points"], list), (
                f"Flow '{flow['id']}': integration_points must be a list"
            )
            assert len(flow["integration_points"]) > 0, (
                f"Flow '{flow['id']}': integration_points must not be empty"
            )

    def test_verisure_notes_are_strings(self):
        for flow in PROCESS_FLOWS:
            assert isinstance(flow["verisure_notes"], str), (
                f"Flow '{flow['id']}': verisure_notes must be a string"
            )

    def test_all_modules_present(self):
        """Ensure critical Verisure ERP modules are covered."""
        modules = get_all_modules()
        expected_modules = {
            "Financials",
            "Procurement",
            "Supply Chain",
            "Project Portfolio Management",
            "Human Capital Management",
        }
        for expected in expected_modules:
            assert expected in modules, f"Module '{expected}' not found in knowledge base"


# ---------------------------------------------------------------------------
# Knowledge Base – Query Functions
# ---------------------------------------------------------------------------


class TestGetProcessById:
    def test_returns_correct_process(self):
        flow = get_process_by_id("fi-ap-01")
        assert flow is not None
        assert flow["id"] == "fi-ap-01"
        assert flow["module"] == "Financials"
        assert flow["sub_module"] == "Accounts Payable"

    def test_returns_none_for_unknown_id(self):
        assert get_process_by_id("xx-zz-99") is None

    def test_returns_none_for_empty_id(self):
        assert get_process_by_id("") is None

    def test_all_ids_in_flows_are_retrievable(self):
        for flow in PROCESS_FLOWS:
            retrieved = get_process_by_id(flow["id"])
            assert retrieved is not None
            assert retrieved["id"] == flow["id"]


class TestGetAllModules:
    def test_returns_sorted_unique_list(self):
        modules = get_all_modules()
        assert modules == sorted(set(modules))

    def test_returns_at_least_five_modules(self):
        assert len(get_all_modules()) >= 5


class TestGetAllSubModules:
    def test_returns_sorted_unique_list(self):
        sub_modules = get_all_sub_modules()
        assert sub_modules == sorted(set(sub_modules))

    def test_no_duplicates(self):
        sub_modules = get_all_sub_modules()
        assert len(sub_modules) == len(set(sub_modules))


class TestGetProcessesByModule:
    def test_financials_module_has_processes(self):
        flows = get_processes_by_module("Financials")
        assert len(flows) > 0
        for flow in flows:
            assert flow["module"] == "Financials"

    def test_case_insensitive_match(self):
        flows_lower = get_processes_by_module("financials")
        flows_proper = get_processes_by_module("Financials")
        assert flows_lower == flows_proper

    def test_unknown_module_returns_empty_list(self):
        flows = get_processes_by_module("NonExistentModule")
        assert flows == []

    def test_procurement_module(self):
        flows = get_processes_by_module("Procurement")
        assert len(flows) > 0

    def test_hcm_module(self):
        flows = get_processes_by_module("Human Capital Management")
        assert len(flows) > 0


class TestSearchProcesses:
    def test_search_by_keyword_returns_results(self):
        results = search_processes("pagamento")
        assert len(results) > 0

    def test_search_returns_most_relevant_first(self):
        results = search_processes("folha pagamento payroll")
        assert len(results) > 0
        # The payroll process should be in the top 3
        top_ids = [r["id"] for r in results[:3]]
        assert "hcm-py-01" in top_ids

    def test_search_accounts_payable(self):
        results = search_processes("contas a pagar fatura fornecedor")
        assert len(results) > 0
        assert results[0]["id"] == "fi-ap-01"

    def test_search_no_results_for_unrelated_query(self):
        results = search_processes("xyzxyzxyz999nonexistent")
        assert results == []

    def test_empty_query_returns_all_flows(self):
        results = search_processes("")
        assert len(results) == len(PROCESS_FLOWS)

    def test_search_inventory(self):
        results = search_processes("estoque inventário alarme")
        assert len(results) > 0
        ids = [r["id"] for r in results]
        assert "scm-inv-01" in ids


# ---------------------------------------------------------------------------
# Tools – Output Validation (no LLM required)
# ---------------------------------------------------------------------------


class TestToolOutputs:
    """Test tool functions directly (bypassing LangChain's @tool wrapper)."""

    def test_list_erp_modules_output(self):
        from tools import list_erp_modules
        result = list_erp_modules.invoke({})
        assert "Financials" in result
        assert "Procurement" in result
        assert "Módulos ERP" in result

    def test_list_processes_in_module_financials(self):
        from tools import list_processes_in_module
        result = list_processes_in_module.invoke({"module_name": "Financials"})
        assert "fi-ap-01" in result
        assert "fi-gl-01" in result

    def test_list_processes_in_module_unknown(self):
        from tools import list_processes_in_module
        result = list_processes_in_module.invoke({"module_name": "Foo"})
        assert "Nenhum processo" in result

    def test_get_process_details_valid_id(self):
        from tools import get_process_details
        result = get_process_details.invoke({"process_id": "fi-ap-01"})
        assert "Contas a Pagar" in result
        assert "Etapas" in result
        assert "Verisure" in result

    def test_get_process_details_invalid_id(self):
        from tools import get_process_details
        result = get_process_details.invoke({"process_id": "invalid-id"})
        assert "não encontrado" in result

    def test_get_process_steps_valid_id(self):
        from tools import get_process_steps
        result = get_process_steps.invoke({"process_id": "scm-po-01"})
        assert "Passo a Passo" in result
        assert "1." in result

    def test_get_process_roles_valid_id(self):
        from tools import get_process_roles
        result = get_process_roles.invoke({"process_id": "hcm-py-01"})
        assert "Payroll" in result

    def test_get_verisure_config_notes_valid_id(self):
        from tools import get_verisure_config_notes
        result = get_verisure_config_notes.invoke({"process_id": "fi-ap-01"})
        assert "Verisure" in result

    def test_get_verisure_config_notes_invalid_id(self):
        from tools import get_verisure_config_notes
        result = get_verisure_config_notes.invoke({"process_id": "bad-id"})
        assert "não encontrado" in result

    def test_search_erp_processes(self):
        from tools import search_erp_processes
        result = search_erp_processes.invoke({"query": "fechamento contábil"})
        assert "fi-gl-01" in result

    def test_list_all_processes(self):
        from tools import list_all_processes
        result = list_all_processes.invoke({})
        assert "Financials" in result
        assert "fi-ap-01" in result
        assert "hcm-py-01" in result


# ---------------------------------------------------------------------------
# Agent Builder – Mock Test (no real API call)
# ---------------------------------------------------------------------------


class TestAgentBuilder:
    """Test that the agent is built correctly without making real API calls."""

    def test_build_agent_returns_executor(self, monkeypatch):
        """Verify build_agent returns an AgentExecutor when API key is set."""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key-for-unit-test")

        # Mock ChatOpenAI so no real HTTP client is constructed
        from unittest.mock import MagicMock, patch
        mock_llm = MagicMock()
        mock_llm.bind_tools = MagicMock(return_value=mock_llm)

        with patch("agent.ChatOpenAI", return_value=mock_llm):
            from langchain.agents import AgentExecutor
            from agent import build_agent

            executor = build_agent(verbose=False)
            assert isinstance(executor, AgentExecutor)
            assert len(executor.tools) == len(__import__("tools").ALL_TOOLS)
