"""Check that the public snapshot still matches the frozen bytes.

Does not recompute scores, refit the selector, or run inference.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SMS_SHA256 = "264e288b89a430005de7b72fdfeb77862e46b23b7415c76df285e4e5e1a7f992"

# SHA-256 of the bytes copied from the working tree on 26 September 2026.
EXPECTED_SHA256 = {
    "configs/sms_rule.txt": SMS_SHA256,
    "results/raw/performance_p0_p1.json": "0248e7e456a900cd474ab37fb997ccc8e4414d269431d0475b2e195b3e9a4c15",
    "results/raw/performance_dg.json": "f0e24ef621e713f17cc8fe3896241c6b147184528bdb8dbef257f2eb97aa5d6e",
    "results/raw/selector_sd1.json": "83d652172a6f6045a59f5e7375f3609c24776f99b79cbb202b035e45c398d8dd",
    "data/fingerprint/fingerprint.json": "45ecafcbbf0c6c060483b19dd842bf26b9ab3229c8aa3a6fdc0ea19a4d88f830",
}

REQUIRED = [
    "README.md",
    "LICENSE",
    "LICENSES.md",
    "CITATION.cff",
    "FREEZE.md",
    "LIMITATIONS.md",
    "docs/datasets.md",
    "docs/numerical_fingerprint_manifest.md",
    "docs/performance_matrix.md",
    "docs/selector_target.md",
    "docs/selector_design.md",
    "docs/selector_results.md",
    "docs/evaluation_protocol.md",
    "docs/task_fingerprint_spec.md",
    "docs/primitive_pins.md",
    "docs/reproducibility.md",
    "CHANGELOG.md",
    "docs/validity_audit.md",
    "paper/main.pdf",
    "paper/latex/main.tex",
    "paper/latex/references.bib",
    "configs/sms_rule.txt",
    "src/selector/fit_sd1.py",
    "src/primitives/measure_p0_p1.py",
    "src/primitives/measure_dg.py",
    "src/fingerprint/compute_static_fingerprint.py",
    "src/fingerprint/render_manifest.py",
    "scripts/make_figures.py",
    "requirements-figures.txt",
    "data/fingerprint/fingerprint.json",
    "data/fingerprint/sms_train_indices.json",
    "data/fingerprint/pubmedqa_fold0_train_pmids.json",
    "results/raw/performance_p0_p1.json",
    "results/raw/performance_dg.json",
    "results/raw/selector_sd1.json",
    "results/raw/banking77_eval_indices.json",
    "results/raw/clinc_oos_plus_eval_indices.json",
    "results/raw/civil_comments_binary_eval_indices.json",
    "results/raw/sms_spam_eval_indices.json",
    "results/raw/esci_en_us_task2_eval_indices.json",
    "results/raw/ledgar_eval_indices.json",
    "results/raw/pubmedqa_fold0_eval_indices.json",
    "results/raw/vitaminc_eval_indices.json",
]

FIGURES = [
    "figure1_pipeline.pdf",
    "figure2_heterogeneity.pdf",
    "figure3_prediction.pdf",
    "figure4_error_difference.pdf",
    "figure5_esci.pdf",
]

FREEZE_IDS = ("FPS-1", "FPS-2", "EP-1", "ST-1", "SD-1")

BANNED_KEYS = {
    "text",
    "sentence",
    "utterance",
    "comment",
    "question",
    "context",
    "product_title",
    "description",
    "input",
    "content",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_label_metadata(value) -> bool:
    """A banned key may stay only when the value is a list of label names."""
    if not isinstance(value, list) or not value:
        return False
    return all(isinstance(item, str) and "\n" not in item and len(item) <= 120 for item in value)


def walk(obj, path: str, errors: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in BANNED_KEYS and not is_label_metadata(value):
                errors.append(f"banned field {path}.{key}")
            walk(value, f"{path}.{key}", errors)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            if isinstance(value, (dict, list)):
                walk(value, f"{path}[{i}]", errors)


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing {rel}")

    for name in FIGURES:
        latex = ROOT / "paper" / "latex" / "figures" / name
        public = ROOT / "paper" / "figures" / name
        if not latex.is_file():
            errors.append(f"missing paper/latex/figures/{name}")
        if not public.is_file():
            errors.append(f"missing paper/figures/{name}")
        if latex.is_file() and public.is_file() and latex.read_bytes() != public.read_bytes():
            errors.append(f"figure bytes differ for {name}")

    pdf = ROOT / "paper" / "main.pdf"
    if pdf.is_file() and pdf.stat().st_size == 0:
        errors.append("paper/main.pdf is empty")

    for rel, expected in EXPECTED_SHA256.items():
        path = ROOT / rel
        if not path.is_file():
            continue
        digest = sha256(path)
        if digest != expected:
            errors.append(f"sha256 mismatch {rel}: {digest}")

    rule = ROOT / "configs" / "sms_rule.txt"
    if rule.is_file() and sha256(rule) != SMS_SHA256:
        errors.append("sms rule hash is not the frozen digest")

    for path in list((ROOT / "results").rglob("*.json")) + list((ROOT / "data").rglob("*.json")):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"json parse {path.relative_to(ROOT)}: {exc}")
            continue
        walk(obj, path.name, errors)
        rel = path.relative_to(ROOT).as_posix()
        if rel.endswith("_eval_indices.json") or rel.endswith("sms_train_indices.json"):
            if not isinstance(obj, list) or not all(isinstance(i, int) and not isinstance(i, bool) for i in obj):
                errors.append(f"{rel} is not a list of integer row ids")
        if rel.endswith("pubmedqa_fold0_train_pmids.json"):
            if not isinstance(obj, list) or not all(isinstance(i, str) and i.isdigit() for i in obj):
                errors.append(f"{rel} is not a list of PMID identifiers")

    selector_path = ROOT / "results" / "raw" / "selector_sd1.json"
    if selector_path.is_file():
        selector = json.loads(selector_path.read_text(encoding="utf-8"))
        if selector.get("freeze") != "SD-1":
            errors.append("selector_sd1.json freeze is not SD-1")

    finger_path = ROOT / "data" / "fingerprint" / "fingerprint.json"
    if finger_path.is_file():
        finger = json.loads(finger_path.read_text(encoding="utf-8"))
        protocol = str(finger.get("protocol", ""))
        for token in ("FPS-1", "FPS-2"):
            if token not in protocol:
                errors.append(f"fingerprint protocol missing {token}")

    freeze = ROOT / "FREEZE.md"
    if freeze.is_file():
        text = freeze.read_text(encoding="utf-8")
        for token in FREEZE_IDS:
            if token not in text:
                errors.append(f"FREEZE.md missing {token}")

    script = ROOT / "scripts" / "make_figures.py"
    if script.is_file():
        source = script.read_text(encoding="utf-8")
        needles = (
            'ROOT / "results" / "raw"',
            'ROOT / "paper" / "latex" / "figures"',
            'ROOT / "paper" / "figures"',
        )
        for needle in needles:
            if needle not in source:
                errors.append(f"make_figures.py does not point at {needle}")

    checks = [
        ("freeze identifiers", not any(item.startswith("FREEZE.md") or "freeze" in item or item.startswith("fingerprint protocol") for item in errors)),
        ("performance_p0_p1.json", (ROOT / "results/raw/performance_p0_p1.json").is_file() and not any("performance_p0_p1.json" in item for item in errors)),
        ("performance_dg.json", (ROOT / "results/raw/performance_dg.json").is_file() and not any("performance_dg.json" in item for item in errors)),
        ("selector_sd1.json", (ROOT / "results/raw/selector_sd1.json").is_file() and not any("selector_sd1.json" in item for item in errors)),
        ("fingerprint.json", (ROOT / "data/fingerprint/fingerprint.json").is_file() and not any("fingerprint.json" in item or item.startswith("fingerprint protocol") for item in errors)),
        ("SMS rule SHA-256", (ROOT / "configs/sms_rule.txt").is_file() and not any("sms rule" in item or "sms_rule.txt" in item for item in errors)),
        ("public index files contain no text fields", not any("banned field" in item or "row ids" in item or "PMID" in item or "json parse" in item for item in errors)),
        ("five figures", not any("figure" in item for item in errors)),
        ("paper/main.pdf", pdf.is_file() and pdf.stat().st_size > 0),
    ]

    print("Task-Level Predictability — Snapshot Verification")
    print()
    failed = False
    for label, ok in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            failed = True
        print(f"[{status}] {label}")
    other = [item for item in errors if not any(
        token in item
        for token in (
            "FREEZE.md",
            "freeze",
            "fingerprint",
            "performance_p0_p1.json",
            "performance_dg.json",
            "selector_sd1.json",
            "sms",
            "banned field",
            "row ids",
            "PMID",
            "json parse",
            "figure",
            "paper/main.pdf",
        )
    )]
    for item in other:
        failed = True
        print(f"[FAIL] {item}")
    print()
    if failed or errors:
        print("Snapshot verification: FAIL")
        return 1
    print("Snapshot verification: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
