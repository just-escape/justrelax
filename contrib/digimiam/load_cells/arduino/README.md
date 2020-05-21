sudo apt install arduino-mk

udevadm info -a -n /dev/ttyACM0 |grep '{idVendor}' |head -n1  # XXXX
udevadm info -a -n /dev/ttyACM0 |grep '{idProduct}' |head -n1  # YYYY
udevadm info -a -n /dev/ttyACM0 |grep '{serial}' |head -n1  # ZZZZ

vim /etc/udev/rules.d/99-usb-serial.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="XXXX", ATTRS{idProduct}=="YYYY", ATTRS{serial}=="ZZZZ", SYMLINK+="arduino"

// Unplug, plug

make upload

Optional:
sudo apt install screen

make upload monitor
