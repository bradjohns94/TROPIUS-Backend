#!/usr/bin/python2

# hosts.py
# python adder/getter file which supplies a list of utility functions
# for any additions, removals, or alterations of a computer end device

import sqlite3

# Add the base TROPIUS directory to the build path
import sys
sys.path.append('/home/tropius/TROPIUS/')

from py_tropius import device


def add(db, hostName, ip, mac, state):
    """ Add the new host to the device and host tables """
    hostid = device.add(db, hostName, ip, mac)
    db.execute("""INSERT INTO host VALUES (
                        %d, ?, ? )
                   """ % hostid, (state, hostName))
    return hostid


def get(db, hostid):
    """ Get the host data of the host with the given hostid """
    _validate_hostid(db, hostid)
    res = db.execute("SELECT * FROM host WHERE sid = %d" % hostid)
    res = res.fetchall()
    return {'sid': res[0],
            'state': res[1].replace("'", "")
           }


def get_detail(db, sid):
    """
        Get all information from both the host and device tables for the endpoint with
        the specified sid
    """
    _validate_hostid(db, sid)
    res = db.execute("SELECT * FROM device NATURAL JOIN host WHERE sid = %d" % sid)
    res = res.fetchone()
    return {'sid': res[0],
            'devicename': res[1].replace("'",""),
            'ip': res[2].replace("'", ""),
            'mac': res[3].replace("'", ""),
            'state': res[4].replace("'", "")
           }


def get_all(db):
    res = db.execute("SELECT sid FROM host")
    ids = res.fetchall()
    ret = {}
    for sid in ids:
        sid = sid[0] # Formatting fix
        ret[sid] =  get_detail(db, sid)
    return ret


def delete(db, hostid):
    """ Delete the host with the given hostid from the database """
    _validate_hostid(db, hostid)
    db.execute("DELETE FROM host WHERE sid = %d" % (hostid,))
    device.delete(db, hostid)


def update_state(db, hostid, state):
    """ change the hosts state to the specified state """
    _validate_hostid(db, hostid)
    db.execute("UPDATE host SET state = ? WHERE sid = %d" % hostid, (state,))

def _validate_hostid(db, hostid):
    """ Make sure there is exactly one instance of the given hostid in the database """
    res = db.execute("SELECT COUNT(*) FROM host WHERE sid = %d" % hostid)
    if len(res.fetchall()) == 1:
        return
    raise ValueError('Invalid HostID: %s' % hostid)
