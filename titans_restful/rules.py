import os
import yaml
import requests
import datetime
from flask_restful import reqparse, abort, Resource
from flask import request, jsonify
from titans_restful.configs import mysql_host, mysql_port, mysql_user, mysql_password, mysql_db_tsap
import pymysql

class FaUpload(Resource):
    def put(self):
        file = request.files['file']
        if not file.filename.endswith('yml'):
            return jsonify({'failed': 'only yml file accepted'})
        try:
            data = file.read()
            yml = yaml.load(data)
        except Exception as e:
            return jsonify({'failed': 'only yml file accepted'})
        if 'name' not in yml or 'condition' not in yml or 'combination' not in yml or 'action' not in yml:
            return jsonify({'failed': 'format error!'})

        try:
            client = pymysql.connect(host=mysql_host,
                                     port=mysql_port,
                                     user=mysql_user,
                                     password=mysql_password,
                                     database=mysql_db_tsap,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
            try:
                cursor = client.cursor()
                sqlinsert = '''INSERT INTO rule_fa(`name`, `rule`, `date`) VALUES('%s', '%s', '%s')''' % \
                                    (data['name'], data, datetime.datetime.now().isoformat)
                cursor.execute(sqlinsert)
                client.commit()
            except Exception as e:
                client.rollback()
            client.close()
        except Exception as e:
            return jsonify({'failed': str(e)})
        return jsonify({'success': 'rule <%s> upload success' % yml['name']})