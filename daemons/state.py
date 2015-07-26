#!/usr/bin/python2

# state.py
# The startup daemon designed to maintain a check on all hosts
# connected to TROPIUS and test whether or not they are currently
# active. If the state of the host differs from the state listed
# by the database, this daemon is responsible to update the database

from time import sleep
import os
import sqlite3

# Add the TROPIUS directory structure to PYTHONPATH
import sys
sys.path.append('/home/tropius/TROPIUS/')

from py_tropius import hosts

while True:
    # Create a connection to the database
    db = sqlite3.connect("/home/tropius/TROPIUS/TROPIUS.db")
    # Build a list of dictionaries contain data for each host
    res = hosts.get_all(db)
    host_list = []
    for sid in res:
        host_list.append(res[sid])
    
    for host in host_list:
        ip = host['ip']
        response = os.system("ping -c 1 " + ip)
        if response == 0:
            if host['state'] == 'off':
                # Connection successful, set state to on
                hosts.update_state(db, host['sid'], 'on')
                db.commit()
        else:
            if host['state'] == 'on':
                # Connection failed, set the state to off
                hosts.update_state(db, host['sid'], 'off')
                db.commit()
    sleep(120) # We'll perform this check every other minute
