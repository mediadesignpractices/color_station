color-station
=============


Using color sensors and gps coordinates to map the color of light at night in Los Angeles

#### Dependencies:

*this doc assumes you have recent versions of bower and python on your computer*

Run ``bower install`` to automatically load dependencies.

Move components e.g. (Adafruit_TCS34725) to your Arduino library.

-----------------
<br>
## The Device

### Arduino Mega 2560

http://arduino.cc/en/Main/arduinoBoardMega2560

### Adafruit Color Sensor

Documentation:
https://learn.adafruit.com/adafruit-color-sensors/programming

Dependencies:
https://github.com/adafruit/Adafruit_TCS34725


### Adafruit Ultimate GPS Sheild

Documentation: 
https://learn.adafruit.com/adafruit-ultimate-gps-logger-shield/sd-logging

Dependencies:
- https://github.com/adafruit/Adafruit-GPS-Library
- https://github.com/adafruit/SD

</br>
##csvtogpx

I wrote a python script that converts a directory of .csv log files to .gpx waypoint coordinates that can be mapped in other programs.

It is a command line script... to use it
    
1. navigate to the directory with the script
2. `python csvtogpx.py './relative/directory/of/csv/files'`
3. marvel your fancy new gpx files.

So you might be wondering why we don't just generate the gpx file on the device. How thoughtful of you. We are trying to limit the amount of parsing that needs to done on the device, csv files are light weight and don't require complicated headers etc.'
