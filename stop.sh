#!/bin/bash

docker-compose -f telegraf.yml stop

# sh log.sh

docker-compose -f telegraf.yml down

docker-compose down
