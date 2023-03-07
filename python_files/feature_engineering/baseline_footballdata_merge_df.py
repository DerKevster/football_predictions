#! Script to generate all dataframes from raw_data folder and extract the following columns from footballdata.co.uk to merge with the transfermarkt data:

# Imports bby
import os
import pandas as pd
import numpy as np
import datetime as dt

# Generate all dfs from raw_data folder

def make_footballdatauk_DataFrames():
    # assign path
    file_count = 0
    dataframes = {}

    for (path, dirs, files) in os.walk("../raw_data/football-data_co_uk/"):
        file_count = len(files)

        # appned dfs to dict using file names as keys
        for i in range(file_count):
            dataframes[files[i]] = pd.read_csv(os.path.join("../raw_data/football-data_co_uk/", files[i]))

    return dataframes

def make_transfermarkt_DataFrames():
    # assign path
    file_count = 0
    dataframes = {}

    for (path, dirs, files) in os.walk("../raw_data/data-transfermarkt/"):
        file_count = len(files)

        # appned dfs to dict using file names as keys
        for i in range(file_count):
            dataframes[files[i]] = pd.read_csv(os.path.join("../raw_data/data-transfermarkt/", files[i]))

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
