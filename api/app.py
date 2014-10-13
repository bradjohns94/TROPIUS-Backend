#!/usr/bin/python2

from flask import Flask
from devices import device_api

app = Flask(__name__)
app.register_blueprint(device_api)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.8.200', port=8073)
