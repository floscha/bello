import sys

from client import cli
from client.server import app as server


if __name__ == '__main__':
    args = sys.argv[1:]
    mode = args[0]

    if mode == 'server':
        # Run web server.
        server.run(host='0.0.0.0', debug=True)
    else:
        # Run standalone CLI.
        cli.run()
