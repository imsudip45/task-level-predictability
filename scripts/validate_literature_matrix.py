#!/usr/bin/env python3
"""
Validation script for docs/novelty/literature_matrix.csv.

Enforces schema integrity, uniqueness constraints, URL validity,
placeholder arXiv detection, and verification requirements.
"""

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

FIELDNAMES = [
    "paper_id",
    "title",
    "authors",
    "year",
    "venue",
    "peer_reviewed",
    "paper_url",
    "code_url",
    "doi",
    "research_area",
    "selection_level",
    "task_domain",
    "number_of_tasks_or_datasets",
    "number_of_models_or_algorithms",
    "candidate_system_types",
    "task_or_instance_features",
    "predicted_outcomes",
    "selection_objective",
    "evaluation_scheme",
    "baselines",
    "uses_oracle",
    "uses_regret",
    "handles_cost",
    "handles_latency",
    "handles_output_validity",
    "main_finding",
    "main_limitation",
    "overlap_with_proposed_study",
    "difference_from_proposed_study",
    "novelty_threat_level",
    "verification_status",
    "notes",
    "verification_source",
    "verification_date",
    "full_text_checked",
    "correction_notes",
    "exclusion_reason",
]

VALID_VERIFICATION_STATUSES = {
    "fully_verified",
    "metadata_verified",
    "partially_verified",
    "unverified",
    "excluded_metadata_error",
}

VALID_NOVELTY_THREAT_LEVELS = {
    "critical",
    "high",
    "moderate",
    "low",
}


def is_placeholder_arxiv(url: str) -> bool:
    """Check if the URL contains a placeholder arXiv identifier ending in 00000."""
    if not url:
        return False
    u = url.strip()
    # Check for placeholder patterns like 2405.00000, 2402.00000
    if re.search(r"\b\d{4}\.00000(?:\b|v\d+)", u):
        return True
    if "2405.00000" in u:
        return True
    if "00000" in u and ("arxiv" in u.lower() or u.startswith("http")):
        return True
    if u.endswith("00000"):
        return True
    return False


def is_valid_doi(doi_str: str) -> bool:
    """Check if a string looks like a legitimate DOI."""
    if not doi_str:
        return False
    d = doi_str.strip()
    if d.lower() in {"not reported", "none", "n/a", "unknown"}:
        return False
    if d.lower().startswith("https://doi.org/") or d.lower().startswith("http://doi.org/"):
        return True
    if d.lower().startswith("doi:"):
        d = d[4:].strip()
    return bool(re.match(r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$", d))


def is_valid_url_or_doi(url: str, doi: str = "") -> bool:
    """
    Check if a URL starts with http(s) or if either url or doi is a real DOI.
    """
    u = (url or "").strip()
    d = (doi or "").strip()
    if u.lower().startswith("http://") or u.lower().startswith("https://"):
        return True
    if is_valid_doi(u):
        return True
    if is_valid_doi(d):
        return True
    return False


def validate_row(
    row: Dict[str, str],
    seen_ids: Optional[Set[str]] = None,
    seen_title_years: Optional[Set[Tuple[str, str]]] = None,
    row_idx: Optional[int] = None,
) -> List[str]:
    """
    Validate a single row dict against business rules.
    Returns a list of error messages (empty if row is valid).
    """
    errors: List[str] = []
    prefix = f"Row {row_idx}" if row_idx is not None else "Row"

    # 1. paper_id uniqueness and non-empty check
    paper_id = (row.get("paper_id") or "").strip()
    if not paper_id:
        errors.append(f"{prefix}: paper_id is empty or missing")
    elif seen_ids is not None:
        if paper_id in seen_ids:
            errors.append(f"{prefix}: duplicate paper_id '{paper_id}'")
        else:
            seen_ids.add(paper_id)

    row_label = f"{prefix} ({paper_id or 'unknown'})"

    # 2. title + year combination uniqueness
    title = (row.get("title") or "").strip()
    raw_year = (str(row.get("year", "")) if row.get("year") is not None else "").strip()

    if not title:
        errors.append(f"{row_label}: title is empty or missing")

    if title and raw_year and seen_title_years is not None:
        norm_title = title.lower()
        norm_key = (norm_title, raw_year)
        if norm_key in seen_title_years:
            errors.append(
                f"{row_label}: duplicate normalized title and year combination ('{title}', '{raw_year}')"
            )
        else:
            seen_title_years.add(norm_key)

    # 3. Validate year as integer between 1970 and 2027
    if not raw_year:
        errors.append(f"{row_label}: year is empty or missing")
    else:
        try:
            year_int = int(raw_year)
            if year_int < 1970 or year_int > 2027:
                errors.append(
                    f"{row_label}: year '{raw_year}' is outside the valid range [1970, 2027]"
                )
        except (ValueError, TypeError):
            errors.append(
                f"{row_label}: year '{raw_year}' is not a valid integer between 1970 and 2027"
            )

    # 4. Validate novelty_threat_level
    threat = (row.get("novelty_threat_level") or "").strip().lower()
    if not threat:
        errors.append(f"{row_label}: novelty_threat_level is empty or missing")
    elif threat not in VALID_NOVELTY_THREAT_LEVELS:
        errors.append(
            f"{row_label}: invalid novelty_threat_level '{threat}', expected one of: "
            f"{', '.join(sorted(VALID_NOVELTY_THREAT_LEVELS))}"
        )

    # 5. Validate verification_status
    status = (row.get("verification_status") or "").strip().lower()
    if not status:
        errors.append(f"{row_label}: verification_status is empty or missing")
    elif status not in VALID_VERIFICATION_STATUSES:
        errors.append(
            f"{row_label}: invalid verification_status '{status}', expected one of: "
            f"{', '.join(sorted(VALID_VERIFICATION_STATUSES))}"
        )

    # 6. Reject placeholder arXiv identifiers ending in 00000 in paper_url
    paper_url = (row.get("paper_url") or "").strip()
    if is_placeholder_arxiv(paper_url):
        errors.append(
            f"{row_label}: placeholder arXiv identifier ending in 00000 in paper_url: '{paper_url}'"
        )

    # 7. Requirements for fully_verified and metadata_verified
    if status in {"fully_verified", "metadata_verified"}:
        v_source = (row.get("verification_source") or "").strip()
        v_date = (row.get("verification_date") or "").strip()
        if not v_source:
            errors.append(
                f"{row_label}: verification_source must be non-empty for status '{status}'"
            )
        if not v_date:
            errors.append(
                f"{row_label}: verification_date must be non-empty for status '{status}'"
            )

    # 8. Requirements specific to fully_verified
    if status == "fully_verified":
        authors = (row.get("authors") or "").strip()
        if not authors or "unknown" in authors.lower():
            errors.append(
                f"{row_label}: fully_verified rows must not have 'Unknown' or empty authors: got '{authors}'"
            )

        doi = (row.get("doi") or "").strip()
        if not is_valid_url_or_doi(paper_url, doi):
            errors.append(
                f"{row_label}: fully_verified rows require a paper_url starting with http or a real DOI, "
                f"got paper_url='{paper_url}', doi='{doi}'"
            )

    return errors


def validate_matrix(rows: List[Dict[str, str]]) -> Tuple[List[str], Dict[str, int], Dict[str, int]]:
    """
    Validate a list of row dicts representing the literature matrix.
    Returns (errors, status_counts, threat_counts).
    """
    errors: List[str] = []
    seen_ids: Set[str] = set()
    seen_title_years: Set[Tuple[str, str]] = set()

    status_counts: Counter = Counter()
    threat_counts: Counter = Counter()

    for idx, row in enumerate(rows, start=1):
        row_errors = validate_row(
            row,
            seen_ids=seen_ids,
            seen_title_years=seen_title_years,
            row_idx=idx,
        )
        errors.extend(row_errors)

        st = (row.get("verification_status") or "").strip().lower()
        if st:
            status_counts[st] += 1

        th = (row.get("novelty_threat_level") or "").strip().lower()
        if th:
            threat_counts[th] += 1

    return errors, dict(status_counts), dict(threat_counts)


def validate_file(csv_path: Path) -> Tuple[bool, List[str], Dict[str, int], Dict[str, int], int]:
    """
    Parse and validate a literature matrix CSV file.
    Returns (is_valid, errors, status_counts, threat_counts, total_rows).
    """
    if not csv_path.exists():
        return False, [f"File not found: {csv_path}"], {}, {}, 0

    try:
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as exc:
        return False, [f"Failed to read CSV file '{csv_path}': {exc}"], {}, {}, 0

    if not rows:
        return False, [f"CSV file '{csv_path}' contains no data rows."], {}, {}, 0

    errors, status_counts, threat_counts = validate_matrix(rows)
    is_valid = len(errors) == 0
    return is_valid, errors, status_counts, threat_counts, len(rows)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate literature matrix CSV.")
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="docs/novelty/literature_matrix.csv",
        help="Path to literature matrix CSV (default: docs/novelty/literature_matrix.csv)",
    )
    parser.add_argument(
        "--path",
        "-p",
        dest="csv_path_opt",
        default=None,
        help="Alternative path to literature matrix CSV",
    )
    args = parser.parse_args(argv)

    target_path = Path(args.csv_path_opt or args.csv_path)

    is_valid, errors, status_counts, threat_counts, total_papers = validate_file(target_path)

    critical_or_high = threat_counts.get("critical", 0) + threat_counts.get("high", 0)

    # Report counts by status and threat level
    print("=== Literature Matrix Validation Report ===")
    print(f"File: {target_path}")
    print("\nCounts by Verification Status:")
    for st in sorted(VALID_VERIFICATION_STATUSES):
        print(f"  {st}: {status_counts.get(st, 0)}")

    print("\nCounts by Novelty Threat Level:")
    for th in ["critical", "high", "moderate", "low"]:
        print(f"  {th}: {threat_counts.get(th, 0)}")

    # Exact required summary lines
    print("\nSummary:")
    print(f"papers: {total_papers}")
    print(f"fully_verified: {status_counts.get('fully_verified', 0)}")
    print(f"metadata_verified: {status_counts.get('metadata_verified', 0)}")
    print(f"partially_verified: {status_counts.get('partially_verified', 0)}")
    print(f"unverified: {status_counts.get('unverified', 0)}")
    print(f"critical_or_high: {critical_or_high}")

    if not is_valid:
        print(f"\nValidation FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("\nValidation PASSED: all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
