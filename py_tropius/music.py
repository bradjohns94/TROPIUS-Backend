#!/usr/bin/python2

# music.py
# Utility file full of functions for managing music playback of VLC on remote
# hosts. This file runs under the assumption that the music library is set
# up in an iTunes like format having a base music folder with artist
# sub-directories. Each artist sub-directories should be sub-divided into
# album directories which contains the songs themselves.

import base64
import urllib2
import xml.etree.ElementTree as ET

def get_library(address, port, username, password):
    """ Given basic http auth info, get the music library for the given host """
    # Create the base url request
    req = urllib2.Request("http://%s:%s/requests/playlist.xml" % (address, port))
    # Add username/password authentication
    auth = base64.encodestring("%s:%s" % ("", "vlcremote"))
    req.add_header("Authorization", "Basic %s" % auth)
    # Send the request convert the response into a string
    res = urllib2.urlopen(req)
    data = res.readlines()
    xml_string = ""
    for line in data:
        xml_string = xml_string + line
    # Get an XML reference to the Media Library and return
    root = ET.fromstring(xml_string)
    library = root.find("./node[@name='Media Library']/node")
    return library


def get_song_id(library, title, artist=None, album=None):
    """ Given a library result from get_library find a specific song id """
    # Build the XML query path based on the passed parameters
    path = "."
    path = path + "/node"
    if artist:
        path = path + "[@name='%s']" % artist
    path = path + "/node"
    if album:
        path = path + "[@name='%s']" % album
    path = path + "/leaf[@name='%s']" % title
    # Search the query path for any songs matching the provided data
    res = library.findall(path)
    if len(res) == 1:
        # Search successful, return ID of the found song
        return res[0].get('id')
    elif len(res) == 0:
        raise ValueError("No such song found.")
        return -1
    else:
        # TODO determine whether or not we should make this best effort
        raise ValueError("Ambiguous query: multiple results found.")
        return -1


def play_song(address, port, username, password, song_id=None):
    """
        using the same http auth used in get_library and a song_id from
        get_song_id send the request to make vlc play the given song.
        If no id is given, simply resume play if paused/stopped.
    """
    # Build the url to play the selected song
    url = "http://%s:%s/requests/status.xml" % (address, port)
    url = url + "?command=pl_play"
    if song_id:
        url = url + "&id=%s" % song_id
    req = urllib2.Request(url)
    # add authentication to the request
    auth = base64.encodestring("%s:%s" % ("", "vlcremote"))
    req.add_header("Authorization", "Basic %s" % auth)
    urllib2.urlopen(req)


def run_command(address, port, username, password, command):
    """
        Using the same http auth in get_library, run a vlc command
        corresponding to status.xml with no params. This should primarily
        be used for the following commands:
            pl_pause -- pause the playing song
            pl_stop -- stop the playing song
            pl_next -- play the next song
            pl_previous -- play the previous song
            pl_random -- toggle on/off shuffle
    """
    # Generate the base url
    url = "http://%s:%s/requests/status.xml" % (address, port)
    url = url + "?command=%s" % command
    # add authentication to the request
    auth = base64.encodestring("%s:%s" % ("", "vlcremote"))
    req.add_header("Authorization", "Basic %s" % auth)
    urllib2.urlopen(req)
