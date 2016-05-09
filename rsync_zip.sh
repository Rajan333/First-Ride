#/bin/bash

set -e

LOCATION="/root/First-Ride-master/"
echo " " > "$LOCATION"rsync_status.log
if [ ! -f "$LOCATION"request.lock ];then
	
    ENDPOINT=`curl -s http://devmeet.dev.pressplaytv.in/util/box-version/latest`
    STATUS=`echo $ENDPOINT | jq -r '.process_status'`
    ROW_ID=`echo $ENDPOINT | jq -r '.row_id'`


    if [ $STATUS == "success" ];then

        touch "$LOCATION"request.lock
        echo "Zip File created successfully" >> "$LOCATION"rsync_status.log
        mkdir -p "$LOCATION"zipfolder
        ZIP_LOCATION=`echo $ENDPOINT | jq -r '.zip_location'`
        ZIP_FILE=`echo $ZIP_LOCATION"complete_content.zip"`
        echo "zip file : " $ZIP_FILE >> "$LOCATION"rsync_status.log
        echo "rsync initiated" >> "$LOCATION"rsync_status.log
        rsync --progress -rave "ssh -i /root/First-Ride-master/devmeet" devmeet@54.255.151.235:$ZIP_FILE "$LOCATION"zipfolder >> "$LOCATION"status.lock
        echo "rsync completed" >> "$LOCATION"rsync_status.log
        rm -rf "$LOCATION"request.lock

	# CURL REQUEST TO CHECK STATUS
	curl -i http://devmeet.dev.pressplaytv.in/util/box-version/update?row_id=$ROW_ID
    else

        echo "mmll"

    fi
else
    echo "Waiting for zip to complete"
fi
