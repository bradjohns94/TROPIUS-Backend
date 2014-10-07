#!/usr/bin/env/python
# TROPIUS
# Territorial Remote Operated PI Utility System
# By Bradley Johns
#
# wol.py
# The base functionality script for the Wake-On-LAN part of TROPIUS.
# This script relies on an initial configuration being formed from
# running the initial hardware address configuration from config.py.
# If the initial configuration has not yet been run this script will
# exit with an error

import socket
import struct

# Add the base TROPIUS directory to the build path
import sys
sys.path.append('/home/brad/TROPIUS/')

from py_tropius import device

def wake_on_lan(cursor, sid):
    """ Switches on remote computers using WOL. """
    # Create the hex value of the packet
    mac = device.get_mac(cursor, sid) + ':'
    mac = 'ff:ff:ff:ff:ff:ff:' + (mac * 16)
    mac = mac[:-1] # Remove trailing ':'

    # Pack the value into a byte array
    byte_vals = mac.split(':')
    send_data = [struct.pack('B', int(val, 16)) for val in byte_vals]
    send_data = b''.join(send_data)

    # send out the magic packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('192.168.8.255', 80))
