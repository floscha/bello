from trello_facade import TrelloFacade


trello = TrelloFacade()


def run():
    while True:
        try:
            input_ = input()
            year, week = input_.split('/')
            try:
                week = trello.get_week(year, week)
            except Exception as e:
                print("Week not found:\n%s" % e)
            finally:
                print(week)
        except KeyboardInterrupt:
            print("CLI exited")
