# BOSCO

I have had to make several changes to get the system I have working. Here are they are:

## settings

* Enable SPI (do this through raspi-config). We need to use the neopixels through an SPI pin, since otherwise they need to be run as root and interfere with audio.

## libraries

* rpi_ws281x adafruit-circuitpython-neopixel: together allow the use of neopixels. Install with pip3.
* vorbis-tools: provides the program ogg123. Install with apt-get.
* espeak-ng: speech synthesis. Install with apt-get.
