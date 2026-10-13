#!/bin/bash
# Update system first
sudo pacman -Syu --noconfirm

# Install packages
sudo pacman -S --noconfirm \
  hyprland kitty fish neovim git ufw \
  ttf-jetbrains-mono-nerd tesseract-data-eng \
  vlc obs-studio zen-browser-bin brave-bin \
  vesktop telegram-desktop steam \
  btop tree npm paru yay fuse2 obsidian \
  vim openssh nautilus heroic-games-launcher-bin \
  gnome-calendar gnome-keyring gnome-text-editor \
  firefox foot ffmpeg kdenlive pear-desktop \
  fastfetch python

paru -S visual-studio-code-bin --noconfirm
