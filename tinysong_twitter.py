# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2012-2014, Gianluca Fiore
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
import tweepy
from time import sleep
from browser import open_url_in_browser
from tinysongconfig import PREP, POSTP

def tw_authenticate(apikey, ck, cs):
    """OAuth authentication on Twitter"""

    auth = tweepy.OAuthHandler(ck, cs)
    auth_url = auth.get_authorization_url()

    print("Please authorize this application by giving access to your Twitter account")
    open_url_in_browser(auth_url)
    pin = input('Paste PIN here: ')
    auth.get_access_token(pin)
    if auth.access_token.key and auth.access_token.secret:
        tw_format_string = """# Format of the tweet:
# PREP is what comes before the song link, POSTP is what comes after
# Leave empty either (or even both) if you want the the tinysong link to be
# at the beginning/end of the tweet.
# Don't use too many characters or you'll risk hitting the 140 chars limit.
"""
        with open('tinysongconfig.py', 'w') as f:
            f.write("#-*- coding: utf-8 -*-\n\n")
            f.write("APIKEY = '%s'\n" % apikey)
            f.write("TW_CONSUMER = '%s'\nTW_CONSUMER_SECRET = '%s'\n"
                    % (ck, cs))
            f.write("TW_ACCESS = '%s'\nTW_ACCESS_SECRET = '%s'\n\n" 
                    % (auth.access_token.key, auth.access_token.secret))
            f.write(tw_format_string)
            f.write("PREP = '%s'\n" % PREP.decode("utf-8"))
            f.write("POSTP = '%s'\n" % POSTP.decode("utf-8"))
        return auth.access_token.key, auth.access_token.secret
    else:
        print("Authentication unsuccessful (perhaps wrong PIN?")
        sys.exit(1)


def tw_tweet_song(ck, cs, acc_key, acc_sec, link, artist, song):
    """Tweet a tinysong's song on Twitter"""
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(acc_key, acc_sec)

    api = tweepy.API(auth)
    if api:
        print("%s %s - %s %s %s" % (PREP.decode("utf-8"), artist, song, link, POSTP.decode("utf-8")))
        sleep(3) # sleep 3 seconds to give user time to abort
        api.update_status("%s %s - %s %s %s" % (PREP.decode("utf-8"), artist, song, link, POSTP.decode("utf-8")))
