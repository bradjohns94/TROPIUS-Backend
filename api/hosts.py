#!/usr/bin/python2

# The portion of the TROPIUS REST API that performs operations specific
# to hosts

import psycopg2

from flask import Flask, Blueprint
from flask import jsonify
from flask import request
from flask import abort

from time import sleep

# Add the TROPIUS directory strucutre to PYTHONPATH
import sys
sys.path.append('/home/brad/TROPIUS/')

from py_tropius import hosts
from py_tropius import netutil

host_api = Blueprint('host_api', __name__)

@host_api.route('/TROPIUS/hosts/list', methods=['GET'])
def list_hosts():
    """
        Return to the requesting hosts a json string containing
        the results of a SELECT * command on the hosts table
    """
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    return jsonify(hosts.get_all(cursor))


@host_api.route('/TROPIUS/hosts/add', methods=['POST'])
def add_host():
    """
        Return to the requesting ost a josn string containing the sid
        of the host that was just added to the database
    """
    # Attempt to recieve POST data
    name = None
    ip = None
    mac = None
    state = None
    if not request.json:
        abort(400)
    try:
        name = request.json.get('deviceName')
        ip = request.json.get('ip')
        mac = request.json.get('mac')
        state = request.json.get('state')
    except:
        abort(400)

    # Perform the transaction itself
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    ret = hosts.add(cursor, name, ip, mac, state)
    ret = {'sid': ret}
    tx.commit()
    return jsonify(ret)


@host_api.route('/TROPIUS/hosts/remove/<int:sid>', methods=['DELETE'])
def remove_host(sid):
    """ Delete the given host from the database """
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    try:
        hosts.delete(cursor, sid)
        tx.commit()
        return jsonify({'success': True})
    except:
        abort(400)


@host_api.route('/TROPIUS/hosts/get/', methods=['GET'])
def get_host():
    # TODO get the host data from the given information
    pass


@host_api.route('/TROPIUS/hosts/<int:sid>/power', methods=['PATCH'])
def set_power(sid):
    """ Toggle the power of the device using shutdown and wake on lan scripts """
    # Resolve the passed parameters if any
    timer = None
    os = None
    if request.json:
        if timer in request.json:
            timer = request.json.get('timer')
        if os in request.json:
            os = request.json.get('os')
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    state = hosts.get(cursor, sid)['state']
    
    if state == 'on':
        # The host is on -- turn it off
        # TODO make a unix shell util file
        # TODO make a windows util file
        return
    elif state == 'off':
        # The host is off -- turn it on
        if timer is not None:
            sleep(timer)
        netutil.wake_on_lan(cursor, sid)
        return jsonify({'success': True})
        # TODO find a keyboard driver and implement OS parameter


@host_api.route('/TROPIUS/hosts/<int:id>/reboot/<params>', methods=['PATCH'])
def reboot(params):
    # TODO make a unix shell util file
    # TODO make a windows util file
    pass
