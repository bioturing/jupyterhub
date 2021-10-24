#!/bin/bash

docker run  -d -e API_HOSTNAME="http://192.168.10.145:9999" \
    -p 9999:8000 nb-album
