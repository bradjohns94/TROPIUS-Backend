#!/usr/bin/python2

# device.py
# Utility file full of functions for adding data to the device
# table of the database. The device table should contain any
# endpoint for commands to or from the TROPIUS device, including
# the TROPIUS system itself.

import sqlite3
import socket
import re
import json

def add(db, deviceName, ip, mac):
    """ Add a device to the device table with the passed information """
    deviceName = "'" + deviceName + "'"
    # Validate the passed ip address
    try:
        socket.inet_aton(ip)
    except:
        raise ValueError('Invalid IP Address: %s' % ip)
    ip = "'" + ip + "'"
    # Validate the passed mac address
    mac_regex = '^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$'
    match = re.match(mac_regex, mac)
    if match is None:
        raise ValueError('Invalid Hardware Address: %s' % mac)
    mac = "'" + mac + "'"
    # Figure out what the hostid will be
    res = db.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'device'")
    hostid = res.fetchone()[0]
    if not hostid:
        hostid = 0
    # Add the device to the database
    db.execute("""INSERT INTO device VALUES (
                        NULL, ?, ?, ? )
                   """, (deviceName, ip, mac))
    return hostid + 1


def get(db, deviceid):
    """ Get the device data of the device with the given deviceid """
    _validate_deviceid(db, deviceid)
    res = db.execute("SELECT * FROM device WHERE sid = %d" % deviceid)
    res = res.fetchone()
    return {'sid': res[0],
            'devicename': res[1].replace("'", ""),
            'ip': res[2].replace("'", ""),
            'mac': res[3].replace("'", "")}


def get_all(db):
    """ Get the device data of all devices in the device table """
    res = db.execute("SELECT sid FROM device")
    ids = res.fetchall()
    ret = {}
    for sid in ids:
        sid = sid[0] # Formatting fix
        ret[sid] =  get(db, sid)
    return ret


def delete(db, deviceid):
    """ Remove the device with the given deviceid from the database """
    # Do not let user remove TROPIUS device from the database
    if deviceid == 101:
        raise ValueError('Cannot Remove TROPIUS Device')
    _validate_deviceid(db, deviceid)
    # TODO delete sid from all other tables when device is deleted
    db.execute("DELETE FROM device WHERE sid = %d" % (deviceid))


def get_name(db, deviceid):
    """ Get the name of the device with the given sid """
    return get(db, deviceid)['devicename']


def get_ip(db, deviceid):
    """ Get the ip address of the device with the given sid """
    return get(db, deviceid)['ip']


def get_mac(db, deviceid):
    """ Get the mac address of the device with the given sid """
    return get(db, deviceid)['mac']


def _validate_deviceid(db, deviceid):
    """ Make sure there is exactly one instance of the given deviceid in the database """
    res = db.execute("SELECT COUNT(*) FROM device WHERE sid = %d" % deviceid)
    if len(res.fetchall()) == 1:
        return
    raise ValueError('Invalid DeviceID: %s' % deviceid)
