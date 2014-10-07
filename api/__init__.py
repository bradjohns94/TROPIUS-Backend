#!/usr/bin/python

from flask import Flask

api = Flask(__name__)

api.add_api(devices.api)
api.add_api(hosts.api)
