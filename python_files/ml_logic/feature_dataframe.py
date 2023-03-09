import pandas as pd
from python_files.feature_engineering import feature_functions as ff

def make_dataframe_row(home, away, matchday, df, past_matchdays = 5):
    dicto = {}
    dicto = {'home':home,
             'away':away,
             'matchday': matchday,
             'shots_h':ff.get_shots(home, matchday, df, past_matchdays),
             'targets_h':ff.get_targets(home, matchday, df, past_matchdays),
             'goals_h':ff.get_goals(home, matchday, df, past_matchdays),
             'conc_h':ff.get_conc(home, matchday, df, past_matchdays),
             'corner_h':ff.get_corner(home, matchday, df, past_matchdays),
             'goaldiff_h':ff.get_goal_diff(home, matchday, df),
             'opp_avg_h':ff.get_opp_avg(home, matchday, df, past_matchdays),
             'value_h [M]':(ff.get_squad_value(home)/1000000),
             'targets_a':ff.get_targets(away, matchday, df, past_matchdays),
             'shots_a':ff.get_shots(away, matchday, df, past_matchdays),
             'goals_a':ff.get_goals(away, matchday, df, past_matchdays),
             'conc_a':ff.get_conc(away, matchday, df, past_matchdays),
             'corner_a':ff.get_corner(away, matchday, df, past_matchdays),
             'goaldiff_a':ff.get_goal_diff(home, matchday, df),
             'opp_avg_a':ff.get_opp_avg(away, matchday, df, past_matchdays),
             'value_a [M]':(ff.get_squad_value(away)/1000000),
             'win_home':ff.get_win_home(home, away, matchday, df),
             'draw':ff.get_draw(home, away, matchday, df),
             'win_away':ff.get_win_away(home, away, matchday, df)}
    return pd.DataFrame(dicto, index=[0])
