#!/bin/bash

set -e

ENDPOINT="pp-content-dev-db.cthkpx3mbvub.ap-southeast-1.rds.amazonaws.com" 
USER="groot"
DB="content"
export PGPASSWORD=homeironmanlogslumberSweeppy

if [ ! -f version.lock ]; then
    LATEST_VERSION=`psql -h $ENDPOINT -U $USER $DB -t -c "select id from version_store where environment = 'box' order by id desc limit 1"`
    echo $LATEST_VERSION
    OLD_VERSION=$LATEST_VERSION
    touch version.lock
else
    LATEST_VERSION=`psql -h $ENDPOINT -U $USER $DB -t -c "select id from version_store where environment = 'box' order by id desc limit 1"`
    rm -rf version.lock

