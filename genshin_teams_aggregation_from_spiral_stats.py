import os
import csv
import numpy as np

THRESHOLD = 5
directory = "../Spiral-Stats/data/raw_csvs"
destination = "./inputs"

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("PULLING DATA FROM SPIRAL STATS BY LVLURARTI")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

# For each file, open and convert

for filename in os.listdir(directory):

    print("PROCESSING FILE: " + filename)

    f = os.path.join(directory, filename)

    # Checking if it is a file
    if os.path.isfile(f) == False or "_char" in f or "lock" in f:
        print("SKIPPING FILE, NOT WHAT WE ARE LOOKING FOR")
        continue

    print("LOADING FILE DATA")
    fr = open(f, 'r')
    compArray = np.loadtxt(fr, delimiter=",", dtype=str)

    # Remove headers
    compArray = compArray[1:]
    fr.close()

    print("FILTERING CRITERIA AND FORMATTING")

    # Remove everything that is chamber 11
    inds = np.where(compArray == "11")
    compArray = np.delete(compArray, inds[0], axis=0)

    # Remove usage count column, uid, floor, chamber, half
    compArray = compArray[:, -4:]

    print("CONSOLIDATING TEAMS AND FILTERING LOW USAGE TEAMS")

    # Consolidate teams and add to count
    unq, cnt = np.unique(compArray, axis=0, return_counts=True)

    # After everything is consolidated, remove everything that has <5 uses
    compArray = unq[cnt >= THRESHOLD]

    print("EXPORTING RESULTS")

    resultFileName = filename[:-4] + "Processed" + ".csv"

    # Export to CSV
    resultPath = os.path.join(destination, resultFileName)

    np.savetxt(resultPath, compArray, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)

    print("EXPORT COMPLETE, OUTPUT FILE: " + resultFileName)

print("COMPLETE")