"""Seed demo documents into the RAG pipeline.

Usage:
    python scripts/seed_demo.py [--dir path/to/sample/docs]
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed demo documents")
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("backend/data/demo"),
        help="Directory containing sample documents to ingest",
    )
    args = parser.parse_args()

    demo_dir = args.dir
    if not demo_dir.exists():
        print(f"Demo directory not found: {demo_dir}")
        print("Create it and add sample PDF/DOCX/TXT files, then re-run.")
        return

    files = list(demo_dir.glob("*"))
    if not files:
        print(f"No files found in {demo_dir}")
        return

    print(f"Found {len(files)} file(s) in {demo_dir}")
    # TODO: wire up ingest_file for each document once RAG pipeline is implemented
    for path in files:
        print(f"  - {path.name} (skipped — ingest not yet implemented)")


if __name__ == "__main__":
    main()
