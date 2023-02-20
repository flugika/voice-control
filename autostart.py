#!/usr/bin/python3

import os

cmd = 'lxterminal -e "/usr/bin/python3 /PATH/TO/DIRECTORY/voice_command.py" & lxterminal -e "/usr/bin/python3 /PATH/TO/DIRECTORY/runSpotify.py" &'

os.system(cmd)
