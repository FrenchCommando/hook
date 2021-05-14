#!/bin/sh

docker build -t hookbuild .
docker run --rm -p 1340:1340 -v /home/pi:/home/pi hookbuild
