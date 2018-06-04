from flask import Flask
from flask_restful import Api
from titans_restful import tasks
from titans_restful import intelligence
from titans_restful import rules
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


def start(debug=False):
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(tasks.Upload, '/tasks/upload/')
    api.add_resource(tasks.Run, '/tasks/run/<name>')
    api.add_resource(intelligence.Update, '/intelligence/update/')
    api.add_resource(rules.FaUpload, '/rule/fa/upload/')

    if debug:
        app.run(debug=debug, host='0.0.0.0', port=9527, threaded=True)
    else:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(9527)
        IOLoop.instance().start()
