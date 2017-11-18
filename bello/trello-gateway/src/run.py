from flask import Flask, request
from flask_restful import Resource, Api

from trello_fascade import TrelloFascade


app = Flask(__name__)
api = Api(app)

trello = TrelloFascade()


class Tasks(Resource):
    """CRUD endpoint for tasks."""

    def get(self, year, week, day):
        """Get all tasks."""
        response = trello.get_tasks(year, week, day)

        return response

    def post(self, year, week, day):
        """Create a new task."""
        json_data = request.get_json()
        new_task_name = json_data['name']

        response = trello.add_task(year, week, day,
                                   new_task_name)

        return response

    def put(self, year, week, day):
        """Change an existing task."""
        json_data = request.get_json()
        new_task_name = json_data['name']
        new_task_done = json_data['done']

        response = trello.update_task(year, week, day,
                                      new_task_name,
                                      new_task_done)

        return response

    def delete(self, year, week, day):
        """Delete an existing task."""
        json_data = request.get_json()
        new_task_name = json_data['name']

        response = trello.delete_task(year, week, day, new_task_name)

        return response


api.add_resource(Tasks, '/tasks/<int:year>/<int:week>/<int:day>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
