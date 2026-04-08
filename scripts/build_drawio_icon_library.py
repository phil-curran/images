#!/usr/bin/env python3
"""
Build a draw.io custom library file from all SVGs under icons/.

Output is a JSON array in libraries/all-icons.xml (same pattern as jgraph/drawio-libs).
Run from repo root: python3 scripts/build_drawio_icon_library.py
"""

from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ICONS_DIR = REPO / "icons"
OUT_FILE = REPO / "libraries" / "all-icons.xml"


def svg_to_data_uri(svg_bytes: bytes) -> str:
    b64 = base64.standard_b64encode(svg_bytes).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


def parse_display_size(content: str) -> tuple[int, int]:
    """Pick a reasonable w/h for the library grid (max dimension ~64px)."""
    def num(s: str) -> float | None:
        s = s.strip().rstrip("px").rstrip("pt")
        try:
            v = float(s)
            return v if v > 0 else None
        except ValueError:
            return None

    w = h = None
    m = re.search(r"<svg\b[^>]*\bwidth=\"([^\"]+)\"", content, re.I)
    if m:
        w = num(m.group(1))
    m = re.search(r"<svg\b[^>]*\bheight=\"([^\"]+)\"", content, re.I)
    if m:
        h = num(m.group(1))
    if w and h:
        s = 64.0 / max(w, h)
        return max(1, round(w * s)), max(1, round(h * s))

    m = re.search(r'viewBox="([^"]+)"', content)
    if m:
        parts = m.group(1).replace(",", " ").split()
        if len(parts) >= 4:
            bw = num(parts[2])
            bh = num(parts[3])
            if bw and bh:
                s = 64.0 / max(bw, bh)
                return max(1, round(bw * s)), max(1, round(bh * s))

    return 64, 64


def main() -> int:
    if not ICONS_DIR.is_dir():
        print(f"Missing icons directory: {ICONS_DIR}", file=sys.stderr)
        return 1

    svgs = sorted(ICONS_DIR.rglob("*.svg"))
    if not svgs:
        print(f"No SVG files under {ICONS_DIR}", file=sys.stderr)
        return 1

    entries: list[dict] = []
    for path in svgs:
        rel = path.relative_to(ICONS_DIR)
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        w, h = parse_display_size(text)
        title = path.stem.replace("_", " ").replace("-", " ")
        tag_parts = list(rel.parts[:-1]) + [path.stem]
        tags = " ".join(p.replace("-", " ").replace("_", " ") for p in tag_parts)

        entries.append(
            {
                "data": svg_to_data_uri(raw),
                "w": w,
                "h": h,
                "aspect": "fixed",
                "title": title,
                "tags": tags,
            }
        )

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(entries)} icons -> {OUT_FILE} ({OUT_FILE.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
