"""Seed demo documents into the RAG pipeline.

Usage:
    python scripts/seed_demo.py [--dir path/to/sample/docs]
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from starlette.datastructures import UploadFile  # noqa: E402

from app.rag.ingest import ingest_file  # noqa: E402
from app.rag.loaders import SUPPORTED_EXTENSIONS  # noqa: E402


async def ingest_path(path: Path) -> None:
    content = path.read_bytes()
    upload = UploadFile(
        filename=path.name,
        file=BytesIO(content),
        headers={"content-type": "application/octet-stream"},
    )
    metadata = await ingest_file(upload)
    print(f"  - {path.name}: {metadata.chunk_count} chunk(s)")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Seed demo documents")
    parser.add_argument(
        "--dir",
        type=Path,
        default=BACKEND / "data" / "demo",
        help="Directory containing sample documents to ingest",
    )
    args = parser.parse_args()

    demo_dir = args.dir
    if not demo_dir.exists():
        print(f"Demo directory not found: {demo_dir}")
        print("Create it and add sample PDF/DOCX/TXT files, then re-run.")
        return

    files = [
        path
        for path in demo_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    if not files:
        print(f"No supported files found in {demo_dir}")
        return

    print(f"Ingesting {len(files)} file(s) from {demo_dir}")
    for path in files:
        await ingest_path(path)


if __name__ == "__main__":
    asyncio.run(main())
