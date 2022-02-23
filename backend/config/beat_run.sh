#!/bin/bash
trap "{cat /home/webmaster/neuraldating/backend/backend/celerybeat.pid | xargs kill ; rm /home/webmaster/neuraldating/backend/backend/celerybeat.pid; exit 0; }" SIGHUP SIGINT SIGTERM
sleep 5
cd /home/webmaster/neuraldating/ && ./bin/start_beat
