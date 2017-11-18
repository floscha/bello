import calendar
import os

from trello import TrelloClient


class TrelloFascade(object):
    """A simple fascade for communicating with the Trello API."""

    def __init__(self):
        """Initialize a new TrelloFascade instance."""
        self.trello = self._init_trello_client()

    def _init_trello_client(self):
        # Read API keys from env.
        api_key = os.environ['TRELLO_API_KEY']
        api_secret = os.environ['TRELLO_API_SECRET']
        token = os.environ['TRELLO_TOKEN']
        token_secret = os.environ['TRELLO_TOKEN_SECRET']

        trello_client = TrelloClient(
            api_key=api_key,
            api_secret=api_secret,
            token=token,
            token_secret=token_secret
        )

        return trello_client

    def _day_name_from_int(self, weekday_number):
        if weekday_number < 1 or weekday_number > 7:
            raise ValueError("Weekday number has to be >= 1 and <= 7")

        day_name = calendar.day_name[weekday_number - 1]
        return day_name

    def _find_boards_by_name(self, name):
        """Find all boards with the given name."""
        boards = self.trello.list_boards()
        res = [b for b in boards if b.name == name]
        return res

    def _find_board_by_name(self, name):
        """Find a single board with the given name."""
        candidates = self._find_boards_by_name(name)

        if len(candidates) == 0:
            raise Exception("No board '%s' found" % name)
        elif len(candidates) > 1:
            raise Exception("Multiple boards '%s' found" % name)
        else:  # Excactly one list found.
            return candidates[0]

    def _find_lists_by_name(self, board, name):
        """Find all lists with the given name."""
        lists = board.all_lists()
        res = [l for l in lists if l.name == name]
        return res

    def _find_list_by_name(self, board, name):
        """Find a single list with the given name."""
        candidates = self._find_lists_by_name(board, name)

        if len(candidates) == 0:
            raise Exception("No list '%s' in board '%s' found" % (name, board))
        elif len(candidates) > 1:
            raise Exception("Multiple lists '%s' in board '%s' found" %
                            (name, board))
        else:  # Excactly one list found.
            return candidates[0]

    def _find_cards_by_name(self, list_, name):
        """Find all cards with the given name."""
        cards = list_.list_cards()
        res = [c for c in cards if c.name == name]
        return res

    def _find_card_by_name(self, list_, name):
        """Find a single card with the given name."""
        candidates = self._find_cards_by_name(list_, name)

        if len(candidates) == 0:
            raise Exception("No card '%s' in list '%s' found" % (name, list_))
        elif len(candidates) > 1:
            raise Exception("Multiple cards '%s' in list '%s' found" %
                            (name, list_))
        else:  # Excactly one card found.
            return candidates[0]

    def _get_checklist(self, year, week, day):
        board_name = 'Bullet Journal %d' % year
        board = self._find_board_by_name(board_name)
        list_name = str(week)
        list_ = self._find_list_by_name(board, list_name)
        card_name = self._day_name_from_int(day)
        card = self._find_card_by_name(list_, card_name)

        # FIXME Necessary to retrieve checklists?!
        card.checklists
        # Assume a card has excactly one checklist.
        checklist = card.checklists[0]

        return checklist

    def get_tasks(self, year, week, day):
        """Get a list of tasks for the current day."""
        checklist = self._get_checklist(year, week, day)
        checklist_items = checklist.items

        tasks = [{'name': ci['name'],
                  'done': ci['checked']}
                 for ci in checklist_items]

        return tasks

    def add_task(self, year, week, day, name):
        """Create a new task."""
        checklist = self._get_checklist(year, week, day)
        checklist.add_checklist_item(name)

        created_checklist_item = checklist.items[-1]
        created_task = {'name': created_checklist_item['name'],
                        'done': created_checklist_item['checked']}

        return created_task

    def update_task(self, year, week, day, name, done):
        """Change an existing task."""
        checklist = self._get_checklist(year, week, day)

        checklist_item_index = checklist._get_item_index(name)
        if checklist_item_index:
            checklist.set_checklist_item(name, done)
        else:
            raise ValueError("Task with name '%s' does not exist" % name)

        updated_checklist_item = checklist.items[checklist_item_index]
        updated_task = {'name': updated_checklist_item['name'],
                        'done': updated_checklist_item['checked']}

        return updated_task

    def delete_task(self, year, week, day, name):
        """Delete an existing task."""
        checklist = self._get_checklist(year, week, day)

        checklist_item_index = checklist._get_item_index(name)
        if checklist_item_index:
            checklist_item_to_delete = checklist.items[checklist_item_index]
            checklist.delete_checklist_item(name)
        else:
            raise ValueError("Task with name '%s' does not exist" % name)

        deleted_task = {'name': checklist_item_to_delete['name'],
                        'done': checklist_item_to_delete['checked']}

        return deleted_task
