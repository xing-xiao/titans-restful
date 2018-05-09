from flask_restful import reqparse, abort, Resource
from flask import request, jsonify
from titans_restful.configs import mysql_host, mysql_port, mysql_user, mysql_password, mysql_db_intelligence
import pymysql


class Update(Resource):
    def put(self):
        file = request.files['file']
        count = 0
        try:
            data = file.readlines()
            client = pymysql.connect(host=mysql_host,
                                     port=mysql_port,
                                     user=mysql_user,
                                     password=mysql_password,
                                     database=mysql_db_intelligence,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
            for i in data:
                try:
                    sqlfind = '''SELECT  *  FROM  intelligence WHERE data='%s' ''' % (i)
                    client.cursor().execute(sqlfind)
                    rst = client.cursor().fetchone()
                    if rst is None:
                        # j = [x.strip() for x in i.split(',', 2)]
                        count += 1
                        sqlinsert = '''INSERT INTO intelligence(data, type, ioc) VALUES(%s)''' % i
                        client.cursor().execute(sqlinsert)
                        client.commit()
                except Exception as e:
                    client.rollback()
            client.close()
        except Exception as e:
            return jsonify({'failed': str(e)})
        return jsonify({'success': 'db upload success, %d items inserted' % count})
