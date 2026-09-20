hl.config({
    input = {
        accel_profile = "flat",
        force_no_accel = true,
        sensitivity=2,
    },
})

hl.bind("SUPER + Return", hl.dsp.exec_cmd("kitty --directory ~"))
hl.bind("SUPER + CTRL + S", hl.dsp.exec_cmd("bash /home/cykler/.local/bin/ssh-menu.sh"))
hl.bind("SUPER + SPACE", hl.dsp.exec_cmd("bash /home/cykler/.local/bin/power-menu.sh"))
hl.bind("SUPER + T", hl.dsp.exec_cmd("bash /home/cykler/.local/bin/todo-list.sh"))

hl.dsp.exec_cmd("killall -e xdg-desktop-portal-hyprland")
hl.dsp.exec_cmd("killall -e xdg-desktop-portal-wlr")
hl.dsp.exec_cmd("killall -e xdg-desktop-portal-gtk")
hl.dsp.exec_cmd("killall -e xdg-desktop-portal")
hl.dsp.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
hl.dsp.exec_cmd("systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
hl.dsp.exec_cmd("/usr/lib/xdg-desktop-portal-hyprland &")
hl.dsp.exec_cmd("sleep 1")
hl.dsp.exec_cmd("/usr/lib/xdg-desktop-portal &")