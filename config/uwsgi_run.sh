#!/bin/bash
trap "{pkill -9 uwsgi; exit 0;}" SIGHUP SIGINT SIGTERM
sleep 10
cd /home/webmaster/neuraldating/ && ./bin/start_uwsgi
