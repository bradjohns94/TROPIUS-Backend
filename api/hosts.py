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
sys.path.append('/home/tropius/TROPIUS/')

from py_tropius import hosts
from py_tropius import netutil
from py_tropius import music

host_api = Blueprint('host_api', __name__)

@host_api.route('/TROPIUS/hosts/list', methods=['GET'])
def list_hosts():
    """
        Return to the requesting hosts a json string containing
        the results of a SELECT * command on the hosts table
    """
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    res = hosts.get_all(cursor)
    res = {'list': res}
    return jsonify(res)


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
    ret = {'add': ret}
    return jsonify(ret)


@host_api.route('/TROPIUS/hosts/remove/<int:sid>', methods=['DELETE'])
def remove_host(sid):
    """ Delete the given host from the database """
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    try:
        hosts.delete(cursor, sid)
        tx.commit()
        ret = {'remove': {'success': True}}
        return jsonify(ret)
    except:
        abort(400)


@host_api.route('/TROPIUS/hosts/<int:sid>/get', methods=['GET'])
def get_host(sid):
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    ret = hosts.get_detail(cursor, sid)
    ret = {'get': ret}
    return jsonify(ret)


@host_api.route('/TROPIUS/hosts/<int:sid>/power', methods=['POST'])
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
        ret = {'power': {'state': 'on'}}
        return jsonify(ret)
        # TODO find a keyboard driver and implement OS parameter


@host_api.route('/TROPIUS/hosts/<int:id>/reboot/<params>', methods=['POST'])
def reboot(params):
    # TODO make a unix shell util file
    # TODO make a windows util file
    pass


@host_api.route('/TROPIUS/hosts/<int:sid>/music/play', methods=['POST'])
def play_music(sid):
    """ Gather music request data from the json parameters and play the song """
    # Get the parameters for the get_song_id request
    artist = None
    album = None
    title = None
    if not request.json:
        abort(400)
    try:
        title = request.json.get('title')
        if request.json.has_key('album'):
            album = request.json.get('album')
        if request.json.has_key('artist'):
            artist = request.json.get('artist')
    except:
        abort(400)
    # Get the host data from the database
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    host = hosts.get_detail(cursor, sid)
    # TODO make this more customizable/secure
    library = music.get_library(host['ip'], '8080', '', 'vlcremote')
    # Get the song id if possible and play the song if successful
    try:
        song = music.get_song_id(library, title, artist, album)
        music.play_song(host['ip'], '8080', '', 'vlcremote', song_id=song)
        abort(200)
    except:
        abort(400)
