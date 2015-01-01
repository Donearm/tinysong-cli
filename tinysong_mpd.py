#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2012-2015, Gianluca Fiore
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
###############################################################################

__author__ = "Gianluca Fiore"
__license__ = "GPL"
__version__ = "0.2"
__date__ = "20120530"
__email__ = "forod.g@gmail.com"
__status__ = "beta"

import sys
from mpd import MPDClient, CommandError
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
CON_ID = {'host': HOST, 'port': PORT}

def mpd_authenticate(c, secret):
    """Authenticate on MPD server"""
    try:
        c.password(secret)
    except CommandError:
        print("Unable to authenticate on MPD server, exiting...")
        sys.exit(1)

def mpd_connect(c, con_id):
    """Connect to the MPD server"""
    try:
        c.connect(**con_id)
    except SocketError:
        print("Can't connect to MPD server, check that it's running and properly configured")
        sys.exit(1)


def mpd_get_song():
    """Get current playing song info"""
    client = MPDClient()
    mpd_connect(client, CON_ID)

    if PASSWORD:
        # MPD server needs a valid password
        mpd_authenticate(client, PASSWORD)

    currentsong_dict = client.currentsong()
    try:
        artist = currentsong_dict['artist']
        album = currentsong_dict['album']
        song = currentsong_dict['title']
    except KeyError:
        print("Nothing is been played on this MPD server...")
        sys.exit(1)
    finally:
        client.disconnect()

    print(artist, album, song)
    return artist, album, song
