#!/usr/bin/env sh
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - 'flaskr:create_app()'