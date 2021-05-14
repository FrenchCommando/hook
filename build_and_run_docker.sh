#!/bin/sh

docker build -t hookbuild .
docker run -d --rm -p 1340:1340 hookbuild
