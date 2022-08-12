import requests
import pandas as pd

player_positions = {
    'Goalkeeper': 'GK',
    'Defender': 'DF',
    'Midfielder': 'MF',
    'Forward': 'FW'
}

pd.set_option('display.max_columns', None)

# base url for all FPL API endpoints
base_url = 'https://fantasy.premierleague.com/api/'

# get data from bootstrap-static endpoint
r = requests.get(base_url+'bootstrap-static/').json()

# create players dataframe
players = pd.json_normalize(r['elements'])

# create teams dataframe
teams = pd.json_normalize(r['teams'])

# get position information from 'element_types' field
positions = pd.json_normalize(r['element_types'])

# join players to teams
df = pd.merge(
    left=players,
    right=teams,
    left_on='team',
    right_on='id'
)

# join player positions
df = df.merge(
    positions,
    left_on='element_type',
    right_on='id'
)

# rename columns
df = df.rename(
    columns={'name':'team_name', 'singular_name':'position_name'}
)

df_fpl = pd.DataFrame()
i=0
# iterate through each player, fetch data and add to dataframe
for id_x in df['id_x']:
    
    player = df[df['id_x']==id_x]
    player_name = player['first_name'][i] + ' ' + player['second_name'][i]
    print(f"Fetching historical season data for {player_name} [{id_x}]")
    uri = base_url + 'element-summary/' + str(id_x) + '/'
    
    # call the element-summary method on the fpl api to get the player's historical data
    id_x_resp = requests.get(base_url + 'element-summary/' + str(id_x) + '/').json()
    dfr = pd.DataFrame(id_x_resp['history_past'])
    
    # add player's name to dataframe
    dfr.insert(0, 'second_name', [player['second_name'][i] for j in range(len(dfr))])
    dfr.insert(0, 'first_name', [player['first_name'][i] for j in range(len(dfr))])
    dfr.insert(0, 'player_name', [player_name for j in range(len(dfr))])
    dfr.insert(0, 'player_position', [player_positions.get(player['position_name'][i]) for j in range(len(dfr))])

    # check if data return non-empty
    if ('season_name' in dfr.columns):
        # add 'season_year_ending' column
        dfr['season_year_ending'] = [2000+int(sn.split('/')[1]) for sn in dfr['season_name']]
        # union this player's data to overall dataframe
        df_fpl = pd.concat([df_fpl, dfr])

    i+=1

# save dataframe to csv file
df_fpl.to_csv('./fantasy-premier-league/data/fpl_season_player_history.csv')
