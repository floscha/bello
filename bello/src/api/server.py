from flask import Flask
from flask_restful import Api

from api.resources.tasks import Tasks
from api.resources.weeks import Weeks


flask_server = app = Flask(__name__)
api = Api(app)

api.add_resource(Weeks, '/weeks/<int:year>/<int:week>')
api.add_resource(Tasks, '/tasks/<int:year>/<int:week>/<int:day>')