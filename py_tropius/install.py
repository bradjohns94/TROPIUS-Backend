#!/usr/bin/python2

# install.py
# creates the initial schema for the TROPIUS database and adds
# default data for the TROPIUS device itself

from uuid import getnode as get_mac
import socket
import sqlite3
import re

import device

if __name__ == '__main__':
    # Create the initial transaction
    db = sqlite3.connect('/home/tropius/TROPIUS/TROPIUS.db')
    
    # Create the device table
    db.execute("""CREATE TABLE device (
                        sid         INTEGER PRIMARY KEY AUTOINCREMENT,
                        deviceName  TEXT,
                        ip          INET NOT NULL,
                        mac         MACADDR NOT NULL )
                   """)
    # Create the host table
    db.execute("""CREATE TABLE host (
                        sid         INTEGER PRIMARY KEY NOT NULL REFERENCES device(sid),
                        state       TEXT NOT NULL,
                        nickname    TEXT UNIQUE NOT NULL)
                   """)

    # Get the localhosts MAC Address
    mac = re.sub(r'(?<=..)(..)', r':\1', hex(get_mac()).strip('0x'))
    mac = mac.strip('L')
    mac = mac.upper()
    # Get the localhosts IP Address and hostname
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    # Add the TROPIUS system to the database
    device.add(db, hostname, ip, mac)

    # Commit the changes made to the database
    db.commit()
