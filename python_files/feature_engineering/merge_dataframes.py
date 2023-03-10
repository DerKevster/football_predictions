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

    # Select the Bundesliga (L1)
    bundesliga_games = games["competition_id"] == league
    bundesliga_df = games_clean[bundesliga_games]

    # Select season 2018/19
    season_2018 = bundesliga_df["season"] == season
    bundesliga_2018 = bundesliga_df[season_2018]
    bundesliga_2018_sorted = bundesliga_2018.sort_values(by=["home_club_id", "date"])

    #drop duplicates
    bundesliga_final18 = bundesliga_2018_sorted.drop_duplicates(subset=["date", "home_club_id"])

    #merge by combining club id and club name
    bund = bundesliga_final18.merge(clubs_clean, left_on="home_club_id", right_on="club_id")
    bundesliga_final = bund.merge(clubs_clean, left_on="away_club_id", right_on="club_id")
    bundesliga_final = bundesliga_final.rename(columns= {"name_x":"HomeTeam", "name_y":"away_team", "date" : "Date"})
    bundesliga_final = bundesliga_final.drop(columns=["club_id_x", "club_id_y"])
    return bundesliga_final.sort_values(by='Date')

def squad_value_df():
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
    renamed_columns = {
        '1 Fc Nurnberg' : "Nurnberg",
        'Bayer 04 Leverkusen': "Leverkusen",
        'Borussia Dortmund': "Dortmund",
        'Borussia Monchengladbach': "M'gladbach",
        'Eintracht Frankfurt': "Ein Frankfurt",
        'Fc Bayern Munchen' : "Bayern Munich",
        'Fc Schalke 04': "Schalke 04",
        'Fortuna Dusseldorf': "Fortuna Dusseldorf",
        'Hannover 96': "Hannover",
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
    squad_value_final = squad_value_final.replace(to_replace=renamed_columns)
    return squad_value_final

# the next function merges the transfermarkt and footballdata data into one dataframe so we cna extract the cumulative sums of the previous five days

def make_merged_df(league, season):
  import warnings; warnings.filterwarnings("ignore")
  football_df = make_footballdata_df_to_merge(league, season)
  tmarkt_df = make_tranfermarkt_df_to_merge(league, season)
  #fifa_df = make_fifa_df_to_merge(league, season)

  # Get teams
  translator = tf_to_fb_translator(league)
  tmarkt_df = tmarkt_df.replace(to_replace=translator)

  merged_df = tmarkt_df.merge(football_df, on=["Date", "HomeTeam"])
  merged_df.drop(columns=["game_id", "competition_id", "season", "home_club_id", "away_club_id"], inplace=True)
  merged_df[['round', 'HomeTeam', 'away_team', 'home_club_goals', 'away_club_goals', 'HC', 'AC', 'HS', 'HST', 'AS', 'AST']]
  merged_df['round'] = merged_df['round'].map(lambda round: round.strip(". Matchday")).map(lambda number: int(number))
  for index, row in merged_df.iterrows():
      if merged_df.at[index, "home_club_goals"] > merged_df.at[index, "away_club_goals"]:
       merged_df.at[index, "outcome"] = 0
      elif merged_df.at[index, "home_club_goals"] < merged_df.at[index, "away_club_goals"]:
       merged_df.at[index, "outcome"] = 2
      else:
       merged_df.at[index, "outcome"] = 1
  merged_df=merged_df.rename(columns={'round':'matchday'})
  return merged_df

def tf_to_fb_translator(league):

  BL_translator = {
      'Sv Werder Bremen':'Werder Bremen',
      'Eintracht Frankfurt':'Ein Frankfurt',
      'Fortuna Dusseldorf':'Fortuna Dusseldorf',
      'Fc Augsburg':'Augsburg',
      'Borussia Monchengladbach':"M'gladbach",
      'Spvgg Greuther Furth':'Greuther Furth',
      'Borussia Dortmund':'Dortmund',
      'Tsg 1899 Hoffenheim':'Hoffenheim',
      'Vfl Bochum':'Bochum',
      'Fc Bayern Munchen':'Bayern Munich',
      '1 Fc Koln':'FC Koln',
      'Sc Freiburg':'Freiburg',
      'Vfl Wolfsburg':'Wolfsburg',
      'Hannover 96':'Hannover',
      'Fc Schalke 04':'Schalke 04',
      'Rasenballsport Leipzig':'RB Leipzig',
      'Hertha Bsc':'Hertha',
      'Arminia Bielefeld':'Bielefeld',
      '1 Fsv Mainz 05':'Mainz',
      'Vfb Stuttgart':'Stuttgart',
      '1 Fc Union Berlin':'Union Berlin',
      'Sc Paderborn 07':'Paderborn',
      'Bayer 04 Leverkusen':'Leverkusen',
      '1 Fc Nurnberg':'Nurnberg'
    }


  PL_translator = {
      'Aston Villa':'Aston Villa',
      'Norwich City':'Norwich',
      'Brighton Amp Hove Albion':'Brighton',
      'Nottingham Forest':"Nott'm Forest",
      'Sheffield United':'Sheffield United',
      'Manchester City':'Man City',
      'Fc Chelsea':'Chelsea',
      'Cardiff City':'Cardiff',
      'Fc Burnley':'Burnley',
      'Crystal Palace':'Crystal Palace',
      'Fc Arsenal':'Arsenal',
      'Fc Liverpool':'Liverpool',
      'Fc Fulham':'Fulham',
      'Huddersfield Town':'Huddersfield',
      'Leicester City':'Leicester',
      'West Bromwich Albion':'West Brom',
      'Afc Bournemouth':'Bournemouth',
      'Fc Everton':'Everton',
      'West Ham United':'West Ham',
      'Wolverhampton Wanderers':'Wolves',
      'Fc Watford':'Watford',
      'Leeds United':'Leeds',
      'Manchester United':'Man United',
      'Newcastle United':'Newcastle',
      'Tottenham Hotspur':'Tottenham',
      'Fc Southampton':'Southampton',
      'Fc Brentford':'Brentford'
    }


  LL_translator = {
      'Fc Getafe' : 'Getafe' ,
      'Fc Girona' : 'Girona',
      'Fc Barcelona' : 'Barcelona',
      'Atletico Madrid' : 'Ath Madrid',
      'Fc Villarreal' : 'Villarreal',
      'Fc Valencia' : 'Valencia',
      'Real Betis Sevilla' : 'Betis',
      'Athletic Bilbao' : 'Ath Bilbao',
      'Sd Huesca' : 'Huesca',
      'Rayo Vallecano' : 'Vallecano',
      'Rcd Mallorca' : 'Mallorca',
      'Deportivo Alaves' : 'Alaves',
      'Fc Granada' : 'Granada',
      'Fc Cadiz' : 'Cadiz',
      'Espanyol Barcelona' : 'Espanol',
      'Fc Elche' : 'Elche',
      'Sd Eibar' : 'Eibar',
      'Real Sociedad San Sebastian' : 'Sociedad',
      'Fc Sevilla' : 'Sevilla',
      'Real Valladolid' : 'Valladolid',
      'Real Madrid' : 'Real Madrid',
      'Ca Osasuna' : 'Osasuna',
      'Cd Leganes' : 'Leganes',
      'Celta Vigo' : 'Celta',
      'Ud Levante' : 'Levante',
      'Ud Almeria' : 'Almeria'
    }


  SA_translator = {
      'Udinese Calcio':'Udinese',
      'Sampdoria Genua':'Sampdoria',
      'Lazio Rom':'Lazio',
      'Atalanta Bergamo':'Atalanta',
      'Ac Florenz':'Fiorentina',
      'Benevento Calcio':'Benevento',
      'Venezia Fc':'Venezia',
      'Genua Cfc':'Genoa',
      'Hellas Verona':'Verona',
      'Ac Monza':'Monza',
      'Juventus Turin':'Juventus',
      'Spal':'Spal',
      'Fc Turin':'Torino',
      'Parma Calcio 1913':'Parma',
      'Fc Crotone':'Crotone',
      'Us Sassuolo':'Sassuolo',
      'Spezia Calcio':'Spezia',
      'Us Cremonese':'Cremonese',
      'Cagliari Calcio':'Cagliari',
      'Fc Bologna':'Bologna',
      'Chievo Verona':'Chievo',
      'Fc Empoli':'Empoli',
      'Us Lecce':'Lecce',
      'Ssc Neapel':'Napoli',
      'Ac Mailand':'Milan',
      'Brescia Calcio':'Brescia',
      'Inter Mailand':'Inter',
      'Frosinone Calcio':'Frosinone',
      'Us Salernitana 1919':'Salernitana',
      'As Rom':'Roma'
    }

  league_translator = {
    'BL' : BL_translator,
    'PL' : PL_translator,
    'SA' : SA_translator,
    'LL' : LL_translator
  }


  translator = league_translator[league]
  return translator
