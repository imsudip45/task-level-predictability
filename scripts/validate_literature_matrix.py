#!/usr/bin/env python3
"""
Comprehensive validation script for Task 1C.
Validates:
1. docs/novelty/literature_matrix.csv
2. docs/novelty/search_hits.csv
3. docs/novelty/screening_ledger.csv
4. docs/novelty/search_protocol.md

Enforces schema integrity, cross-ledger consistency, uniqueness constraints,
URL validity, placeholder arXiv detection, verification requirements,
exclusion reasoning, and valid database statuses.
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

VALID_SCREENING_DECISIONS = {
    "included",
    "excluded_irrelevant",
    "excluded_duplicate_version",
    "excluded_metadata_unverifiable",
    "excluded_wrong_selection_level",
    "excluded_other",
}

VALID_DATABASE_STATUSES = {
    "directly_searched",
    "indirectly_represented",
    "inaccessible",
    "not_searched",
}


def is_placeholder_arxiv(url: str) -> bool:
    """Check if the URL contains a placeholder arXiv identifier ending in 00000."""
    if not url:
        return False
    u = url.strip()
    if re.search(r"\b\d{4}\.00000(?:\b|v\d+)", u):
        return True
    if "2405.00000" in u or "2402.00000" in u:
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
    """Check if a URL starts with http(s) or if either url or doi is a real DOI."""
    u = (url or "").strip()
    d = (doi or "").strip()
    if u.lower().startswith("http://") or u.lower().startswith("https://"):
        return True
    if is_valid_doi(u):
        return True
    if is_valid_doi(d):
        return True
    return False


def validate_matrix_row(
    row: Dict[str, str],
    seen_ids: Optional[Set[str]] = None,
    seen_title_years: Optional[Set[Tuple[str, str]]] = None,
    row_idx: Optional[int] = None,
) -> List[str]:
    """Validate a single row dict of literature_matrix.csv."""
    errors: List[str] = []
    prefix = f"Matrix row {row_idx}" if row_idx is not None else "Matrix row"

    # paper_id uniqueness
    paper_id = (row.get("paper_id") or "").strip()
    if not paper_id:
        errors.append(f"{prefix}: paper_id is empty or missing")
    elif seen_ids is not None:
        if paper_id in seen_ids:
            errors.append(f"{prefix}: duplicate paper_id '{paper_id}'")
        else:
            seen_ids.add(paper_id)

    row_label = f"{prefix} ({paper_id or 'unknown'})"

    # title + year uniqueness
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

    # year range [1970, 2027]
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

    # novelty_threat_level
    threat = (row.get("novelty_threat_level") or "").strip().lower()
    if not threat:
        errors.append(f"{row_label}: novelty_threat_level is empty or missing")
    elif threat not in VALID_NOVELTY_THREAT_LEVELS:
        errors.append(
            f"{row_label}: invalid novelty_threat_level '{threat}', expected one of: "
            f"{', '.join(sorted(VALID_NOVELTY_THREAT_LEVELS))}"
        )

    # verification_status
    status = (row.get("verification_status") or "").strip().lower()
    if not status:
        errors.append(f"{row_label}: verification_status is empty or missing")
    elif status not in VALID_VERIFICATION_STATUSES:
        errors.append(
            f"{row_label}: invalid verification_status '{status}', expected one of: "
            f"{', '.join(sorted(VALID_VERIFICATION_STATUSES))}"
        )

    # Placeholder arXiv reject
    paper_url = (row.get("paper_url") or "").strip()
    if is_placeholder_arxiv(paper_url):
        errors.append(
            f"{row_label}: placeholder arXiv identifier ending in 00000 in paper_url: '{paper_url}'"
        )

    # Requirements for authors across all included rows
    authors = (row.get("authors") or "").strip()
    if not authors or "unknown" in authors.lower() or "not verified" in authors.lower():
        errors.append(
            f"{row_label}: included row must not have unverified or unknown authors: got '{authors}'"
        )

    # Generic search result verification source rejection
    v_source = (row.get("verification_source") or "").strip()
    if v_source:
        lower_src = v_source.lower()
        if lower_src in {"web search results", "search results", "web search", "google search"}:
            errors.append(
                f"{row_label}: verification_source cannot be a generic search summary: got '{v_source}'"
            )

    # verification_source and date non-empty for verified rows
    if status in {"fully_verified", "metadata_verified"}:
        v_date = (row.get("verification_date") or "").strip()
        if not v_source:
            errors.append(
                f"{row_label}: verification_source must be non-empty for status '{status}'"
            )
        if not v_date:
            errors.append(
                f"{row_label}: verification_date must be non-empty for status '{status}'"
            )

    # URL / DOI requirements for fully_verified
    if status == "fully_verified":
        doi = (row.get("doi") or "").strip()
        if not is_valid_url_or_doi(paper_url, doi):
            errors.append(
                f"{row_label}: fully_verified rows require a paper_url starting with http or a real DOI, "
                f"got paper_url='{paper_url}', doi='{doi}'"
            )

    return errors


validate_row = validate_matrix_row


def validate_matrix(rows: List[Dict[str, str]]) -> Tuple[List[str], Counter, Counter]:
    """Validate all rows of literature_matrix.csv."""
    errors: List[str] = []
    seen_ids: Set[str] = set()
    seen_title_years: Set[Tuple[str, str]] = set()

    status_counts: Counter = Counter()
    threat_counts: Counter = Counter()

    for idx, row in enumerate(rows, start=1):
        row_errors = validate_matrix_row(
            row,
            seen_ids=seen_ids,
            seen_title_years=seen_title_years,
            row_idx=idx,
        )
        errors.extend(row_errors)
        status = (row.get("verification_status") or "").strip().lower()
        if status in VALID_VERIFICATION_STATUSES:
            status_counts[status] += 1
        threat = (row.get("novelty_threat_level") or "").strip().lower()
        if threat in VALID_NOVELTY_THREAT_LEVELS:
            threat_counts[threat] += 1

    return errors, status_counts, threat_counts


def validate_search_hits(hit_rows: List[Dict[str, str]]) -> List[str]:
    """Validate search_hits.csv."""
    errors: List[str] = []
    if not hit_rows:
        return ["search_hits.csv is empty"]

    seen_hit_ids: Set[str] = set()

    for idx, row in enumerate(hit_rows, start=1):
        prefix = f"Hit row {idx}"
        hid = (row.get("hit_id") or "").strip()
        if not hid:
            errors.append(f"{prefix}: hit_id is empty")
        elif hid in seen_hit_ids:
            errors.append(f"{prefix}: duplicate hit_id '{hid}'")
        else:
            seen_hit_ids.add(hid)

        cr_id = (row.get("canonical_record_id") or "").strip()
        if not cr_id:
            errors.append(f"{prefix} ({hid}): canonical_record_id is empty")

        db = (row.get("database") or "").strip()
        if not db:
            errors.append(f"{prefix} ({hid}): database is empty")

        query = (row.get("exact_query") or "").strip()
        if not query:
            errors.append(f"{prefix} ({hid}): exact_query is empty")

    return errors


def validate_screening_ledger(
    screening_rows: List[Dict[str, str]],
    matrix_rows: Optional[List[Dict[str, str]]] = None,
) -> List[str]:
    """Validate screening_ledger.csv and cross-check with literature_matrix.csv."""
    errors: List[str] = []
    if not screening_rows:
        return ["screening_ledger.csv is empty"]

    seen_cr_ids: Set[str] = set()
    included_cr_to_paper: Dict[str, str] = {}
    included_paper_ids: Set[str] = set()

    matrix_paper_ids = set()
    if matrix_rows is not None:
        matrix_paper_ids = {
            (r.get("paper_id") or "").strip() for r in matrix_rows if (r.get("paper_id") or "").strip()
        }

    for idx, row in enumerate(screening_rows, start=1):
        prefix = f"Screening row {idx}"
        cr_id = (row.get("canonical_record_id") or "").strip()
        if not cr_id:
            errors.append(f"{prefix}: canonical_record_id is empty")
        elif cr_id in seen_cr_ids:
            errors.append(f"{prefix}: duplicate canonical_record_id '{cr_id}'")
        else:
            seen_cr_ids.add(cr_id)

        dec = (row.get("screening_decision") or "").strip().lower()
        if not dec:
            errors.append(f"{prefix} ({cr_id}): screening_decision is empty")
        elif dec not in VALID_SCREENING_DECISIONS:
            errors.append(f"{prefix} ({cr_id}): invalid screening_decision '{dec}'")

        reason = (row.get("exclusion_reason") or "").strip()
        paper_id = (row.get("included_paper_id") or "").strip()

        if dec == "included":
            if not paper_id:
                errors.append(f"{prefix} ({cr_id}): included record missing included_paper_id")
            else:
                if paper_id in included_paper_ids:
                    errors.append(f"{prefix} ({cr_id}): duplicate included_paper_id '{paper_id}'")
                included_paper_ids.add(paper_id)
                included_cr_to_paper[cr_id] = paper_id

            if reason:
                errors.append(
                    f"{prefix} ({cr_id}): included record should have empty exclusion_reason, got '{reason}'"
                )

            # Authors must not be unverified in included records
            authors = (row.get("authors") or "").strip()
            if not authors or "unknown" in authors.lower() or "not verified" in authors.lower():
                errors.append(
                    f"{prefix} ({cr_id}): included record has unverified/unknown authors '{authors}'"
                )
        else:
            # Excluded records must have a non-empty exclusion reason
            if not reason:
                errors.append(f"{prefix} ({cr_id}): excluded record has empty exclusion_reason")
            if paper_id:
                errors.append(
                    f"{prefix} ({cr_id}): excluded record should have empty included_paper_id, got '{paper_id}'"
                )

    # Cross-check with matrix_rows if provided
    if matrix_rows is not None:
        missing_from_screening = matrix_paper_ids - included_paper_ids
        if missing_from_screening:
            errors.append(
                f"Matrix paper_ids missing from screening ledger: {', '.join(sorted(missing_from_screening))}"
            )

        missing_from_matrix = included_paper_ids - matrix_paper_ids
        if missing_from_matrix:
            errors.append(
                f"Screening included_paper_ids missing from matrix: {', '.join(sorted(missing_from_matrix))}"
            )

        if len(matrix_paper_ids) != len(included_paper_ids):
            errors.append(
                f"Count mismatch: matrix has {len(matrix_paper_ids)} papers, "
                f"screening ledger has {len(included_paper_ids)} included records"
            )

    return errors


def validate_database_status(status_str: str) -> bool:
    """Validate that a database status is one of the four allowed strings."""
    return status_str.strip().lower() in VALID_DATABASE_STATUSES


def validate_all(
    matrix_path: Path,
    hits_path: Path,
    screening_path: Path,
    protocol_path: Optional[Path] = None,
) -> Tuple[bool, List[str], Counter, Counter]:
    """Run all validation checks across all files."""
    all_errors: List[str] = []

    # 1. Literature matrix
    if not matrix_path.exists():
        all_errors.append(f"Matrix file not found: {matrix_path}")
        return False, all_errors, Counter(), Counter()

    with matrix_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        matrix_rows = list(reader)

    matrix_errors, status_counts, threat_counts = validate_matrix(matrix_rows)
    all_errors.extend(matrix_errors)

    # 2. Search hits
    if not hits_path.exists():
        all_errors.append(f"Search hits file not found: {hits_path}")
        hit_rows = []
    else:
        with hits_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            hit_rows = list(reader)
        hit_errors = validate_search_hits(hit_rows)
        all_errors.extend(hit_errors)

    # 3. Screening ledger
    if not screening_path.exists():
        all_errors.append(f"Screening ledger file not found: {screening_path}")
        screening_rows = []
    else:
        with screening_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            screening_rows = list(reader)
        screening_errors = validate_screening_ledger(screening_rows, matrix_rows=matrix_rows)
        all_errors.extend(screening_errors)

    # 4. Check that hits connect to screening canonical IDs
    if hit_rows and screening_rows:
        screening_cr_ids = {
            (r.get("canonical_record_id") or "").strip() for r in screening_rows
        }
        for idx, h in enumerate(hit_rows, start=1):
            h_cr = (h.get("canonical_record_id") or "").strip()
            if h_cr and h_cr not in screening_cr_ids:
                all_errors.append(
                    f"Hit row {idx} ({h.get('hit_id')}): canonical_record_id '{h_cr}' not in screening ledger"
                )

    # 5. Check protocol file if provided
    if protocol_path and protocol_path.exists():
        protocol_content = protocol_path.read_text(encoding="utf-8")
        # Check raw hits count match
        raw_match = re.search(r"Raw search hits\s*\|\s*(\d+)", protocol_content)
        if raw_match:
            prot_raw = int(raw_match.group(1))
            if prot_raw != len(hit_rows):
                all_errors.append(
                    f"Protocol reports {prot_raw} raw hits, but search_hits.csv has {len(hit_rows)}"
                )

        # Check unique canonical records match
        unique_match = re.search(r"Unique canonical records[^\n|]*\|\s*(\d+)", protocol_content)
        if unique_match:
            prot_unique = int(unique_match.group(1))
            if prot_unique != len(screening_rows):
                all_errors.append(
                    f"Protocol reports {prot_unique} unique records, but screening_ledger.csv has {len(screening_rows)}"
                )

        # Check included count match
        inc_match = re.search(r"Records included\s*\|\s*(\d+)", protocol_content)
        if inc_match:
            prot_inc = int(inc_match.group(1))
            if prot_inc != len(matrix_rows):
                all_errors.append(
                    f"Protocol reports {prot_inc} included records, but literature_matrix.csv has {len(matrix_rows)}"
                )

    passed = len(all_errors) == 0
    return passed, all_errors, status_counts, threat_counts


def main():
    parser = argparse.ArgumentParser(
        description="Validate literature matrix and search screening ledgers."
    )
    parser.add_argument(
        "--matrix",
        default="docs/novelty/literature_matrix.csv",
        help="Path to literature_matrix.csv",
    )
    parser.add_argument(
        "--hits",
        default="docs/novelty/search_hits.csv",
        help="Path to search_hits.csv",
    )
    parser.add_argument(
        "--screening",
        default="docs/novelty/screening_ledger.csv",
        help="Path to screening_ledger.csv",
    )
    parser.add_argument(
        "--protocol",
        default="docs/novelty/search_protocol.md",
        help="Path to search_protocol.md",
    )
    args = parser.parse_args()

    matrix_path = Path(args.matrix)
    hits_path = Path(args.hits)
    screening_path = Path(args.screening)
    protocol_path = Path(args.protocol) if args.protocol else None

    passed, errors, status_counts, threat_counts = validate_all(
        matrix_path, hits_path, screening_path, protocol_path
    )

    print("=== Literature Matrix & Screening Validation Report ===")
    print(f"Matrix: {matrix_path}")
    print(f"Hits: {hits_path}")
    print(f"Screening: {screening_path}")
    print()

    # Read rows count for summary
    total_papers = 0
    if matrix_path.exists():
        with matrix_path.open("r", encoding="utf-8") as f:
            total_papers = sum(1 for _ in csv.DictReader(f))

    print("Counts by Verification Status:")
    for status in sorted(VALID_VERIFICATION_STATUSES):
        print(f"  {status}: {status_counts.get(status, 0)}")
    print()

    print("Counts by Novelty Threat Level:")
    for threat in ["critical", "high", "moderate", "low"]:
        print(f"  {threat}: {threat_counts.get(threat, 0)}")
    print()

    critical_or_high = threat_counts.get("critical", 0) + threat_counts.get("high", 0)
    print("Summary:")
    print(f"papers: {total_papers}")
    print(f"fully_verified: {status_counts.get('fully_verified', 0)}")
    print(f"metadata_verified: {status_counts.get('metadata_verified', 0)}")
    print(f"partially_verified: {status_counts.get('partially_verified', 0)}")
    print(f"unverified: {status_counts.get('unverified', 0)}")
    print(f"critical_or_high: {critical_or_high}")
    print()

    if passed:
        print("Validation PASSED: all checks passed.")
        sys.exit(0)
    else:
        print(f"Validation FAILED: {len(errors)} error(s) found:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
