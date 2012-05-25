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

import webbrowser

def open_url_in_browser(u):
    """open a tinysong url in default web browser"""
    try:
        webbrowser.open_new_tab(u)
    except webbrowser.Error as e:
        print(e)