"""`python -m app.modules.corpus.import_cli <file.jsonl> --source ... \
--split test --dataset-version v0`

Imports a founder-curated jsonl corpus (spec §4.3: volunteer/synthetic
essays with a founder-assigned "ground truth" label) into
`training_corpus_item` + `human_label`, ready for `eval_cli`.

Each line: `{"task_type": ..., "prompt": ..., "essay": ...,
"label": {"criteria_scores": {...}, "overall_score": ..., "notes": ...},
"is_injection": false}` (`is_injection` optional, defaults to false).
"""

import argparse
import json
from typing import Literal, cast

from app.modules.corpus import service
from app.modules.corpus.service import Split

ImportSource = Literal["volunteer", "synthetic"]


def run_import(
    path: str, *, source: ImportSource, split: Split, dataset_version: str
) -> int:
    """Import every line of `path` as a `training_corpus_item` (no AI
    outcome - `outcome=None`) plus its founder `human_label` (labeler
    "import"). Returns the number of lines imported. Raises `ValueError`
    (from `add_label`) on the first line whose label has an out-of-range or
    non-half-step score - nothing after that line is imported."""
    count = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            label = row["label"]
            item_id, _delete_code = service.add_item_and_get_id(
                source,
                row["task_type"],
                row["prompt"],
                row["essay"],
                None,
                split=split,
                dataset_version=dataset_version,
                is_injection=row.get("is_injection", False),
            )
            service.add_label(
                item_id,
                labeler="import",
                criteria_scores=label["criteria_scores"],
                overall_score=label["overall_score"],
                issue_verdicts=None,
                missed_issues="",
                notes=label.get("notes", ""),
            )
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import a jsonl corpus into training_corpus_item + human_label."
    )
    parser.add_argument("file", help="Path to the .jsonl file to import.")
    parser.add_argument("--source", required=True, choices=["volunteer", "synthetic"])
    parser.add_argument("--split", required=True, choices=["unassigned", "dev", "test"])
    parser.add_argument("--dataset-version", required=True)
    args = parser.parse_args()

    count = run_import(
        args.file,
        source=cast(ImportSource, args.source),
        split=cast(Split, args.split),
        dataset_version=args.dataset_version,
    )
    print(  # noqa: T201
        f"Imported {count} item(s) into split={args.split!r} "
        f"dataset_version={args.dataset_version!r} source={args.source!r}."
    )


if __name__ == "__main__":
    main()
