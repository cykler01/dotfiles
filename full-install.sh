#!/usr/bin/env bash
set -euo pipefail

# Get the absolute path of the directory where full-install.sh lives
DOTFILES_ROOT="$(cd "$(dirname "$(realpath "$0")")" && pwd)"

echo "Starting system setup..."

"$DOTFILES_ROOT/scripts/installation/pacman.sh"
"$DOTFILES_ROOT/scripts/installation/appimages.sh"
"$DOTFILES_ROOT/scripts/installation/lazyvim-install.sh"
"$DOTFILES_ROOT/scripts/installation/install-bash.sh"
"$DOTFILES_ROOT/scripts/installation/install-fetch.sh"
"$DOTFILES_ROOT/scripts/installation/install-config.sh"
"$DOTFILES_ROOT/scripts/installation/wallpapers.sh"

echo "Bootstrap complete!"
