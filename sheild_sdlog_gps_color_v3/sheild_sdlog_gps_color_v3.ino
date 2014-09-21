#include <SPI.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
#include <SD.h>
#include <Wire.h>
#include <Adafruit_TCS34725.h>
#include <avr/sleep.h>

// Code hacked together by Nick Meehan nick@unsalted.nu -
// In association with: Art Center College of Design - Media Design Practices - MFA
//
// This code is a combination of two code sets:
// https://github.com/adafruit/Adafruit-GPS-Library/tree/master/examples/shield_sdlog
// https://github.com/adafruit/Adafruit_TCS34725/tree/master/examples/tcs34725
//
// With additional help from: http://www.instructables.com/id/Personal-Black-Box-Arduino-Mega-Ultimate-GPS-Shiel/
// The goal of this code is to map coordinates with color data taken by TCS34725
//
//
// Developed on the Adafruit Ultimate GPS + Logging Shield & TCS34725 RGB Color Sensor
// on an Arduino Mega 2560
// 

HardwareSerial mySerial = Serial1;    //This line is only for mega
Adafruit_GPS GPS(&mySerial);

// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO  false
/* set to true to only log to SD when GPS has a fix, for debugging, keep it false */
#define LOG_FIXONLY false  

// this keeps track of whether we're using the interrupt
// off by default!
boolean usingInterrupt = false;
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy

// Set the pins used
#define chipSelect 10
#define ledPin 13

File logfile;

// read a Hex value and return the decimal equivalent
uint8_t parseHex(char c) {
  if (c < '0')
  return 0;
  if (c <= '9')
  return c - '0';
  if (c < 'A')
  return 0;
  if (c <= 'F')
  return (c - 'A')+10;
}

// Errors not vurrently used on board but could come in handy.
// Blink out an error code
void error(uint8_t errno) {
  /*
  if (SD.errorCode()) {
   putstring("SD error: ");
   Serial.print(card.errorCode(), HEX);
   Serial.print(',');
   Serial.println(card.errorData(), HEX);
   }
   */
   while(1) {
    uint8_t i;
    for (i=0; i<errno; i++) {
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
      delay(100);
    }
    for (i=errno; i<10; i++) {
      delay(200);
    }
  }
}

Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_700MS, TCS34725_GAIN_1X);

void setup() {
  
  if (tcs.begin()) {
    Serial.println("Found sensor");
    } else {
      Serial.println("No TCS34725 found ... check your connections");
      while (1);
    }

    tcs.setInterrupt(true);

  // connect at 115200 so we can read the GPS fast enough and echo without dropping chars
  // also spit it out
  Serial.begin(115200);
  Serial.println("\r\nUltimate GPSlogger Shield");
  pinMode(ledPin, OUTPUT);

  // make sure that the default chip select pin is set to
  // output, even if you don't use it:
  pinMode(10, OUTPUT);

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect, 11, 12, 13)) {
  Serial.println("Card init. failed!");
  error(2);
}


char filename[15];
strcpy(filename, "GPSLOG00.CSV");

for (uint8_t i = 0; i < 100; i++) {
  filename[6] = '0' + i/10;
  filename[7] = '0' + i%10;
    // create if does not exist, do not open existing, write, sync after write
    if (! SD.exists(filename)) {
      break;
    }
  }

  logfile = SD.open(filename, FILE_WRITE);
  if( ! logfile ) {
    Serial.print("Couldnt create "); 
    Serial.println(filename);
    error(3);
  }
  Serial.print("Writing to "); 
  Serial.println(filename);
  // Print csv header
  logfile.println("Time, Date, Latitude, Longitude, Elevation, Speed (Knots), Angle, Satellites, Color Temp, Lux, R, G, B, C");
  logfile.flush();

  // connect to the GPS at the desired rate
  GPS.begin(9600);

  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For logging data, we don't suggest using anything but either RMC only or RMC+GGA
  // to keep the log files at a reasonable size
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 100 millihertz (once every 10 seconds), 1Hz or 5Hz update rate

  // Turn off updates on antenna status, if the firmware permits it
  GPS.sendCommand(PGCMD_NOANTENNA);

  // the nice thing about this code is you can have a timer0 interrupt go off
  // every 1 millisecond, and read data from the GPS for you. that makes the
  // loop code a heck of a lot easier!
  useInterrupt(true);

  Serial.println("Ready!");
  // Print CSV headers to serial
  Serial.println("Time, Date, Latitude, Longitude, Elevation, Speed (Knots), Angle, Satellites, Color Temp, Lux, R, G, B, C\n");
}


// Interrupt is called once a millisecond, looks for any new GPS data, and stores it
SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  #ifdef UDR0
  if (GPSECHO)
  if (c) UDR0 = c;  
      // writing direct to UDR0 is much much faster than Serial.print 
      // but only one character can be written at a time. 
      #endif
    }

    void useInterrupt(boolean v) {
      if (v) {
    // Timer0 is already used for millis() - we'll just interrupt somewhere
    // in the middle and call the "Compare A" function above
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
    usingInterrupt = true;
  } 
  else {
    // do not call the interrupt function COMPA anymore
    TIMSK0 &= ~_BV(OCIE0A);
    usingInterrupt = false;
  }
}


void loop() {

  tcs.setInterrupt(true);      // turn on LED

  // Declare color sensor variables
  uint16_t r, g, b, c, colorTemp, lux;
  
  tcs.getRawData(&r, &g, &b, &c);
  colorTemp = tcs.calculateColorTemperature(r, g, b);
  lux = tcs.calculateLux(r, g, b);
  
  
  if (! usingInterrupt) {
    // read data from the GPS in the 'main loop'
    char c = GPS.read();
    // if you want to debug, this is a good time to do it!
    if (GPSECHO)
    if (c) Serial.print(c);
  }
  
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences! 
    // so be very wary if using OUTPUT_ALLDATA and trying to print out data
    
    // Don't call lastNMEA more than once between parse calls!  Calling lastNMEA 
    // will clear the received flag and can cause very subtle race conditions if
    // new data comes in before parse is called again.
    char *stringptr = GPS.lastNMEA();
    
    if (!GPS.parse(stringptr))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another

    // Sentence parsed! 
    Serial.println("GPS parsed OK");
    if (LOG_FIXONLY && !GPS.fix) {
      Serial.print("No Fix");
      return;
    }

    // Super. log it!
    Serial.println("Log: start");
    //Time  
    logfile.print(GPS.hour, DEC);
    logfile.print(':');
    logfile.print(GPS.minute, DEC);
    logfile.print(':');
    logfile.print(GPS.seconds, DEC);
    logfile.print('.');
    logfile.print(GPS.milliseconds);
    logfile.print(",");
    //Date
    logfile.print(GPS.month, DEC); 
    logfile.print('/');
    logfile.print(GPS.day, DEC);
    logfile.print("/20");
    logfile.print(GPS.year, DEC);
    logfile.print(",");
    //Coordinates
    logfile.print(GPS.latitude, 4);
    logfile.print(GPS.lat);
    logfile.print(",");
    logfile.print(GPS.longitude, 4);
    logfile.print(GPS.lon);
    logfile.print(",");
    logfile.print(GPS.altitude);
    logfile.print(",");
    logfile.print(GPS.speed);
    logfile.print(",");
    logfile.print(GPS.angle);
    logfile.print(",");
    logfile.print((int)GPS.satellites);
    logfile.print(",");
    //Color
    logfile.print(colorTemp, DEC); 
    logfile.print(",");
    logfile.print(lux, DEC); 
    logfile.print(",");
    logfile.print(r, DEC); 
    logfile.print(",");
    logfile.print(g, DEC); 
    logfile.print(",");
    logfile.print(b, DEC); 
    logfile.print(",");
    logfile.println(c, DEC);
    // Wait for logging to finish
    logfile.flush();
    // Print to serial
    Serial.println("Log: complete");
    Serial.println();
    Serial.println("Logged Data:");
    // Time
    Serial.print(GPS.hour, DEC);
    Serial.print(':');
    Serial.print(GPS.minute, DEC);
    Serial.print(':');
    Serial.print(GPS.seconds, DEC);
    Serial.print('.');
    Serial.print(GPS.milliseconds);
    Serial.print(",");
    // Date
    Serial.print(GPS.month, DEC); 
    Serial.print('/');
    Serial.print(GPS.day, DEC);
    Serial.print("/20");
    Serial.print(GPS.year, DEC);
    Serial.print(",");
    // Coordinates
    Serial.print(GPS.latitude, 4);
    Serial.print(GPS.lat);
    Serial.print(",");
    Serial.print(GPS.longitude, 4);
    Serial.print(GPS.lon);
    Serial.print(",");
    Serial.print(GPS.altitude);
    Serial.print(",");
    Serial.print(GPS.speed);
    Serial.print(",");
    Serial.print(GPS.angle);
    Serial.print(",");
    Serial.print((int)GPS.satellites);
    Serial.print(",");
    // Color temp
    Serial.print(colorTemp, DEC); 
    Serial.print(",");
    Serial.print(lux, DEC); 
    Serial.print(",");
    Serial.print(r, DEC); 
    Serial.print(",");
    Serial.print(g, DEC); 
    Serial.print(",");
    Serial.print(b, DEC); 
    Serial.print(",");
    Serial.println(c, DEC);

    Serial.print("\n");
    Serial.println();
  }
}


/* End code */

