#!/usr/bin/env python3
"""Render fastfetch's config from the live Caelestia colour scheme.

This reads ~/.local/state/caelestia/scheme.json (or the SCHEME_COLOURS env var
that Caelestia exports to its theme post-hook) and substitutes tokens in
config.template.jsonc, writing the result to config.jsonc.

Token syntax inside config.template.jsonc:

    {{ name }}              -> 6-digit hex, no '#'   (e.g. bac5ee)
    {{! name }}             -> truecolor ANSI escape, JSON-escaped
                               (i.e. the literal text \\u001b[38;2;R;G;Bm)
    {{! name | light }}     -> same, blended toward white
    {{! name | dark }}      -> same, multiplied down (for borders/outlines)
    {{! name | mute }}      -> same, blended toward the foreground

`name` is any key from scheme.json's "colours" object (primary, tertiary,
onSurfaceVariant, peach, mauve, ...).
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HOME = Path.home()
BASE = Path(__file__).resolve().parent
TEMPLATE = BASE / "config.template.jsonc"
OUTPUT = BASE / "config.jsonc"
SCHEME = Path(
    os.environ.get("CAELESTIA_SCHEME_PATH", HOME / ".local/state/caelestia/scheme.json")
)

TOKEN = re.compile(
    r"\{\{(!?)\s*([A-Za-z0-9_]+)\s*(?:\|\s*(light|dark|mute)\s*)?\}\}"
)


def load_colours() -> dict[str, str]:
    # Prefer what Caelestia hands us when running as a theme post-hook.
    raw = os.environ.get("SCHEME_COLOURS")
    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
    data = json.loads(SCHEME.read_text())
    return data.get("colours", data)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")[:6].ljust(6, "0")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    return "".join(f"{max(0, min(255, round(c))):02x}" for c in rgb)


def blend(a, b, t: float):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def make_replacer(colours: dict[str, str]):
    fg = hex_to_rgb(colours.get("onSurface", "ffffff"))

    def transform(rgb, style: str):
        if style == "light":
            return tuple(min(255, c + (255 - c) * 0.45) for c in rgb)
        if style == "dark":
            return tuple(c * 0.55 for c in rgb)
        if style == "mute":
            return blend(rgb, fg, 0.5)
        return rgb

    def repl(match: re.Match) -> str:
        escape, name, style = match.group(1), match.group(2), match.group(3)
        rgb = hex_to_rgb(colours.get(name, "ffffff"))
        if style:
            rgb = transform(rgb, style)
        if escape:
            # Literal backslash-u-0-0-1-b so the JSON parser turns it into ESC.
            return "\\u001b[38;2;%d;%d;%dm" % rgb
        return rgb_to_hex(rgb)

    return repl


def main() -> int:
    if not TEMPLATE.is_file():
        print(f"render.py: missing template {TEMPLATE}", file=sys.stderr)
        return 1
    try:
        colours = load_colours()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"render.py: could not read colours ({exc})", file=sys.stderr)
        return 1

    rendered = TOKEN.sub(make_replacer(colours), TEMPLATE.read_text())

    # Validate before clobbering the working config. The template is JSONC, so
    # drop whole-line // comments before handing it to the strict parser.
    probe = "\n".join(l for l in rendered.splitlines() if not l.strip().startswith("//"))
    try:
        json.loads(probe)
    except json.JSONDecodeError as exc:
        print(f"render.py: rendered config is invalid JSON ({exc})", file=sys.stderr)
        return 1

    OUTPUT.write_text(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
