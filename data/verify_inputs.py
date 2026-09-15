#!/usr/bin/env python3
"""Verify that local E-SEAT R1 input files match the frozen manifest."""

from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "MANIFEST.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE
    failures = 0

    with MANIFEST.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        if row["used_by_master"] != "yes":
            continue
        path = root / row["file"]
        if not path.exists():
            print(f"MISSING  {row['file']}")
            failures += 1
            continue

        expected_size = int(row["size_bytes"])
        actual_size = path.stat().st_size
        actual_hash = sha256(path)

        size_ok = actual_size == expected_size
        hash_ok = actual_hash == row["sha256"]
        status = "OK" if size_ok and hash_ok else "FAIL"
        print(f"{status:7} {row['file']}")

        if not size_ok:
            print(f"         size: expected {expected_size}, got {actual_size}")
        if not hash_ok:
            print(f"         sha256: expected {row['sha256']}")
            print(f"                 got {actual_hash}")
        if not (size_ok and hash_ok):
            failures += 1

    if failures:
        print(f"\n{failures} input check(s) failed.")
        return 1

    print("\nAll authoritative E-SEAT R1 input files match the frozen manifest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
