# cyklers dotfiles

This repository is mainly for personal use, but if you want to yoink things, go ahead.

---

## Installation scripts
Run these scripts from the `scripts/installation/` directory to set up your environment:
 - `appimages.sh` -> all appimages 
 - `pacman.sh` -> sysmtem uprade and installs all pacman packages 
 - `install-bash.sh` -> bash scripts (cpcpl, pscpl) 
 - `install-config.sh` -> binds hyprland and caelestia config 
 - `install-fetch.sh` -> installs the fastfetch/spacefetch fetch combo (see below) 
 - `lazyvim-install.sh` -> installs lazyvim for neovim 
 - `wallpapers.sh` -> installs all my wallpapers 
 - `full-install.sh` -> runs all of the install commands 

## Fetch
The terminal fetch setup, themed off the live Caelestia colour scheme (it re-tints itself whenever the wallpaper changes):

 - `config/fastfetch/` -> fastfetch rice: `config.template.jsonc` is rendered into `config.jsonc` by `render.py` using the wallpaper scheme, and `caelestia-fetch` runs an animated ASCII galaxy (`galaxy.py`) beside the infobox
 - `scripts/fetch/spacefetch/` -> spacefetch (patched fork of [DCaioP/spacefetch](https://github.com/DCaioP/spacefetch), GPL-3.0), wired to the scheme (black hole by default, `--mono` for greyscale) with an install wrapper at `scripts/fetch/spacefetch/spacefetch`
 - `config/caelestia/cli.json` -> caelestia theme post-hook that re-renders the fetch colours on wallpaper change
 - `config/fish/functions/fish_greeting.fish` -> terminal greeting: Caelestia ASCII logo + one static spacefetch frame

## Scripts
Tools and shortcuts included in this repository:
### Bash Tools:
 - `cpcpl` -> copy the contntents of a file or the output of a command to clipboard
 - `pscpl` -> paste the clipboard into a file

*god i really need to switch to nixos*

:wq