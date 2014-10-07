#!/usr/bin/python

# install.py
# creates the initial schema for the TROPIUS database and adds
# default data for the TROPIUS device itself

from uuid import getnode as get_mac
import socket
import psycopg2
import re

import device

if __name__ == '__main__':
    # Create the initial transaction
    tx = psycopg2.connect("host='localhost' dbname='TROPIUS'")
    cursor = tx.cursor()
    
    # Create the device table
    cursor.execute("""CREATE TABLE device (
                        sid         INT PRIMARY KEY NOT NULL,
                        deviceName  TEXT,
                        ip          INET NOT NULL,
                        mac         MACADDR NOT NULL )
                   """)
    # Create the host table
    cursor.execute("""CREATE TABLE host (
                        sid         INT PRIMARY KEY NOT NULL,
                        state       TEXT NOT NULL,
                        nickname    TEXT UNIQUE NOT NULL)
                   """)
    # Create the system id sequence
    cursor.execute("CREATE SEQUENCE sid START 101")

    # Get the localhosts MAC Address
    mac = re.sub(r'(?<=..)(..)', r':\1', hex(get_mac()).strip('0x'))
    mac = mac.strip('L')
    mac = mac.capitalize()
    # Get the localhosts IP Address and hostname
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    # Add the TROPIUS system to the database
    device.add(cursor, hostname, ip, mac)

    # Commit the changes made to the database
    tx.commit()
