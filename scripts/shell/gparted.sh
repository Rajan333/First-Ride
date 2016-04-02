#!/bin/bash
# fast-create-sdcard.sh v0.1

export START_DIR=`pwd`
cat <<EOM

+------------------------------------------------------------------------------+
|                                                                              |
|             This script will create a bootable SD card.                      |
|             The script must be run with root permissions.                    |
|                                                                              |
+------------------------------------------------------------------------------+
EOM

#######################################
 AMIROOT=`whoami | awk {'print $1'}`
 if [ "$AMIROOT" != "root" ] ; then

   echo "  **** Error *** must run script with sudo"
   echo ""
   read -p 'Press ENTER to finish' FILEPATHOPTION
   exit
 fi

# show available SD card and select which to use
cat <<EOM

+------------------------------------------------------------------------------+
|                       List of available drives                               |
+------------------------------------------------------------------------------+
EOM

ROOTDRIVE=`mount | grep 'on / ' | awk {'print $1'} |  cut -c6-8`

GPARTED_DRIVE=`df -h | awk '{print $1}' | grep  "/dev" | grep -v $ROOTDRIVE | cut -c8 | head -1`

DEVICEDRIVENAME="sd"$GPARTED_DRIVE

echo $DEVICEDRIVENAME

DRIVE=/dev/$DEVICEDRIVENAME

echo "$DRIVE was selected"

#unmount drives if they are mounted
 unmounted1=`df | grep '\<'$DEVICEDRIVENAME'1\>' | awk '{print $1}'`
 unmounted2=`df | grep '\<'$DEVICEDRIVENAME'2\>' | awk '{print $1}'`
 unmounted3=`df | grep '\<'$DEVICEDRIVENAME'3\>' | awk '{print $1}'`

if [ -n "$unmounted1" ]; then
  sudo umount -f ${DRIVE}1
fi
if [ -n "$unmounted2" ]; then
  sudo umount -f ${DRIVE}2
fi
if [ -n "$unmounted3" ]; then
  sudo umount -f ${DRIVE}3
fi


cat <<EOM

+------------------------------------------------------------------------------+
|                           Now making partitions                              |
+------------------------------------------------------------------------------+
EOM

dd if=/dev/zero of=$DRIVE bs=1024 count=1
sync
parted --script $DRIVE -- mklabel msdos
parted --script $DRIVE -- mkpart primary fat32 4M 104M
parted --script $DRIVE -- mkpart primary ext2 104M 4200M
parted --script $DRIVE -- mkpart primary ext2 4200M 100%

mkfs.vfat -n "boot" ${DRIVE}1
mkfs.ext4 -L "root" ${DRIVE}2
mkfs.ext4 -L "content" ${DRIVE}3


echo "Operation Finished"
