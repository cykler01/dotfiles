#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
DOTFILES_ROOT="$(realpath "$SCRIPT_DIR/../..")"

HYPR_TARGET="$HOME/.config/hypr"
CAELESTIA_TARGET="$HOME/.config/caelestia"

# Create target directories
mkdir -p "$HYPR_TARGET"
mkdir -p "$(dirname "$CAELESTIA_TARGET")"

rm -rf "$HYPR_TARGET"/*

# 2. Symlink subdirectories inside config/hypr (hyprland, scheme)
for dir in "$DOTFILES_ROOT/config/hypr/"*/; do
  dirname=$(basename "$dir")
  ln -sf "$dir" "$HYPR_TARGET/$dirname"
done

# 3. Symlink root-level files inside config/hypr (hyprland.lua, variables.lua)
for file in "$DOTFILES_ROOT/config/hypr/"*.lua; do
  [ -e "$file" ] && ln -sf "$file" "$HYPR_TARGET/"
done

# 4. Properly symlink the caelestia directory to ~/.config/caelestia
rm -rf "$CAELESTIA_TARGET"
ln -sf "$DOTFILES_ROOT/config/caelestia" "$CAELESTIA_TARGET"

# 5. Pear Desktop (YouTube Music) Caelestia theme
YM_TARGET="$HOME/.config/YouTube Music"
YM_THEME="$YM_TARGET/themes/caelestia.css"
mkdir -p "$YM_TARGET/themes"
ln -sf "$DOTFILES_ROOT/config/youtube-music/themes/caelestia.css" "$YM_THEME"

# Register the theme in the app config (Pear only loads CSS listed in options.themes)
python3 - "$YM_TARGET/config.json" "$YM_THEME" <<'PY'
import json, os, sys

config_path, theme_path = sys.argv[1], sys.argv[2]
data = {}
if os.path.exists(config_path):
    with open(config_path) as f:
        data = json.load(f)

themes = data.setdefault("options", {}).setdefault("themes", [])
if theme_path not in themes:
    themes.append(theme_path)
    with open(config_path, "w") as f:
        json.dump(data, f, indent="\t")
    print(f"Registered {theme_path} in {config_path}")
PY

echo "Hyprland, Caelestia and Pear Desktop configurations successfully installed!"
