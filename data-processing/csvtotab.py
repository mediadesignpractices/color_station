# First row of the csv file must be header!
# CSV to tab delimited spreadsheet


import csv
import datetime
import sys
import os

if len(sys.argv) != 2:
    os._exit(1)
path=sys.argv[1] # get folder as a command line argument
os.chdir(path)
if not os.path.exists('./txt'):
    os.makedirs('./txt')
csvFiles = [f for f in os.listdir('.') if f.endswith('.csv') or f.endswith('.CSV')]

for csvFile in csvFiles:
    txtFile = './txt/'+csvFile[:-4] + '.txt'
    csvData = csv.reader(open(csvFile))
    tabData = open(txtFile, 'w')

    csvData = csv.reader(open(csvFile))
    tabData = open(txtFile, 'w')

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

    # there must be only one top-level tag
    #write data to waypoints    
    rowNum = 0
    for row in csvData:
        if rowNum == 0:
            tags = row
            # replace spaces w/ underscores in tag names
            for i in range(len(tags)):
                tags[i] = tags[i].replace(' ', '')

        else:
            if row[11] :
                tabData.write(row[0]+'\t');
                tabData.write(row[9]+'\n');
        rowNum +=1
    tabData.close()
    print ('writing '+csvFile+' to '+ txtFile +'\n')
print ('finished writing '+str(len(csvFiles))+' .json Files\n')



