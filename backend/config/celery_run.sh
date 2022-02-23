#!/bin/bash
trap "{ echo Stopping celery; ps xa| grep python3 | grep celery | grep worker | grep -v grep | awk '{print $1}' | xargs kill ; exit 0; }" SIGHUP SIGINT SIGTERM
cd /home/webmaster/neuraldating/ && ./bin/start_celery
