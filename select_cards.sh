#/bin/bash

set -e

SELECTEDCARDS=$*


for card in ${SELECTEDCARDS[@]}
do
	DRIVE=`echo $card | cut -c 8`
	echo $DRIVE
	echo "Starting Gpart"
	sleep 5
	echo " "
	bash /root/First-Ride-master/scripts/shell/gparted.sh $DRIVE
done
