import os
import csv
import json
import numpy as np
import numba as nb

primarySustain = ["Hu Tao", "Beidou", "Thoma", "Xinyan"]
secondarySustain = ["Xingqiu"]
fullSustain = ["Barbara", "Bennett", "Diona", "Dori", "Jean", "Shinobu", "Noelle", "Qiqi", "Kokomi", "Sayu", "Zhongli", "Layla", "Yaoyao"]
freezeTeamBans = ["dendro", "electro", "geo", "pyro"]

def setdiff2d_bc(arr1, arr2):
    idx = (arr1[:, None] != arr2).any(-1).all(1)
    return arr1[idx]

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("SANITIZING AND COMBINING ENTRIES TO SINGLE OUTPUT CSV")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

jsonFile = open("../genshin-impact-team-randomizer/src/data/characterData.json")

mainFileName = "genshinTeamsNamed.csv"
denyListFileName = "denyList.csv"
travelerReviewFileName = "reviewTravelerTeams.csv"
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

# Moving entries that are lacking proper sustain (will not be stable for majority of players) to denyList automatically
denyListAppend = np.empty((0, 4), str)
# Moving entries that have ambiguous traveler and need to be manually reviewed to reviewTravelerTeams automatically
travelerReview = np.empty((0, 4), str)

for filename in os.listdir(directory):
    processFile = os.path.join(directory, filename)
    if os.stat(processFile).st_size != 0:
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
            if charData["fullName"] != "Traveler":
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

        # Parse through data
        idx = -1
        for team in data:
            idx += 1
            # If team is just "Traveler" it needs to know what kind of Traveler contextually so for now it must go to auto review.
            if "Traveler" in team:
                travelerReview = np.concatenate((travelerReview,[team]),axis=0)
                data = np.delete(data, idx, axis=0)
                idx -= 1
                continue
            # If either has character in fullSustain or a character in secondarySustain AND primarySustain, continue
            if np.any(np.in1d(fullSustain, team)):
                continue
            if np.any(np.in1d(primarySustain, team)) and np.any(np.in1d(secondarySustain, team)):
                continue
            passFreezeCheck = True
            hasCryo = False
            hasHydro = False
            # Check if freeze team
            for character in team:
                # Must have a hydro and cryo, and no pyro, geo, electro, dendro
                for charData in characterData:
                    if character == charData["shortName"]:
                        if np.any(np.in1d(freezeTeamBans, charData["elements"])) or character == "Eula":
                            passFreezeCheck = False
                            break
                        if "cryo" in charData["elements"]:
                            hasCryo = True
                        if "hydro" in charData["elements"]:
                            hasHydro = True
                if passFreezeCheck == False:
                    break
            if hasCryo == False or hasHydro == False:
                passFreezeCheck = False
            if passFreezeCheck:
                continue
            # Otherwise add to denyList array
            denyListAppend = np.concatenate((denyListAppend,[team]),axis=0)
            # Remove from main array
            data = np.delete(data, idx, axis=0)
            idx -= 1

        mainData = np.append(mainData, data, axis=0)

        pf.close()

        print("CLEANING UP FILES")

        if os.path.exists(processFile[:-4] + "Filtered" + ".csv"):
            os.remove(processFile[:-4] + "Filtered" + ".csv")
        else:
            print(processFile[:-4] + "Filtered" + ".csv" + "does not exist")


# Remove bad Traveler teams
idx = -1
for team in travelerReview:
    idx += 1
    # If either has character in fullSustain or a character in secondarySustain AND primarySustain, continue
    if np.any(np.in1d(fullSustain, team)):
        continue
    if np.any(np.in1d(primarySustain, team)) and np.any(np.in1d(secondarySustain, team)):
        continue
    passFreezeCheck = True
    hasCryo = False
    hasHydro = False
    # Check if freeze team
    for character in team:
        # Must have a hydro and cryo, and no pyro, geo, electro, dendro
        for charData in characterData:
            if character == charData["shortName"]:
                if np.any(np.in1d(freezeTeamBans, charData["elements"])):
                    passFreezeCheck = False
                    break
        if passFreezeCheck == False:
            break
    if passFreezeCheck:
        continue
    # Remove from main array
    travelerReview = np.delete(travelerReview, idx, axis=0)
    idx -= 1

# Remove duplicates in Traveler Teams
uniqueConvert = [tuple(row) for row in travelerReview]
travelerReview = np.unique(uniqueConvert, axis=0)

# Append data to aggregatedTeams

print("SAVING OUTPUT CSV FILES")

np.savetxt("./outputs/" + "aggregatedTeams.csv", mainData, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)

# Append denyList array to deny list in append mode
with open(denyListFileName, "ab") as dla:
    np.savetxt(dla, denyListAppend, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)
    dla.close()
# Append to traveler list
with open(travelerReviewFileName, "ab") as tla:
    np.savetxt(tla, travelerReview, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)
    tla.close()

print("COMPLETE")