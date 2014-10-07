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
            # check if has correct coord
            coord = row[13].replace('(', '').replace(')', '').split(', ')
            if len(coord) == 2 :
                jsonData.write('\t\t'+'{'+'\n')
                jsonData.write('\t\t\t'+'"type": "Feature",'+'\n')
                jsonData.write('\t\t\t'+'"properties": {'+'\n')
                jsonData.write('\t\t\t\t'+'"name": "'+row[8]+'",'+'\n')
                jsonData.write('\t\t\t\t'+'"time": "'+row[2]+'T'+row[3]+'",'+'\n')
                jsonData.write('\t\t\t\t'+'"sym": "Dot"'+'\n')
                jsonData.write('\t\t\t'+'},'+'\n')
                jsonData.write('\t\t\t'+'"geometry": {'+'\n')
                jsonData.write('\t\t\t\t'+'"type": "Point",'+'\n')
                jsonData.write('\t\t\t\t'+'"coordinates": ['+'\n')
                jsonData.write('\t\t\t\t\t'+coord[1]+','+'\n')
                jsonData.write('\t\t\t\t\t'+coord[0]+','+'\n')
                jsonData.write('\t\t\t\t\t'+'0\n')
                jsonData.write('\t\t\t\t'+']\n')
                jsonData.write('\t\t\t'+'}\n')
                jsonData.write('\t\t'+'},\n')
        rowNum +=1

    jsonData.write('\t]' + '\n')
    jsonData.write('}' + '\n')
    jsonData.close()
    print ('writing '+csvFile+' to '+ jsonFile +'\n')
print ('finished writing '+str(len(csvFiles))+' .json Files\n')



