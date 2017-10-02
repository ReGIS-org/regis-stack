#!/bin/sh

# TODO: Make user able to set the task and job db's here, or use the config.ini
. env/bin/activate
while ! curl -s http://backend:5984/
do
  echo "Waiting for task db..."
  sleep 1
done
# while ! curl -s http://jobdb:5984/
# do
#   echo "Waiting for job db..."
#   sleep 1
# done
TIME=`date`
echo "$TIME - connected successfully"
sed -i "s/COUCHDB_USER_PLACEHOLDER/$COUCHDB_USER/g" config.ini
sed -i "s/COUCHDB_PASSWORD_PLACEHOLDER/$COUCHDB_PASSWORD/g" config.ini

# TODO: Make user and password settable through environment variable?
simcity init -u $COUCHDB_USER -p $COUCHDB_PASSWORD &&
  python -m bottle scripts.app --bind 0.0.0.0:9090 -s gevent
