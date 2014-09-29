# csv2gpx.py
# First row of the csv file must be header!
# Large part of code from: http://code.activestate.com/recipes/577423-convert-csv-to-xml/


import csv
import datetime
import sys
import os

if len(sys.argv) != 2:
    os._exit(1)
path=sys.argv[1] # get folder as a command line argument
os.chdir(path)
if not os.path.exists('./xml'):
    os.makedirs('./xml')
csvFiles = [f for f in os.listdir('.') if f.endswith('.csv') or f.endswith('.CSV')]

for csvFile in csvFiles:
    xmlFile = './xml/'+csvFile[:-4] + '.xml'
    csvData = csv.reader(open(csvFile))
    xmlData = open(xmlFile, 'w')

    csvData = csv.reader(open(csvFile))
    xmlData = open(xmlFile, 'w')

    #DEFINE FUNCTIONS
    # convert coordinates
    def latConvert(coord):
        if ('S') in coord:
          coord = coord.replace('S', '')
          coord = float(coord)/100*-1
          M = coord % -1*100/60
        else:
          coord = coord.replace('N', '')
          coord = float(coord)/100
          M = coord % 1*100/60
        # seperate
        D = str(int(coord))
        M = "{0:.8f}".format(M).lstrip('0')
        coord = D+M
        return coord

    def lonConvert(coord):
        if 'W' in coord:
          coord = coord.replace('W', '')
          coord = float(coord)/100*-1
          M = coord % -1*100/60
        else:
          coord = coord.replace('E', '')
          coord = float(coord)/100
          M = coord % 1*100/60

        D = str(int(coord))
        M = "{0:.8f}".format(M).lstrip('-').lstrip('0')
        coord = D+M
        return coord
    # return fix type
    def fix(f, s):
        if (f == 0):
          return 'none'
        elif (f == 1):
          if (s <= 2):
            return '2d'
          else:
            return'3d'
        else:
          return 'dgps'

    # write header
    xmlData.write('<?xml version="1.0"?>' + '\n')
    # there must be only one top-level tag
    xmlData.write('<gpx' + "\n")
    xmlData.write('\t'+'version="1.1"' + '\n')
    xmlData.write('\t'+'creator="Nick Meehan">' + "\n")
    xmlData.write('\t'+'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' + '\n')
    xmlData.write('\t'+'xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">' + '\n')
    xmlData.write('\t'+'<time>'+datetime.datetime.utcnow().isoformat()+'</time>' + '\n') # e.g. 2002-02-27T17:18:33Z
    
    #write data to waypoints    
    rowNum = 0
    for row in csvData:
        if rowNum == 0:
            tags = row
            # replace spaces w/ underscores in tag names
            for i in range(len(tags)):
                tags[i] = tags[i].replace(' ', '')
                print tags[i]
        else:
            xmlData.write('\t'+'<wpt lat="'+latConvert(row[2])+'" lon="'+lonConvert(row[3])+'">'+'\n')
            xmlData.write('\t\t'+'<ele>'+row[4]+'</ele>'+'\n')
            xmlData.write('\t\t'+'<time>'+row[1]+'T'+row[0]+'</time>'+'\n')
            xmlData.write('\t\t'+'<name>'+row[10]+'</name>'+'\n')
            xmlData.write('\t\t'+'<sym>Dot</sym>'+'\n')
            xmlData.write('\t\t'+'<sat>'+row[9]+'</sat>'+'\n')
            xmlData.write('\t\t'+'<fix>'+fix(row[8], row[9])+'</fix>'+'\n')
            xmlData.write('\t\t'+'<src>Arduino Mega with GPS sheild</sat>'+'\n')
            #xmlData.write('\t'+'<sat>'+row[]+'</sat>'+'\n')
            xmlData.write('\t'+'</wpt>' + "\n")
        rowNum +=1

    xmlData.write('</gpx>' + '\n')
    xmlData.write('</xml>' + '\n')
    xmlData.close()



