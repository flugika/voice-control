# Voice Command

<hr />

### 523354 Operating System 2/2565 | Section 1 Group 8

<hr />

### Voice Command with Raspberry Pi and Python3

Hi, this is just a little project from our education. It's fun to control other device with OUR VOICE.

#### Tools

1) Raspberry Pi 3 Model B+ ``x 1``

2) Micro USB cable ``x 1``

3) Ethernet cable or HDMI cable ``x 1``

4) Jump wire ``> 14``

5) LED (Unique colors) ``x 4``

6) Microphone and Y cable ``x 1``

7) Speaker and Jack wire ``x 1``

8) USB Sound Card ``x 1``

9) Micro SD Card (> 16 GB) and Reader ``x 1``

##### You can change these tools into something you have instead

1) MAX-7219 7 segments 8 digits ``x 1``

2) DHT11 or DHT 22 ``x 1``
 

#### Install OS

1) Download Raspberry Pi Imager and OS: https://www.raspberrypi.com/software/

2) Install Raspberry Pi OS: https://www.youtube.com/watch?v=F5OYpPUJiOw

3) Don't forget setting your OS in Raspberry Pi Imager in below

    1) Set hostname: raspberrypi.local

    2) Enable SSH
        
            Check> Use password authentication
    
    3) Set username and password

            set your os password

4) When you installed the OS. Create new file in Disk "BOOT"

    ```
    file name "ssh"
    ====================== IMPORTANT ==================
    NO file extension it's just FILE and NO text inside
    ```

#### Install Libraries

I used Python 3.9.2

```
I can't tell you what I installed in my raspberry Pi, I forgot it LMAO.
You can install libraries which error module detect, sorry.
```

``sudo apt-get update``

#### Setup Circuit



if you can't understand this, you can read GPIO in our python file.

luma GPIO: https://luma-led-matrix.readthedocs.io/en/latest/install.html#max7219-devices-spi


### You can find /PATH/TO/DIRECTORY/ and replace it with your path

### Spotifyd

Tutorial: https://www.youtube.com/watch?v=GGXJuzSise4

``sudo nano /home/pi.config/spotifyd/spotifyd.conf``

```
[global]
username = "Your username" # not name but code name ex. 317812cfy4ajsdk...
password = "Your password"
backend = "alsa"
device = "hw:CARD=Device,DEV=0" # aplay -L and copy speaker you want to use ex hw:...
mixer = "PCM"
volume-controller = "alsa"
device_name = "Raspberry_PI"
bitrate = 320 # bitrate has 96, 160, 320 kbit/s IF you have a spotify premium you can use 320 bitrates
cache_path = "cache_directory"
volume-normalisation = true
normalisation-pregain = -100
initial_volume = "75" # Can config default volume here
```

### Auto Start

we run the autostart.py for run 2 terminal when start

``sudo nano /etc/xdg/lxsession/LXDE-pi/autostart``

add this code below

```
@/usr/bin/python3 /PATH/TO/DIRECTORY/autostart.py
```

<hr />

## Written: Chookiat Kainta