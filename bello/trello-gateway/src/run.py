from flask import Flask
from flask_restful import Api

from resources.tasks import Tasks
from resources.tasks import Weeks


app = Flask(__name__)
api = Api(app)

api.add_resource(Weeks, '/weeks/<int:year>/<int:week>')
api.add_resource(Tasks, '/tasks/<int:year>/<int:week>/<int:day>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
