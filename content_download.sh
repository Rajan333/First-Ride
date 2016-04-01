#!/bin/bash

set -e

VERSION_ID=$1

# Write json
python scripts/python/getVersionDump.py $VERSION_ID > json/output.json 2>&1

# Convert the json to box format
python scripts/python/jsonparser.py json/output.json json/new_box.json others/file.csv



