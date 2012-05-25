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
import webbrowser
import tweepy
from urllib import urlencode
from optparse import OptionParser

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

    (options, args) = arguments.parse_args()
    return options, args

def tw_authenticate(ck, cs):
    """OAuth authentication on Twitter"""

    auth = tweepy.OAuthHandler(ck, cs)
    auth_url = auth.get_authorization_url()

    print("Please authorize this application by giving access to your Twitter account")
    open_url_in_browser(auth_url)
    pin = input('Paste PIN here: ')
    auth.get_access_token(pin)
    if auth.access_token.key and auth.access_token.secret:
        with open('tinysongconfig.py', 'w') as f:
            f.write("APIKEY = '%s'\n" % APIKEY)
            f.write("TW_CONSUMER = '%s'\nTW_CONSUMER_SECRET = '%s'\n"
                    % (ck, cs))
            f.write("TW_ACCESS = '%s'\nTW_ACCESS_SECRET = '%s'" 
                    % (auth.access_token.key, auth.access_token.secret))
        return auth.access_token.key, auth.access_token.secret
    else:
        print("Authentication unsuccessful (perhaps wrong PIN?")
        sys.exit(1)


def tw_tweet_song(ck, cs, acc_key, acc_sec):
    """Tweet a tinysong's song on Twitter"""
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(acc_key, acc_sec)

    api = tweepy.API(auth)
    if api:
        #TODO
        pass



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

def open_url_in_browser(u):
    """open a tinysong url in default web browser"""
    try:
        webbrowser.open_new_tab(u)
    except webbrowser.Error as e:
        print(e)


def main():
    options, args = argument_parser()

    joined_args = '+'.join(args)


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
            TW_ACCESS, TW_ACCESS_SECRET = tw_authenticate(TW_CONSUMER, TW_CONSUMER_SECRET)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
