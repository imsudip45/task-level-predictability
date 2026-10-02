"""
Tests for literature matrix validation rules.
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
        VALID_NOVELTY_THREAT_LEVELS,
        VALID_VERIFICATION_STATUSES,
        is_placeholder_arxiv,
        is_valid_doi,
        is_valid_url_or_doi,
        validate_matrix,
        validate_row,
    )
except ImportError:
    from validate_literature_matrix import (
        FIELDNAMES,
        VALID_NOVELTY_THREAT_LEVELS,
        VALID_VERIFICATION_STATUSES,
        is_placeholder_arxiv,
        is_valid_doi,
        is_valid_url_or_doi,
        validate_matrix,
        validate_row,
    )


def make_mock_row(**overrides: Any) -> Dict[str, str]:
    """
    Generate a valid mock row dict with all 37 CSV fields populated.
    Allows overriding individual keys.
    """
    row = {
        "paper_id": "P01",
        "title": "The Algorithm Selection Problem: Requirements and Methodology",
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
        "verification_date": "2026-10-02",
        "full_text_checked": "yes",
        "correction_notes": "",
        "exclusion_reason": "",
    }
    row.update(overrides)
    return row


def validate_single_row(
    row: Dict[str, str],
    seen_ids: Optional[Set[str]] = None,
    seen_title_years: Optional[Set[Tuple[str, str]]] = None,
) -> List[str]:
    """Helper function to validate a single row dict."""
    return validate_row(row, seen_ids=seen_ids, seen_title_years=seen_title_years)


def validate_rows(rows: List[Dict[str, str]]) -> List[str]:
    """Helper function to validate multiple row dicts together."""
    errors, _, _ = validate_matrix(rows)
    return errors


def test_no_duplicate_ids():
    """Two rows with same paper_id should fail."""
    row1 = make_mock_row(paper_id="P01", title="Title One")
    row2 = make_mock_row(paper_id="P01", title="Title Two")

    # Multi-row validation
    errors = validate_rows([row1, row2])
    assert len(errors) > 0
    assert any("duplicate paper_id" in err.lower() for err in errors)

    # Single-row stateful validation with seen_ids
    seen_ids: Set[str] = set()
    e1 = validate_single_row(row1, seen_ids=seen_ids)
    assert len(e1) == 0
    e2 = validate_single_row(row2, seen_ids=seen_ids)
    assert len(e2) > 0
    assert any("duplicate paper_id" in err.lower() for err in e2)


def test_no_duplicate_title_year():
    """Two rows with same title+year should fail, even with case/whitespace variations."""
    row1 = make_mock_row(paper_id="P01", title="The Algorithm Selection Problem", year="1976")
    row2 = make_mock_row(paper_id="P02", title="  the algorithm selection problem  ", year="1976")

    # Multi-row validation
    errors = validate_rows([row1, row2])
    assert len(errors) > 0
    assert any("duplicate" in err.lower() and "title" in err.lower() for err in errors)

    # Single-row stateful validation with seen_title_years
    seen_title_years: Set[Tuple[str, str]] = set()
    e1 = validate_single_row(row1, seen_title_years=seen_title_years)
    assert len(e1) == 0
    e2 = validate_single_row(row2, seen_title_years=seen_title_years)
    assert len(e2) > 0
    assert any("duplicate" in err.lower() and "title" in err.lower() for err in e2)


def test_unknown_authors_fully_verified():
    """A fully_verified row with 'Unknown' authors should fail."""
    row = make_mock_row(verification_status="fully_verified", authors="Unknown")
    errors = validate_single_row(row)
    assert len(errors) > 0
    assert any("unknown" in err.lower() and "author" in err.lower() for err in errors)


def test_missing_verification_source():
    """A fully_verified row with empty verification_source should fail."""
    row = make_mock_row(verification_status="fully_verified", verification_source="")
    errors = validate_single_row(row)
    assert len(errors) > 0
    assert any("verification_source" in err.lower() for err in errors)


def test_invalid_status():
    """A row with status 'confirmed' should fail."""
    row = make_mock_row(verification_status="confirmed")
    errors = validate_single_row(row)
    assert len(errors) > 0
    assert any("verification_status" in err.lower() for err in errors)


def test_placeholder_arxiv():
    """A row with URL containing '2405.00000' should fail."""
    row = make_mock_row(paper_url="https://arxiv.org/abs/2405.00000")
    errors = validate_single_row(row)
    assert len(errors) > 0
    assert any("00000" in err or "placeholder" in err.lower() for err in errors)


def test_valid_row():
    """A properly filled row should pass with no errors."""
    row = make_mock_row()
    errors = validate_single_row(row)
    assert errors == []


def test_year_range_validation():
    """Validate year integer between 1970 and 2027."""
    # Under lower bound
    row_low = make_mock_row(year="1969")
    errors_low = validate_single_row(row_low)
    assert any("year" in err.lower() and "range" in err.lower() for err in errors_low)

    # Over upper bound
    row_high = make_mock_row(year="2028")
    errors_high = validate_single_row(row_high)
    assert any("year" in err.lower() and "range" in err.lower() for err in errors_high)

    # Non-integer
    row_str = make_mock_row(year="twenty-twenty-four")
    errors_str = validate_single_row(row_str)
    assert any("year" in err.lower() and "integer" in err.lower() for err in errors_str)

    # Boundary cases that should pass
    assert validate_single_row(make_mock_row(year="1970")) == []
    assert validate_single_row(make_mock_row(year="2027")) == []


def test_novelty_threat_level():
    """Validate novelty threat level must be one of critical, high, moderate, low."""
    for threat in ["critical", "high", "moderate", "low"]:
        row = make_mock_row(novelty_threat_level=threat)
        assert validate_single_row(row) == []

    invalid_row = make_mock_row(novelty_threat_level="extreme")
    errors = validate_single_row(invalid_row)
    assert any("novelty_threat_level" in err.lower() for err in errors)


def test_metadata_verified_requires_source_and_date():
    """metadata_verified rows require verification_source and verification_date."""
    row = make_mock_row(
        verification_status="metadata_verified",
        verification_source="",
        verification_date="",
    )
    errors = validate_single_row(row)
    assert any("verification_source" in err.lower() for err in errors)
    assert any("verification_date" in err.lower() for err in errors)


def test_fully_verified_url_requirement():
    """fully_verified rows require a real http URL or DOI."""
    # Invalid url and empty doi
    row_no_url = make_mock_row(
        verification_status="fully_verified",
        paper_url="not reported",
        doi="not reported",
    )
    errors = validate_single_row(row_no_url)
    assert any("url" in err.lower() or "doi" in err.lower() for err in errors)

    # Real DOI only passes
    row_doi_only = make_mock_row(
        verification_status="fully_verified",
        paper_url="not reported",
        doi="10.1145/2487575.2487629",
    )
    assert validate_single_row(row_doi_only) == []
