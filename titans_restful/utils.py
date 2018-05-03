import requests
import json


def get_jar_ids(flink_host, flink_port):
    jarids = {'cep': None, 'ti': None}
    rsp = requests.get('http://%s:%d/jars/' % (flink_host, flink_port))
    for jar in json.loads(rsp.text)['files']:
        if jar['name'] == 'TsapCepEngine.jar':
            jarids['cep'] = jar['id']
    return jarids
