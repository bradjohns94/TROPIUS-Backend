#!/usr/bin/python2

# The portion of the TROPIUS REST API that incorporates all API references
# to generic device information
import sqlite3

from flask import Flask, Blueprint
from flask import jsonify
from flask import request
from flask import abort

# Add the TROPIUS directory structure to PYTHONPATH
import sys
sys.path.append('/home/tropius/TROPIUS/')

from py_tropius import device

device_api = Blueprint('device_api', __name__)

@device_api.route('/TROPIUS/devices/list', methods=['GET'])
def list_devices():
    """
        Return to the requesting host a json string containing the results
        of a SELECT * command on the device table
    """
    db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
    ret = device.get_all(db)
    ret = {'list': ret}
    return jsonify(ret)


@device_api.route('/TROPIUS/devices/add/', methods=['POST'])
def add_device():
    """
        Return to the requesting host a json string containing the sid
        of device that was just added to the database
    """
    # Attempt to recieve the POST data
    name = None
    ip = None
    mac = None
    if not request.json:
        abort(400)
    try:
        name = request.json.get('deviceName')
        ip = request.json.get('ip')
        mac = request.json.get('mac')
    except:
        abort(400)

    # Perform the transaction itself
    db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
    ret = device.add(db, data['deviceName'], data['ip'], data['mac'])
    ret = {'add': {'sid': ret}}
    return jsonify(ret)


@device_api.route('/TROPIUS/devices/remove/<int:sid>', methods=['DELETE'])
def remove_device(sid):
    """ Delete the given host from the database """
    db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
    try:
        device.delete(db, sid)
        db.commit()
        return jsonify({'delete': {'success': True}})
    except:
        abort(400)


@device_api.route('/TROPIUS/devices/get/', methods=['GET'])
def get_device():
    #TODO get the device from the given keys
    pass
