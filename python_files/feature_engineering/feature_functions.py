from python_files.feature_engineering.merge_data import make_transfermarkt_DataFrames
import pandas as pd
import numpy as np

# Make a dataframe of the last [past_rounds] match days
def make_past_rounds_df(matchday, df, past_rounds):
    prev_round_df = df.loc[df['round'] == matchday-1]
    past_rounds_df = pd.DataFrame()

    if matchday - past_rounds > 0:
        if past_rounds == 1:
            return prev_round_df
        else:
            for i in range(past_rounds):
                next_past_rounds_df = df.loc[df['round'] == matchday-1-i]
                if i == 0:
                    past_rounds_df = prev_round_df
                else:
                    past_rounds_df = pd.concat([past_rounds_df, next_past_rounds_df], axis=0)
    else:
        print("Error: The past rounds you are asking for do not exist")
    return past_rounds_df

# Function to get the number of goals scored for a [team] in the last [past_rounds] match days
def get_goals(team, matchday, df, past_rounds):
    past_rounds_df = make_past_rounds_df(matchday, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['home_club_goals']
        elif current_game['away_team'] == team:
            goals += current_game['away_club_goals']
        #print(current_game)
    return goals

# Function to get the number of goals conceded for a [team] in the last [past_rounds] match days
def get_conc(team, matchday, df, past_rounds):
    past_rounds_df = make_past_rounds_df(matchday, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['away_club_goals']
        elif current_game['away_team'] == team:
            goals += current_game['home_club_goals']
    return goals

# Function to get the number of corner kicks for a [team] in the last [past_rounds] match days
def get_corner(team, matchday, df, past_rounds):
    past_rounds_df = make_past_rounds_df(matchday, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['HC']
        elif current_game['away_team'] == team:
            goals += current_game['AC']
    return goals

# Function to get the number of shots for a [team] in the last [past_rounds] match days
def get_shots(team, matchday, df, past_rounds):
    past_rounds_df = make_past_rounds_df(matchday, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['HS']
        elif current_game['away_team'] == team:
            goals += current_game['AS']
    return goals

# Function to get the number of shots on target for a [team] in the last [past_rounds] match days
def get_targets(team, matchday, df, past_rounds):
    past_rounds_df = make_past_rounds_df(matchday, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['HST']
        elif current_game['away_team'] == team:
            goals += current_game['AST']
    return goals

# Function to get the goal difference for a [team] for the entire season
def get_goal_diff(team, matchday, df):
    past_rounds_df = make_past_rounds_df(matchday, df, (matchday-1))
    goal_diff = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goal_diff += (current_game['home_club_goals'] - current_game['away_club_goals'])
        elif current_game['away_team'] == team:
            goal_diff += (current_game['away_club_goals'] - current_game['home_club_goals'])
        #print(current_game)
    return goal_diff

# Function to get the average seasonal goal difference of the last [past_rounds] opponents
def get_opp_avg(team, matchday, df, past_rounds):

    # make dataframe of last [past_rounds]
    past_rounds_df = make_past_rounds_df(matchday, df, past_rounds)

    # make list of last n opponents
    oppos = []
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            oppos.append(current_game['away_team'])
        elif current_game['away_team'] == team:
            oppos.append(current_game['HomeTeam'])

    # get goal differences for all opponents
    oppos_goaldiff = [get_goal_diff(oppo, matchday, df) for oppo in oppos]

    # return the average value of the opponents goal difference
    return np.average(oppos_goaldiff)

# Function to get the squad value for a Bundesliga team for the season 2018
def get_squad_value(club_name):

    # Extract Features from Transfermarkt
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
    squad_value_final = squad_value_final.replace(to_replace=renamed_columns)

    # Getting the right season and the right team
    season_mask = squad_value_final["season"] == 2018
    club_mask = squad_value_final["name"] == club_name
    competition_mask = squad_value_final["domestic_competition_id"] == "L1"
    squad_value_season = squad_value_final[season_mask]
    now_really_the_final = squad_value_season[club_mask]
    bundesliga_value = now_really_the_final[competition_mask]

    # Return the squad value per season.
    bundesliga_value
    return bundesliga_value

# Make a dataframe of the current match day
def make_current_round_df(matchday, df):
    current_round = df.loc[df['round'] == matchday]
    return current_round

# function to find if the result of of a specific game is a home win, returns 1 if true and 0 if false
def get_win_home(home, away, matchday, df):
    current_round_df = make_current_round_df(matchday, df)
    outcome = 0
    for i in range(len(current_round_df)):
        current_game = current_round_df.iloc[i, :]
        if current_game['HomeTeam'] == home and current_game['away_team'] == away and current_game['outcome'] == 'H':
            outcome = 1
        else:
            pass
    return outcome

# function to find if the result of of a specific game is an away win, returns 1 if true and 0 if false
def get_win_away(home, away, matchday, df):
    current_round_df = make_current_round_df(matchday, df)
    outcome = 0
    for i in range(len(current_round_df)):
        current_game = current_round_df.iloc[i, :]
        if current_game['HomeTeam'] == home and current_game['away_team'] == away and current_game['outcome'] == 'A':
            outcome = 1
        else:
            pass
    return outcome

# function to find if the result of of a specific game is a draw, returns 1 if true and 0 if false
def get_draw(home, away, matchday, df):
    current_round_df = make_current_round_df(matchday, df)
    outcome = 0
    for i in range(len(current_round_df)):
        current_game = current_round_df.iloc[i, :]
        if current_game['HomeTeam'] == home and current_game['away_team'] == away and current_game['outcome'] == 'D':
            outcome = 1
        else:
            pass
    return outcome
