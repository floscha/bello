import datetime
import os
import time

import requests
from slackclient import SlackClient


class SlackBot(object):
    """Chatbot to interact with the user through Slack."""

    def __init__(self):
        """Initialize a new SlackBot object."""
        # Take token from environment and initialize client.
        slack_token = os.environ['SLACK_API_TOKEN']
        self.slack = SlackClient(slack_token)
        self.bot_id = self._get_bot_id()

    def _get_bot_id(self, bot_name='bot'):
        api_call = self.slack.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == bot_name:
                    bot_id = user.get('id')
                    print("Bot ID for '%s' is %s." % (user['name'], bot_id))
                    return bot_id
        else:
            print("Could not find bot user with the name " + bot_name)

    def connect(self):
        """Connect to Slack and return True if successfull or False if not."""
        return self.slack.rtm_connect()

    def handle_command(self, command, channel):
        """Handle incoming text messages from the user."""
        text = ''
        attachments = None

        # Set URL to tasks for current date.
        current_date = datetime.date.today()
        calendar_date = current_date.isocalendar()
        url = 'http://trello:5000/tasks/' + '%d/%d/%d' % (calendar_date)

        try:
            split_command = command.split()
            if split_command[:2] == ['list', 'tasks']:
                response = requests.get(url).json()

                attachments = []
                for task in response:
                    new_attachment = {
                        'text': task['name'],
                        'color': '#2ecc71' if task['done'] else '#95a5a6',
                        'attachment_type': 'default'
                    }
                    attachments.append(new_attachment)

                if attachments:
                    text = 'Here are your tasks for today:'
                else:
                    text = 'No tasks for today :information_desk_person:'
            elif split_command[:2] == ['add', 'task']:
                task_name = ' '.join(split_command[2:])
                response = requests.post(url, json={'name': task_name})
                text = 'Task \'%s\' created.' % task_name
            elif split_command[:2] == ['delete', 'task']:
                task_name = ' '.join(split_command[2:])
                response = requests.delete(url, json={'name': task_name})
                text = 'Task \'%s\' deleted.' % task_name
            else:
                text = 'Sorry, I did not quite catch that :confused:'
        except Exception as e:
            print("Error while calling Bello:")
            print(e.value)
            return

        self.slack.api_call(
            "chat.postMessage",
            channel=channel,
            text=text,
            attachments=attachments,
            as_user=True
        )

    def _parse_slack_output(self, slack_rtm_output):
        """Parse a badge of new messages."""
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output:
                    # Avoid feedback loops triggered by bot messages.
                    if 'user' in output and output['user'] != self.bot_id:
                        return (output['text'].strip(),
                                output['channel'])
        return None, None

    def read_and_parse(self):
        """Read and parse new events from the Slack Real Time Messaging API."""
        return self._parse_slack_output(self.slack.rtm_read())


if __name__ == "__main__":
    # Set delay between checking messages from the firehose.
    READ_WEBSOCKET_DELAY = 0.2

    bot = SlackBot()

    if bot.connect():
        print("Slack Bot connected and running!")

        while True:
            command, channel = bot.read_and_parse()
            if command and channel:
                bot.handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
