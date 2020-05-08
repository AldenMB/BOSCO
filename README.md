# BOSCO

Sadly BOSCO needs to be run as root, to use the lights.

## setup

* Set up pigpio daemon as follows: 

run this on the command line:

    wget https://raw.githubusercontent.com/joan2937/pigpio/master/util/pigpiod.service
    sudo mv pigpiod.service /etc/systemd/system
    sudo systemctl enable pigpiod.service
    sudo systemctl start pigpiod.service

* choose the usb auio device as the default

following directions at https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi?view=all
we must run `sudo nano /usr/share/alsa/alsa.conf` and 
on the lines `defaults.ctl.card 0` and `defaults.pcm.card 0`
replace 0 with 1.

## libraries

This project requires the following libraries installed:

* rpi_ws281x adafruit-circuitpython-neopixel: together allow the use of neopixels. Install with pip3.
* vorbis-tools: provides the program ogg123. Install with apt-get.
* espeak-ng: speech synthesis. Install with apt-get.