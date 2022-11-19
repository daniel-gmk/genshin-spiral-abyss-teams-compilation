@echo off
python ./genshin_teams_aggregation_from_spiral_stats.py
python ./genshin_teams_aggregation_from_mihoyo.py
python ./genshin_teams_filter_existing_teams.py
pause