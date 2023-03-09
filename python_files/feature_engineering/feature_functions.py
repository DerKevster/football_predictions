from python_files.feature_engineering.merge_dataframes import make_transfermarkt_DataFrames, squad_value_df
import pandas as pd
import numpy as np

# Make a dataframe of the last [past_matchdays] match days
def make_past_matchdays_df(matchday, df, past_matchdays):
    prev_matchday_df = df.loc[df['matchday'] == matchday-1]
    past_matchdays_df = pd.DataFrame()

    if matchday - past_matchdays > 0:
        if past_matchdays == 1:
            return prev_matchday_df
        else:
            for i in range(past_matchdays):
                next_past_matchdays_df = df.loc[df['matchday'] == matchday-1-i]
                if i == 0:
                    past_matchdays_df = prev_matchday_df
                else:
                    past_matchdays_df = pd.concat([past_matchdays_df, next_past_matchdays_df], axis=0)
    else:
        print("Error: The past matchdays you are asking for do not exist")
    return past_matchdays_df

# Function to get the number of goals scored for a [team] in the last [past_matchdays] match days
def get_goals(team, matchday, df, past_matchdays):
    past_matchdays_df = make_past_matchdays_df(matchday, df, past_matchdays)
    goals = 0
    for i in range(len(past_matchdays_df)):
        current_game = past_matchdays_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['home_club_goals']
        elif current_game['away_team'] == team:
            goals += current_game['away_club_goals']
        #print(current_game)
    return goals

# Function to get the number of goals conceded for a [team] in the last [past_matchdays] match days
def get_conc(team, matchday, df, past_matchdays):
    past_matchdays_df = make_past_matchdays_df(matchday, df, past_matchdays)
    goals = 0
    for i in range(len(past_matchdays_df)):
        current_game = past_matchdays_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['away_club_goals']
        elif current_game['away_team'] == team:
            goals += current_game['home_club_goals']
    return goals

# Function to get the number of corner kicks for a [team] in the last [past_matchdays] match days
def get_corner(team, matchday, df, past_matchdays):
    past_matchdays_df = make_past_matchdays_df(matchday, df, past_matchdays)
    goals = 0
    for i in range(len(past_matchdays_df)):
        current_game = past_matchdays_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['HC']
        elif current_game['away_team'] == team:
            goals += current_game['AC']
    return goals

# Function to get the number of shots for a [team] in the last [past_matchdays] match days
def get_shots(team, matchday, df, past_matchdays):
    past_matchdays_df = make_past_matchdays_df(matchday, df, past_matchdays)
    goals = 0
    for i in range(len(past_matchdays_df)):
        current_game = past_matchdays_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['HS']
        elif current_game['away_team'] == team:
            goals += current_game['AS']
    return goals

# Function to get the number of shots on target for a [team] in the last [past_matchdays] match days
def get_targets(team, matchday, df, past_matchdays):
    past_matchdays_df = make_past_matchdays_df(matchday, df, past_matchdays)
    goals = 0
    for i in range(len(past_matchdays_df)):
        current_game = past_matchdays_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['HST']
        elif current_game['away_team'] == team:
            goals += current_game['AST']
    return goals

# Function to get the goal difference for a [team] for the entire season
def get_goal_diff(team, matchday, df):
    past_matchdays_df = make_past_matchdays_df(matchday, df, (matchday-1))
    goal_diff = 0
    for i in range(len(past_matchdays_df)):
        current_game = past_matchdays_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goal_diff += (current_game['home_club_goals'] - current_game['away_club_goals'])
        elif current_game['away_team'] == team:
            goal_diff += (current_game['away_club_goals'] - current_game['home_club_goals'])
        #print(current_game)
    return goal_diff

# Function to get the average seasonal goal difference of the last [past_matchdays] opponents
def get_opp_avg(team, matchday, df, past_matchdays):

    # make dataframe of last [past_matchdays]
    past_matchdays_df = make_past_matchdays_df(matchday, df, past_matchdays)

    # make list of last n opponents
    oppos = []
    for i in range(len(past_matchdays_df)):
        current_game = past_matchdays_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            oppos.append(current_game['away_team'])
        elif current_game['away_team'] == team:
            oppos.append(current_game['HomeTeam'])

    # get goal differences for all opponents
    oppos_goaldiff = [get_goal_diff(oppo, matchday, df) for oppo in oppos]

    # return the average value of the opponents goal difference
    return np.average(oppos_goaldiff)

# Function to get the squad value for a Bundesliga team for the season 2018 in Millions €
def get_squad_value(club_name):

    # Extract Features from Transfermarkt
    squad_value_final = squad_value_df()

    # Getting the right season and the right team
    season_mask = squad_value_final["season"] == 2018
    club_mask = squad_value_final["name"] == club_name
    competition_mask = squad_value_final["domestic_competition_id"] == "L1"
    squad_value_season = squad_value_final[season_mask]
    now_really_the_final = squad_value_season[club_mask]
    bundesliga_value = now_really_the_final[competition_mask]

    # Return the squad value per season.
    bundesliga_value
    return (bundesliga_value["market_value_in_eur"].max()/1000000)

# Make a dataframe of the current match day
def make_current_matchday_df(matchday, df):
    current_matchday = df.loc[df['matchday'] == matchday]
    return current_matchday

# function to find if the result of of a specific game is a home win, returns 1 if true and 0 if false
def get_win_home(home, away, matchday, df):
    current_matchday_df = make_current_matchday_df(matchday, df)
    outcome = 0
    for i in range(len(current_matchday_df)):
        current_game = current_matchday_df.iloc[i, :]
        if current_game['HomeTeam'] == home and current_game['away_team'] == away and current_game['outcome'] == 'H':
            outcome = 1
        else:
            pass
    return outcome

# function to find if the result of of a specific game is an away win, returns 1 if true and 0 if false
def get_win_away(home, away, matchday, df):
    current_matchday_df = make_current_matchday_df(matchday, df)
    outcome = 0
    for i in range(len(current_matchday_df)):
        current_game = current_matchday_df.iloc[i, :]
        if current_game['HomeTeam'] == home and current_game['away_team'] == away and current_game['outcome'] == 'A':
            outcome = 1
        else:
            pass
    return outcome

# function to find if the result of of a specific game is a draw, returns 1 if true and 0 if false
def get_draw(home, away, matchday, df):
    current_matchday_df = make_current_matchday_df(matchday, df)
    outcome = 0
    for i in range(len(current_matchday_df)):
        current_game = current_matchday_df.iloc[i, :]
        if current_game['HomeTeam'] == home and current_game['away_team'] == away and current_game['outcome'] == 'D':
            outcome = 1
        else:
            pass
    return outcome
