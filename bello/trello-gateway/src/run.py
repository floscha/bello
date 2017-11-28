from flask import Flask
from flask_restful import Api

from resources.tasks import Tasks


app = Flask(__name__)
api = Api(app)

api.add_resource(Tasks, '/tasks/<int:year>/<int:week>/<int:day>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
