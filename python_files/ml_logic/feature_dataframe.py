import pandas as pd
from python_files.feature_engineering import feature_functions as ff
from python_files.feature_engineering.merge_dataframes import make_merged_df, make_fifa_df

def make_dataframe_row(home, away, matchday, merged_df, fifa_df, past_matchdays = 5):

    dicto = {}
    dicto = {'home':home,
             'away':away,
             'matchday' : matchday,
             'shots_h' : ff.get_shots(home, matchday, merged_df, past_matchdays),
             'targets_h' : ff.get_targets(home, matchday, merged_df, past_matchdays),
             'goals_h' : ff.get_goals(home, matchday, merged_df, past_matchdays),
             'conc_h' : ff.get_conc(home, matchday, merged_df, past_matchdays),
             'corner_h' : ff.get_corner(home, matchday, merged_df, past_matchdays),
             'goaldiff_h' : ff.get_goal_diff(home, matchday, merged_df),
             'opp_avg_h' : ff.get_opp_avg(home, matchday, merged_df, past_matchdays),
             'value_h' : ff.get_squad_value(home, fifa_df),
             'attack_h' : ff.get_attack(home, fifa_df),
             'midfield_h' : ff.get_midfield(home, fifa_df),
             'defense_h' : ff.get_defense(home, fifa_df),
             'bench_h' : ff.get_bench(home, fifa_df),
             'targets_a' : ff.get_targets(away, matchday, merged_df, past_matchdays),
             'shots_a' : ff.get_shots(away, matchday, merged_df, past_matchdays),
             'goals_a' : ff.get_goals(away, matchday, merged_df, past_matchdays),
             'conc_a' : ff.get_conc(away, matchday, merged_df, past_matchdays),
             'corner_a' : ff.get_corner(away, matchday, merged_df, past_matchdays),
             'goaldiff_a' : ff.get_goal_diff(away, matchday, merged_df),
             'opp_avg_a' : ff.get_opp_avg(away, matchday, merged_df, past_matchdays),
             'value_a' : ff.get_squad_value(away),
             'attack_a' : ff.get_attack(away, fifa_df),
             'midfield_a' : ff.get_midfield(away, fifa_df),
             'defense_a' : ff.get_defense(away, fifa_df),
             'bench_a' : ff.get_bench(away, fifa_df),
             'outcome' : ff.get_outcome(home, away, matchday, merged_df)}

    return pd.DataFrame(dicto, index=[0])



def make_feature_df(league, season, past_matchdays):

    merged_df = make_merged_df(league, season)
    fifa_df = make_fifa_df(season)

    index_match = merged_df.index[merged_df['matchday']==(past_matchdays+1)].tolist()[0]
    feature_df = pd.DataFrame()

    for index, matchday in merged_df.loc[index_match : , : ].iterrows():
        new_df = make_dataframe_row(merged_df.at[index, "HomeTeam"], merged_df.at[index, "away_team"], merged_df.at[index,"matchday"], df)
        feature_df = pd.concat([feature_df, pd.DataFrame(new_df)], axis=0)
    feature_df = feature_df.reset_index()
    feature_df = feature_df.drop(columns=["index"])
    return feature_df
