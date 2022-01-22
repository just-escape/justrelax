No login screen at boot:

/etc/lightdm/lightdm.conf
```
[Seat:*]
autologin-user=jbb  # No login prompt
xserver-command=X -s 0 -dpms -nocursor  # No sleep mode, no cursor
```

Run chrome in kiosk mode:
```
chromium --kiosk --app=<url> --window-position=0,0 --noerrdialogs --user-data-dir=/path/to/directory --password-store=basic --autoplay-policy=no-user-gesture-required --disable-features=TranslateUI --disable-pinch  --check-for-update-interval=315360000
```
--noerrordialors for popups ("translate this page")
--user-data-dir for separate instances (sound)
--password-store=basic to prevent error messages due to this autologin-user=jbb
--autoplay-policy=no-user-gesture-required to allow html videos 'play' property to work all the time
--disable-features=TranslateUI (or just Translate) to prevent "Translate this page?" popup
--disable-pinch to prevent the pinch-to-zoom feature

Cinnamon startup application conf file:
~/.config/autostart/<name>.desktop
```
[Desktop Entry]
Type=Application
Exec=<command>
X-GNOME-Autostart-enabled=true
NoDisplay=false
Hidden=false
Name[en_US]=<name>
Comment[en_US]=No description
X-GNOME-Autostart-Delay=0
```

Small monitors:
```
https://www.waveshare.com/wiki/Main_Page
```

# Use a deterministic audio source for d1tower
pactl set-default-sink alsa_output.pci-0000_0c_00.4.analog-stereo
