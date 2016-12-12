#!/bin/sh
#/Applications/mongodb/bin/mongod --dbpath /Applications/mongodb/data/db
#Localhost and network
/Applications/mongodb/bin/mongod --dbpath /Applications/mongodb/data/db --bind_ip 127.0.0.1,10.0.0.37 #<your ip>
#backup script
#/Applications/mongodb/bin/mongodump --archive=carsdbbackup --gzip --db cars-database