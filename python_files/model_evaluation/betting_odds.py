# Imports bby
import pandas as pd
from python_files.feature_engineering.merge_dataframes import make_footballdatauk_DataFrames

# Function to generate df to show bet365 and pinnacle betting odds along date, teams, and result
def make_betting_odds_df(league, season, proba=False):
    # Extract features
    betting_odds_df = make_footballdatauk_DataFrames()

    # Translate league names
    league_translator = {
    'BL' : 'BuLi',
    'PL' : 'Prem',
    'SA' : 'SerieA',
    'LL' : 'LaLiga'
    }

    league_translated = league_translator[league]
    betting_odds_df = betting_odds_df[f'{league_translated}_{season}.csv']

    # Strip whitespace from column names
    betting_odds_df.columns = betting_odds_df.columns.str.strip()

    # Sort by dates as datetime objects
    betting_odds_df['Date'] = pd.to_datetime(betting_odds_df['Date'], dayfirst=True)
    betting_odds_df.sort_values(by='Date', ascending=True)

    # Get follwing Columns: 'Date', 'HomeTeam', 'away_team', 'B365H', 'B365D', 'B365A', 'PSH', 'PSD', 'PSA'
    betting_odds_df = betting_odds_df[['Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', 'PSH', 'PSD', 'PSA', 'FTR']]

    if proba:
        columns = ['B365H', 'B365D', 'B365A', 'PSH', 'PSD', 'PSA']

        for col in columns:
            betting_odds_df[col] = (1 / betting_odds_df[col])

    return betting_odds_df
    # To convert odds to percentage: decimal_percentage = (1 / odds)
