#!/usr/bin/python2

# The portion of the TROPIUS REST API that performs operations specific
# to hosts
import sqlite3

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
from py_tropius import spotify

host_api = Blueprint('host_api', __name__)

@host_api.route('/TROPIUS/hosts/list', methods=['GET'])
def list_hosts(): 
    """ 
        Return to the requesting hosts a json string containing
        the results of a SELECT * command on the hosts table
    """
    db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
    res = hosts.get_all(db)
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
    except:
        abort(400)
    try: # Try to get the state, otherwise default it to off and let the daemon clean up
        state = request.json.get('state')
        if state == None:
            state = 'off'
    except:
        state = 'off'
    # Perform the transaction itself
    db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
    ret = hosts.add(db, name, ip, mac, state)
    ret = {'sid': ret}
    db.commit()
    ret = {'add': ret}
    return jsonify(ret)


@host_api.route('/TROPIUS/hosts/remove/<int:sid>', methods=['DELETE'])
def remove_host(sid):
    """ Delete the given host from the database """
    db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
    try:
        hosts.delete(db, sid)
        db.commit()
        ret = {'remove': {'success': True}}
        return jsonify(ret)
    except:
        abort(400)


@host_api.route('/TROPIUS/hosts/<int:sid>/get', methods=['GET'])
def get_host(sid):
    db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
    ret = hosts.get_detail(db, sid)
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
    db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
    state = hosts.get(db, sid)['state']
    
    if state == 'on':
        # The host is on -- turn it off
        # TODO make a unix shell util file
        # TODO make a windows util file
        return
    elif state == 'off':
        # The host is off -- turn it on
        if timer is not None:
            sleep(timer)
        netutil.wake_on_lan(db, sid)
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
        # If no JSON parameters were given, just resume playing the song
        db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
        host = hosts.get_detail(db, sid)
        spotify.resume(host['ip'])
        return jsonify({})
    try:
        # Get the host data from the database
        db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
        host = hosts.get_detail(db, sid)
        artist = None
        album = None
        track = None
        if request.json.has_key('song'):
            song = request.json.get('song')
            #spotify.play(host['ip'], request.json.get('song'), 'song')
        elif request.json.has_key('album'):
            album = request.json.get('album')
            #spotify.play(host['ip'], request.json.get('album'), 'album')
        elif request.json.has_key('artist'):
            artist = request.json.get('artist')
            #spotify.play(host['ip'], request.json.get('artist'), 'artist')
        else:
            spotify.resume(host['ip'])
            return jsonify({})
        spotify.compound_play(host['ip'], artist=artist, album=album, song=song)
        return jsonify({})
    except:
        abort(400)

@host_api.route('/TROPIUS/hosts/<int:sid>/music/pause', methods=['POST'])
def pause_music(sid):
    """ pause the song that is currently playing """
    try:
        # Get the host data from the database
        db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
        host = hosts.get_detail(db, sid)
        spotify.pause(host['ip'])
        return jsonify({})
    except:
        abort(400)

@host_api.route('/TROPIUS/hosts/<int:sid>/music/next', methods=['POST'])
def next_song(sid):
    """ Play the next song in the media library """
    try:
        # Get the host data from the database
        db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
        host = hosts.get_detail(db, sid)
        spotify.next(host['ip'])
        return jsonify({})
    except:
        abort(400)

