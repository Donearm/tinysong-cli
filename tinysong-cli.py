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
from urllib import urlencode
from optparse import OptionParser
from apikey import APIKEY


BASEURL = 'http://tinysong.com'
HEADERS = {'Accept': ['text/plain', 'application/json', 'text/html'],
        'User-Agent': 'tinysong-cli' }


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

    (options, args) = arguments.parse_args()
    return options, args


def tinysong_search(url):
    """make a search on tinysong"""

    response = urllib2.urlopen(url, urlencode(HEADERS))

    return json.loads(response.read())

# Python 3.*
    #response = urllib.request.urlopen(url)
    
    # save the charset of the page to be used after to decode
    #enc = response.headers.get_content_charset()
    #print(response.headers.get_content_charset())

# this doesn't work, see 
# http://stackoverflow.com/questions/2143206/convert-google-search-results-into-json-in-python-3-1
    #print(response.read())
    #print(type(response.read()))
    #print(type(response.msg))
    #return json.loads(response.read().decode(enc))
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
            print("%s - %s - %s # %s" % (result[n]['ArtistName'], result[n]['AlbumName'], result[n]['SongName'], result[n]['Url']))
    else:
        url = BASEURL + '/a/' + joined_args + '?format=json&key=' + APIKEY
        result = tinysong_search(url)
        print(result)
        result_url = [result]

    if options.openbrowser:
        open_url_in_browser(result_url[0])



if __name__ == '__main__':
    status = main()
    sys.exit(status)
