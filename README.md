color station
=============

**Author:** [Nick Meehan](https://github.com/unsalted)  
**Year:** 2014  
**Class:** Lab C  
**Instructor:** Luke Johnson  


## Synopsis

This is a combination of two sets of code. The [first part](color_station/sheild_sdlog_gps_color/) is the code is a *Arduino Mega* needed to log GPS and color data.  [The second](/data-processing/) is a series of *Python* scripts I wrote to process the data in to various formats, which was necessary to visualize the project.


## Motivation

A single purpose device made up of a color sensors and gps coordinates to map the color of light at night in Los Angeles.

## Code Example

Show what the library or code does as concisely as possible, people should be able to figure out **how** your project solves their problem by looking at the code example or in the case of projects an example of what your code does by linking to a website or an image.

## Installation

Provide code examples and explanations of how to get the project.


## Installation:

*this doc assumes you have recent versions of bower and python on your computer*

Run ``bower install`` to automatically load dependencies.

Move components e.g. (Adafruit_TCS34725) to your Arduino library.

-----------------

###csvtogpx

I wrote a python script that converts a directory of .csv log files to .gpx waypoint coordinates that can be mapped in other programs.

It is a command line script... to use it
    
1. navigate to the directory with the script
2. `python csvtogpx.py './relative/directory/of/csv/files'`
4. navigate to a directory called '/xml' which is in the root of the processed directory
3. marvel your fancy new gpx files

So you might be wondering why I didn't just generate the gpx file on the device. How thoughtful of you. I was trying to limit the amount of parsing that needed to be done on the device, csv files are light weight and don't require complicated headers etc.'

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


## License

MIT License