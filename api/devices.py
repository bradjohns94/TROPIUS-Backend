#!/usr/bin/python

# The portion of the TROPIUS REST API that incorporates all API references
# to generic device information

import psycopg2

from flask import Flask
from flask import jsonify
from flask import request
from flask import abort

# Add the TROPIUS directory structure to PYTHONPATH
import sys
sys.path.append('/home/brad/TROPIUS/')

from py_tropius import device

app = Flask(__name__)

@app.route('/TROPIUS/devices/list', methods=['GET'])
def list_devices():
    """
        Return to the requesting host a json string containing the results
        of a SELECT * command on the device table
    """
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    return jsonify(device.get_all(cursor))


@app.route('/TROPIUS/devices/add/', methods=['POST'])
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
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    ret = device.add(cursor, data['deviceName'], data['ip'], data['mac'])
    ret = {'sid': ret}
    return jsonify(ret)


@app.route('/TROPIUS/devices/remove/<int:sid>', methods=['DELETE'])
def remove_device(sid):
    """ Delete the given host from the database """
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    try:
        device.delete(cursor, sid)
        tx.commit()
        abort(200)
    except:
        abort(400)


@app.route('/TROPIUS/devices/get/', methods=['GET'])
def get_device():
    #TODO get the device from the given keys
    pass


if __name__ == '__main__':
    app.run(debug=True, host='192.168.8.200', port=8073)
