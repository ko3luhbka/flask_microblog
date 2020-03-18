#!/usr/bin/env sh

# Wait till MySQL contaner is ready
timeout=60
waited=0
wait_step=5

while [ $waited -lt $timeout ]; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        echo Connected to database in $waited seconds
        break
    fi
    echo Failed to upgrade database, retrying in $wait_step seconds...
    waited=$((waited + $wait_step))
    sleep $wait_step
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - 'flaskr:create_app()'