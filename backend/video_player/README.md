Update configuration in raspi-config / /boot/config.txt :
  - Enable 4k so that 2 videos can be played at the same time
  - Configure gpu_mem=256
  - hdmi_force_hotplug=1

/etc/lightdm/lightdm.conf
xserver-command=X -s 0 -dpms -nocursor

```
pi@d1advertiser ~/justrelax % cat /boot/config.txt|grep -v "#"


disable_overscan=1



hdmi_force_hotplug=1









dtparam=audio=on

[pi4]
dtoverlay=vc4-fkms-v3d
max_framebuffers=2

[all]
gpu_mem=256
initramfs initrd.img-4.19.118-v7l+-overlay
```
