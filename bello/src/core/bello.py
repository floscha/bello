from trello_facade import TrelloFacade


class Bello(object):
    """CRUD endpoint for tasks."""

    def __init__(self):
        self.trello = TrelloFacade()

    def get_tasks(self, year, week, day):
        """Get all tasks."""
        response = self.trello.get_tasks(year, week, day)
        return response

    def add_task(self, year, week, day, new_task_name):
        """Create a new task."""
        response = self.trello.add_task(year, week, day,
                                        new_task_name)
        return response

    def update_task(self, year, week, day, new_task_name, new_task_done):
        """Change an existing task."""
        response = self.trello.update_task(year, week, day,
                                           new_task_name,
                                           new_task_done)
        return response

    def delete_task(self, year, week, day, task_name):
        """Delete an existing task."""
        response = self.trello.delete_task(year, week, day, task_name)
        return response
