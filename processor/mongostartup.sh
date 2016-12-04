#!/bin/sh
/Applications/mongodb/bin/mongod --dbpath /Applications/mongodb/data/db
#backup script
#/Applications/mongodb/bin/mongodump --archive=carsdbbackup --gzip --db cars-database