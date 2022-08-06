from numpy import NaN
import pandas as pd


class Fbref: 
    
    ################################################################################
    def __init__(self, browse):
        """Class Constructor"""
        self.browse = browse

    ################################################################################
    def get_standard_stats(self, url, year, season, team):
        """
        Returns pandas dataframe parsed from a club's standard stats table in html from fbref.com
        """
        
        print('Fetching {}'.format(url))
        
        self.browse.get(url)

        division = self.browse.find_by_css('div#meta h1 span.header_end').get_attribute('innerHTML')
        division = division.strip('\s\t\n\r()')

        #swe = self.browse.find_by_css('div#all_stats_standard table.stats_table tbody tr:not(.thead):not(.spacer)')
        swe = self.browse.find_by_css('div#all_stats_standard table.stats_table')
        html = swe.get_attribute('outerHTML')
        df = pd.read_html(html)[0]

        # drop duplicate header rows and match logs column
        df = df[df[("Unnamed: 0_level_0","Player")]!="Player"].reset_index(drop=True)
        df = df[df[("Unnamed: 1_level_0","Nation")].isnull() == False].reset_index(drop=True)
        df.drop(columns="Matches", level=1, inplace=True)

        # convert column types to numeric where applicable
        df.apply(pd.to_numeric, errors='ignore')

        df.insert(0, 'team', team, allow_duplicates=False)
        df.insert(0, 'division', division, allow_duplicates=False)
        df.insert(0, 'season', season, allow_duplicates=False)
        df.insert(0, 'season_year_ending', year, allow_duplicates=False)

        # some leagues don't have 'expected' stats, add columns manually with default values
        if (len(df.columns) < 25):
            df['xg'] = NaN
            df['npxg'] = NaN
            df['xa'] = NaN
            df['npxg_xa'] = NaN
            df['xg_per90'] = NaN
            df['xa_per90'] = NaN
            df['xg_xa_per90'] = NaN
            df['npxg_per90'] = NaN
            df['npxg_xa_per90'] = NaN

        cols = [
            'season_year_ending', 'season', 'division', 'team',  # new columns
            'player_name', 'nationality', 'position', 'age',  # unnamed
            'games', 'games_starts', 'minutes', 'nbr_90s',  # playing time
            'goals', 'assists', 'non_penalty_goals', 'penalties_successful', 'penalties_attempted', 'cards_yellow', 'cards_red',  # performance
            'goals_per90', 'assists_per90', 'goals_assists_per90', 'goals_pens_per90', 'goals_assists_pens_per90',  # performance/90
            'xg', 'npxg', 'xa', 'npxg_xa',  # expected
            'xg_per90', 'xa_per90', 'xg_xa_per90', 'npxg_per90', 'npxg_xa_per90'  # expected/90
        ]
        df.columns = cols

        # Clean up 'nationality' text
        df['nationality'] = df['nationality'].apply(lambda n : n  if (len(n.split(' ')) < 2) else n.split(' ')[1])

        #dfPer90 = df["Per 90 Minutes"].add_suffix('/90')

        return df
