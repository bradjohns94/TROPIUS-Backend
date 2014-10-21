#!/usr/bin/python2

# The portion of the TROPIUS REST API used to initially test the connection
# Ping requests don't work for every ISP, so a rest request is a more reliable
# way to check if the connection is successful.

from flask import Flask, Blueprint
from flask import jsonify
from flask import request
from flask import abort

conn_api = Blueprint('conn_api', __name__)

@conn_api.route('/TROPIUS/connection/test', methods=['GET'])
def test_connection():
    """ Respond that the connection was successful """
    res = {'test': {'ip': request.environ['REMOTE_ADDR']}}
    return jsonify(res)
