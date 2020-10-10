#!/bin/sh

docker build . -t developeum:1.0
docker run --detach --name crawlers developeum:1.0