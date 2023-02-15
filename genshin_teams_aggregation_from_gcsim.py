import json
import requests
import numpy as np

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("PULLING DATA FROM GCSIM DATABASE")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


print("QUERYING GCSIM API FOR LIST OF CHARACTERS")
# Query https://db.gcsim.app/api/db/ for all characters
r =requests.get('https://db.gcsim.app/api/db/')

characterList = r.json()
teamsList = []

mappings = {
    "yunjin": "Yun Jin",
    "yaemiko": "Yae",
    "kuki": "Shinobu",
    "hutao": "Hu Tao",
    "aetheranemo": "TravelerAnemo",
    "aethergeo": "TravelerGeo",
    "aetherelectro": "TravelerElectro",
    "aetherdendro": "TravelerDendro",
    "lumineanemo": "TravelerAnemo",
    "luminegeo": "TravelerGeo",
    "lumineelectro": "TravelerElectro",
    "luminedendro": "TravelerDendro"
}

# For each character 
for character in characterList:
    characterName = character["avatar_name"]
    print("RETRIEVING AND FORMATTING DATA FOR: " + characterName)

    # Call https://db.gcsim.app/api/db/CHARACTER
    cr =requests.get('https://db.gcsim.app/api/db/' + characterName)
    characterData = cr.json()
    for rawTeamData in characterData:
        # Pull each object and convert each metadata attribute to json object
        # Grab char_names attribute from metadata, which is an array
        team = json.loads(rawTeamData["metadata"])["char_names"]
        newTeam = []
        for character in team:
            newCharacter = character
            # Convert mappings, if not mapping needed just Capitalize
            if character in mappings.keys():
                newCharacter = mappings[newCharacter]
            else:
                newCharacter = character.capitalize()
            newTeam.append(newCharacter)
        teamsList.append(newTeam)

print("SANITIZING TEAMS")
# Remove teams less than 4

teamsList = np.array([row for row in teamsList if len(row)==4])

# Convert to Numpy array
teamsListNP = np.array(teamsList, dtype=str)

# Remove duplicates in teams
uniqueConvert = [tuple(row) for row in teamsListNP]
teamsListNP = np.unique(uniqueConvert, axis=0)

print("EXPORTING TO CSV")

# Append to traveler list
with open("./inputs/genshinTeamsExportFromGcsim.csv", "w") as f:
    np.savetxt(f, teamsListNP, fmt='%s', delimiter=',', newline='\n', header='', footer='', comments='# ', encoding=None)
    f.close()

print("COMPLETE")