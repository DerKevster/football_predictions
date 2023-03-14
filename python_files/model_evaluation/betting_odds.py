# Imports bby
import pandas as pd
from python_files.feature_engineering.merge_dataframes import make_footballdatauk_DataFrames

# Function to generate df to show bet365 and pinnacle betting odds along date, teams, and result
def make_odds_df(league, season):
    # Extract features
    odds_df = make_footballdatauk_DataFrames()

    # Translate league names
    league_translator = {
    'BL' : 'BuLi',
    'PL' : 'Prem',
    'SA' : 'SerieA',
    'LL' : 'LaLiga'
    }

    league_translated = league_translator[league]
    odds_df = odds_df[f'{league_translated}_{season}.csv']

    # Strip whitespace from column names
    odds_df.columns = odds_df.columns.str.strip()

    # Sort by dates as datetime objects
    odds_df['Date'] = pd.to_datetime(odds_df['Date'], dayfirst=True)
    odds_df.sort_values(by='Date', ascending=True)

    # Get follwing Columns: 'Date', 'HomeTeam', 'away_team', 'B365H', 'B365D', 'B365A', 'PSH', 'PSD', 'PSA'
    odds_df = odds_df[['Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'PSH', 'PSD', 'PSA', 'FTR']]
    return odds_df
    # To convert odds to percentage: decimal percentage = (1 / odds) * 100
