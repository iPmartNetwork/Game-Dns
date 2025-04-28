#!/bin/bash

apt update && apt install docker docker-compose unzip -y

docker-compose build
docker-compose up -d
