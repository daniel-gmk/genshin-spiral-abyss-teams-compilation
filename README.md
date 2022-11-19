# Genshin Impact Spiral Abyss Compilation of Valid Teams

This repository is for the game Genshin Impact.
It contains a curated csv file of valid teams to use in the Spiral Abyss.

&nbsp;

## Who uses this list?

- My Genshin Randomizer: https://spiralabyss.genshinteams.online/
- Forked and endorsed from Pustur's Genshin Randomizer: https://genshin-impact-team-randomizer.pages.dev/

&nbsp;

## Criteria

The criteria for a "valid team" will always be arbitrary, but the criteria used here is as follows:

- A supermajority of players (70%+) can use any team here and clear Spiral Abyss with 33-36 stars
- Players may have to swap around artifacts/weapons but most players have a "pool" of both to switch around

Likely setups the average player has includes:

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
- gcsim database
- Personal testing with above average setup

**Automated**

- Mihoyo's Lineup Simulator: Using the script `genshin_teams_aggregation_from_mihoyo.py`
- LvlUrArti's Spiral Stats repository: Using the script `genshin_teams_aggregation_from_spiral_stats.py`. Need to clone the repository from [here](https://github.com/piedorr/Spiral-Stats)

To start the entire automated process, I recommend creating a "inputs" and "outputs" folder in this repository, and using the Run.bat on Windows (or port it to a .sh script if you're on Mac or Linux). To ensure the script works you need the following folder structure:

```
Root
└───Spiral-Stats repository
│   └───data
│       └───raw_csvs
│               │Spiral Stats csvs
└─── This repository
        │ inputs folder (can be empty)
        │ outputs folder (can be empty)
        │ denyList.csv (This is a csv of comps from the automated sources that are to not be added or recommended)
        │ Python Scripts
        │ genshinTeamsNamed.csv
        │ Run.bat (or linux/mac equivalent)
```

&nbsp;

## Contributing

Pull requests will NOT be taken. A website is planned for user submission or omission requests. In the meantime if there is a team you feel is missing or one that does not meet the above criteria, please create an issue.

&nbsp;

## License

[MIT](https://choosealicense.com/licenses/mit/)
