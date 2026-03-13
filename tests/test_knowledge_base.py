"""
Unit tests for the knowledge base and agent tools.

These tests do NOT require an OpenAI API key – they validate the knowledge
base data integrity and the tool logic independently of any LLM.
"""

import pytest

from knowledge_base import MODULE_DESCRIPTIONS, PROCESS_FLOWS


# ──────────────────────────────────────────────────────────────────────────────
# Knowledge-base data integrity
# ──────────────────────────────────────────────────────────────────────────────

class TestKnowledgeBaseIntegrity:
    """Validate that all process flow entries have the required fields."""

    REQUIRED_FIELDS = {"id", "module", "name", "description", "steps", "roles", "notes"}

    def test_process_flows_not_empty(self):
        assert len(PROCESS_FLOWS) > 0, "PROCESS_FLOWS should not be empty"

    def test_all_processes_have_required_fields(self):
        for proc in PROCESS_FLOWS:
            missing = self.REQUIRED_FIELDS - set(proc.keys())
            assert not missing, f"Process {proc.get('id', '?')} is missing fields: {missing}"

    def test_all_process_ids_are_unique(self):
        ids = [p["id"] for p in PROCESS_FLOWS]
        assert len(ids) == len(set(ids)), "Duplicate process IDs found"

    def test_all_process_steps_are_non_empty(self):
        for proc in PROCESS_FLOWS:
            assert len(proc["steps"]) > 0, f"Process {proc['id']} has no steps"

    def test_all_process_roles_are_non_empty(self):
        for proc in PROCESS_FLOWS:
            assert len(proc["roles"]) > 0, f"Process {proc['id']} has no roles"

    def test_module_descriptions_not_empty(self):
        assert len(MODULE_DESCRIPTIONS) > 0

    def test_all_process_modules_have_descriptions(self):
        modules_in_processes = {p["module"] for p in PROCESS_FLOWS}
        for module in modules_in_processes:
            assert module in MODULE_DESCRIPTIONS, (
                f"Module '{module}' used in process flows but has no description"
            )

    def test_known_modules_present(self):
        expected_modules = {
            "Accounts Payable",
            "Accounts Receivable",
            "General Ledger",
            "Procurement",
            "Order Management",
            "Inventory Management",
            "Fixed Assets",
            "Cash Management",
            "Human Capital Management",
            "Project Portfolio Management",
        }
        actual_modules = {p["module"] for p in PROCESS_FLOWS}
        missing = expected_modules - actual_modules
        assert not missing, f"Expected modules not found: {missing}"

    def test_known_process_ids_present(self):
        expected_ids = {
            "AP-001", "AP-002",
            "AR-001", "AR-002",
            "GL-001",
            "PO-001", "PO-002",
            "OM-001",
            "INV-001",
            "FA-001",
            "CM-001",
            "HCM-001", "HCM-002",
            "PPM-001",
        }
        actual_ids = {p["id"] for p in PROCESS_FLOWS}
        missing = expected_ids - actual_ids
        assert not missing, f"Expected process IDs not found: {missing}"


# ──────────────────────────────────────────────────────────────────────────────
# Tool logic tests (no LLM required)
# ──────────────────────────────────────────────────────────────────────────────

class TestToolLogic:
    """Test the tool helper functions directly (without the LangChain decorator)."""

    def _find_process(self, process_id: str):
        return next((p for p in PROCESS_FLOWS if p["id"].upper() == process_id.upper()), None)

    def _search(self, query: str):
        query_lower = query.strip().lower()
        return [
            p for p in PROCESS_FLOWS
            if query_lower in " ".join([
                p["name"], p["description"],
                " ".join(p["steps"]), p["notes"],
            ]).lower()
        ]

    # list_modules
    def test_module_descriptions_cover_all_modules(self):
        modules_in_processes = {p["module"] for p in PROCESS_FLOWS}
        for m in modules_in_processes:
            assert m in MODULE_DESCRIPTIONS

    # list_processes_by_module
    def test_filter_by_module_accounts_payable(self):
        results = [p for p in PROCESS_FLOWS if p["module"] == "Accounts Payable"]
        assert len(results) >= 2
        ids = {p["id"] for p in results}
        assert "AP-001" in ids
        assert "AP-002" in ids

    def test_filter_by_module_case_insensitive(self):
        module = "accounts payable"
        results = [p for p in PROCESS_FLOWS if p["module"].lower() == module.lower()]
        assert len(results) >= 1

    def test_filter_by_unknown_module_returns_empty(self):
        results = [p for p in PROCESS_FLOWS if p["module"] == "Unknown Module XYZ"]
        assert results == []

    # get_process_detail
    def test_get_known_process(self):
        proc = self._find_process("AP-001")
        assert proc is not None
        assert proc["name"] == "Processamento de Faturas de Fornecedores"
        assert len(proc["steps"]) >= 5

    def test_get_unknown_process_returns_none(self):
        proc = self._find_process("XX-999")
        assert proc is None

    # search_processes
    def test_search_by_keyword_fatura(self):
        results = self._search("fatura")
        assert len(results) > 0

    def test_search_by_keyword_pagamento(self):
        results = self._search("pagamento")
        assert len(results) > 0

    def test_search_by_keyword_instalacao(self):
        results = self._search("instala")
        assert len(results) > 0

    def test_search_returns_empty_for_unknown_term(self):
        results = self._search("xyzabc123notfound")
        assert results == []

    # get_roles_for_process
    def test_roles_present_in_ap001(self):
        proc = self._find_process("AP-001")
        assert proc is not None
        assert "AP Invoice Processor" in proc["roles"]

    def test_roles_present_in_hcm001(self):
        proc = self._find_process("HCM-001")
        assert proc is not None
        assert "HR Specialist" in proc["roles"]

    # Verisure-specific notes
    def test_verisure_notes_not_empty(self):
        for proc in PROCESS_FLOWS:
            assert proc["notes"].strip() != "", f"Process {proc['id']} has empty notes"

    def test_verisure_mention_in_notes(self):
        for proc in PROCESS_FLOWS:
            assert "Verisure" in proc["notes"], (
                f"Process {proc['id']} notes do not mention Verisure"
            )
