from flask import request
from flask_restful import Resource

from trello_facade import TrelloFacade


class Weeks(Resource):
    """CR(U)D endpoint for weeks."""

    def __init__(self):
        self.trello = TrelloFacade()

    def get(self, year, week):
        """Get a single week."""
        try:
            response = self.trello.get_week(year, week)
        except Exception as e:
            response = "Week not found.", 404
            print(e)

        return response

    def post(self, year, week):
        """Create a new week."""
        json_data = request.get_json()
        new_week_name = json_data['name']

        response = self.trello.add_week(year, week,
                                        new_week_name)

        return response

    def delete(self, year, week):
        """Delete an existing week."""
        json_data = request.get_json()
        new_week_name = json_data['name']

        response = self.trello.delete_week(year, week, new_week_name)

        return response
