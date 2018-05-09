import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(os.path.abspath('.'), 'titans.cfg')))

flink_host = config['FLINK']['host']
flink_port = int(config['FLINK']['port'])

kafka_brokers = config['KAFKA']['brokers']

mysql_host = config['MYSQL']['host']
mysql_port = int(config['MYSQL']['port'])
mysql_user = config['MYSQL']['user']
mysql_password = config['MYSQL']['password']
mysql_db_intelligence = config['MYSQL']['db_intelligence']
