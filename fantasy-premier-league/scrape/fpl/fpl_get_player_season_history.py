import requests, json
import pandas as pd

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

i=0
for id_x in df['id_x']:
    file_path_name = './data/fpl/' + str(id_x) + '.json'
    player = df[df['id_x']==id_x]
    player_name = player['first_name'][i] + ' ' + player['second_name'][i]
    uri = base_url + 'element-summary/' + str(id_x) + '/'
    id_x_resp = requests.get(base_url + 'element-summary/' + str(id_x) + '/').json()
    print(f"{id_x} Saving historical season data for {player_name}.") #.format(mean_legendary_hp - mean_not_legendary_hp))
    dfr = pd.DataFrame(id_x_resp['history_past'])
    dfr.insert(0, 'second_name', [player['second_name'][i] for j in range(len(dfr))])
    dfr.insert(0, 'first_name', [player['first_name'][i] for j in range(len(dfr))])
    dfr.insert(0, 'player_name', [player_name for j in range(len(dfr))])

    if ('season_name' in dfr.columns):
        dfr['season_year_ending'] = [2000+int(sn.split('/')[1]) for sn in dfr['season_name']]
        # print(df_fpl.head())
        df_fpl = pd.concat([df_fpl, dfr])
        # print(df_tmp.head())

    # dfr
    # result = dfr.to_json(orient='records')
    # parsed = json.loads(result)
    # json_str = json.dumps(parsed, indent=2)
    # f = open(file_path_name, 'w')
    # f.write(json_str)
    # f.close()
    i+=1
