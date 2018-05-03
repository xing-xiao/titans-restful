import os
import yaml
import requests
import json
from flask_restful import reqparse, abort, Resource
from flask import jsonify
from flask import request

abspath = os.path.abspath('.')
jar_dir = os.path.abspath(os.path.join(abspath, '..', '..', 'jars'))
rule_dir = os.path.abspath(os.path.join(abspath, '..', '..', 'rules'))


def get_jar_id():
    cep_jarid = None
    with open(os.path.join(jar_dir, "jar.id")) as f:
        for line in f:
            rsp = json.loads(line)
            if 'TsapCEPEngine' in rsp['filename']:
                cep_jarid = rsp['filename']
    return cep_jarid


cep_jarid = get_jar_id()


class APITasks(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, help='Rate to charge for this resource')

    def get(self, name):
        args = self.parser.parse_args()
        print("test:", args.type)
        if args.type == "":
            print("true")
        return {'hello': 'world'}

    def delete(self, name):
        print(name)
        return '', 204

    def put(self, name):
        args = self.parser.parse_args()
        if args.type == "lucene":
            pass
        elif args.type == "esdsl":
            rtn = request.get_json(force=True)
            print(rtn)
        elif args.type == "yaml":
            pass
        elif args.type == "json" or args.type is None:
            rtn = request.get_json(force=True)
            print("json")
        else:
            return '', 405
        return '', 201

    def post(self, name):
        return '', 201


class APITaskUpload(Resource):
    def put(self):
        file = request.files['file']
        if not file.filename.endswith('yml'):
            return jsonify({'failed': 'only yml file accepted'})
        try:
            data = file.read()
            yml = yaml.load(data)
        except Exception as e:
            return jsonify({'failed': 'only yml file accepted'})
        if 'title' not in yml:
            return jsonify({'failed': 'title needed'})
        newf = os.path.join(rule_dir, yml['title'] + '.yml')
        if os.path.isfile(newf):
            return jsonify({'failed': 'rule <%s> exists' % yml['title']})
        with open(newf, 'wb')as f:
            f.write(data)
        return jsonify({'success': 'rule <%s> upload success' % yml['title']})


class APITaskRun(Resource):
    def post(self, name):
        if not os.path.isfile(os.path.join(rule_dir, name + '.yml')):
            return jsonify({'failed': 'rule <%s> dose not exists' % name})
        url = "http://jobmanager:8081/jars/%s/run?" \
              "allowNonRestoredState=false" \
              "&entry-class=" \
              "&parallelism=" \
              "&program-args=--kafka.brokers+kafka:9092+--kafka.input.topics+tsap+--kafka.output.topics+alarm+--rule.path+%s" \
              "&savepointPath=" % (cep_jarid, os.path.join(rule_dir, name)+'.yml')
        data = {}
        requests.post(url=url, data=data)
        return jsonify({'success': 'rule <%s> started' % name})
