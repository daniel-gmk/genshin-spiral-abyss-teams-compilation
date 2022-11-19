import os
import csv
import json
import numpy as np
import numba as nb

def setdiff2d_bc(arr1, arr2):
    idx = (arr1[:, None] != arr2).any(-1).all(1)
    return arr1[idx]

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("RUNNING TRAVELER SANITIZING/FILTERING SCRIPT")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

travelerReviewFileName = "reviewTravelerTeams.csv"
mainFileName = "genshinTeamsNamed.csv"

print("LOADING CSVS TO COMPARE AGAINST")

fr = open(travelerReviewFileName, 'r')
fr.readline()
fr.readline()
fr.readline()
fr.readline()
travelerReviewArray = np.loadtxt(fr, delimiter=",", dtype=str, ndmin=2)
travelerReviewArray = travelerReviewArray[1:]
travelerReviewArray = np.sort(travelerReviewArray)
fr.close()

if "Traveler" in travelerReviewArray:
    print("UNCHECKED TRAVELER FOUND, EXITING")
    exit(0)

fr = open(mainFileName, 'r')
mainFileArray = np.loadtxt(fr, delimiter=",", dtype=str)
mainFileArray = mainFileArray[1:]
mainFileArray = np.sort(mainFileArray)
fr.close()

print("REMOVING DATA ALREADY IN MAIN LIST OF TEAMS")

# Removing duplicates
uniqueConvert = [tuple(row) for row in travelerReviewArray]
travelerReviewArray = np.unique(uniqueConvert, axis=0)

travelerReviewArray = setdiff2d_bc(travelerReviewArray, mainFileArray)

print("WRITING NEW UPDATES TO TRAVELER CSV")

# Append to traveler list
with open(travelerReviewFileName, "w") as tla:
    tla.write("INSTRUCTIONS: Some teams do not have a specified Traveler type so we need to manually review.\nCopy all these values into the denyList so they do not show up again. Then change the Traveler to the following: \nTravelerElectro / TravelerAnemo / TravelerGeo / TravelerDendro. Lastly close this csv and run genshin_teams_traveler_sanitize.py\nAfter the script is finished open the csv and move the teams to the main list and save. DO NOT remove these instructions.\n")
    np.savetxt(tla, travelerReviewArray, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)
    tla.close()

print("COMPLETE")