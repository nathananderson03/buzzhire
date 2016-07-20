#!/bin/bash
#dbcreator.sh
psql -c "CREATE USER buzzhire WITH ENCRYPTED PASSWORD 'buzzhire'"
createdb -O buzzhire buzzhire
psql buzzhire -c 'CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;'
