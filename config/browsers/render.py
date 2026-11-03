#!/usr/bin/env python3
"""Render Caelestia colours into Firefox and Zen browser profiles.

The caelestia dotfiles deliver browser colours with the CaelestiaFox
extension plus a native messaging host in /usr/lib/caelestia. That needs a
root-owned native host and a signed XPI, so instead this writes a small
generated `caelestia.css` colour layer into each profile's chrome/ dir and
imports it from userChrome.css. Layout tweaks stay in userChrome.css.

Reads ~/.local/state/caelestia/scheme.json and is safe to re-run.
"""

import json
import os
import pathlib
import re

HOME = pathlib.Path.home()
SCHEME = pathlib.Path(os.environ.get("XDG_STATE_HOME", HOME / ".local/state")) / "caelestia" / "scheme.json"

MARKER = "/* caelestia: generated colour layer, do not edit here */"
IMPORT_LINE = '@import url("caelestia.css");'
HERE = pathlib.Path(__file__).resolve().parent
FIREFOX_LAYOUT = HERE / "firefox-layout.css"
LAYOUT_NAME = "caelestia-layout.css"
LAYOUT_IMPORT = f'@import url("{LAYOUT_NAME}");'

PROFILE_ROOTS = [
    HOME / ".config/zen",  # zen-browser
    HOME / ".mozilla/firefox",  # firefox
]

TEMPLATE = """/* Caelestia palette for Zen/Firefox - generated, do not edit.
 * Regenerate with: python3 ~/.config/browsers/render.py
 * scheme: {name} / {variant} / {mode}
 */

:root {{
  --cael-surface: {surface};
  --cael-surface-low: {surfaceContainerLow};
  --cael-surface-container: {surfaceContainer};
  --cael-surface-high: {surfaceContainerHigh};
  --cael-surface-highest: {surfaceContainerHighest};
  --cael-on-surface: {onSurface};
  --cael-on-surface-variant: {onSurfaceVariant};
  --cael-outline: {outline};
  --cael-outline-variant: {outlineVariant};
  --cael-primary: {primary};
  --cael-on-primary: {onPrimary};
  --cael-primary-container: {primaryContainer};
  --cael-secondary: {secondary};
  --cael-tertiary: {tertiary};

  /* --- toolbar / tab strip --- */
  --lwt-accent-color: {surface} !important;
  --lwt-text-color: {onSurface} !important;
  --toolbar-bgcolor: {surfaceContainer} !important;
  --toolbar-color: {onSurface} !important;
  --toolbarbutton-icon-fill: {primary} !important;
  --toolbarbutton-icon-fill-attention: {primary} !important;
  --toolbarbutton-icon-fill-attention-text-light: {onSurface} !important;
  --toolbarbutton-icon-fill-attention-text-dark: {surface} !important;
  --tab-selected-bgcolor: {surfaceContainerHigh} !important;
  --tab-loading-fill: {primary} !important;
  --tabpanel-background-color: {surface} !important;
  --zen-themed-toolbar-bg: {surface} !important;
  --zen-main-browser-background: {surface} !important;
  --zen-colors-primary: {primary} !important;
  --zen-colors-secondary: {surfaceContainer} !important;
  --zen-colors-tertiary: {surface} !important;
  --zen-colors-border: {outlineVariant} !important;
  --zen-primary-color: {primary} !important;

  /* --- url bar / panels / popups --- */
  --toolbar-field-background-color: {surfaceContainerHigh} !important;
  --toolbar-field-color: {onSurface} !important;
  --toolbar-field-focus-background-color: {surfaceContainerHighest} !important;
  --toolbar-field-focus-color: {onSurface} !important;
  --toolbar-field-border-color: {outlineVariant} !important;
  --toolbar-field-focus-border-color: {primary} !important;
  --arrowpanel-background: {surfaceContainer} !important;
  --arrowpanel-color: {onSurface} !important;
  --arrowpanel-border-color: {surfaceContainerHighest} !important;
  --urlbarView-highlight-background: {primaryContainer} !important;
  --urlbarView-highlight-color: {onSurface} !important;
  --urlbarView-separator-color: {outlineVariant} !important;
  --autocomplete-popup-background: {surfaceContainer} !important;
  --autocomplete-popup-color: {onSurface} !important;
  --autocomplete-popup-highlight-background: {primaryContainer} !important;
  --autocomplete-popup-highlight-color: {onSurface} !important;

  /* --- sidebar / new tab / misc --- */
  --lwt-sidebar-background-color: {surface} !important;
  --lwt-sidebar-text-color: {onSurface} !important;
  --newtab-background-color: {surface} !important;
  --newtab-text-primary-color: {onSurface} !important;
  --in-content-page-background: {surface} !important;
  --in-content-page-color: {onSurface} !important;
  --in-content-primary-button-background: {primaryContainer} !important;
  --in-content-primary-button-text-color: {onSurface} !important;
  --focus-outline-color: {primary} !important;
  --link-color: {primary} !important;
  --button-background-color-hover: {surfaceContainerHigh} !important;
  --button-background-color-active: {surfaceContainerHighest} !important;
}}

/* --- element-level fixes for parts that ignore the variables above --- */
#navigator-toolbox,
#TabsToolbar,
#nav-bar,
#PersonalToolbar {{
  background-color: {surface} !important;
  color: {onSurface} !important;
  border-color: {surfaceContainerHighest} !important;
}}

#urlbar-background,
#searchbar {{
  background-color: {surfaceContainerHigh} !important;
  border: 1px solid {outlineVariant} !important;
  border-radius: 10px !important;
}}

#urlbar[focused] > #urlbar-background {{
  border-color: {primary} !important;
}}

.tabbrowser-tab[selected] .tab-background {{
  background-color: {surfaceContainerHigh} !important;
}}

.tabbrowser-tab .tab-label {{
  color: {onSurface} !important;
}}

.tabbrowser-tab:not([selected]) .tab-label {{
  color: {onSurfaceVariant} !important;
}}

menupopup,
panel {{
  --panel-background: {surfaceContainer} !important;
  --panel-color: {onSurface} !important;
  --panel-border-color: {surfaceContainerHighest} !important;
}}

.sidebar-panel,
#sidebar-box,
#sidebar-header {{
  background-color: {surface} !important;
  color: {onSurface} !important;
}}

/* scrollbars */
* {{
  scrollbar-color: {outlineVariant} {surface} !important;
}}
"""


def find_profiles() -> list[pathlib.Path]:
    profiles = []
    for root in PROFILE_ROOTS:
        if not root.is_dir():
            continue
        for candidate in root.iterdir():
            # a real profile always has prefs.js; skip cache/group dirs
            if candidate.is_dir() and (candidate / "prefs.js").is_file():
                profiles.append(candidate)
    return profiles


def ensure_pref(profile: pathlib.Path) -> str:
    """Ensure userChrome.css is enabled, via user.js (survives Firefox rewriting prefs.js)."""
    prefs = profile / "prefs.js"
    if prefs.is_file() and re.search(
        r'user_pref\("toolkit\.legacyUserProfileCustomizations\.stylesheets",\s*true\)', prefs.read_text()
    ):
        return "pref already on"

    user_js = profile / "user.js"
    line = 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);'
    if user_js.is_file():
        text = user_js.read_text()
        if "toolkit.legacyUserProfileCustomizations.stylesheets" in text:
            return "pref set in user.js"
        user_js.write_text(text.rstrip() + "\n" + line + "\n")
    else:
        user_js.write_text("// Required for userChrome.css to be loaded.\n" + line + "\n")
    return "added pref to user.js"


def install_import(profile: pathlib.Path) -> str:
    """Make userChrome.css pull in the generated colour layer, without eating existing tweaks."""
    user_chrome = profile / "chrome" / "userChrome.css"
    if not user_chrome.is_file():
        user_chrome.write_text(f"{MARKER}\n{IMPORT_LINE}\n")
        return "created userChrome.css with import"

    text = user_chrome.read_text()
    if IMPORT_LINE in text:
        return "import already present"

    backup = user_chrome.with_suffix(".css.pre-caelestia.bak")
    if not backup.exists():
        backup.write_text(text)
    user_chrome.write_text(f"{MARKER}\n{IMPORT_LINE}\n\n{text}")
    return f"prepended import (backup: {backup.name})"


def append_import(profile: pathlib.Path, line: str) -> str:
    """Add an extra import without touching the existing tweaks or making a backup."""
    user_chrome = profile / "chrome" / "userChrome.css"
    text = user_chrome.read_text()
    if line in text:
        return "layout import already present"
    user_chrome.write_text(f"{MARKER}\n{line}\n\n{text}")
    return "layout import added"


def main() -> None:
    scheme = json.loads(SCHEME.read_text())
    colours = {name: f"#{value}" for name, value in scheme["colours"].items()}
    css = TEMPLATE.format(
        name=scheme.get("name"), variant=scheme.get("variant"), mode=scheme.get("mode"), **colours
    )

    # Brave (Chromium) cannot be userChrome-themed. Its only supported hook is a
    # policy file under /etc, which needs root, so render it here for the user to install.
    brave_policy = HOME / ".config/browsers/brave-policy.json"
    brave_policy.parent.mkdir(parents=True, exist_ok=True)
    brave_policy.write_text(
        json.dumps({"BrowserThemeColor": colours["surface"], "BrowserColorScheme": "device"}, indent=2)
        + "\n"
    )
    print(f"brave policy written to {brave_policy}")

    profiles = find_profiles()
    if not profiles:
        print("no Firefox/Zen profiles found")
        return

    for profile in profiles:
        chrome = profile / "chrome"
        chrome.mkdir(parents=True, exist_ok=True)
        (chrome / "caelestia.css").write_text(css)
        print(f"{profile.name}:")
        print(f"  chrome/caelestia.css written")
        print(f"  userChrome.css: {install_import(profile)}")
        if "firefox" in str(profile) and FIREFOX_LAYOUT.is_file():
            (chrome / LAYOUT_NAME).write_text(FIREFOX_LAYOUT.read_text())
            print(f"  chrome/{LAYOUT_NAME} written")
            print(f"  userChrome.css: {append_import(profile, LAYOUT_IMPORT)}")
        print(f"  stylesheet pref: {ensure_pref(profile)}")


if __name__ == "__main__":
    main()
