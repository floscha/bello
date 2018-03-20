import client.server.app as server


if __name__ == '__main__':
    server.flask_server.run(host='0.0.0.0', debug=True)
