"""Stratified, reproducible block randomization.

Each new subject is assigned to one of the (group, subgroup) cells, stratified
by sex. The cells that currently hold the fewest subjects of that sex are the
candidates; if all cells are balanced, every cell is a candidate. The choice
among candidates is pseudo-random but fully reproducible: the random generator
is seeded with ``seed + (number of subjects already in the stratum)``.

Given the same seed and the same history of records, the output is always
identical.

Author: LC (https://github.com/MrLiuk36)
License: MIT
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
from pathlib import Path
from typing import Iterable, Mapping, Sequence

DEFAULT_SEED = 12345
DEFAULT_GROUPS: tuple[str, ...] = ("C", "S")
DEFAULT_SUBGROUPS: tuple[str, ...] = ("1", "2")

# Columns expected in the records file / dictionaries.
COL_ID = "subject_id"
COL_SEX = "sex"
COL_GROUP = "group"
COL_SUBGROUP = "subgroup"
REQUIRED_COLUMNS = (COL_SEX, COL_GROUP, COL_SUBGROUP)


def assign_next_subject(
    target_sex: str,
    records: Iterable[Mapping[str, str]],
    seed: int = DEFAULT_SEED,
    groups: Sequence[str] = DEFAULT_GROUPS,
    subgroups: Sequence[str] = DEFAULT_SUBGROUPS,
) -> tuple[str, str, int]:
    """Assign the next subject of a given sex to a (group, subgroup) cell.

    Args:
        target_sex: Sex/stratum of the new subject (e.g. "M", "F").
        records: Previous assignments. Each item is a mapping with the keys
            "sex", "group" and "subgroup".
        seed: Base seed of the pseudo-random generator.
        groups: Allowed group labels.
        subgroups: Allowed subgroup labels.

    Returns:
        (group, subgroup, subject_number) where subject_number is the
        progressive number of the new subject within its sex stratum.

    Raises:
        ValueError: if a record of the target sex has a group/subgroup
            combination that is not allowed.
    """
    cells = [(g, s) for g in groups for s in subgroups]
    counts = dict.fromkeys(cells, 0)
    n_in_stratum = 0

    for record in records:
        if record[COL_SEX] != target_sex:
            continue
        cell = (record[COL_GROUP], record[COL_SUBGROUP])
        if cell not in counts:
            raise ValueError(
                f"Unknown group/subgroup {cell} in records "
                f"(allowed: {cells})."
            )
        counts[cell] += 1
        n_in_stratum += 1

    max_count = max(counts.values())
    underrepresented = [c for c in cells if counts[c] < max_count]
    candidates = underrepresented or cells

    # Local generator: does not touch the global `random` state.
    rng = random.Random(seed + n_in_stratum)
    group, subgroup = rng.choice(candidates)
    return group, subgroup, n_in_stratum + 1


def load_records(path: Path) -> list[dict[str, str]]:
    """Read the records CSV (header: subject_id,sex,group,subgroup)."""
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(
                f"Missing column(s) {missing} in {path}. "
                f"Expected header: {COL_ID},{COL_SEX},{COL_GROUP},{COL_SUBGROUP}"
            )
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def append_record(path: Path, subject_id: str, sex: str, group: str, subgroup: str) -> None:
    """Append a new assignment to the records CSV."""
    with path.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([subject_id, sex, group, subgroup])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Stratified reproducible block randomization."
    )
    parser.add_argument("--records", type=Path, required=True,
                        help="CSV with columns subject_id,sex,group,subgroup")
    parser.add_argument("--sex", required=True,
                        help="Sex/stratum of the new subject (e.g. M or F)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help=f"Base seed (default {DEFAULT_SEED})")
    parser.add_argument("--subject-id",
                        help="If given, the new assignment is appended to the CSV")
    args = parser.parse_args(argv)

    records = load_records(args.records)
    group, subgroup, number = assign_next_subject(args.sex, records, seed=args.seed)
    print(f"sex={args.sex} group={group} subgroup={subgroup} "
          f"(subject n. {number} of this stratum)")

    if args.subject_id:
        append_record(args.records, args.subject_id, args.sex, group, subgroup)
        print(f"Appended to {args.records}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
