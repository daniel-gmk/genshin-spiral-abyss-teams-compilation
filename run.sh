#!/bin/sh

echo STARTING SCRIPTS
echo Updating Spiral-Stats repository

cd ../Spiral-Stats
git pull origin main
cd $OLDPWD

python ./genshin_teams_aggregation_from_gcsim.py
python ./genshin_teams_aggregation_from_spiral_stats.py
python ./genshin_teams_aggregation_from_akashadata.py
python ./genshin_teams_aggregation_from_mihoyo.py

python ./genshin_teams_filter_existing_teams.py
