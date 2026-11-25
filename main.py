#!/usr/bin/env python3
"""Entry for make.fun u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Writes the invitation letter image (entry.png, rendered by the agent and
shipped in this repository) to the output directory, after validating it:
PNG magic bytes, at most 1 MiB, at most 1024x1024 px.

Standard library only; deterministic - every run writes identical bytes.
No network access, no writes outside the output directory.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

MAX_BYTES = 1048576
MAX_DIM = 1024


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
        f.seek(-12, os.SEEK_END)
        tail = f.read(12)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    if tail[4:8] != b"IEND":
        raise ValueError("truncated PNG: missing IEND chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        raise ValueError("entry.png is %d bytes, over the 1 MiB limit"
                         % size)
    width, height = png_size(SRC)
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError("entry.png is %dx%d, over the 1024x1024 limit"
                         % (width, height))
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote %s (%dx%d, %d bytes)" % (dst, width, height, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
