import traceback
import pandas as pd
from browse import Browse
from fbref import Fbref
from fbref_constants import FbrefConstants
from pprint import pprint

try:
    browse = Browse()
    fbref = Fbref(browse)
    df = pd.DataFrame()
    base_url = "https://fbref.com/en/squads/"
    year = 2022
    while year > 2015:
        i = 0
        for team in FbrefConstants.TEAMS:
            team_id = FbrefConstants.TEAM_IDS[i]
            season = str(year-1) + '-' + str(year)
            team_stats_url = team.replace(' ', '-') + '-Stats'
            url = base_url + team_id + '/' + season + '/' + team_stats_url
            df_out = fbref.get_standard_stats(url=url, year=year, team=team, season=season)
            pprint(df_out)
            df = pd.concat([df, df_out])
            i+=1
        year-=1
except:
    traceback.print_exc()
finally:
    df.to_csv('./fantasy-premier-league/data/fbref_season_player_history.csv')
    browse.close()
