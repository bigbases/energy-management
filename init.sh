#!/bin/bash

echo 'jhim712' | sudo -S rm -Rf volume data

mkdir data
mkdir data/input
mkdir data/err
mkdir data/finished

mkdir volume
mkdir volume/kafka
mkdir volume/kafka/kafka1
mkdir volume/kafka/kafka1/data
mkdir volume/kafka/kafka2
mkdir volume/kafka/kafka2/data
mkdir volume/kafka/kafka3
mkdir volume/kafka/kafka3/data

echo 'jhim712' | sudo -S chmod 777 -Rf volume data

docker-compose up -d

sleep 10

docker exec -it kafka_water1 kafka-topics --bootstrap-server localhost:9092 --topic water_connect --partitions 3 --replication-factor 1 --create

sleep 5

docker-compose -f telegraf.yml up -d

sleep 5

TS=$(date "+%s")

docker exec -it kafka_water1 connect-standalone /etc/kafka/connect-standalone.properties /etc/kafka/connect-file-source.properties >> ./log/kafka/$TS.log