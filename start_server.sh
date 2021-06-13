#!/bin/sh

uwsgi --http :5050 --gevent 10 --http-websockets --master --wsgi-file src/app.py --callable app &
nginx -g "daemon off;"
