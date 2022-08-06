import os
import pandas as pd

df_fpl = pd.DataFrame()
df_fbref = pd.read_csv('./data/fbref/fbref_players.csv')
print(df_fbref.head())

dir = './data/fpl/'
i=0
for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    if os.path.isfile(f):
        df_tmp = pd.read_json(f)
        if ('season_name' in df_tmp.columns):
            print(f + ' - ' + df_tmp[:1]['player_name'][0])
            df_tmp['season_year_ending'] = [2000+int(sn.split('/')[1]) for sn in df_tmp['season_name']]
            # print(df_fpl.head())
            df_fpl = pd.concat([df_fpl, df_tmp])
            # print(df_tmp.head())
        df = pd.merge(df_fbref, df_fpl, left_on=['season_year_ending', 'player_name'], right_on=['season_year_ending', 'player_name'], how='left')
    i+=1
df.drop(df.columns[[0, 1]], axis=1, inplace=True)
df.drop(columns=['season_name'], axis=1, inplace=True)
df.to_csv('./data/combined_season_player_history.csv')
