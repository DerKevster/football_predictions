from python_files.feature_engineering.merge_dataframes import make_transfermarkt_DataFrames, make_squad_value_df, clean_FIFA_df
import pandas as pd
import numpy as np

# Make a dataframe of the last [past_matches] match days
def make_past_matches_df(date, team, merged_df, past_matches):
  mask_home = merged_df["HomeTeam"] == team
  mask_away = merged_df["away_team"] == team
  home_df = merged_df[mask_home]
  away_df = merged_df[mask_away]
  past_game_df = pd.concat([home_df, away_df], axis=0).sort_values(by="Date").reset_index()
  past_game_df = past_game_df.drop(columns=["index"])
  # Get the index of the current date
  current_index = past_game_df[past_game_df["Date"] == date].index[0]
  past_game_df = past_game_df.loc[current_index-past_matches : current_index-1, :]
  return past_game_df


# Base function to count totals of specific stat (goals, goals conceded, shots, shots on target and corners) depending on if team is home or away, for the given past matchdays
def get_totals(team, matchday, df, past_matches, for_home, for_away):
  past_matches_df = make_past_matches_df(matchday, df, past_matches)
  stat_count = 0
  for i in range(len(past_matches_df)):
      current_game = past_matches_df.iloc[i, :]
      if current_game['HomeTeam'] == team:
          stat_count += current_game[for_home]
      elif current_game['away_team'] == team:
          stat_count += current_game[for_away]
  return stat_count

# Function to get the number of goals scored for a [team] in the last [past_matches] match days
def get_goals(team, matchday, df, past_matches):
    return get_totals(team, matchday, df, past_matches, 'home_club_goals', 'away_club_goals')

# Function to get the number of goals conceded for a [team] in the last [past_matches] match days
def get_conc(team, matchday, df, past_matches):
  return get_totals(team, matchday, df, past_matches, 'away_club_goals', 'home_club_goals')

# Function to get the number of corner kicks for a [team] in the last [past_matches] match days
def get_corners(team, matchday, df , past_matches):
    return get_totals(team, matchday, df, past_matches, 'HC', 'AC')

# Function to get the number of shots for a [team] in the last [past_matches] match days
def get_shots(team, matchday, df , past_matches):
    return get_totals(team, matchday, df, past_matches, 'HS', 'AS')

# Function to get the number of shots on target for a [team] in the last [past_matches] match days
def get_shots_ot(team, matchday, df , past_matches):
    return get_totals(team, matchday, df, past_matches, 'HST', 'AST')

# Function to get the goal difference for a [team] for the entire season
def get_goal_diff(team, matchday, df):
    past_matches_df = make_past_matches_df(matchday, df, (matchday-1))
    goal_diff = 0
    for i in range(len(past_matches_df)):
        current_game = past_matches_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goal_diff += (current_game['home_club_goals'] - current_game['away_club_goals'])
        elif current_game['away_team'] == team:
            goal_diff += (current_game['away_club_goals'] - current_game['home_club_goals'])
        #print(current_game)
    return goal_diff

# Function to get the average seasonal goal difference of the last [past_matches] opponents
def get_opp_avg(team, matchday, df, past_matches):

    # make dataframe of last [past_matches]
    past_matches_df = make_past_matches_df(matchday, df, past_matches)

    # make list of last n opponents
    oppos = []
    for i in range(len(past_matches_df)):
        current_game = past_matches_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            oppos.append(current_game['away_team'])
        elif current_game['away_team'] == team:
            oppos.append(current_game['HomeTeam'])

    # get goal differences for all opponents
    oppos_goaldiff = [get_goal_diff(oppo, matchday, df) for oppo in oppos]

    # return the average value of the opponents goal difference
    return np.average(oppos_goaldiff)

# Function to get the squad value for a Bundesliga team for the season 2018 in Millions €
def get_squad_value(club_name, squad_value_df):
    import warnings; warnings.filterwarnings("ignore")

    # Extract Features from Transfermarkt
    squad_value_final = squad_value_df

    # Getting the right season and the right team
    club_mask = squad_value_final["name"] == club_name
    now_really_the_final = squad_value_final[club_mask]

    # Return the squad value per season.
    now_really_the_final
    return (now_really_the_final["market_value_in_eur"].max()/1000000)

# Make a dataframe of the current match day
def make_current_matchday_df(matchday, df):
    current_matchday = df.loc[df['matchday'] == matchday]
    return current_matchday

# function to find if the result of of a specific game is a home win, returns 1 if true and 0 if false
def get_outcome(home, away, matchday, df):
    # 0 = Home Team wins, 1 = Draw, 2 = Away Team wins
    current_matchday_df = make_current_matchday_df(matchday, df)
    outcome = 0
    for i in range(len(current_matchday_df)):
        current_game = current_matchday_df.iloc[i, :]
        if current_game['HomeTeam'] == home and current_game['away_team'] == away and current_game['home_club_goals'] > current_game['away_club_goals']:
            outcome = 0
        elif current_game['HomeTeam'] == home and current_game['away_team'] == away and current_game['home_club_goals'] < current_game['away_club_goals']:
            outcome = 2
        elif current_game['HomeTeam'] == home and current_game['away_team'] == away and current_game['home_club_goals'] == current_game['away_club_goals']:
            outcome = 1
    return outcome

 # Function to compute the average over each teams defense
def get_defense(team, clean_df):
    return round(clean_df[clean_df.Club == team][clean_df.Field == 'Defense']['Overall'].mean(),1)

# Function to compute the average over each teams midfield
def get_midfield(team, clean_df):
    return round(clean_df[clean_df.Club == team][clean_df.Field == 'Midfield']['Overall'].mean(),1)

# Function to compute the average over each teams attack
def get_attack(team, clean_df):
    return round(clean_df[clean_df.Club == team][clean_df.Field == 'Attack']['Overall'].mean(),1)

# Function to compute the average over each teams bench
def get_bench(team, clean_df):
    return round(clean_df[clean_df.Club == team][clean_df.Field == 'Bench']['Overall'].mean(),1)
