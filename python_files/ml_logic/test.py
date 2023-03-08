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

make_footballdatauk_DataFrames()
