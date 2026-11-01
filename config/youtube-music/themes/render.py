#!/usr/bin/env python3
"""Render the Caelestia theme for Pear Desktop (YouTube Music).

Reads the live scheme at $XDG_STATE_HOME/caelestia/scheme.json (defaults to
~/.local/state/caelestia/scheme.json) and writes caelestia.css next to this
script. Pear only injects the CSS at window creation, so restart the app after
re-rendering.
"""

import json
import os
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
SCHEME = (
    pathlib.Path(os.environ.get("XDG_STATE_HOME", os.path.expanduser("~/.local/state")))
    / "caelestia"
    / "scheme.json"
)

TEMPLATE = """/* Caelestia theme for Pear Desktop (YouTube Music)
 * Generated from ~/.local/state/caelestia/scheme.json
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
  --cael-error: {error};
  --cael-success: {success};

  /* ---- surfaces ---- */
  --ytmusic-background: {surface} !important;
  --dark-theme-background-color: {surface} !important;
  --ytmusic-color-black1: {surfaceContainer} !important;
  --ytmusic-color-black2: {surface} !important;
  --ytmusic-color-black3: {surface} !important;
  --ytmusic-color-black4: {background} !important;
  --ytmusic-color-blackpure: {background} !important;
  --yt-spec-base-background: {surface} !important;
  --yt-spec-raised-background: {surfaceContainer} !important;
  --yt-spec-menu-background: {surfaceContainerHigh} !important;
  --yt-spec-general-background-a: {surfaceContainerLow} !important;
  --yt-spec-general-background-b: {surface} !important;
  --yt-spec-general-background-c: {background} !important;
  --yt-spec-brand-background-solid: {surface} !important;
  --yt-spec-brand-background-primary: {surface} !important;
  --yt-spec-static-overlay-background-solid: {surface} !important;
  --yt-spec-static-overlay-background-heavy: {surfaceContainerHigh}cc !important;
  --yt-spec-static-overlay-background-medium: {surfaceContainerHigh}99 !important;
  --yt-spec-static-overlay-background-light: {surfaceContainerHigh}4d !important;
  --yt-spec-black-1: {surfaceContainerHigh} !important;
  --yt-spec-black-2: {surfaceContainer} !important;
  --yt-spec-black-3: {surfaceContainerLow} !important;
  --yt-spec-black-4: {surface} !important;
  --yt-spec-black-pure: {background} !important;
  --ytmusic-search-background: {surfaceContainer} !important;
  --ytmusic-search-background-paper: {surfaceContainer} !important;
  --paper-dialog-background-color: {surfaceContainerHigh} !important;
  --paper-toast-background-color: {surfaceContainerHigh} !important;
  --ytmusic-menu-item-hover-background-color: {surfaceContainerHigh} !important;
  --ytmusic-setting-item-toggle-active: {primary} !important;
  --ytmusic-setting-item-toggle-inactive: {outlineVariant} !important;

  /* ---- text ---- */
  --ytmusic-text-primary: {onSurface} !important;
  --ytmusic-text-secondary: {onSurfaceVariant} !important;
  --yt-spec-text-primary: {onSurface} !important;
  --yt-spec-text-secondary: {onSurfaceVariant} !important;
  --yt-spec-text-disabled: {outline} !important;
  --yt-spec-text-primary-inverse: {surface} !important;
  --yt-spec-static-brand-white: {onSurface} !important;

  /* ---- accents / icons / controls ---- */
  --yt-spec-call-to-action: {primary} !important;
  --yt-spec-call-to-action-inverse: {primaryContainer} !important;
  --yt-spec-brand-icon-active: {primary} !important;
  --yt-spec-brand-icon-inactive: {onSurfaceVariant} !important;
  --yt-spec-icon-active-other: {onSurface} !important;
  --yt-spec-icon-inactive: {onSurfaceVariant} !important;
  --yt-spec-icon-disabled: {outline} !important;
  --yt-spec-brand-link-text: {primary} !important;
  --yt-spec-brand-button-background: {primary} !important;
  --yt-spec-brand-button-background-hover: {primaryContainer} !important;
  --yt-spec-filled-button-background: {primary} !important;
  --yt-spec-filled-button-text: {onPrimary} !important;
  --yt-spec-chip-background: {surfaceContainerHighest} !important;
  --yt-spec-badge-chip-background: {surfaceContainerHighest} !important;
  --yt-spec-button-chip-background-hover: {surfaceContainerHigh} !important;
  --yt-spec-inverted-background: {primary} !important;
  --yt-spec-static-brand-black: {surfaceContainerHigh} !important;
  --yt-spec-10-percent-layer: {outlineVariant}1a !important;
  --yt-spec-20-percent-layer: {outlineVariant}33 !important;
  --paper-progress-active-color-1: {primary} !important;
  --paper-progress-active-color-2: {secondary} !important;
  --paper-slider-knob-color: {primary} !important;
  --paper-slider-active-color: {primary} !important;
  --paper-slider-container-color: {surfaceContainerHighest} !important;
  --paper-toggle-button-checked-bar-color: {primary} !important;
  --paper-toggle-button-checked-button-color: {primary} !important;
  --yt-spec-overlay-background-medium: {surfaceContainerHigh}99 !important;
  --yt-spec-alert-error-background: {error} !important;
  --yt-spec-alert-success-background: {success} !important;
}}

/* ---- explicit containers ---- */
html,
body {{
  background-color: {surface} !important;
  color: {onSurface} !important;
}}

ytmusic-app,
ytmusic-app-layout,
#layout {{
  background-color: {surface} !important;
  color: {onSurface} !important;
}}

#nav-bar-background,
ytmusic-nav-bar {{
  background-color: {surfaceContainerHigh} !important;
  color: {onSurface} !important;
}}

#guide-wrapper,
#mini-guide-background {{
  background-color: {surfaceContainer} !important;
}}

#player-bar-background,
ytmusic-player-bar {{
  background-color: {surfaceContainer} !important;
  color: {onSurface} !important;
  border-top: 1px solid {surfaceContainerHighest} !important;
}}

#player-page,
ytmusic-player {{
  background-color: {surface} !important;
  color: {onSurface} !important;
}}

/* greyed metadata in the player bar and queue */
.duration.ytmusic-player-queue-item,
.byline.ytmusic-player-queue-item,
.time-info.ytmusic-player-bar,
.menu.ytmusic-player-bar,
.icon.ytmusic-menu-navigation-item-renderer {{
  color: {onSurfaceVariant} !important;
  --yt-endpoint-color: {onSurfaceVariant} !important;
  --yt-endpoint-hover-color: {primary} !important;
  --yt-endpoint-visited-color: {onSurfaceVariant} !important;
  --iron-icon-fill-color: {onSurfaceVariant} !important;
}}

/* playback progress + volume */
#progress-bar.ytmusic-player-bar {{
  --paper-slider-active-color: {primary} !important;
  --paper-slider-knob-color: {primary} !important;
  --paper-slider-container-color: {surfaceContainerHighest} !important;
  --paper-slider-secondary-color: {outlineVariant} !important;
}}

.volume-slider.ytmusic-player-bar,
.expand-volume-slider.ytmusic-player-bar {{
  --paper-slider-active-color: {primary} !important;
  --paper-slider-knob-color: {primary} !important;
  --paper-slider-container-color: {surfaceContainerHighest} !important;
}}

/* selection + scrollbars */
::selection {{
  background-color: {primaryContainer} !important;
  color: {onPrimaryContainer} !important;
}}

::-webkit-scrollbar-thumb {{
  background-color: {outlineVariant} !important;
  border-radius: 999px !important;
}}

::-webkit-scrollbar-thumb:hover {{
  background-color: {outline} !important;
}}

::-webkit-scrollbar {{
  width: 10px !important;
}}
"""


def main() -> None:
    scheme = json.loads(SCHEME.read_text())
    colours = {name: f"#{value}" for name, value in scheme["colours"].items()}
    out = HERE / "caelestia.css"
    out.write_text(
        TEMPLATE.format(
            name=scheme.get("name"),
            variant=scheme.get("variant"),
            mode=scheme.get("mode"),
            **colours,
        )
    )
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
