import os
import csv
import json
import numpy as np
import numba as nb

primarySustain = ["Hu Tao", "Beidou", "Thoma", "Layla", "Xinyan"]
secondarySustain = ["Xingqiu"]
fullSustain = ["Barbara", "Bennett", "Diona", "Dori", "Jean", "Shinobu", "Noelle", "Qiqi", "Kokomi", "Sayu", "Zhongli"]
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
mainFileArray = np.sort(mainFileArray)
fr.close()

# Moving entries that are lacking proper sustain (will not be stable for majority of players) to denyList automatically
denyListAppend = np.empty((0, 4), str)
# Moving entries that have ambiguous traveler and need to be manually reviewed to reviewTravelerTeams automatically
travelerReview = np.empty((0, 4), str)

print("CLEANING UP FILES")

# Removing duplicates
uniqueConvert = [tuple(row) for row in mainFileArray]
mainFileArray = np.unique(uniqueConvert, axis=0)

# Append data to aggregatedTeams

print("SAVING OUTPUT CSV FILES")

np.savetxt("genshinTeamsNamed.csv", mainFileArray, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)

print("COMPLETE")