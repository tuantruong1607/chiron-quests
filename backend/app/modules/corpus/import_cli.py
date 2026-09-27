"""`python -m app.modules.corpus.import_cli <file.jsonl> --source ... \
--split test --dataset-version v0`

Imports a founder-curated jsonl corpus (spec §4.3: volunteer/synthetic
essays with a founder-assigned "ground truth" label) into
`training_corpus_item` + `human_label`, ready for `eval_cli`.

Each line: `{"task_type": ..., "prompt": ..., "essay": ...,
"label": {"criteria_scores": {...}, "overall_score": ..., "notes": ...},
"is_injection": false}` (`is_injection` optional, defaults to false).

Every line is validated before anything is written: a bad line (invalid
JSON, a missing key, a bad `task_type`, or a score outside [0, 10] in
steps of 0.5) aborts the whole import with nothing written - never a
partial import with an orphaned item or a half-imported file.
"""

import argparse
import json
import sys
from typing import Any, Literal, cast

from app.modules.corpus import service
from app.modules.corpus.models import HumanLabel, TrainingCorpusItem
from app.modules.corpus.service import Split

ImportSource = Literal["volunteer", "synthetic"]

_VALID_TASK_TYPES = {"task1", "task2"}
_REQUIRED_ROW_KEYS = {"task_type", "prompt", "essay", "label"}
_REQUIRED_LABEL_KEYS = {"criteria_scores", "overall_score"}


class ImportValidationError(ValueError):
    """Raised by `run_import` for the first invalid line, naming its line
    number (1-indexed, matching what a person would see in an editor) so
    it can be found and fixed."""

    def __init__(self, line_number: int, reason: str) -> None:
        super().__init__(f"line {line_number}: {reason}")
        self.line_number = line_number
        self.reason = reason


def _validate_row(line_number: int, row: object) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise ImportValidationError(line_number, "expected a JSON object")
    missing = _REQUIRED_ROW_KEYS - row.keys()
    if missing:
        raise ImportValidationError(
            line_number, f"missing required key(s): {sorted(missing)}"
        )
    if row["task_type"] not in _VALID_TASK_TYPES:
        raise ImportValidationError(
            line_number,
            f"task_type must be one of {sorted(_VALID_TASK_TYPES)}, "
            f"got {row['task_type']!r}",
        )
    label = row["label"]
    if not isinstance(label, dict):
        raise ImportValidationError(line_number, "label must be a JSON object")
    missing_label = _REQUIRED_LABEL_KEYS - label.keys()
    if missing_label:
        raise ImportValidationError(
            line_number, f"label missing required key(s): {sorted(missing_label)}"
        )
    scores = [*label["criteria_scores"].values(), label["overall_score"]]
    for score in scores:
        if not service.is_valid_score(score):
            raise ImportValidationError(
                line_number, f"score {score!r} must be in [0, 10] in steps of 0.5"
            )
    return row


def _build_pairs(
    rows: list[tuple[int, dict[str, Any]]],
    *,
    source: ImportSource,
    split: Split,
    dataset_version: str,
) -> list[tuple[TrainingCorpusItem, HumanLabel]]:
    """Build every row's (item, label) pair with no DB access (per-row
    validation already happened in `_validate_row`) - the whole batch is
    inserted afterward in one transaction."""
    pairs: list[tuple[TrainingCorpusItem, HumanLabel]] = []
    for line_number, row in rows:
        label = row["label"]
        item, _delete_code = service.build_item(
            source,
            row["task_type"],
            row["prompt"],
            row["essay"],
            None,
            split=split,
            dataset_version=dataset_version,
            is_injection=row.get("is_injection", False),
        )
        try:
            human_label = service.build_label(
                item.id,
                labeler="import",
                criteria_scores=label["criteria_scores"],
                overall_score=label["overall_score"],
                issue_verdicts=None,
                missed_issues="",
                notes=label.get("notes", ""),
            )
        except ValueError as exc:
            # Re-validated here (build_item/build_label are also called
            # directly, so this can't only rely on _validate_row), named
            # with its line number for the same reason _validate_row is.
            raise ImportValidationError(line_number, str(exc)) from exc
        pairs.append((item, human_label))
    return pairs


def run_import(
    path: str, *, source: ImportSource, split: Split, dataset_version: str
) -> int:
    """Validate every line of `path`, then insert every resulting
    `training_corpus_item` + `human_label` (labeler "import") in one
    transaction. Returns the number of lines imported. Raises
    `ImportValidationError` (naming the first bad line) if any line is
    invalid - nothing is written in that case, whether the file has 1 line
    or 1000."""
    numbered_lines: list[tuple[int, str]] = []
    with open(path, encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            stripped = raw_line.strip()
            if stripped:
                numbered_lines.append((line_number, stripped))

    rows: list[tuple[int, dict[str, Any]]] = []
    for line_number, line in numbered_lines:
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ImportValidationError(line_number, f"invalid JSON: {exc}") from exc
        rows.append((line_number, _validate_row(line_number, parsed)))

    pairs = _build_pairs(
        rows, source=source, split=split, dataset_version=dataset_version
    )
    service.bulk_add_items_and_labels(pairs)
    return len(pairs)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import a jsonl corpus into training_corpus_item + human_label."
    )
    parser.add_argument("file", help="Path to the .jsonl file to import.")
    parser.add_argument("--source", required=True, choices=["volunteer", "synthetic"])
    parser.add_argument("--split", required=True, choices=["unassigned", "dev", "test"])
    parser.add_argument("--dataset-version", required=True)
    args = parser.parse_args()

    try:
        count = run_import(
            args.file,
            source=cast(ImportSource, args.source),
            split=cast(Split, args.split),
            dataset_version=args.dataset_version,
        )
    except ImportValidationError as exc:
        print(f"Import aborted, nothing written: {exc}", file=sys.stderr)  # noqa: T201
        raise SystemExit(1) from exc

    print(  # noqa: T201
        f"Imported {count} item(s) into split={args.split!r} "
        f"dataset_version={args.dataset_version!r} source={args.source!r}."
    )


if __name__ == "__main__":
    main()
