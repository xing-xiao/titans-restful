import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(os.path.abspath('.'), 'titans.cfg')))

flink_host = config['FLINK']['host']
flink_port = int(config['FLINK']['port'])

kafka_brokers = config['KAFKA']['brokers']