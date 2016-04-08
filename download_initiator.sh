#!/bin/bash

set -e

VERSION_ID=$1

# Write json
    python scripts/python/getVersionDump.py $VERSION_ID > json/output.json 2>&1

# Convert the json to box format
    python scripts/python/jsonparser.py json/output.json json/new_box.json others/file_$VERSION_ID.csv appurl.txt

# Download apks
    mkdir -p apps
    echo "Downloading apps..."
    echo " "
    for app in `cat appurl.txt`
    do 
        wget -O apps/$app
    done

# Download content from aws
    mkdir -p aws_content

    for content in `cat others/file_$VERSION_ID.csv`
    do
        RAW_CONTENT=`echo $content | tr ',' ' ' | awk '{print $1}'`
        CONTENT_ID=`echo $content | tr ',' ' ' | awk '{print $2}'`
        echo "downloading $RAW_CONTENT as $CONTENT_ID"
#       aws s3 cp s3://pp-brightcove-source/$RAW_CONTENT aws_content/$CONTENT_ID
        touch aws_content/$CONTENT_ID
    done
    
    echo " "

    echo "Creating complete_content.zip..."
    echo " "
# Create zip file for content
    zip -r complete_content contentitems channelitems sponsoritems aws_content json/new_box.json

    echo " "
    echo "Removing extra content..."
    echo " "
    rm -rf contentitems channelitems sponsoritems aws_content

    echo "zip created suucessfully...!!!"
