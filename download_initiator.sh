#!/bin/bash

set -e

VERSION_ID=$1
ZIP_LOCATION=$2

# Write json
    python scripts/python/getVersionDump.py $VERSION_ID > json/output.json 2>&1

# Convert the json to box format
    python scripts/python/jsonparser.py json/output.json json/new_box.json others/file_$VERSION_ID.csv appurl.txt
exit

# Download apks

    mkdir -p apps
    echo "Downloading apps..." >> progress.log
    echo " "
    for app in `cat appurl.txt`
    do 
        wget -O apps/$app >> progress.log
    done

# Download content from aws

    echo "Downloading content from aws..." >> progress.log
    mkdir -p aws_content

    for content in `cat others/file_$VERSION_ID.csv`
    do
        RAW_CONTENT=`echo $content | tr ',' ' ' | awk '{print $1}'`
        CONTENT_ID=`echo $content | tr ',' ' ' | awk '{print $2}'`
        echo "downloading $RAW_CONTENT as $CONTENT_ID"
        aws s3 cp s3://pp-brightcove-source/$RAW_CONTENT aws_content/$CONTENT_ID >> progress.log
#        touch aws_content/$CONTENT_ID
    done
    
    echo " "

    echo "Creating complete_content.zip..." >> progress.log
    echo " "
# Create zip file for content
    zip -r $ZIP_LOCATION/complete_content contentitems channelitems sponsoritems aws_content json/new_box.json

    echo " "
    echo "Removing extra content..." >> progress.log
    echo " "
    rm -rf contentitems channelitems sponsoritems aws_content

    echo "zip created suucessfully...!!!" >> progress.log
