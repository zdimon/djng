#!/bin/bash
trap "{cat /home/webmaster/cybeready/backend/backend/celerybeat.pid | xargs kill ; rm /home/webmaster/djng/backend/backend/celerybeat.pid; exit 0; }" SIGHUP SIGINT SIGTERM
sleep 5
cd /home/webmaster/djng/ && ./bin/start_beat
