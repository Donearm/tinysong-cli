#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2012, Gianluca Fiore
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

import sys
import time
import urllib2
#import urllib.request, urllib.error, urllib.parse
import json
import tweepy
from urllib import urlencode
from argparse import ArgumentParser
from browser import open_url_in_browser
from tinysong_twitter import tw_authenticate, tw_tweet_song
from tinysong_mpd import mpd_get_song
import tinysong_cmus


BASEURL = 'http://tinysong.com'
HEADERS = {'Accept': ['text/plain', 'application/json', 'text/html'],
        'User-Agent': 'tinysong-cli' }

try:
    from tinysongconfig import APIKEY
except ImportError: 
    print("You should request a tinysong key at %s" % BASEURL + '/api')
    print("Paste it in a tinysongconfig.py file like \'APIKEY = 'your_api'\' and retry") 
    sys.exit(1)



def argument_parser():
    usage = "usage: pytinysong.py [options] searchterm(s)"
    parser = ArgumentParser(usage=usage, version="%prog 0.1")
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument("-b", "--metasearch",
            help="do a metasearch (returns back more info about the song)",
            action="store_true",
            dest="metasearch")
    parser.add_argument("-l", "--limit",
            # API limit should be 32 but apparently it stops returning results 
            # at 14
            help="the limit to the number of results, between 1 and 14",
            action="store",
            dest="limit")
    parser.add_argument("-o", "--open-url",
            help="open the url in browser.\nUrl will be the only or the first one (in case of multiple results)",
            action="store_true",
            dest="openbrowser")
    parser.add_argument("-t", "--tweet",
            help="tweet the first song found on Twitter",
            action="store_true",
            dest="tweet")
    exclusive_group.add_argument("-m", "--mpd",
            help="get current playing song from a MPD server",
            action="store_true",
            dest="mpd")
    exclusive_group.add_argument("-c", "--cmus",
            help="get current playing song from Cmus",
            action="store_true",
            dest="cmus")
    parser.add_argument(action="store",
            help="query parameters for tinysong",
            nargs="*",
            dest="args")

    options = parser.parse_args()
    return options

def tinysong_search(url):
    """make a search on tinysong"""

    response = urllib2.urlopen(url, urlencode(HEADERS))

    try:
        return json.loads(response.read())
    except ValueError:
        return

def not_found():
    print("Song not found on tinysong, sorry")
    sys.exit(1)


# Python 3.*
#    response = urllib.request.urlopen(url)
    
    # save the charset of the page to be used after to decode
#    enc = response.headers.get_content_charset()

#    bytes_response = response.read()
#    decoded_response = bytes_response.decode(enc)
#    return json.loads(decoded_response)
# End Python 3.*

class TinySongSearcher():
    def __init__(self):
        self.song = ''
        self.artist = ''
        self.album = ''
        self.json = ''

    def search(self, url):
        """open tinysong url and parse its json results"""

        self.response = urllib2.urlopen(url, urlencode(HEADERS))

        try:
            return json.loads(self.response.read())
        except ValueError:
            return
    def not_found(self):
        print("Song not found on tinysong, sorry")
        sys.exit(1)

    def basic_search(self, args):
        """basic search on tinysong"""
        self.url = BASEURL + '/a/' + args + '?format=json&key=' + APIKEY
        self.json = self.search(self.url)
        if not self.json:
            self.not_found()
        self.result_url = self.json
        print(self.result_url)
        return self.result_url

    def meta_search(self, args):
        """metasearch on tinysong"""
        self.url = BASEURL + '/b/' + args + '?format=json&key=' + APIKEY
        self.json = self.search(self.url)
        try:
            self.result_url = self.json['Url']
            self.song = self.json['SongName']
            self.artist = self.json['ArtistName']
            self.album = self.json['AlbumName']
            print("%s - %s - %s # %s" % (self.artist, self.album, self.song, self.result_url))
            return self.result_url, self.artist, self.album, self.song
        except IndexError:
            self.not_found()

    def limit_search(self, args, limit):
        """search on tinysong with a results limit"""
        self.url = BASEURL + '/s/' + args + '?format=json&limit=' + str(limit) + '&key=' + APIKEY
        self.json = self.search(self.url)
        try:
            self.result_url = self.json[0]['Url']
            for n in range(0, int(limit)):
                try:
                    print("%s - %s - %s # %s" % (self.json[n]['ArtistName'], self.json[n]['AlbumName'], self.json[n]['SongName'], self.json[n]['Url']))
                except IndexError:
                    pass
            self.song = self.json[0]['SongName']
            self.artist = self.json[0]['ArtistName']
            self.album = self.json[0]['AlbumName']
            return self.result_url, self.artist, self.album, self.song
        except (TypeError, IndexError):
            self.not_found()


def main():
    options = argument_parser()

    joined_args = '+'.join(options.args)

    ts = TinySongSearcher()

    if options.mpd:
        mpdartist, mpdalbum, mpdsong = mpd_get_song()
        # we use what mpd gives back as tinysong arguments
        joined_args = '+'.join([mpdartist, mpdalbum, mpdsong])

    if options.cmus:
        c = tinysong_cmus.CmusStatusParser()
        cmusartist, cmusalbum, cmussong = c.parse()
        print(cmusartist, cmusalbum, cmussong)
        # form arguments for tinysong query
        joined_args = '+'.join([cmusartist, cmusalbum, cmussong])

    if options.metasearch:
        result_url, artistname, albumname, songname = ts.meta_search(joined_args)
    elif options.limit:
        result_url, artistname, albumname, songname = ts.limit_search(joined_args, options.limit)
    else:
        result_url = ts.basic_search(joined_args)

    # stop if we haven't got any result from tinysong
    if not result_url:
        ts.not_found()

    if options.openbrowser:
        open_url_in_browser(result_url)

    if options.tweet:
        try:
            from tinysongconfig import TW_CONSUMER, TW_CONSUMER_SECRET, \
        TW_ACCESS, TW_ACCESS_SECRET
        except ImportError:
            # we need to authenticate
            TW_ACCESS, TW_ACCESS_SECRET = tw_authenticate(APIKEY, TW_CONSUMER, TW_CONSUMER_SECRET)
        finally:
            try:
                tw_tweet_song(TW_CONSUMER, TW_CONSUMER_SECRET, TW_ACCESS, TW_ACCESS_SECRET, result_url, artistname, songname)
            except UnboundLocalError:
                # we might had been looking for the url only, no point in tweeting
                # without artistname and songname
                print("Only a url was found, are you sure you want to tweet just that?")
                print("Try a meta search maybe?")
                sys.exit(0)



if __name__ == '__main__':
    status = main()
    sys.exit(status)
