import os
import csv
import json
import numpy as np
import numba as nb

def setdiff2d_bc(arr1, arr2):
    idx = (arr1[:, None] != arr2).any(-1).all(1)
    return arr1[idx]

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("SANITIZING AND COMBINING ENTRIES TO SINGLE OUTPUT CSV")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

jsonFile = open("../genshin-impact-team-randomizer/src/data/characterData.json")

mainFileName = "genshinTeamsNamed.csv"
denyListFileName = "denyList.csv"
directory = "./inputs"
characterData = json.load(jsonFile)

print("LOADING MAIN CSV TO COMPARE AGAINST")

fr = open(mainFileName, 'r')
mainFileArray = np.loadtxt(fr, delimiter=",", dtype=str)
mainFileArray = mainFileArray[1:]
mainFileArray = np.sort(mainFileArray)
fr.close()

denyListArray = np.empty((0, 4), str)

if os.stat(denyListFileName).st_size != 0:
    print("LOADING DENY LIST FOR DENIED TEAMS")
    dr = open(denyListFileName, 'r')
    denyListArray = np.loadtxt(dr, delimiter=",", dtype=str, ndmin=2)
    denyListArray = np.sort(denyListArray)
    dr.close()

mainData = np.empty((0, 4), str)

for filename in os.listdir(directory):
    processFile = os.path.join(directory, filename)
    # Remove listings less than 4 rows
    print("REMOVING TEAMS WITH LESS THAN 4 CHARACTERS")

    with open(processFile, 'r') as infile, open(processFile[:-4] + "Filtered" + ".csv", 'w') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)
        for line in csv_reader:
            if all(line):
                csv_writer.writerow(line)

    pf = open(processFile[:-4] + "Filtered" + ".csv", 'r')
    data = np.loadtxt(pf, delimiter=",", dtype=str)

    # Convert to shorthand
    print("CONVERTING CHARACTER NAMES TO COMPATIBLE FORMAT")
    for charData in characterData:
        data[data == charData["fullName"]] = charData["shortName"]
    data = np.sort(data)

    # Removing duplicates
    uniqueConvert = [tuple(row) for row in data]
    data = np.unique(uniqueConvert, axis=0)
    
    # Remove entries that are already in main sheet and other sheets
    data = setdiff2d_bc(data, mainFileArray)
    data = setdiff2d_bc(data, mainData)
    if len(denyListArray) > 0:
        print("REMOVING DENY LIST ITEMS")
        data = setdiff2d_bc(data, denyListArray)

    mainData = np.append(mainData, data, axis=0)

    pf.close()

    print("CLEANING UP FILES")

    if os.path.exists(processFile[:-4] + "Filtered" + ".csv"):
        os.remove(processFile[:-4] + "Filtered" + ".csv")
    else:
        print(processFile[:-4] + "Filtered" + ".csv" + "does not exist")

print("SAVING OUTPUT CSV FILE")

np.savetxt("./outputs/" + "aggregatedTeams.csv", mainData, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)

print("COMPLETE")