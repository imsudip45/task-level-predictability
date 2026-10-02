"""
Unit tests for literature matrix, search hits, and screening ledger validation.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Ensure project root and scripts/ directory are in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from scripts.validate_literature_matrix import (
        FIELDNAMES,
        VALID_DATABASE_STATUSES,
        VALID_NOVELTY_THREAT_LEVELS,
        VALID_SCREENING_DECISIONS,
        VALID_VERIFICATION_STATUSES,
        is_placeholder_arxiv,
        is_valid_doi,
        is_valid_url_or_doi,
        validate_database_status,
        validate_matrix,
        validate_matrix_row,
        validate_row,
        validate_screening_ledger,
        validate_search_hits,
    )
except ImportError:
    from validate_literature_matrix import (
        FIELDNAMES,
        VALID_DATABASE_STATUSES,
        VALID_NOVELTY_THREAT_LEVELS,
        VALID_SCREENING_DECISIONS,
        VALID_VERIFICATION_STATUSES,
        is_placeholder_arxiv,
        is_valid_doi,
        is_valid_url_or_doi,
        validate_database_status,
        validate_matrix,
        validate_matrix_row,
        validate_row,
        validate_screening_ledger,
        validate_search_hits,
    )


def make_mock_row(**overrides: Any) -> Dict[str, str]:
    """Generate a valid mock row dict with all 37 CSV fields populated."""
    row = {
        "paper_id": "P01",
        "title": "The Algorithm Selection Problem",
        "authors": "John R. Rice",
        "year": "1976",
        "venue": "Advances in Computers",
        "peer_reviewed": "yes",
        "paper_url": "https://doi.org/10.1016/S0065-2458(08)60520-3",
        "code_url": "not reported",
        "doi": "10.1016/S0065-2458(08)60520-3",
        "research_area": "Algorithm selection",
        "selection_level": "Task",
        "task_domain": "General",
        "number_of_tasks_or_datasets": "not reported",
        "number_of_models_or_algorithms": "not reported",
        "candidate_system_types": "abstract algorithms",
        "task_or_instance_features": "problem characteristics",
        "predicted_outcomes": "performance",
        "selection_objective": "minimize cost",
        "evaluation_scheme": "theoretical",
        "baselines": "none",
        "uses_oracle": "yes",
        "uses_regret": "no",
        "handles_cost": "yes",
        "handles_latency": "yes",
        "handles_output_validity": "no",
        "main_finding": "Formalizes algorithm selection problem",
        "main_limitation": "Theoretical framework",
        "overlap_with_proposed_study": "Foundational task formulation",
        "difference_from_proposed_study": "Does not apply to heterogeneous ML models",
        "novelty_threat_level": "low",
        "verification_status": "fully_verified",
        "notes": "",
        "verification_source": "ScienceDirect / Elsevier",
        "verification_date": "2026-10-03",
        "full_text_checked": "yes",
        "correction_notes": "",
        "exclusion_reason": "",
    }
    row.update(overrides)
    return row


def make_mock_hit(**overrides: Any) -> Dict[str, str]:
    """Generate a valid mock search hit dict."""
    hit = {
        "hit_id": "H001",
        "database": "arXiv",
        "query_id": "Q01",
        "exact_query": '"algorithm selection" "meta-learning"',
        "search_date": "2026-10-03",
        "result_position": "1",
        "reported_title": "The Algorithm Selection Problem",
        "reported_authors": "John R. Rice",
        "reported_year": "1976",
        "result_url": "https://doi.org/10.1016/S0065-2458(08)60520-3",
        "canonical_record_id": "CR01",
        "notes": "Primary hit",
    }
    hit.update(overrides)
    return hit


def make_mock_screening(**overrides: Any) -> Dict[str, str]:
    """Generate a valid mock screening record dict."""
    rec = {
        "canonical_record_id": "CR01",
        "normalized_title": "the algorithm selection problem",
        "authors": "John R. Rice",
        "year": "1976",
        "canonical_url": "https://doi.org/10.1016/S0065-2458(08)60520-3",
        "duplicate_hit_ids": "H001",
        "screening_decision": "included",
        "exclusion_reason": "",
        "included_paper_id": "P01",
        "verification_status": "metadata_verified",
        "verification_source": "ScienceDirect",
        "verification_date": "2026-10-03",
    }
    rec.update(overrides)
    return rec


# --- Literature Matrix Row Tests ---

def test_valid_row():
    row = make_mock_row()
    errors = validate_row(row)
    assert errors == [], f"Expected valid row, got: {errors}"


def test_no_duplicate_ids():
    row1 = make_mock_row(paper_id="P01", title="Paper One")
    row2 = make_mock_row(paper_id="P01", title="Paper Two")
    errors, _, _ = validate_matrix([row1, row2])
    assert any("duplicate paper_id 'P01'" in e for e in errors)


def test_no_duplicate_title_year():
    row1 = make_mock_row(paper_id="P01", title="Identical Title", year="2020")
    row2 = make_mock_row(paper_id="P02", title="identical title", year="2020")
    errors, _, _ = validate_matrix([row1, row2])
    assert any("duplicate normalized title and year" in e for e in errors)


def test_unknown_authors_fully_verified():
    row = make_mock_row(authors="Unknown Authors", verification_status="fully_verified")
    errors = validate_row(row)
    assert any("must not have 'Unknown' or empty authors" in e or "unverified" in e for e in errors)


def test_missing_verification_source():
    row = make_mock_row(
        verification_status="fully_verified",
        verification_source="",
        verification_date="2026-10-03",
    )
    errors = validate_row(row)
    assert any("verification_source must be non-empty" in e for e in errors)


def test_invalid_status():
    row = make_mock_row(verification_status="confirmed")
    errors = validate_row(row)
    assert any("invalid verification_status 'confirmed'" in e for e in errors)


def test_placeholder_arxiv():
    row1 = make_mock_row(paper_url="https://arxiv.org/abs/2405.00000")
    errors1 = validate_row(row1)
    assert any("placeholder arXiv identifier" in e for e in errors1)

    row2 = make_mock_row(paper_url="https://arxiv.org/abs/2402.00000")
    errors2 = validate_row(row2)
    assert any("placeholder arXiv identifier" in e for e in errors2)


# --- Search Hits & Screening Ledger Tests (Task 1C additions) ---

def test_search_hit_duplicate_ids():
    hit1 = make_mock_hit(hit_id="H001")
    hit2 = make_mock_hit(hit_id="H001")
    errors = validate_search_hits([hit1, hit2])
    assert any("duplicate hit_id 'H001'" in e for e in errors)


def test_screening_duplicate_canonical_ids():
    rec1 = make_mock_screening(canonical_record_id="CR01", included_paper_id="P01")
    rec2 = make_mock_screening(canonical_record_id="CR01", included_paper_id="P02")
    errors = validate_screening_ledger([rec1, rec2])
    assert any("duplicate canonical_record_id 'CR01'" in e for e in errors)


def test_included_record_missing_paper_id():
    rec = make_mock_screening(
        canonical_record_id="CR01",
        screening_decision="included",
        included_paper_id="",
    )
    errors = validate_screening_ledger([rec])
    assert any("included record missing included_paper_id" in e for e in errors)


def test_matrix_paper_missing_from_screening():
    matrix_row = make_mock_row(paper_id="P99")
    screening_rec = make_mock_screening(canonical_record_id="CR01", included_paper_id="P01")
    errors = validate_screening_ledger([screening_rec], matrix_rows=[matrix_row])
    assert any("Matrix paper_ids missing from screening ledger: P99" in e for e in errors)


def test_excluded_record_missing_exclusion_reason():
    rec = make_mock_screening(
        canonical_record_id="CR02",
        screening_decision="excluded_irrelevant",
        exclusion_reason="",
        included_paper_id="",
    )
    errors = validate_screening_ledger([rec])
    assert any("excluded record has empty exclusion_reason" in e for e in errors)


def test_inconsistent_counts():
    row1 = make_mock_row(paper_id="P01")
    row2 = make_mock_row(paper_id="P02")
    screening_rec = make_mock_screening(canonical_record_id="CR01", included_paper_id="P01")
    errors = validate_screening_ledger([screening_rec], matrix_rows=[row1, row2])
    assert any("Count mismatch" in e for e in errors)


def test_invalid_database_status():
    assert validate_database_status("directly_searched") is True
    assert validate_database_status("indirectly_represented") is True
    assert validate_database_status("inaccessible") is True
    assert validate_database_status("not_searched") is True
    assert validate_database_status("searched") is False
    assert validate_database_status("partially_searched") is False


def test_included_record_unverified_authors():
    rec = make_mock_screening(
        canonical_record_id="CR01",
        screening_decision="included",
        included_paper_id="P01",
        authors="not verified",
    )
    errors = validate_screening_ledger([rec])
    assert any("unverified/unknown authors" in e for e in errors)


def test_valid_linked_set():
    matrix_row = make_mock_row(paper_id="P01")
    hit = make_mock_hit(hit_id="H001", canonical_record_id="CR01")
    screening_rec = make_mock_screening(
        canonical_record_id="CR01",
        screening_decision="included",
        included_paper_id="P01",
        duplicate_hit_ids="H001",
    )
    m_errors, _, _ = validate_matrix([matrix_row])
    h_errors = validate_search_hits([hit])
    s_errors = validate_screening_ledger([screening_rec], matrix_rows=[matrix_row])

    assert m_errors == []
    assert h_errors == []
    assert s_errors == []
