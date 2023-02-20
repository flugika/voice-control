#!/usr/bin/python3

import requests
import os

check = True

while check:
    try:
        if requests.get('https://google.com').ok:
            os.system("/PATH/TO/DIRECTORY/spotifyd --no-daemon")
            check = False
    except:
        print("You're Offline")