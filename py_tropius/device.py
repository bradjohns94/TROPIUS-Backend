#!/usr/bin/python2

# device.py
# Utility file full of functions for adding data to the device
# table of the database. The device table should contain any
# endpoint for commands to or from the TROPIUS device, including
# the TROPIUS system itself.

import psycopg2
import socket
import re
import json

def add(cursor, deviceName, ip, mac):
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
    # Get a new sid from the sid sequence
    cursor.execute("SELECT nextval('sid')")
    deviceid = cursor.fetchone()
    deviceid = int(deviceid[0])
    # Add the device to the database
    cursor.execute("""INSERT INTO device VALUES (
                        %s, %s, %s, %s )
                   """ % (deviceid, deviceName, ip, mac))
    return deviceid


def get(cursor, deviceid):
    """ Get the device data of the device with the given deviceid """
    _validate_deviceid(cursor, deviceid)
    cursor.execute("SELECT * FROM device WHERE sid = %s" % deviceid)
    res = cursor.fetchone()
    return {'sid': res[0],
            'devicename': res[1],
            'ip': res[2],
            'mac': res[3]}


def get_all(cursor):
    """ Get the device data of all devices in the device table """
    cursor.execute("SELECT sid FROM device")
    ids = cursor.fetchall()
    ret = {}
    for sid in ids:
        ret[sid] =  get(cursor, sid)
    return ret


def delete(cursor, deviceid):
    """ Remove the device with the given deviceid from the database """
    # Do not let user remove TROPIUS device from the database
    if deviceid == 101:
        raise ValueError('Cannot Remove TROPIUS Device')
    _validate_deviceid(cursor, deviceid)
    # TODO delete sid from all other tables when device is deleted
    cursor.execute("DELETE FROM device WHERE sid = %s" % deviceid)


def get_name(cursor, deviceid):
    """ Get the name of the device with the given sid """
    return get(cursor, deviceid)['devicename']


def get_ip(cursor, deviceid):
    """ Get the ip address of the device with the given sid """
    return get(cursor, deviceid)['ip']


def get_mac(cursor, deviceid):
    """ Get the mac address of the device with the given sid """
    return get(cursor, deviceid)['mac']


def _validate_deviceid(cursor, deviceid):
    """ Make sure there is exactly one instance of the given deviceid in the database """
    cursor.execute("SELECT COUNT(*) FROM device WHERE sid = %s" % deviceid)
    if len(cursor.fetchall()) == 1:
        return
    raise ValueError('Invalid DeviceID: %s' % deviceid)
