import pandas as pd
from python_files.feature_engineering import feature_functions as ff
from python_files.feature_engineering.merge_dataframes import make_merged_df, make_fifa_df, make_squad_value_df

# Standard League and Season inputs:
# Leagues: ['PL', 'BL', 'LL', 'SA']
# Seasons: ['18-19', '19-20', '20-21', '21-22', '22-23']

def make_dataframe_row(home, away, date, merged_df, fifa_df, squad_value_df, past_matches = 5):

    dicto = {}
    dicto = {'home':home,
             'away':away,
             'date' : date,
             'shots_h' : ff.get_shots(home, date, merged_df, past_matches),
             'shots_ot_h' : ff.get_shots_ot(home, date, merged_df, past_matches),
             'goals_h' : ff.get_goals(home, date, merged_df, past_matches),
             'conc_h' : ff.get_conc(home, date, merged_df, past_matches),
             'corner_h' : ff.get_corners(home, date, merged_df, past_matches),
             'goaldiff_h' : ff.get_goal_diff(home, date, merged_df),
             #'opp_avg_h' : ff.get_opp_avg(home, date, merged_df, past_matches),
             'value_h' : ff.get_squad_value(home, squad_value_df),
             'attack_h' : ff.get_attack(home, fifa_df),
             'midfield_h' : ff.get_midfield(home, fifa_df),
             'defense_h' : ff.get_defense(home, fifa_df),
             'bench_h' : ff.get_bench(home, fifa_df),
             'shots_ot_a' : ff.get_shots_ot(away, date, merged_df, past_matches),
             'shots_a' : ff.get_shots(away, date, merged_df, past_matches),
             'goals_a' : ff.get_goals(away, date, merged_df, past_matches),
             'conc_a' : ff.get_conc(away, date, merged_df, past_matches),
             'corner_a' : ff.get_corners(away, date, merged_df, past_matches),
             'goaldiff_a' : ff.get_goal_diff(away, date, merged_df),
             #'opp_avg_a' : ff.get_opp_avg(away, date, merged_df, past_matches),
             'value_a' : ff.get_squad_value(away, squad_value_df),
             'attack_a' : ff.get_attack(away, fifa_df),
             'midfield_a' : ff.get_midfield(away, fifa_df),
             'defense_a' : ff.get_defense(away, fifa_df),
             'bench_a' : ff.get_bench(away, fifa_df),
             'outcome' : ff.get_outcome(home, away, merged_df)}

    return pd.DataFrame(dicto, index=[0])


# Function to get the right starting index so all teams have played at least 5 games
def get_starting_index(league, season, past_matches = 5):
  merged_df = make_merged_df(league, season)
  teams = merged_df["HomeTeam"].unique()
  index_last_game = 0
  for team in teams:
      past_matches = past_matches +1
      for index, match in merged_df.iterrows():
          if past_matches == 0:
              break
          elif match["HomeTeam"] == team:
              if index_last_game < index:
                  index_last_game = index
              past_matches = past_matches - 1
          elif match["away_team"] == team:
              if index_last_game < index:
                  index_last_game = index
              past_matches = past_matches - 1

  index_last_game
  start_index = index_last_game + 1
  print(f"For the {league} in season {season} the starting match is {merged_df.loc[start_index,['HomeTeam']][0]} vs. {merged_df.loc[start_index,['away_team']][0]}")
  return start_index


def make_feature_df(league, season, past_matches):

    merged_df = make_merged_df(league, season)
    fifa_df = make_fifa_df(season)
    squad_value_df = make_squad_value_df(season)

    starting_index = get_starting_index(league, season, past_matches)
    feature_df = pd.DataFrame()

    for index, date in merged_df.loc[starting_index : , : ].iterrows():
        new_df = make_dataframe_row(merged_df.at[index, "HomeTeam"], merged_df.at[index, "away_team"], merged_df.at[index,"Date"], merged_df, fifa_df, squad_value_df, past_matches=5)
        feature_df = pd.concat([feature_df, pd.DataFrame(new_df)], axis=0)
    feature_df = feature_df.reset_index()
    feature_df = feature_df.drop(columns=["index"])
    return feature_df

def make_multi_feature_df(leagues, seasons, past_matchdays):
    full_df = pd.DataFrame()
    for league in leagues:
        for season in seasons:
            season_df = make_feature_df(league, season, past_matchdays)
            full_df = pd.concat([full_df, season_df], axis=0, ignore_index=True)
    return full_df
