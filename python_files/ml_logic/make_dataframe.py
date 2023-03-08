import pandas as pd

def make_dataframe_row(home, away, round, df):
    dicto = {}
    dicto = {'home':home}
    dicto = {'away':away}
    dicto = {'date':get_date(home, round, df)}
    dicto = {'shots_h':get_shots(home, round, df, 5)}
    dicto = {'targets_h':get_targets(home, round, df, 5)}
    dicto = {'goals_h':get_goals(home, round, df, 5)}
    dicto = {'conc_h':get_conc(home, round, df, 5)}
    dicto = {'corner_h':get_corners(home, round, df, 5)}
    dicto = {'goaldiff_h':get_goal_diff(home, df)}
    dicto = {'opp_avg_h':get_opp_avg(home, round, df, 5)}
    dicto = {'value_h':get_squad_value(home)}
    dicto = {'targets_a':get_targets(away, round, df, 5)}
    dicto = {'shots_a':get_shots(away, round, df, 5)}
    dicto = {'goals_a':get_goals(away, round, df, 5)}
    dicto = {'conc_a':get_conc(away, round, df, 5)}
    dicto = {'corner_a':get_corners(away, round, df, 5)}
    dicto = {'goaldiff_a':get_goal_diff(away, df)}
    dicto = {'opp_avg_a':get_opp_avg(away, round, df, 5)}
    dicto = {'value_a':get_squad_value(away)}
    dicto = {'win_home':get_win(home, away)}
    dicto = {'draw':get_draw(home, away)}
    dicto = {'win_away':get_win(away, home)}
    return pd.DataFrame(dicto)
