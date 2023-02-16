#!env python

from bs4 import BeautifulSoup
import csv
import re
import requests


def fix_character_name(name):
    if name.startswith("Traveler"):
        return re.sub(" |\(|\)", "", name)

    try:
        return {
            "Kuki Shinobu": "Shinobu",
            "Yae Miko": "Yae",
        }[name]
    except KeyError:
        return name


def parse_characters(team_el):
    char_els = team_el.find_all(class_="character-name")
    return [fix_character_name(char_el.text) for char_el in char_els]


def parse_teams(tier_el):
    team_els = tier_el.find_all("div", class_="character-list")
    return [parse_characters(team_el) for team_el in team_els]


print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("PULLING DATA FROM GENSHIN.GG")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


page = requests.get("https://genshin.gg/teams/")
document = BeautifulSoup(page.content, "html.parser")
tier_els = document.find_all("div", class_="tier-list-teams")

out = [parse_teams(tier_el) for tier_el in tier_els]


for i, suffix in enumerate(["Top", "Other"]):
    file_name = "genshinTeamsExportFromGenshinGG" + suffix
    with open(f"./inputs/{file_name}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(out[i])


print("COMPLETE")
