#!/bin/bash

set -e

VERSION_ID=$1

# Write json
python scripts/getVersionDump.py $VERSION_ID > json/output.json 2>&1

# Convert the json to box format
python scripts/jsonparser.py json/output.json json/new_box.json others/file.csv



