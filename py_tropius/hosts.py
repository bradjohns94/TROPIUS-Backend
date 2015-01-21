#!/usr/bin/python2

# hosts.py
# python adder/getter file which supplies a list of utility functions
# for any additions, removals, or alterations of a computer end device

import psycopg2

# Add the base TROPIUS directory to the build path
import sys
sys.path.append('/home/tropius/TROPIUS/')

from py_tropius import device


def add(cursor, hostName, ip, mac, state):
    """ Add the new host to the device and host tables """
    hostid = device.add(cursor, hostName, ip, mac)
    cursor.execute("""INSERT INTO host VALUES (
                        %s, '%s', '%s' )
                   """ % (hostid, state, hostName))
    return hostid


def get(cursor, hostid):
    """ Get the host data of the host with the given hostid """
    _validate_hostid(cursor, hostid)
    cursor.execute("SELECT * FROM host WHERE sid = %s" % hostid)
    res = cursor.fetchone()
    return {'sid': res[0],
            'state': res[1]
           }


def get_detail(cursor, sid):
    """
        Get all information from both the host and device tables for the endpoint with
        the specified sid
    """
    _validate_hostid(cursor, sid)
    cursor.execute("SELECT * FROM device NATURAL JOIN host WHERE sid = %s" % sid)
    res = cursor.fetchone()
    return {'sid': res[0],
            'devicename': res[1],
            'ip': res[2],
            'mac': res[3],
            'state': res[4]
           }


def get_all(cursor):
    cursor.execute("SELECT sid FROM host")
    ids = cursor.fetchall()
    ret = {}
    for sid in ids:
        sid = sid[0] # Formatting fix
        ret[sid] =  get_detail(cursor, sid)
    return ret


def delete(cursor, hostid):
    """ Delete the host with the given hostid from the database """
    _validate_hostid(cursor, hostid)
    cursor.execute("DELETE FROM host WHERE sid = %s" % hostid)
    device.delete(cursor, hostid)


def update_state(cursor, hostid, state):
    """ change the hosts state to the specified state """
    _validate_hostid(cursor, hostid)
    cursor.execute("UPDATE host SET state = '%s' WHERE sid = %s" % (state, hostid))

def _validate_hostid(cursor, hostid):
    """ Make sure there is exactly one instance of the given hostid in the database """
    cursor.execute("SELECT COUNT(*) FROM host WHERE sid = %s" % hostid)
    if len(cursor.fetchall()) == 1:
        return
    raise ValueError('Invalid HostID: %s' % hostid)
