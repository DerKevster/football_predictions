from python_files.feature_engineering.baseline_footballdata_merge_df import make_merged_df, make_transfermarkt_DataFrames
import pandas as pd
import numpy as np

df = make_merged_df()

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

def get_opp_avg(team, matchday, past_rounds, df):
    past_rounds_df = make_past_rounds_df(matchday, df, past_rounds)

    oppos = []
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            oppos.append(current_game['away_team'])
        elif current_game['away_team'] == team:
            oppos.append(current_game['HomeTeam'])

    oppos_goaldiff = [get_goal_diff(oppo, matchday, df) for oppo in oppos]
    return oppos_goaldiff.mean()

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
    squad_value_final = squad_value[["name", "season", "market_value_in_eur", "club_id"]]
    squad_value_final["season"] = squad_value_final["season"].astype("int")

    # Getting the right season and the right team
    season_mask = squad_value_final["season"] == 2018
    club_mask = squad_value_final["name"] == club_name
    competition_mask = squad_value_final["domestic_competition_id"] == "L1"

    squad_value_season = squad_value_final[season_mask]
    now_really_the_final = squad_value_season[club_mask]
    bundesliga_value = now_really_the_final[competition_mask]

    # Return the squad value per season.

    return bundesliga_value["market_value_in_eur"]
