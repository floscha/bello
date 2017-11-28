from flask import request
from flask_restful import Resource

from trello_fascade import TrelloFascade


class Tasks(Resource):
    """CRUD endpoint for tasks."""

    def __init__(self):
        self.trello = TrelloFascade()

    def get(self, year, week, day):
        """Get all tasks."""
        response = self.trello.get_tasks(year, week, day)

        return response

    def post(self, year, week, day):
        """Create a new task."""
        json_data = request.get_json()
        new_task_name = json_data['name']

        response = self.trello.add_task(year, week, day,
                                        new_task_name)

        return response

    def put(self, year, week, day):
        """Change an existing task."""
        json_data = request.get_json()
        new_task_name = json_data['name']
        new_task_done = json_data['done']

        response = self.trello.update_task(year, week, day,
                                           new_task_name,
                                           new_task_done)

        return response

    def delete(self, year, week, day):
        """Delete an existing task."""
        json_data = request.get_json()
        new_task_name = json_data['name']

        response = self.trello.delete_task(year, week, day, new_task_name)

        return response
