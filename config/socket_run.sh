#!/bin/bash
trap "{ echo Stopping socket; ps xa| grep socket_server | grep -v grep | awk '{print $1}' | xargs kill -9; exit 0; }" SIGHUP SIGINT SIGTERM
sleep 5
cd /home/webmaster/neuraldating/ && ./bin/start_socket
