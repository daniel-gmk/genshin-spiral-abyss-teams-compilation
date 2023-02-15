# Genshin Impact Spiral Abyss Compilation of Valid Teams

This repository is for the game Genshin Impact.
It contains a curated csv file of valid teams to use in the Spiral Abyss.

&nbsp;

## Who uses this list or the randomizer?

- My Genshin Randomizer: https://spiralabyss.genshinteams.online/
- Forked and endorsed from Pustur's Genshin Randomizer: https://genshin-impact-team-randomizer.pages.dev/
- A bunch of Genshin streamers who love the randomizer
- Wangsheng Funeral Parlor Discord (Command to get link is !!abyssrandomizer)

&nbsp;

## Criteria

The criteria for a "valid team" will always be arbitrary, but the criteria used here is as follows:

- A supermajority of players (70%+) can use any team here and clear Spiral Abyss with 33-36 stars
- Players may have to swap around artifacts/weapons but most players have a "pool" of both to switch around

Likely setups the average AR55+ player has includes:

- 5\* star characters + weapons (C1 / R1)
- 4\* star characters + weapons (C2-C6 / R2-R6)
- A mix of level 80+ characters (5* star or important 4* star characters)
- A mix of level 70+ characters (important 4\* star characters)
- 4th ascension (60/70) support characters
- Talent levels 6+ on most above characters for key abilities

&nbsp;

## Aggregation Method

Currently the data here is supplied by the following:

**Manual**

- Keqingmains character guides
- Personal testing with above average setup

**Automated**

- Mihoyo's Lineup Simulator: Using the script `genshin_teams_aggregation_from_mihoyo.py`
- LvlUrArti's Spiral Stats repository: Using the script `genshin_teams_aggregation_from_spiral_stats.py`. Need to clone the repository from [here](https://github.com/piedorr/Spiral-Stats)
- gcsim.app: Using the script `genshin_teams_aggregation_from_gcsim.py`
- CN Akasha Data: Using the script `genshin_teams_aggregation_from_akashadata`

To start the entire automated process, you MUST:

1. Install Python requirements by running `pip install -r requirements.txt`
2. Create the file structure shown below
3. Run `Run.bat` on Windows or `run.sh` on Linux/MacOS

```
Root
└───Genshin Randomizer (Gottsmillk ver) repository
│   └───src
│       └───data
│               │characterData.json
└───Spiral-Stats repository
│   └───data
│       └───raw_csvs
│               │Spiral Stats csvs
└─── This repository
        │ inputs folder
        │ outputs folder
        │ denyList.csv (This is a csv of comps from the automated sources that are to not be added or recommended)
        │ Python Scripts
        │ genshinTeamsNamed.csv
        │ Run.bat
        │ run.sh
        | Sanitize.bat
        | sanitize.sh
```

Once everything finishes running, you will have the following outputs:

- aggregatedTeams.csv: Contains a filtered list of teams that do not already exist in the main list and guarantee some form of sustain. Add to the genshinTeamsNamed.csv and then sanitize/sort with Sanitize.bat

- denyList.csv: It is already populated, but will be appended with teams that the script deems may not have sustain, but can be manually added to the main list to override and ensure it is added.

- reviewTravelerTeams.csv: Some teams do not have a specified Traveler type so we need to manually review. Copy all these values into the denyList AS IS (with just Traveler) so they do not show up again. Then change the Traveler to the following: TravelerElectro / TravelerAnemo / TravelerGeo / TravelerDendro. Lastly close the csv and run genshin_teams_traveler_sanitize.py. After the script is finished open the csv and move the teams to the main list and save.

&nbsp;

## Contributing

Pull requests will NOT be taken. A website is planned for user submission or omission requests. In the meantime if there is a team you feel is missing or one that does not meet the above criteria, please create an issue.

&nbsp;

## License

[MIT](https://choosealicense.com/licenses/mit/)
