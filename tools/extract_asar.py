#!/usr/bin/env python3
"""Small helper used to extract the simple app.asar from the uploaded Electron app."""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path


def extract(asar_path: Path, out_dir: Path) -> None:
    data = asar_path.read_bytes()
    if len(data) < 16:
        raise ValueError("File is too small to be an Electron ASAR archive")

    header_size = struct.unpack("<I", data[12:16])[0]
    header_start = 16
    header_end = header_start + header_size
    header = json.loads(data[header_start:header_end].decode("utf-8"))
    data_start = header_start + ((header_size + 3) // 4) * 4

    out_dir.mkdir(parents=True, exist_ok=True)
    for name, meta in header.get("files", {}).items():
        if "files" in meta:
            continue
        size = int(meta["size"])
        offset = int(meta["offset"])
        target = out_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data[data_start + offset:data_start + offset + size])
        print(f"extracted {target}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: extract_asar.py <app.asar> <output_dir>", file=sys.stderr)
        raise SystemExit(2)
    extract(Path(sys.argv[1]), Path(sys.argv[2]))
