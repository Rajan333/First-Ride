#!/bin/bash

set -e

ROOTDISK=`mount | grep 'on / ' | awk '{print $1}' |  cut -c6-8`

DRIVE_NAME=`df -h | awk '{print $1}' | grep  "/dev" | grep -v $ROOTDISK | cut -c8 | head -1`

BOOT_DRIVE="/dev/sd"$DRIVE_NAME"1"
ROOT_DRIVE="/dev/sd"$DRIVE_NAME"2"
CONTENT_DRIVE="/dev/sd"$DRIVE_NAME"3"

echo $BOOT_DRIVE $ROOT_DRIVE $CONTENT_DRIVE
exit
# Make Directories if not exist
mkdir -p /mnt/boot /mnt/root /mnt/content

# Mount Drives to Directory
mount $BOOT_DRIVE /mnt/boot
rm -rf /mnt/boot/*

mount $ROOT_DRIVE /mnt/root
rm -rf /mnt/root/*

mount $CONTENT_DRIVE /mnt/content
rm -rf content/*

echo "Cloning Boot..."
rsync --progress -avz boot_drive/* /mnt/boot/ 2>&1

echo "Cloning Root..."
rsync --progress -avz root_drive/* /mnt/root/ 2>&1

echo "Cloning Content..."
rsync --progress -avz content_drive/* /mnt/content/ 2>&1

echo "Unmounting Card..."
umount /mnt/* 
echo "Card Unmounted"

echo "Card Cloned..."

