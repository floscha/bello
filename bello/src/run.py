import sys

from client import cli
import client.server.app as server


if __name__ == '__main__':
    args = sys.argv[1:]
    mode = args[0]

    if mode == 'server':
        # Run web server.
        server.flask_server.run(host='0.0.0.0', debug=True)
    else:
        # Run standalone CLI.
        cli.run()
