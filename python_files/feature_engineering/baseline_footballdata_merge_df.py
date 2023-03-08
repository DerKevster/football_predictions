#! Script to generate all dataframes from raw_data folder and extract the following columns from footballdata.co.uk to merge with the transfermarkt data:
# Imports bby
import re
import os
import pandas as pd
import numpy as np
import datetime as dt
from os.path import expanduser

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
            dataframes[files[i]] = pd.read_csv(os.path.join(os.getcwd(), "raw_data", "football-data_co_uk", files[i]))
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
            dataframes[files[i].replace('.csv', '')] = pd.read_csv(os.path.join(os.getcwd(), "raw_data", "data-transfermarkt", files[i]))
    return dataframes

def transfermarkt_2018_2019():

    # Extract Features from Transfermarkt

    transfermarkt_df = make_transfermarkt_DataFrames()

    # Get Games and Club_Games
    games = transfermarkt_df["games"]
    clubs = transfermarkt_df["clubs"]
    clubs_clean = clubs[["club_id", "name"]]

    games_clean = games[["game_id", "competition_id", "season", "date", "home_club_id", "away_club_id", "home_club_goals", "away_club_goals"]]

    # Select the Bundesliga (L1)
    bundesliga_games = games["competition_id"] == "L1"
    bundesliga_df = games_clean[bundesliga_games]

    # Select season 2018/19
    season_2018 = bundesliga_df["season"] == 2018

    bundesliga_2018 = bundesliga_df[season_2018]

    bundesliga_2018_sorted = bundesliga_2018.sort_values(by=["home_club_id", "date"])

    bundesliga_final18 = bundesliga_2018_sorted.drop_duplicates(subset=["date", "home_club_id"])

    bund = bundesliga_final18.merge(clubs_clean, left_on="home_club_id", right_on="club_id")
    bundesliga_final = bund.merge(clubs_clean, left_on="away_club_id", right_on="club_id")
    bundesliga_final = bundesliga_final.rename(columns= {"name_x":"home_team", "name_y":"away_team"})
    bundesliga_final = bundesliga_final.drop(columns=["club_id_x", "club_id_y"])

    return bundesliga_final



def make_BuLi_18_19_df_to_merge():
    # Extract features from BuLi_18-19
    footballdata_dfs = make_footballdatauk_DataFrames()
    BuLi_18_19_df = footballdata_dfs['BuLi_18-19.csv']
    # Strip whitespace from column names
    BuLi_18_19_df.columns = BuLi_18_19_df.columns.str.strip()
    # Sort by dates as datetime objects
    BuLi_18_19_df['Date'] = pd.to_datetime(BuLi_18_19_df['Date'], dayfirst=True)
    BuLi_18_19_df.sort_values(by='Date', ascending=True)
    # Get follwing Columns: 'Date' 'HomeTeam' 'HC' 'AC' 'HS' 'HST' 'AS' 'AST' in a df to merge with transfermarkt data
    footballdata_df_to_merge = BuLi_18_19_df[['Date', 'HomeTeam', 'HC', 'AC', 'HS', 'HST', 'AS', 'AST']]
    return footballdata_df_to_merge

def transfermarkt_2018_2019():
    # Extract Features from Transfermarkt
    transfermarkt_df = make_transfermarkt_DataFrames()
    # Get Games and Clubs
    games = transfermarkt_df["games"]
    clubs = transfermarkt_df["clubs"]
    clubs_clean = clubs[["club_id", "name"]]
    games_clean = games[["game_id", "round", "competition_id", "season", "date", "home_club_id", "away_club_id", "home_club_goals", "away_club_goals"]]
    games_clean.loc[:, "date"] = pd.to_datetime(games_clean.loc[:, "date"])

    # Select the Bundesliga (L1)
    bundesliga_games = games["competition_id"] == "L1"
    bundesliga_df = games_clean[bundesliga_games]

    # Select season 2018/19
    season_2018 = bundesliga_df["season"] == 2018
    bundesliga_2018 = bundesliga_df[season_2018]
    bundesliga_2018_sorted = bundesliga_2018.sort_values(by=["home_club_id", "date"])

    #drop duplicates
    bundesliga_final18 = bundesliga_2018_sorted.drop_duplicates(subset=["date", "home_club_id"])

    #merge by combining club id and club name
    bund = bundesliga_final18.merge(clubs_clean, left_on="home_club_id", right_on="club_id")
    bundesliga_final = bund.merge(clubs_clean, left_on="away_club_id", right_on="club_id")
    bundesliga_final = bundesliga_final.rename(columns= {"name_x":"HomeTeam", "name_y":"away_team", "date" : "Date"})
    bundesliga_final = bundesliga_final.drop(columns=["club_id_x", "club_id_y"])
    #rename for merge later with footballdata data
    renamed_columns = {
        '1 Fc Nurnberg' : "Nurnberg",
        'Bayer 04 Leverkusen': "Leverkusen",
        'Borussia Dortmund': "Dortmund",
        'Borussia Monchengladbach': "M'gladbach",
        'Eintracht Frankfurt': "Ein Frankfurt",
        'Fc Bayern Munchen' : "Bayern Munich",
        'Fc Schalke 04': "Schalke 04",
        'Fortuna Dusseldorf': "Fortuna Dusseldorf",
        'Hannover 96': "Hannover 96",
        'Hertha Bsc' : "Hertha",
        'Sc Freiburg' : "Freiburg",
        'Vfb Stuttgart': "Stuttgart",
        'Vfl Wolfsburg' : "Wolfsburg",
        'Sv Werder Bremen': "Werder Bremen",
        'Fc Augsburg': "Augsburg",
        'Tsg 1899 Hoffenheim': "Hoffenheim",
        'Rasenballsport Leipzig': "RB Leipzig",
        '1 Fsv Mainz 05': "Mainz"
    }
    bundesliga_renamed = bundesliga_final.replace(to_replace=renamed_columns)
    return bundesliga_renamed.sort_values(by='Date')

# the next function merges the transfermarkt and footballdata data into one dataframe so we cna extract the cumulative sums of the previous five days

def make_merged_df():
    buli_df = make_BuLi_18_19_df_to_merge()
    tmarkt_df = transfermarkt_2018_2019()

    merged_df = tmarkt_df.merge(buli_df, on=["Date", "HomeTeam"])
    merged_df.drop(columns=["game_id", "competition_id", "season", "home_club_id", "away_club_id"], inplace=True)
    merged_df[['round', 'HomeTeam', 'away_team', 'home_club_goals', 'away_club_goals', 'HC', 'AC', 'HS', 'HST', 'AS', 'AST']]
    merged_df['round'] = merged_df['round'].map(lambda matchday: matchday.strip(". Matchday")).map(lambda number: int(number))
    return merged_df

def baseline_df(Home, Away, Date):
    base_df = make_merged_df()
