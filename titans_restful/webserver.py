from flask import Flask
from flask_restful import Api
from titans_restful import tasks


def start(debug=False):


    app = Flask(__name__)
    api = Api(app)

    api.add_resource(tasks.Upload, '/tasks/upload/')
    api.add_resource(tasks.Run, '/tasks/run/<name>')

    app.run(debug=debug, host='0.0.0.0', port=9527, threaded=True)
