#!/bin/bash

set -e

DEF_PATH="/root/First-Ride-master"
mkdir -p /mnt/boot /mnt/root /mnt/content 

SELECTCARD=$*

for card in ${SELECTCARD[@]}
do
	 DRIVE="/dev/sd"$card
	 BOOTDRIVE=$DRIVE"1"
	 ROOTDRIVE=$DRIVE"2"
	 CONTENTDRIVE=$DRIVE"3"
	 echo $BOOTDRIVE $ROOTDRIVE $CONTENTDRIVE

	# Mount card
	echo "Mounting Drives..." >> "$DEF_PATH"/status.log
	mount $BOOTDRIVE /mnt/boot
	mount $ROOTDRIVE /mnt/root
	mount $CONTENTDRIVE /mnt/content
	
	echo "Drives Mounted" >> "$DEF_PATH"/status.log

	mkdir -p /mnt/content/content /mnt/content/posters /mnt/content/json
	
	# Copy Boot & Root
	echo "Cloning boot..." >> "$DEF_PATH"/status.log
	cp -afv "$DEF_PATH"/temp_boot/* /mnt/boot/
	echo "Boot Cloned" >> "$DEF_PATH"/status.log
	echo "Cloning Root..." >> "$DEF_PATH"/status.log
	cp -afv '$DEF_PATH'/temp_root/* /mnt/root/
	rm -rf /mnt/root/home/pi/*
	echo "Root Cloned" >> '$DEF_PATH'/status.log

	# Run Builder
	echo " Aunty is Running builder..." >> '$DEF_PATH'/status.log
	# get builder zip
	mkdir -p '$DEF_PATH'/aunty
	wget -O '$DEF_PATH'/aunty/builder.zip "http://scoop.arsenal.testing.pressplaytv.in/data/builder_source"

	if [ -d '$DEF_PATH'/builder_source ]; then
		rm -rf '$DEF_PATH'/builder_source/*
	else
		mkdir -p '$DEF_PATH'/builder_source/
	fi

	echo " " > builder.log

	rm -rf "$DEF_PATH"/builder_source "$DEF_PATH"/aunty  
	unzip '$DEF_PATH'/aunty/builder.zip -d '$DEF_PATH'/builder_source/

	sudo python '$DEF_PATH'/builder_source/build.py --box --software-version "0.9.9(xerox)" --build-location /mnt/root/ >> builder.log 
	
	# build.py
	#wget -O ./build.py "https://raw.githubusercontent.com/ShradhaTaneja/Builder/software_update_revamp/scripts/source/build.py?token=AOYs9KYyYIceotBG2GDdIKICoVlzURo3ks5XGOAiwA%3D%3D"
	# builder.json
	#wget -O ./builder.json "https://raw.githubusercontent.com/ShradhaTaneja/Builder/software_update_revamp/scripts/source/builder.json?token=AOYs9DTKl7Gy7S7viyNsixhgqniGibvlks5XGOFKwA%3D%3D"
	# Run builder
	#python build.py --box --software-release scoop.arsenal.testing.pressplaytv.in/data/software_release --software-version 0.9.9TEST --build-location /mnt/root/ >> builder.log
	echo "Builder done successfully" >> '$DEF_PATH'/status.log

	# Unzip content
	echo "Content Unzip Process started..." >> '$DEF_PATH'/status.log
	unzip '$DEF_PATH'/zipfolder/complete_content.zip -d '$DEF_PATH'
	echo "Content Unzipped Successfully" >> '$DEF_PATH'/status.log	

	# Copy content from system to card
	echo "Cloning content..." >> '$DEF_PATH'/status.log
	cp -afv '$DEF_PATH'/downloadfiles/*.png /mnt/content/posters/ 2>&1
	cp -afv '$DEF_PATH'/downloadfiles/*.mp4 /mnt/root/home/pi/Beam/static/free-content/ 2>&1
	cp -afv '$DEF_PATH'/aws_content/* /mnt/content/content/ 2>&1
	cp -afv '$DEF_PATH'/json/new_box.json /mnt/content/json/ 2>&1
	cp -afv '$DEF_PATH'/apps/* /mnt/root/home/pi/resources/apps/ANDROID/ 2>&1

	echo "Cloning completed successfully" >> '$DEF_PATH'/status.log
	
	echo "Unmounting Drives..." >> '$DEF_PATH'/status.log
	umount $BOOTDRIVE 
	umount $ROOTDRIVE 
	umount $CONTENTDRIVE
	echo "Drives Unmounted successfully" >> '$DEF_PATH'/status.log

	echo "Base Card is Ready">> '$DEF_PATH'/status.log
 		  
done


