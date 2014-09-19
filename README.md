color-station
=============

A collection of sensors for collecting data on street lamps.

## Possible detour
!!!Parsing the same data from raw image files with gpx data added to them. TBD after more testing.!!!

##Dependencies:

(this doc assumes you have recent versions of homebrew and node on your computer)

ExifTool: brew install exiftool

Run ``bower install`` and ``npm install`` to automatically load other dependencies.

-----------------

## Research

### ExifTool
parses metadata from images.
http://www.sno.phy.queensu.ca/~phil/exiftool/

### Adafruit Color Sensor

Documentation:
https://learn.adafruit.com/adafruit-color-sensors/programming

Dependencies:
https://github.com/adafruit/Adafruit_TCS34725

### Adafruit Lux Sensor
*We may not need this sensor.*

Documentation:
https://learn.adafruit.com/tsl2561

Dependencies:
https://github.com/adafruit/Adafruit_TSL2561

### Adafruit Serial Camera

Documentation: https://learn.adafruit.com/ttl-serial-camera

Dependencies: 
https://github.com/adafruit/Adafruit-VC0706-Serial-Camera-Library

### Adafruit Ultimate GPS Sheild

Documentation: 
https://learn.adafruit.com/adafruit-ultimate-gps-logger-shield/sd-logging

Dependencies:
- https://github.com/adafruit/Adafruit-GPS-Library
- https://github.com/adafruit/SD
