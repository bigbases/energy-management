# Publication and Related Project
- Progject: [지능형(AI) 소규모 수도시설 통합관리시스템 개발", 행안부-과기부 협업 과학기술 활용 주민공감 현장문제 해결 사업, 2021.4 ~ 2022.6.](https://sites.google.com/view/seoultech-bigdata/projects)
- Publication: Jeonghwan Im, Jaekyu Lee, Somin Lee, and Hyuk-Yoon Kwon*, ["Data Pipeline for Real-Time Energy Consumption Data Management and Prediction,"](https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2024.1308236/full?utm_source=Email_to_authors_&utm_medium=Email&utm_content=T1_11.5e1_author&utm_campaign=Email_publication&field&journalName=Frontiers_in_Big_Data&id=1308236) Frontiers in Big Data, Vol. 7, pp. 1-8, Mar. 2024 (Impact Factor: 3.1) (Ack: KETEP-2021202090028D and 2019R1A6A1A03032119 ).

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
| InfluxDB     | 1.11   |
| ChronoGraf   | latest   |
| Grafana      | latest   |
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

connect-standalone /etc/kafka/connect-standalone.properties /etc/kafka/connect-file-source.properties