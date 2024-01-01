Create log directory, chown, chmod

sudo apt-get install gcc python3-dev libffi-dev libssl-dev libasound2-dev
python setup.py develop

Postgresql:
apt install libpq-dev

How resize a sd card before the copy ?

```
sudo umount /dev/sda1
sudo umount /dev/sda2
sudo gparted /dev/sda  # resize the partition to the minimum
sudo fdisk -l /dev/sda

Disk /dev/sda: 29.81 GiB, 32010928128 bytes, 62521344 sectors
Disk model: Storage Device  
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xf420fa12

Device     Boot  Start      End  Sectors  Size Id Type
/dev/sda1         8192   532479   524288  256M  c W95 FAT32 (LBA)
/dev/sda2       532480 19748863 19216384  9.2G 83 Linux

sudo dd if=/dev/sda of=d1_node.img bs=512 count=$[19748863+1] conv=fsync status=progress
```

How to resize a sd card after the copy ?

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
