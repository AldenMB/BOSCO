# BOSCO

Sadly BOSCO needs to be run as root, to use the lights.

## setup

* Enable SPI using raspi-config
* Set up pigpio daemon as follows: 

run this on the command line:


    wget https://raw.githubusercontent.com/joan2937/pigpio/master/util/pigpiod.service
    sudo mv pigpiod.service /etc/systemd/system
    sudo systemctl enable pigpiod.service
    sudo systemctl start pigpiod.service

* Change the CPU core frequency to be compatible with SPI for the neopixels (following directions from [here](https://pypi.org/project/rpi-ws281x/)): 

Add the following line at the end of `/boot/config.txt`:

    core_freq=250

## libraries

This project requires the following libraries installed:

* rpi_ws281x adafruit-circuitpython-neopixel: together allow the use of neopixels. Install with pip3.
* vorbis-tools: provides the program ogg123. Install with apt-get.
* espeak-ng: speech synthesis. Install with apt-get.