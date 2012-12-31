#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2012-2013, Gianluca Fiore
#
#    This program is free software: you can redistribute it and/or modify
#    it under the args of the GNU General Public License as published by
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

import subprocess

class CmusStatusParser():
    def __init__(self):
        self.artist = ''
        self.album = ''
        self.song = ''

    def parse(self):
        r = subprocess.check_output(["cmus-remote", "-Q"])
        s = r.strip().splitlines()
        for t in s:
            if t.startswith("tag artist"):
                split_t = t.split(' ')
                self.artist = ' '.join(split_t[2:])
            elif t.startswith("tag album "):
                split_t = t.split(' ')
                self.album = ' '.join(split_t[2:])
            elif t.startswith("tag title"):
                split_t = t.split(' ')
                self.song = ' '.join(split_t[2:])
            else:
                pass

        return self.artist, self.album, self.song

#c = CmusStatusParser()
#return artist, album, song = c.parse()
