#!/usr/bin/env python2

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
