# First row of the csv file must be header!


import csv
import datetime
import sys
import os

if len(sys.argv) != 2:
    os._exit(1)
path=sys.argv[1] # get folder as a command line argument
os.chdir(path)
if not os.path.exists('./json'):
    os.makedirs('./json')
csvFiles = [f for f in os.listdir('.') if f.endswith('.csv') or f.endswith('.CSV')]

for csvFile in csvFiles:
    jsonFile = './json/'+csvFile[:-4] + '.geo.json'
    csvData = csv.reader(open(csvFile))
    jsonData = open(jsonFile, 'w')

    csvData = csv.reader(open(csvFile))
    jsonData = open(jsonFile, 'w')

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
    jsonData.write('{' + '\n')
    jsonData.write('\t'+'"type": "FeatureCollection",' + '\n')
    jsonData.write('\t'+'"features": [' + '\n')

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
                jsonData.write('\t\t'+'{'+'\n')
                jsonData.write('\t\t\t'+'"type": "Feature",'+'\n')
                jsonData.write('\t\t\t'+'"properties": {'+'\n')
                jsonData.write('\t\t\t\t'+'"time": "'+row[1]+'",'+'\n')
                jsonData.write('\t\t\t\t'+'"color_temp": "'+row[10]+'",'+'\n')
                jsonData.write('\t\t\t\t'+'"lux": "'+row[11]+'",'+'\n')
                jsonData.write('\t\t\t\t'+'"rgbc": "'+row[12]+','+row[13]+','+row[14]+','+row[15]+'",'+'\n')
                jsonData.write('\t\t\t\t'+'"sat": "'+row[9]+'",'+'\n')
                jsonData.write('\t\t\t\t'+'"fix": "'+fix(row[8], row[9])+'",'+'\n')
                jsonData.write('\t\t\t\t'+'"sym": "Dot"'+'\n')
                jsonData.write('\t\t\t'+'},'+'\n')
                jsonData.write('\t\t\t'+'"geometry": {'+'\n')
                jsonData.write('\t\t\t\t'+'"type": "Point",'+'\n')
                jsonData.write('\t\t\t\t'+'"coordinates": ['+'\n')
                jsonData.write('\t\t\t\t\t'+lonConvert(row[3])+','+'\n')
                jsonData.write('\t\t\t\t\t'+latConvert(row[2])+','+'\n')
                jsonData.write('\t\t\t\t\t'+row[4]+'\n')
                jsonData.write('\t\t\t\t'+']\n')
                jsonData.write('\t\t\t'+'}\n')
                jsonData.write('\t\t'+'},\n')
        rowNum +=1

    jsonData.write('\t]' + '\n')
    jsonData.write('}' + '\n')
    jsonData.close()
    print ('writing '+csvFile+' to '+ jsonFile +'\n')
print ('finished writing '+str(len(csvFiles))+' .json Files\n')



