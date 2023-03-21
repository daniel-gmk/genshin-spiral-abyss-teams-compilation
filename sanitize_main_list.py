import os
import csv
import json
import numpy as np
import numba as nb

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("SANITIZING AND COMBINING ENTRIES TO SINGLE OUTPUT CSV")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

mainFileName = "genshinTeamsNamed.csv"

print("LOADING MAIN CSV TO COMPARE AGAINST")

fr = open(mainFileName, 'r')
mainFileArray = np.loadtxt(fr, delimiter=",", dtype=str)
fr.close()

print("CLEANING UP FILES")

# Sorting

mainFileArrayShallowCopy = np.sort(mainFileArray[:, :-1], axis=1)

mainFileArray = np.hstack((mainFileArrayShallowCopy, mainFileArray[:, [-1]]))

mainFileArray = mainFileArray[np.lexsort((mainFileArray[:,3], mainFileArray[:,2],mainFileArray[:,1], mainFileArray[:,0]), axis=0)]

# Removing duplicates
uniqueConvert = [tuple(row) for row in mainFileArray]
mainFileArray = np.unique(uniqueConvert, axis=0)

# Append data to aggregatedTeams

print("SAVING OUTPUT CSV FILES")

np.savetxt("genshinTeamsNamed.csv", mainFileArray, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)

print("COMPLETE")