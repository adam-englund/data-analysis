import pandas as pd

# merge datasets from fbref and fpl and save to new csv file
df_fpl = pd.read_csv('./fantasy-premier-league/data/fbref/fbref_season_player_history.csv')
df_fbref = pd.read_csv('./fantasy-premier-league/data/fbref/fbref_season_player_history.csv')
df = pd.merge(df_fbref, df_fpl, left_on=['season_year_ending', 'player_name'], right_on=['season_year_ending', 'player_name'], how='left')
df.drop(df.columns[[0, 1]], axis=1, inplace=True)
df.drop(columns=['season_name'], axis=1, inplace=True)
df.to_csv('./fantasy-premier-league/data/fpl_fbref_season_player_history.csv')
