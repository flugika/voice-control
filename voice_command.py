#!/usr/bin/python3

import speech_recognition as sr # mic lib
import pandas as pd # read csv lib
from gpiozero import LED
import os
import pyttsx3
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
from spotify import *
import spotipy.util as util
import socket
import time
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment
import board
import adafruit_dht
import psutil

# ================= function =================
def message(msg):
    print("\033[0;32myou:\033[0m " + you)
    print("\033[0;35mpi:\033[0m " + msg)
    
def needSpeak(msg):
    speaker.say(msg)
    speaker.runAndWait()
    
def showTime():
    now = datetime.now()
    seg.text = now.strftime("%H-%M-%S")

def date(seg):
    """
    Display current date on device.
    """
    now = datetime.now()
    seg.text = now.strftime("%d-%m-%y")

def focusMode(checkFocus, command):
    if checkFocus == True:
        red_led.off()
        green_led.off()
        blue_led.off()
        yellow_led.off()
    else:
        if command == "listening":
            red_led.on()
            green_led.off()
            blue_led.off()
        elif command == "no command":
            red_led.off()
            green_led.on()
            blue_led.off()
        elif command == "running":
            red_led.off()
            green_led.off()
            blue_led.on()
    
# ================= setup =================
# list mic
for i, mic_name in enumerate (sr.Microphone.list_microphone_names()):
    print("mic: " + mic_name)

    # You should change microphone name to your device
    if "USB PnP Sound Device" in mic_name:
        print("USB Audio Device " + mic_name)
        # setup mic
        mic = sr.Microphone(device_index=i, chunk_size=1024, sample_rate=48000)

# setup spotify
# Set variables from setup.txt for connect dev.spotify
setup = pd.read_csv('/PATH/TO/DIRECTORY/setup.txt', sep='=', index_col=0, squeeze=True, header=None)
client_id = setup['client_id']
client_secret = setup['client_secret']
device_name = setup['device_name']
redirect_uri = setup['redirect_uri']
scope = setup['scope']
username = setup['username']
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

# Connecting to the Spotify account
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username)
spotify = sp.Spotify(auth_manager=auth_manager)

# Selecting device to play
devices = spotify.devices()
deviceID = None
for d in devices['devices']:
    d['name'] = d['name'].replace('’', '\'')
    if d['name'] == device_name:
        deviceID = d['id']
        break

# setup dht
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D22)

# setup listener (mic)
pi_ear = sr.Recognizer()

# setup speaker
speaker = pyttsx3.init()
speaker.setProperty('rate', 150) # defaut rate = 200

# setup LED
red_led = LED(2) # listening light
green_led = LED(3) # no command light
blue_led = LED(4) # running program
yellow_led = LED(17)

# setup 7 segment
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)

# setup start display
red_led.off()
green_led.off()
blue_led.off()
yellow_led.off()
seg.text = ""

# list of commands
TextSpeech = [
    ["","I can't hear you, please try again"], #0
    ["turn on light", "sure, I'm turning on the light"], #1
    ["turn off light", "sure I'm turning off the light"], #2
    ["bye", "Have a nice day"], #3
    ["blink light", "OK I'm blinking the light"], #4
    ["blink the light", ""], #5
    ["focus mode", "Take youe time"], #6
    ["enable repeat", "OK, Enabled repeat song"], #7
    ["exit repeat", "OK, Disabled repeat song"], #8
    ["stop", "OK, Stoped player"], #9
    ["volume one", "Volume level 1"], #10
    ["volume 1", ""], #11
    ["volume two", "Volume level 2"], #12
    ["volume 2", ""], #13
    ["volume three", "Volume level 3"], #14
    ["volume 3", ""], #15
    ["volume four", "Volume level 4"], #16
    ["volume 4", ""], #17
    ["mute song", "shhh.. Muted"], #18
    ["turn on the light", ""], #19
    ["turn off the light", ""], #20
    ["exit focus", "Exited focus mode"], #21
    ["today", ""], #22
    ["play", "Playing> "], #23
    ["artist", "Artist> "], #24
    ["insert", "Added to queue> "], #25
    ["enable random", "Shuffled"], #26
    ["exit random", "Disabled shuffle"], #27
    ["next song", "Next track"], #28
    ["previous song", "Previous track"], #29
    ["again", "Playing this track again"], #30
    ["continue", "Resume track"], #31
    ["volume zero", ""], #32
    ["volume 0", ""], #33
    ["บาย", ""], #34
    ["weather", ""], #35
    ["โฟกัสโหมด", ""], #36
    ["โฟกัส โหมด", ""], #37
    ["เพลย์", ""], #38
    ]

checkBye = False
checkFocus = False

while checkBye != True:
    showTime()
    if checkFocus == True:
        focusMode(checkFocus, "")
        
    with mic as source:
        pi_ear.adjust_for_ambient_noise(source, duration=0.5)
        print("\033[0;35mpi: \033[0m I'm listening")
        # listening
        focusMode(checkFocus, "listening")
        audio = pi_ear.listen(source)
            
    try:
        you = pi_ear.recognize_google(audio, language="th").lower()
        msg = you
        command = you.split()
        name = ' '.join(command[1:])
        num = 0
        
        if you != "":
            focusMode(checkFocus, "no command")
        if you == TextSpeech[0][0]: # ""
            focusMode(checkFocus, "no command")
            msg = TextSpeech[0][1] # I can't hear you, please try again
            message(msg)
            needSpeak(msg)
        elif TextSpeech[4][0] in you or TextSpeech[5][0] in you: # blink light
            focusMode(checkFocus, "running")
            if checkFocus == True:
                msg = "focus mode"
                message(msg)
                needSpeak(msg)
            else:
                msg = TextSpeech[4][1] # OK I'm blinking the light
                message(msg)
                needSpeak(msg)
                for i in range(5):
                    yellow_led.on()
                    time.sleep(0.5)
                    yellow_led.off()
                    time.sleep(0.5)
        elif TextSpeech[6][0] in you or TextSpeech[36][0] in you or TextSpeech[37][0] in you: # focus mode
            focusMode(checkFocus, "running")
            msg = TextSpeech[6][1]  # Take your time
            checkFocus = True
            message(msg)
            needSpeak(msg)
        elif TextSpeech[21][0] in you: # exit focus
            focusMode(checkFocus, "running")
            msg = TextSpeech[21][1]  # Exited focus mode
            checkFocus = False
            message(msg)
            needSpeak(msg)
        elif TextSpeech[1][0] in you or TextSpeech[19][0] in you: # turn on light
            focusMode(checkFocus, "running")
            if checkFocus == True:
                msg = "focus mode"
            else:
                msg=TextSpeech[1][1] # sure, I'm turning on the light
                yellow_led.on()
            message(msg)
            needSpeak(msg)
        elif TextSpeech[2][0] in you or TextSpeech[20][0] in you: # turn off light
            focusMode(checkFocus, "running")
            msg=TextSpeech[2][1] # sure, I'm turning off the light
            yellow_led.off()
            message(msg)
            needSpeak(msg)
        elif TextSpeech[3][0] in you or TextSpeech[34][0] in you: # bye bye / บาย
            focusMode(checkFocus, "running")
            msg=TextSpeech[3][1] # Have a nice day
            message(msg)
            needSpeak(msg)
            red_led.off()
            green_led.off()
            blue_led.off()
            seg.text = ""
            checkBye = True
        elif command[0] == TextSpeech[24][0]:
            focusMode(checkFocus, "running")
            msg = TextSpeech[24][1] + name # Artsist>
            uri = get_artist_uri(spotify=spotify, name=name)
            play_artist(spotify=spotify, device_id=deviceID, uri=uri)
            message(msg)
        elif command[0] == TextSpeech[23][0] or command[0] == TextSpeech[38][0]:
            focusMode(checkFocus, "running")
            msg = TextSpeech[23][1] + name # Playing>
            uri = get_track_uri(spotify=spotify, name=name)
            play_track(spotify=spotify, device_id=deviceID, uri=uri)
            message(msg)
        elif command[0] == TextSpeech[25][0]: # insert
            focusMode(checkFocus, "running")
            msg = TextSpeech[25][1] + name # Added to queue>
            uri = get_track_uri(spotify=spotify, name=name)
            add_to_queue(spotify=spotify, device_id=deviceID, uri=uri)
            message(msg)
        elif TextSpeech[7][0] in you: # enable repeat
            focusMode(checkFocus, "running")
            msg = TextSpeech[7][1] # OK, Enabled repeat song
            repeat(spotify=spotify, device_id=deviceID, state="track")
            message(msg)
        elif TextSpeech[8][0] in you: # exit repeat
            focusMode(checkFocus, "running")
            msg = TextSpeech[8][1] # OK, Disabled repeat song
            repeat(spotify=spotify, device_id=deviceID, state="off")
            message(msg)
        elif TextSpeech[9][0] in you: # stop
            focusMode(checkFocus, "running")
            msg = TextSpeech[9][1] # OK, Stoped player
            pause_playback(spotify=spotify, device_id=deviceID)
            message(msg)
            needSpeak(msg)
        elif TextSpeech[10][0] in you or TextSpeech[11][0] in you: # volume 1
            focusMode(checkFocus, "running")
            msg = TextSpeech[10][1] # Volume level 1
            volume(spotify=spotify, volume_percent=60, device_id=deviceID)
            message(msg)
        elif TextSpeech[12][0] in you or TextSpeech[13][0] in you: # volume 2
            focusMode(checkFocus, "running")
            msg = TextSpeech[12][1] # Volume level 2
            volume(spotify=spotify, volume_percent=75, device_id=deviceID)
            message(msg)
        elif TextSpeech[14][0] in you or TextSpeech[15][0] in you: # volume 3
            focusMode(checkFocus, "running")
            msg = TextSpeech[14][1] # Volume level 3
            volume(spotify=spotify, volume_percent=85, device_id=deviceID)
            message(msg)
        elif TextSpeech[16][0] in you or TextSpeech[17][0] in you: # volume 4
            focusMode(checkFocus, "running")
            msg = TextSpeech[16][1] # Volume level 4
            volume(spotify=spotify, volume_percent=100, device_id=deviceID)
            message(msg)
        elif TextSpeech[18][0] in you or TextSpeech[32][0] in you or TextSpeech[33][0] in you: # mute song / volume 0
            focusMode(checkFocus, "running")
            msg = TextSpeech[18][1] # shhh.. Muted
            volume(spotify=spotify, volume_percent=0, device_id=deviceID)
            message(msg)
        elif TextSpeech[22][0] in you: # what is the date today
            focusMode(checkFocus, "running")
            now = datetime.now()
            seg.text = now.strftime("%d/%m/%y")
            msg = f"{seg.text}" # date now
            message(msg)
            date(seg)
            time.sleep(5)
        elif TextSpeech[26][0] in you: # enable random
            focusMode(checkFocus, "running")
            msg = TextSpeech[26][1] # Shuffled
            message(msg)
            shuffle(spotify=spotify, state=True, device_id=deviceID)
        elif TextSpeech[27][0] in you: # exit random
            focusMode(checkFocus, "running")
            msg = TextSpeech[27][1] # Disabled shuffled
            message(msg)
            shuffle(spotify=spotify, state=False, device_id=deviceID)
        elif TextSpeech[28][0] in you: # next song
            focusMode(checkFocus, "running")
            msg = TextSpeech[28][1] # Next Track
            message(msg)
            next_track(spotify=spotify, device_id=deviceID)
        elif TextSpeech[29][0] in you: # previous song
            focusMode(checkFocus, "running")
            msg = TextSpeech[29][1] # Previous track
            message(msg)
            previous_track(spotify=spotify, device_id=deviceID)
            previous_track(spotify=spotify, device_id=deviceID)
        elif TextSpeech[30][0] in you: # again
            focusMode(checkFocus, "running")
            msg = TextSpeech[30][1] # Playing this track again
            message(msg)
            previous_track(spotify=spotify, device_id=deviceID)
        elif TextSpeech[31][0] in you: # continue
            focusMode(checkFocus, "running")
            msg = TextSpeech[31][1] # Resume track
            message(msg)
            resume(spotify=spotify, device_id=deviceID, access_token=token)
        elif TextSpeech[35][0] in you: # weather
            focusMode(checkFocus, "running")
            temp = sensor.temperature
            humidity = sensor.humidity
            seg.text = f"{temp}C {humidity}H"
            msg = f"Temperature: {temp} C   Humidity: {humidity}%"
            message(msg)
            needSpeak(f"{temp} celsius")
            
    except:
        you = ""

