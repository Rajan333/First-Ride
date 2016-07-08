#!/bin/bash

set -e

ROOTDRIVE=`mount | grep 'on / ' | awk {'print $1'} |  cut -c6-8`
#LISTCARDS=`df -h | awk '{print $1}' | grep  "/dev" | grep -v $ROOTDRIVE | cut -c1-8 | sort | uniq`

SHOWCARDS=`sudo fdisk -l | grep "Disk" | grep "/dev/" |  awk '{print $2,$3,$4}' | grep -v $ROOTDRIVE | tr -d ' ,' | sort | uniq`
#LISTCARDS=`sudo fdisk -l | grep "Disk" | grep "/dev/" |  awk '{print $2}' | grep -v $ROOTDRIVE | tr -d ' ,' | sort | uniq`

echo $SHOWCARDS
#echo $LISTCARDS 


