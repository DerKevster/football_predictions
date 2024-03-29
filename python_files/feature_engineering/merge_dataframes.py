#! Script to generate all dataframes from raw_data folder and extract the following columns from footballdata.co.uk to merge with the transfermarkt data:
# Imports bby
import re
import os
import pandas as pd
import numpy as np
import datetime as dt
from os.path import expanduser
from python_files.feature_engineering.teams_list import standard_all_teams
from python_files.feature_engineering.team_translator import *

# Generate all dfs from raw_data folder
HOME = expanduser("~")

def make_footballdatauk_DataFrames():
    # assign path
    file_count = 0
    dataframes = {}
    for path, dirs, files in os.walk(os.path.join(HOME, "code", "DerKevster", "football_predictions", "raw_data", "football-data_co_uk")):
        file_count = len(files)
        # appned dfs to dict using file names as keys
        for i in range(file_count):
            dataframes[files[i]] = pd.read_csv(os.path.join(HOME, "code", "DerKevster", "football_predictions", "raw_data", "football-data_co_uk", files[i]))
    return dataframes

def make_transfermarkt_DataFrames():
    # assign path
    file_count = 0
    dataframes = {}
    for (path, dirs, files) in os.walk(os.path.join(HOME, "code", "DerKevster", "football_predictions","raw_data", "data-transfermarkt")):
        file_count = len(files)
        # appned dfs to dict using file names as keys
        for i in range(file_count):
           # dataframes[files[i]] = pd.read_csv(os.path.join("../raw_data/data-transfermarkt/", files[i]))
            dataframes[files[i].replace('.csv', '')] = pd.read_csv(os.path.join(HOME, "code", "DerKevster", "football_predictions", "raw_data", "data-transfermarkt", files[i]))
    return dataframes

def make_footballdata_df_to_merge(league, season):
    # Extract features from BuLi_18-19
    footballdata_dfs = make_footballdatauk_DataFrames()

    # Translate league names
    league_translator = {
    'BL' : 'BuLi',
    'PL' : 'Prem',
    'SA' : 'SerieA',
    'LL' : 'LaLiga'
    }

    league_translated = league_translator[league]
    league_season_df = footballdata_dfs[f'{league_translated}_{season}.csv']
    # Strip whitespace from column names
    league_season_df.columns = league_season_df.columns.str.strip()
    # Sort by dates as datetime objects
    league_season_df['Date'] = pd.to_datetime(league_season_df['Date'], dayfirst=True)
    league_season_df.sort_values(by='Date', ascending=True)
    # Get follwing Columns: 'Date' 'HomeTeam' 'HC' 'AC' 'HS' 'HST' 'AS' 'AST' in a df to merge with transfermarkt data
    footballdata_df_to_merge = league_season_df[['Date', 'HomeTeam', 'HC', 'AC', 'HS', 'HST', 'AS', 'AST']]
    return footballdata_df_to_merge


def make_tranfermarkt_df_to_merge(league, season):
    # League translation
    league_translator = {
    "BL":"L1",
    "PL":"GB1",
    "LL":"ES1",
    "SA":"IT1"
    }
    league = league_translator[league]

    # Season translator
    season = int(f"20{season[:2]}")

    # Extract Features from Transfermarkt
    transfermarkt_df = make_transfermarkt_DataFrames()
    # Get Games and Clubs
    games = transfermarkt_df["games"]
    clubs = transfermarkt_df["clubs"]
    clubs_clean = clubs[["club_id", "name"]]
    games_clean = games[["game_id", "round", "competition_id", "season", "date", "home_club_id", "away_club_id", "home_club_goals", "away_club_goals"]]
    games_clean.loc[:, "date"] = pd.to_datetime(games_clean.loc[:, "date"])

    # Select the league
    league_games = games["competition_id"] == league
    league_df = games_clean[ league_games]

    # Select season
    season =  league_df["season"] == season
    league_season = league_df[season]
    league_season_sorted = league_season.sort_values(by=["home_club_id", "date"])

    #drop duplicates
    league_season_final = league_season_sorted.drop_duplicates(subset=["date", "home_club_id"])

    #merge by combining club id and club name
    league_final = league_season_final.merge(clubs_clean, left_on="home_club_id", right_on="club_id")
    league_final = league_final.merge(clubs_clean, left_on="away_club_id", right_on="club_id")
    league_final = league_final.rename(columns= {"name_x":"HomeTeam", "name_y":"away_team", "date" : "Date"})
    league_final = league_final.drop(columns=["club_id_x", "club_id_y"])
    return league_final.sort_values(by='Date')

def make_squad_value_df(season):
    season = int(f"20{season[:2]}")
    transfermarkt_df = make_transfermarkt_DataFrames()

    # Get both DataFrames
    player_valuation = transfermarkt_df["player_valuations"]
    games = transfermarkt_df["games"]
    clubs = transfermarkt_df["clubs"]

    # Merge the tables
    games_date = games[["date", "season", "home_club_id", "competition_id"]]
    clubs_clean = clubs[["club_id", "name", "domestic_competition_id"]]
    player_full = games_date.merge(player_valuation, on="date")

    # Get the max market value per player
    player_full_max = player_full.groupby(["season", "current_club_id", "player_id"])["market_value_in_eur"].max().reset_index()

    # Get the sum of the players
    max_squad_value = player_full_max.groupby(["current_club_id", "season"]).sum().reset_index()
    squad_val = max_squad_value[["current_club_id", "season", "market_value_in_eur"]]

    # Merge tables to get the club names relativley to their club id
    squad_value = squad_val.merge(clubs_clean, left_on="current_club_id", right_on="club_id")

    # Cleaning up the Data Table
    squad_value = squad_value.drop(columns="current_club_id")
    squad_value_final = squad_value[["name", "season", "market_value_in_eur", "club_id", "domestic_competition_id"]]
    squad_value_final["season"] = squad_value_final["season"].astype("int")

    # Change the squad names from transfermarkt names to football-db names
    bl_translator = tf_to_fb_translator("BL")
    pl_translator = tf_to_fb_translator("PL")
    ll_translator = tf_to_fb_translator("LL")
    sa_translator = tf_to_fb_translator("SA")
    squad_value_final = squad_value_final.replace(to_replace=bl_translator)
    squad_value_final = squad_value_final.replace(to_replace=pl_translator)
    squad_value_final = squad_value_final.replace(to_replace=ll_translator)
    squad_value_final = squad_value_final.replace(to_replace=sa_translator)
    season_mask = squad_value_final['season'] == season
    squad_value_final = squad_value_final[season_mask]
    return squad_value_final

# the next function merges the transfermarkt and footballdata data into one dataframe so we cna extract the cumulative sums of the previous five days
def make_fifa_DataFrames():
    # assign path
    file_count = 0
    dataframes = {}
    for path, dirs, files in os.walk(os.path.join(HOME, "code", "DerKevster", "football_predictions", "raw_data", "fifa-data")):
        file_count = len(files)
        # appned dfs to dict using file names as keys
        for i in range(file_count):
            dataframes[files[i]] = pd.read_csv(os.path.join(HOME, "code", "DerKevster", "football_predictions", "raw_data", "fifa-data", files[i]))
    return dataframes

# Function to clean the FIFA data
def clean_FIFA_df(df):

    # Drop some unecessary functions
    clean_df = df.drop(columns=['ID', 'Photo', 'Flag', 'Club Logo', 'Special',
    'Preferred Foot', 'Skill Moves', 'Work Rate', 'Body Type', 'Real Face', 'Loaned From', 'Best Overall Rating'])

    # define a function to strip HTML tags
    def strip_tags(text):
        return re.sub('<[^<]+?>', '', str(text))

    # apply the function to the 'text' column of the dataframe
    clean_df['Position'] = clean_df['Position'].apply(strip_tags)

    # create a function to map the position to the part of the team
    def get_part(position):
        if position in ['LB', 'RCB', 'LCB', 'RB', 'LWB', 'RWB', 'CB', 'GK']:
            return 'Defense'
        elif position in ['RCM', 'CAM', 'LDM', 'RDM', 'LCM', 'CDM', 'LM', 'CM', 'RM', 'LAM', 'RAM']:
            return 'Midfield'
        elif position in ['RS', 'RW', 'ST', 'LS', 'LW', 'CF', 'LF', 'RF']:
            return 'Attack'
        elif position in ['SUB', 'RW']:
            return 'Bench'
        elif position in ['RES', 'nan', ]:
            return 'Delete'
        else:
            return 'Unknown'

    # apply the function to the 'Position' column of the dataframe to make a new column
    clean_df['Field'] = clean_df['Position'].apply(get_part)

    # Drop the ones with "Delete" in the Column "Field"
    clean_df = clean_df[clean_df.Field != 'Delete']
    translator = fifa_to_fb_translator()
    clean_df = clean_df.replace(to_replace = translator)
    return clean_df

def make_merged_df(league, season):
  import warnings; warnings.filterwarnings("ignore")
  football_df = make_footballdata_df_to_merge(league, season)
  tmarkt_df = make_tranfermarkt_df_to_merge(league, season)

  # Get teams
  translator = tf_to_fb_translator(league)
  tmarkt_df = tmarkt_df.replace(to_replace=translator)

  merged_df = tmarkt_df.merge(football_df, on=["Date", "HomeTeam"])
  merged_df.drop(columns=["game_id", "competition_id", "season", "home_club_id", "away_club_id"], inplace=True)
  merged_df[['Date','round', 'HomeTeam', 'away_team', 'home_club_goals', 'away_club_goals', 'HC', 'AC', 'HS', 'HST', 'AS', 'AST']]
  merged_df['round'] = merged_df['round'].map(lambda round: round.strip(". Matchday")).map(lambda number: int(number))
  merged_df=merged_df.rename(columns={'round':'matchday'})
  merged_df = merged_df.sort_values(by = 'Date')
  merged_df = merged_df.reset_index().drop(columns = "index")
  return merged_df

# Choose a specific FIFA dataframe by giving a season
def make_fifa_df(season):
    sea = season[-2:]
    df = make_fifa_DataFrames()[f'FIFA{sea}_official_data.csv']

    # Clean the data
    clean_df = clean_FIFA_df(df)
    return clean_df
