# Docker Image with InfluxDB and Grafana

[![Docker Pulls](https://img.shields.io/docker/pulls/philhawthorne/docker-influxdb-grafana.svg)](https://dockerhub.com/philhawthorne/docker-influxdb-grafana) [![license](https://img.shields.io/github/license/philhawthorne/docker-influxdb-grafana.svg)](https://dockerhub.com/philhawthorne/docker-influxdb-grafana)

![Grafana][grafana-version] ![Influx][influx-version] ![Chronograf][chronograf-version]


This is a Docker image based on the awesome [Docker Image with Telegraf (StatsD), InfluxDB and Grafana](https://github.com/samuelebistoletti/docker-statsd-influxdb-grafana) from [Samuele Bistoletti](https://github.com/samuelebistoletti).

The main point of difference with this image is:

* Persistence is supported via mounting volumes to a Docker container
* Grafana will store its data in SQLite files instead of a MySQL table on the container, so MySQL is not installed
* Telegraf (StatsD) is not included in this container

The main purpose of this image is to be used to show data from a [Home Assistant](https://home-assistant.io) installation. For more information on how to do that, please see my website about how I use this container.

| Description  | Value   |
|--------------|---------|
| InfluxDB     | 1.8.2   |
| ChronoGraf   | 1.8.6   |
| Grafana      | 7.2.0   |
| Zookeeer     | 3.6.3 (confluent 7.2.1)|
| Kafka     | 3.2.0 (confluent 7.2.1)|
| Telegraf  | 1.19 |

## Quick Start

### docker-compose
docker-compose up -d

## Mapped Ports
### Ports of Kafka must be opened

``` sudo ufw allow 9092 & sudo ufw allow 9093 & sudo ufw allow 9094 ```

|Host	       |	Container	 |	Service   |
|------------|-------------|------------|
|3003	       | 3003		 	   | grafana    |
|3004        | 8083		     | chronograf |
|8086	       | 8086			   | influxdb   |
|2181 ~ 2183 | 2181 ~ 2183 | zookeeper  |
|9092 ~ 9094 | 9092 ~ 9094 | kafka  |

## Grafana

Open <http://localhost:3003>

```
Username: root
Password: root
```

## InfluxDB

### Web Interface (Chronograf)

Open <http://localhost:3004>

```
Username: root
Password: root
Port: 8086
```

### InfluxDB Shell (CLI)

1. Establish a ssh connection with the container
2. Launch `influx` to open InfluxDB Shell (CLI)

[grafana-version]: https://img.shields.io/badge/Grafana-7.2.0-brightgreen
[influx-version]: https://img.shields.io/badge/Influx-1.8.2-brightgreen
[chronograf-version]: https://img.shields.io/badge/Chronograf-1.8.6-brightgreen

