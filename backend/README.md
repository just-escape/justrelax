Create log directory, chown, chmod

sudo apt-get install gcc python3-dev libffi-dev libssl-dev libasound2-dev
python setup.py develop

Postgresql:
apt install libpq-dev

How to resize an sd card ?

https://superuser.com/questions/610819/how-to-resize-img-file-created-with-dd

```
sudo losetup -f
sudo losetup /dev/loop6 myimage.img
sudo partprobe /dev/loop6
sudo gparted /dev/loop6
sudo losetup -d /dev/loop6
fdisk -l myimage.img

Disk myimage.img: 6144 MB, 6144000000 bytes, 12000000 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x000ea37d

      Device Boot      Start         End      Blocks   Id  System
myimage.img1            2048     9181183     4589568    b  W95 FAT32

truncate --size=$[(9181183+1)*512] myimage.img
```
