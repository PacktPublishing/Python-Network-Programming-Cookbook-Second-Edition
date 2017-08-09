#!/bin/bash
##############################################################################
# Python Network Programming Cookbook, Second Edition -- Chapter - 13
##############################################################################


# Start Zookeeper. To view the logs real time, in a terminal: "tail -f zk-server.out".

nohup kafka_2.11-0.11.0.0/bin/zookeeper-server-start.sh kafka_2.11-0.11.0.0/config/zookeeper.properties > zk-server.out &


# Start Kafka-Server. To view the logs real time, in a terminal: "tail -f kafka-server.out".
nohup kafka_2.11-0.11.0.0/bin/kafka-server-start.sh kafka_2.11-0.11.0.0/config/server.properties > kafka-server.out &
