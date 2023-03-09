import pandas as pd
from python_files.feature_engineering import feature_functions as ff

def make_dataframe_row(home, away, matchday, df, past_matchdays = 5):
    dicto = {}
    dicto = {'home':home}
    dicto = {'away':away}
    dicto = {'date': matchday}
    dicto = {'shots_h':ff.get_shots(home, matchday, df, past_matchdays)}
    dicto = {'targets_h':ff.get_targets(home, matchday, df, past_matchdays)}
    dicto = {'goals_h':ff.get_goals(home, matchday, df, past_matchdays)}
    dicto = {'conc_h':ff.get_conc(home, matchday, df, past_matchdays)}
    dicto = {'corner_h':ff.get_corner(home, matchday, df, past_matchdays)}
    dicto = {'goaldiff_h':ff.get_goal_diff(home, matchday, df)}
    dicto = {'opp_avg_h':ff.get_opp_avg(home, matchday, df, past_matchdays)}
    dicto = {'value_h':ff.get_squad_value(home)}
    dicto = {'targets_a':ff.get_targets(away, matchday, df, past_matchdays)}
    dicto = {'shots_a':ff.get_shots(away, matchday, df, past_matchdays)}
    dicto = {'goals_a':ff.get_goals(away, matchday, df, past_matchdays)}
    dicto = {'conc_a':ff.get_conc(away, matchday, df, past_matchdays)}
    dicto = {'corner_a':ff.get_corner(away, matchday, df, past_matchdays)}
    dicto = {'goaldiff_a':ff.get_goal_diff(home, matchday, df)}
    dicto = {'opp_avg_a':ff.get_opp_avg(away, matchday, df, past_matchdays)}
    dicto = {'value_a':ff.get_squad_value(away)}
    dicto = {'win_home':ff.get_win_home(home, away, matchday, df)}
    dicto = {'draw':ff.get_draw(home, away, matchday, df)}
    dicto = {'win_away':ff.get_win_away(home, away, matchday, df)}
    return pd.DataFrame.from_dict(dicto)
