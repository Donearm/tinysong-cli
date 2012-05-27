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
__version__ = "0.1"
__date__ = "20120523"
__email__ = "forod.g@gmail.com"
__status__ = "stable"

import sys
import urllib2
#import urllib.request, urllib.error, urllib.parse
import json
import tweepy
from urllib import urlencode
from optparse import OptionParser
from browser import open_url_in_browser
from tinysong_twitter import tw_authenticate, tw_tweet_song
from tinysong_mpd import mpd_get_song


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
    arguments = OptionParser(usage=usage, version="%prog 0.1")
    arguments.add_option("-b", "--metasearch",
            help="do a metasearch (returns back more info about the song)",
            action="store_true",
            dest="metasearch")
    arguments.add_option("-l", "--limit",
            # API limit should be 32 but apparently it stops returning results 
            # at 14
            help="the limit to the number of results, between 1 and 14",
            action="store",
            dest="limit")
    arguments.add_option("-o", "--open-url",
            help="open the url in browser.\nUrl will be the only or the first one (in case of multiple results)",
            action="store_true",
            dest="openbrowser")
    arguments.add_option("-t", "--tweet",
            help="tweet the first song found on Twitter",
            action="store_true",
            dest="tweet")
    arguments.add_option("-m", "--mpd",
            help="get current playing song from a MPD server",
            action="store_true",
            dest="mpd")

    (options, args) = arguments.parse_args()
    return options, args

def tinysong_search(url):
    """make a search on tinysong"""

    response = urllib2.urlopen(url, urlencode(HEADERS))

    return json.loads(response.read())

# Python 3.*
#    response = urllib.request.urlopen(url)
    
    # save the charset of the page to be used after to decode
#    enc = response.headers.get_content_charset()

#    bytes_response = response.read()
#    decoded_response = bytes_response.decode(enc)
#    return json.loads(decoded_response)
# End Python 3.*


def main():
    options, args = argument_parser()

    joined_args = '+'.join(args)

    if options.mpd:
        mpdartist, mpdalbum, mpdsong = mpd_get_song()
        # we use what mpd gives back as tinysong arguments
        joined_args = '+'.join([mpdartist, mpdalbum, mpdsong])


    if options.metasearch:
        url = BASEURL + '/b/' + joined_args + '?format=json&key=' + APIKEY
        result = tinysong_search(url)
        print(result)
        result_url = [result['Url']]
        print("%s - %s - %s # %s" % (result['ArtistName'], result['AlbumName'], result['SongName'], result_url[0]))
    elif options.limit:
        url = BASEURL + '/s/' + joined_args + '?format=json&limit=' + str(options.limit) + '&key=' + APIKEY
        result = tinysong_search(url)
        print(result)
        result_url = [result[0]['Url']]
        for n in range(0, int(options.limit)):
            try:
                print("%s - %s - %s # %s" % (result[n]['ArtistName'], result[n]['AlbumName'], result[n]['SongName'], result[n]['Url']))
            except IndexError:
                return
    else:
        url = BASEURL + '/a/' + joined_args + '?format=json&key=' + APIKEY
        result = tinysong_search(url)
        print(result)
        result_url = [result]

    if options.openbrowser:
        open_url_in_browser(result_url[0])

    if options.tweet:
        try:
            from tinysongconfig import TW_CONSUMER, TW_CONSUMER_SECRET, \
        TW_ACCESS, TW_ACCESS_SECRET
            tw_tweet_song(TW_CONSUMER, TW_CONSUMER_SECRET, TW_ACCESS, TW_ACCESS_SECRET)
        except ImportError:
            # we need to authenticate
            TW_ACCESS, TW_ACCESS_SECRET = tw_authenticate(APIKEY, TW_CONSUMER, TW_CONSUMER_SECRET)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
