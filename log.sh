#!/bin/bash
TS=$(date "+%s")

docker logs -f telegraf_con1 >& ./log/telegraf/$TS.log
# docker logs -f telegraf_con2 >& ./log/telegraf/2_$TS.log
# docker logs -f telegraf_con3 >& ./log/telegraf/3_$TS.log