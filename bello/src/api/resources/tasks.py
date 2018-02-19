from flask import request
from flask_restful import Resource

from core import Bello


class Tasks(Resource):
    """CRUD endpoint for tasks."""

    def __init__(self):
        self.bello = Bello()

    def get(self, year, week, day):
        """Get all tasks."""
        response = self.bello.get_tasks(year, week, day)

        return response

    def post(self, year, week, day):
        """Create a new task."""
        json_data = request.get_json()
        new_task_name = json_data['name']

        response = self.bello.add_task(year, week, day,
                                       new_task_name)

        return response

    def put(self, year, week, day):
        """Change an existing task."""
        json_data = request.get_json()
        new_task_name = json_data['name']
        new_task_done = json_data['done']

        response = self.bello.update_task(year, week, day,
                                          new_task_name,
                                          new_task_done)

        return response

    def delete(self, year, week, day):
        """Delete an existing task."""
        json_data = request.get_json()
        task_name = json_data['name']

        response = self.bello.delete_task(year, week, day,
                                          task_name)

        return response
