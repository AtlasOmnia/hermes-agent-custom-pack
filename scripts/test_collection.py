#!/usr/bin/env python3
"""Run every skill package's unittest suite."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    test_dirs = sorted(path for path in (ROOT / "skills").glob("*/tests") if path.is_dir())
    if not test_dirs:
        print("ERROR: no skill test directories found")
        return 1
    for test_dir in test_dirs:
        package = test_dir.parent.name
        print(f"TEST_PACKAGE={package}", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(test_dir), "-v"],
            cwd=ROOT,
            check=False,
        )
        if result.returncode:
            return result.returncode
    print(f"COLLECTION_TESTS=PASS packages={len(test_dirs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
