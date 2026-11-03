#!/usr/bin/env python3
"""Render the Caelestia palette into an Obsidian CSS snippet.

Obsidian themes are per-vault CSS, so this writes a `caelestia` snippet into
every vault's .obsidian/snippets/ and enables it in appearance.json. Values
come from ~/.local/state/caelestia/scheme.json, so it follows the wallpaper.
Safe to re-run.
"""

import colorsys
import json
import os
import pathlib

HOME = pathlib.Path.home()
SCHEME = pathlib.Path(os.environ.get("XDG_STATE_HOME", HOME / ".local/state")) / "caelestia" / "scheme.json"
OBSIDIAN_JSON = HOME / ".config/obsidian/obsidian.json"
SNIPPET_NAME = "caelestia"

TEMPLATE = """/* Caelestia palette for Obsidian - generated, do not edit.
 * Regenerate with: python3 ~/.config/obsidian/render.py
 * scheme: {name} / {variant} / {mode}
 */

body {{
  --accent-h: {accent_h};
  --accent-s: {accent_s};
  --accent-l: {accent_l};

  /* surfaces */
  --background-primary: {surface};
  --background-primary-alt: {surfaceContainerLow};
  --background-secondary: {surfaceContainer};
  --background-secondary-alt: {surfaceContainerHigh};
  --background-modifier-border: {outlineVariant};
  --background-modifier-border-hover: {outline};
  --background-modifier-border-focus: {primary};
  --background-modifier-hover: {surfaceContainerHigh};
  --background-modifier-active-hover: {surfaceContainerHighest};
  --background-modifier-message: {surfaceContainerHigh};
  --divider-color: {outlineVariant};
  --code-background: {surfaceContainerLow};
  --code-normal: {onSurface};

  /* text */
  --text-normal: {onSurface};
  --text-muted: {onSurfaceVariant};
  --text-faint: {outline};
  --text-accent: {primary};
  --text-accent-hover: {secondary};
  --text-on-accent: {onPrimary};
  --text-error: {error};
  --text-success: {success};
  --text-selection: {primary}4d;
  --text-highlight-bg: {primary}40;

  /* interactive */
  --interactive-accent: {primary};
  --interactive-accent-hover: {primaryContainer};
  --interactive-normal: {surfaceContainerHigh};
  --interactive-hover: {surfaceContainerHighest};
  --checkbox-color: {primary};
  --checkbox-color-hover: {primaryContainer};
  --slider-thumb-border-color: {surface};
  --toggle-thumb-color: {surface};

  /* links, tags, quotes */
  --link-color: {primary};
  --link-color-hover: {secondary};
  --link-external-color: {secondary};
  --link-unresolved-color: {outline};
  --tag-background: {surfaceContainerHigh};
  --tag-background-hover: {surfaceContainerHighest};
  --tag-color: {primary};
  --tag-color-hover: {onSurface};
  --blockquote-border-color: {primary};
  --blockquote-color: {onSurfaceVariant};

  /* scrollbars */
  --scrollbar-thumb-bg: {outlineVariant};
  --scrollbar-active-thumb-bg: {outline};
  --scrollbar-bg: transparent;

  /* graph */
  --graph-line: {surfaceContainerHighest};
  --graph-node: {onSurface};
  --graph-node-unresolved: {outline};
  --graph-node-focused: {primary};
  --graph-node-tag: {secondary};
  --graph-node-attachment: {tertiary};
}}
"""


def find_vaults() -> list[pathlib.Path]:
    if not OBSIDIAN_JSON.is_file():
        return []
    try:
        data = json.loads(OBSIDIAN_JSON.read_text())
    except json.JSONDecodeError:
        return []
    vaults = []
    for info in data.get("vaults", {}).values():
        path = info.get("path")
        if path and (pathlib.Path(path) / ".obsidian").is_dir():
            vaults.append(pathlib.Path(path))
    return vaults


def enable_snippet(vault: pathlib.Path) -> str:
    appearance = vault / ".obsidian" / "appearance.json"
    if appearance.is_file():
        try:
            data = json.loads(appearance.read_text())
        except json.JSONDecodeError:
            return "appearance.json unreadable - enable the snippet by hand"
    else:
        data = {}

    snippets = data.setdefault("enabledCssSnippets", [])
    if SNIPPET_NAME in snippets:
        return "already enabled"
    snippets.append(SNIPPET_NAME)
    appearance.write_text(json.dumps(data, indent=2) + "\n")
    return "enabled in appearance.json"


def accent_hsl(hex_colour: str) -> tuple[int, int, int]:
    value = hex_colour.lstrip("#")
    r, g, b = (int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return round(h * 360), round(s * 100), round(l * 100)


def main() -> None:
    scheme = json.loads(SCHEME.read_text())
    colours = {name: f"#{value}" for name, value in scheme["colours"].items()}
    h, s, l = accent_hsl(colours["primary"])

    css = TEMPLATE.format(
        name=scheme.get("name"),
        variant=scheme.get("variant"),
        mode=scheme.get("mode"),
        accent_h=h,
        accent_s=f"{s}%",
        accent_l=f"{l}%",
        **colours,
    )

    vaults = find_vaults()
    if not vaults:
        print("no obsidian vaults found")
        return

    for vault in vaults:
        snippets = vault / ".obsidian" / "snippets"
        snippets.mkdir(parents=True, exist_ok=True)
        (snippets / f"{SNIPPET_NAME}.css").write_text(css)
        print(f"{vault.name}:")
        print(f"  snippets/{SNIPPET_NAME}.css written")
        print(f"  {enable_snippet(vault)}")


if __name__ == "__main__":
    main()
