import calendar
from datetime import datetime
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

    def _create_clean_board(self, name):
        created_board = self.trello.add_board(name)

        # Clean up lists Trello creates by default.
        for l in created_board.all_lists():
            l.close()

        return created_board

    def _find_boards_by_name(self, name):
        """Find all boards with the given name."""
        boards = self.trello.list_boards()
        res = [b for b in boards if b.name == name]
        return res

    def _find_board_by_name(self, name, create=False):
        """Find a single board with the given name."""
        candidates = self._find_boards_by_name(name)

        if len(candidates) == 0:
            if create:
                created_board = self._create_clean_board(name)
                return created_board
            else:
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

    def _create_list_for_week(self, board, list_name):
        """Create a Trello list for a week and all its days."""
        created_list = board.add_list(list_name)

        # Create first card for general stuff.
        created_card = created_list.add_card('General')
        for day in calendar.day_name:
            created_card = created_list.add_card(day)
            created_card.add_checklist(title='Tasks', items=[])

    def _find_list_by_name(self, board, name, create=False):
        """Find a single list with the given name."""
        candidates = self._find_lists_by_name(board, name)

        if len(candidates) == 0:
            if create:
                created_list = self._create_list_for_week(board, name)
                return created_list
            else:
                raise Exception("No list '%s' in board '%s' found"
                                % (name, board))
        elif len(candidates) > 1:
            raise Exception("Multiple lists '%s' in board '%s' found"
                            % (name, board))
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
            raise Exception("Multiple cards '%s' in list '%s' found"
                            % (name, list_))
        else:  # Excactly one card found.
            return candidates[0]

    def _get_week_list_string(self, year, week, day):
        year_and_week = '%d-%d' % (year, week)
        week_start_date = datetime.strptime(year_and_week + '-1', '%Y-%W-%u')
        week_start_date_string = datetime.strftime(
            week_start_date,
            '%d. %b'
        )
        week_end_date = datetime.strptime(year_and_week + '-7', '%Y-%W-%u')
        week_end_date_string = datetime.strftime(
            week_end_date,
            '%d. %b'
        )
        list_name = 'Week %d (%s - %s)' % (week,
                                           week_start_date_string,
                                           week_end_date_string)
        return list_name

    def _get_checklist(self, year, week, day):
        board_name = 'Bullet Journal %d' % year
        board = self._find_board_by_name(board_name, create=True)

        list_name = self._get_week_list_string(year, week, day)
        list_ = self._find_list_by_name(board, list_name, create=True)

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
