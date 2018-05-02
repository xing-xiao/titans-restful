from flask import Flask
from flask import Flask
from flask.ext.restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(APITaskUpload, '/tasks/upload/')
api.add_resource(APITaskRun, '/tasks/run/<name>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9527, threaded=True)
