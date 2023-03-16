import pandas as pd
import numpy as np
from python_files.ml_logic.feature_dataframe import make_feature_df
from python_files.model_evaluation.betting_odds import make_betting_odds_df
from python_files.model_evaluation.model_functions import make_predict_df
from python_files.ml_logic.basemodel import make_basemodel


def make_money (betting_odds_df, predict_df, bankroll=100, bet=1, threshold=1):
    # create a df with the betting odds and the predicted probabilities
    # make_betting_odds_df(league, season, proba=False)
    # make_predict_df(df, model)

    df = pd.merge(betting_odds_df, predict_df, on=['Date', 'HomeTeam', 'AwayTeam'], how='inner')
    df['exp_home_win'] = df['home_win'] * df['PSH']
    df['exp_draw'] = df['draw'] * df['PSD']
    df['exp_away_win'] = df['away_win'] * df['PSA']
    df['exp_max'] = df[['exp_home_win', 'exp_draw', 'exp_away_win']].max(axis=1)
    df['exp_max_arg'] = df[['exp_home_win', 'exp_draw', 'exp_away_win']].idxmax(axis=1).map({'exp_home_win': 'H', 'exp_draw': 'D', 'exp_away_win': 'A'}.get)

    # Function to test the betting strategy

    for i in df.index:
        gain = 0
        exp_max = df['exp_max'][i]
        exp_arg_max = df['exp_max_arg'][i]
        if exp_arg_max == 'H':
            odd_id = 'PSH'
        elif exp_arg_max == 'D':
            odd_id = 'PSD'
        else:
            odd_id = 'PSA'
        gain = bet * df[odd_id][i]

        if exp_max > threshold:
            if df['FTR'][i] == exp_arg_max:
                bankroll += gain
            else:
                bankroll -= bet

    return bankroll
