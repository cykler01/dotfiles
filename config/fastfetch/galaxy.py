#!/usr/bin/env python3
"""An animated ASCII spiral galaxy for your fastfetch rice.

Colours are pulled from the live Caelestia scheme, so the galaxy re-tints
itself alongside the rest of the desktop whenever you change wallpaper.

Usage:
    galaxy.py                 animate the galaxy until Ctrl-C
    galaxy.py --fetch         animate beside fastfetch output, then settle
    galaxy.py --once          print a single frame and exit (no cursor magic)
    galaxy.py --seconds 8     how long the animated phase lasts (default 6)

Options:
    --width N / --height N    force the galaxy grid size
    --fps N                   animation frames per second (default 20)
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HOME = Path.home()
SCHEME = Path(
    os.environ.get("CAELESTIA_SCHEME_PATH", HOME / ".local/state/caelestia/scheme.json")
)

RAMP = " .`':;!~+ic*ox#%@"  # increasing brightness
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


# --------------------------------------------------------------------------- #
# colours
# --------------------------------------------------------------------------- #
def load_colours() -> dict[str, str]:
    try:
        data = json.loads(SCHEME.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    return data.get("colours", data)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")[:6].ljust(6, "0")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def scale(rgb, factor: float):
    return tuple(max(0, min(255, round(c * factor))) for c in rgb)


def fg(rgb) -> str:
    return "\x1b[38;2;%d;%d;%dm" % rgb


# --------------------------------------------------------------------------- #
# the galaxy
# --------------------------------------------------------------------------- #
def _noise(a: int, b: int, seed: int = 1) -> float:
    """Deterministic pseudo-random in [0, 1)."""
    n = math.sin(a * 127.1 + b * 311.7 + seed * 74.7) * 43758.5453
    return n - math.floor(n)


def render_frame(
    t: float, width: int, height: int, palette: list[tuple[int, int, int]]
) -> list[list[tuple[str, int]]]:
    """Return a grid of (char, palette-index) for rotation phase `t`."""
    cx, cy = (width - 1) / 2, (height - 1) / 2
    radius = max(cx, 1.0)
    aspect = 2.15  # terminal cells are ~2x taller than wide
    incline = 0.62  # squash the disk vertically: we view it at an angle
    tilt = math.radians(-22.0)
    ct, st = math.cos(tilt), math.sin(tilt)

    grid: list[list[tuple[str, int]]] = []
    for row in range(height):
        line: list[tuple[str, int]] = []
        for col in range(width):
            px = col - cx
            py = (row - cy) * aspect
            # incline the disk, then tilt it
            u, v = px, py * incline
            big_x = u * ct - v * st
            big_y = u * st + v * ct
            r = math.hypot(big_x, big_y) / radius
            theta = math.atan2(big_y, big_x)

            # two logarithmic spiral arms, slowly rotating
            phi = 2.0 * theta + 2.1 * math.log(r + 0.10) - t
            # sharpened arm profile: bright on the arms, dark between them
            arm = math.exp(5.0 * (math.cos(phi) - 1.0))
            edge = 1.0 / (1.0 + (r / 0.9) ** 8)  # soft outer cutoff

            disk = math.exp(-1.7 * r)
            core = math.exp(-((r / 0.12) ** 2))
            value = arm * disk * 1.35 * edge + core + 0.03 * disk

            # drifting field stars
            star = _noise(col, row, 3) < 0.02 and r < 1.02
            if star:
                value += 0.30 + 0.35 * math.sin(t * 2.2 + _noise(col, row, 7) * math.tau)

            value *= 1.0 + 0.08 * math.sin(t * 3.0 + _noise(col, row, 11) * math.tau)

            idx = int(min(1.0, max(0.0, value)) * (len(RAMP) - 1) + 0.5)
            char = RAMP[idx]

            if star and value > 0.2:
                band = 4  # star
            elif core > 0.6 and r < 0.16:
                band = 0  # warm core
            elif r < 0.42:
                band = 1  # inner arms
            elif r < 0.78:
                band = 2  # outer haze
            else:
                band = 3  # dim edge
            line.append((char, band))
        grid.append(line)
    return grid


def paint(grid: list[list[tuple[str, int]]], palette) -> list[str]:
    """Turn a grid into ANSI-coloured strings (no padding)."""
    out = []
    for line in grid:
        parts, last = [], None
        for char, band in line:
            if band != last:
                parts.append(fg(palette[band]))
                last = band
            parts.append(char)
        parts.append("\x1b[0m")
        out.append("".join(parts).rstrip())
    return out


def get_palette(colours: dict[str, str]):
    def pick(name, fallback, factor=1.0):
        return scale(hex_to_rgb(colours.get(name, fallback)), factor)

    return [
        pick("peach", "f5d6a0", 1.05),        # 0 warm core
        pick("primary", "bac5ee"),            # 1 inner arms
        pick("secondary", "c1c6dd", 0.75),    # 2 outer haze
        pick("secondary", "c1c6dd", 0.42),    # 3 dim edge
        pick("mauve", "b2bcff", 1.15),        # 4 stars
    ]


# --------------------------------------------------------------------------- #
# side-by-side with fastfetch
# --------------------------------------------------------------------------- #
def fetch_lines() -> list[str]:
    try:
        proc = subprocess.run(
            ["fastfetch", "-l", "none"], capture_output=True, text=True, timeout=10
        )
        return proc.stdout.splitlines()
    except (OSError, subprocess.SubprocessError):
        return []


def visible_len(text: str) -> int:
    return len(ANSI_RE.sub("", text))


def combine(galaxy_lines: list[str], info_lines: list[str], gap: int = 4) -> list[str]:
    width = max((visible_len(l) for l in galaxy_lines), default=0)
    rows = max(len(galaxy_lines), len(info_lines))
    spacer = " " * gap
    out = []
    for i in range(rows):
        g = galaxy_lines[i] if i < len(galaxy_lines) else ""
        pad = " " * (width - visible_len(g))
        n = info_lines[i] if i < len(info_lines) else ""
        out.append(f"{g}{pad}{spacer}\x1b[0m{n}")
    return out


def block(lines: list[str], width: int) -> str:
    # pad every line to full width so redraws don't leave residue
    padded = [l + " " * max(0, width - visible_len(l)) for l in lines]
    return "\n".join(padded) + "\n"


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--fetch", action="store_true", help="render beside fastfetch")
    ap.add_argument("--once", action="store_true", help="print one frame and exit")
    ap.add_argument("--seconds", type=float, default=6.0)
    ap.add_argument("--fps", type=float, default=20.0)
    ap.add_argument("--width", type=int, default=0)
    ap.add_argument("--height", type=int, default=0)
    args = ap.parse_args()

    term = shutil.get_terminal_size(fallback=(110, 32))
    width = args.width or 42
    height = args.height or 19
    palette = get_palette(load_colours())
    gap = 4
    info = fetch_lines() if args.fetch else []

    def frame(t: float) -> list[str]:
        g = paint(render_frame(t, width, height, palette), palette)
        return combine(g, info, gap) if args.fetch else g

    if args.once or not sys.stdout.isatty():
        sys.stdout.write(block(frame(0.6), term.columns) + "\x1b[0m")
        return 0

    height_rows = max(height, len(info))
    sys.stdout.write("\x1b[?25l")
    start, first = time.monotonic(), True
    try:
        while True:
            elapsed = time.monotonic() - start
            if elapsed > args.seconds:
                break
            out = block(frame(elapsed * 0.9), term.columns)
            if not first:
                sys.stdout.write(f"\x1b[{height_rows}A")
            sys.stdout.write(out)
            sys.stdout.flush()
            first = False
            time.sleep(1.0 / args.fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h")
    # leave a settled frame behind
    if args.fetch:
        sys.stdout.write(block(frame(args.seconds * 0.9), term.columns))
    sys.stdout.write("\x1b[0m\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
