#!/usr/bin/python2

# spotify.py
# The second attempt at a TROPIUS media interface, the spotify interface
# relies on the attached host running the TROPIUS-Client daemon and sends
# a spotify request to the most specific URL it can.
# The TROPIUS-Client API itself performs a search using the Spotify Web API
# and plays the best matching song

import urllib
import urllib2
import json

def play(address, name, media_type):
    encoded = urllib.quote(name)
    url = "http://%s:8074/TROPIUS/spotify/play/%s/%s" % (address, media_type, encoded)
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)

def compound_play(address, artist=None, album=None, song=None):
    data = { 'artist': artist or "",
             'album': album or "",
             'track': song or "" }
    url = "http://%s:8074/TROPIUS/spotify/play" % address
    req = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)

def resume(address):
    url = "http://%s:8074/TROPIUS/spotify/play" % address
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    
def pause(address):
    url = "http://%s:8074/TROPIUS/spotify/pause" % address
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)

def next(address):
    url = "http://%s:8074/TROPIUS/spotify/next" % address
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)

