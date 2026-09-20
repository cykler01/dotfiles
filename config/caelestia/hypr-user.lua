hl.config({
    input = {
        accel_profile = "flat",
        force_no_accel = true,
        sensitivity=2,
    },
})

monitors = {
	{ name = "DP-1", resolution = "1280x1024@60", position = "0x0", scale = "1" },
	{ name = "DP-2", resolution = "1920x1080@144", position = "1280x0", scale = "1" },
	{ name = "HDMI-A-1", resolution = "1920x1080@75", position = "3200x0", scale = "1" },
}

hl.bind("SUPER + Return", hl.dsp.exec_cmd("kitty --directory ~"))
hl.bind("SUPER + CTRL + S", hl.dsp.exec_cmd("bash /home/cykler/.local/bin/ssh-menu.sh"))
hl.bind("SUPER + SPACE", hl.dsp.exec_cmd("bash /home/cykler/.local/bin/power-menu.sh"))
hl.bind("SUPER + T", hl.dsp.exec_cmd("bash /home/cykler/.local/bin/todo-list.sh"))

-- (Set the same combo in Discord Settings -> Keybinds -> Toggle Mute.)
hl.bind("CTRL + SHIFT + M", hl.dsp.send_shortcut({ mods = "CTRL,SHIFT", key = "M", window = "class:^(vesktop)$" }))

hl.dsp.exec_cmd("killall -e xdg-desktop-portal-hyprland")
hl.dsp.exec_cmd("killall -e xdg-desktop-portal-wlr")
hl.dsp.exec_cmd("killall -e xdg-desktop-portal-gtk")
hl.dsp.exec_cmd("killall -e xdg-desktop-portal")
hl.dsp.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
hl.dsp.exec_cmd("systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
hl.dsp.exec_cmd("/usr/lib/xdg-desktop-portal-hyprland &")
hl.dsp.exec_cmd("sleep 1")
hl.dsp.exec_cmd("/usr/lib/xdg-desktop-portal &")
