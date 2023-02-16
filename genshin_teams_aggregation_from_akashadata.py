#!env python

import csv
import json
import requests


def get_character_data():
    res = requests.get("https://t.akashadata.com/xstatic/json/static_card_dict.js").text
    return json.loads(res[res.find("=") + 1:])


def get_teams(usage_threshold, batch=100):
    teams = []

    while len(teams) < 1 or teams[-1]["team_count"] >= usage_threshold:
        res = requests.get("https://akashadata.com/get_team_list", params={
            "team_floor": 12,
            "start": len(teams),
            "length": batch,
        }).json()

        print(f"Teams requested: {(len(teams) + batch) * 2}")
        teams.extend(json.loads(res)["data"])

    return list(filter(lambda x: x["team_count"] >= usage_threshold, teams))


def fix_character_name(name):
    if name.startswith("traveler"):
        return "Traveler"

    try:
        return {
            "alhatham": "Alhaitham",
            "feiyan": "Yan Fei",
            "hutao": "Hu Tao",
            "pingzang": "Heizou",
            "shougun": "Raiden",
            "yaemiko": "Yae",
            "yunjin": "Yun Jin",
        }[name]
    except KeyError:
        return name.capitalize()


def process_team(team, character_data):
    return list(map(lambda i: fix_character_name(character_data[i]["icon"]), team.split(",")))


def flatten(li):
    return [item for sublist in li for item in sublist]


print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("PULLING DATA FROM AKASHA DATA")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

chars = get_character_data()
teams = get_teams(5)

out = flatten(
    [(process_team(t["up_cards"], chars), process_team(t["down_cards"], chars)) for t in teams]
)

with open("./inputs/genshinTeamsExportFromAkashaData.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(out)

print("COMPLETE")
