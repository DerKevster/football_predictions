import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, classification_report
from sklearn.preprocessing import StandardScaler


def make_X_y_split(X_df, y_df, p, n):
  # Split feature_df into train match set of size n from p to p + n, and test match of position p+n+1
    X_train = X_df.iloc[p: p + n, :]
    y_train = y_df.iloc[p: p + n]

    X_test = X_df.iloc[p + n, :]
    y_test = y_df.iloc[p + n]
    return X_train, X_test, y_train, y_test


# Function to split the data in chronological order (i.e take n previous games and predict the following one, then iterate through data in steps of p)
def make_preds_with_split(feature_df, model, n=5, p_increment=1):
    p = 0
    pred_list = []
    match_outcomes = []
    pipe = make_pipeline(StandardScaler(), model)

    while p <= len(feature_df-(n+1)):
      #Create X and y
      X_df = feature_df.drop(columns=['home','away','date','outcome'],axis=1)
      y_df = feature_df['outcome']

      X_train, X_test, y_train, y_test = make_X_y_split(X_df, y_df, p, n)

      pipe.fit(X_train, y_train)
      res_preds = pipe.predict_proba(X_test)
      pred_list.append(res_preds)
      match_outcomes.append(y_test)
      p += p_increment

    return pred_list, match_outcomes


def make_predict_df(df, model, split=True, chrono=False, random_state=42):

    if split:
        #Create X and y
        X = df.drop(columns=['home','away','date','outcome'],axis=1)
        y = df['outcome']

        if not chrono:
            # Split df into train, test set
            X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size = 0.2, random_state = random_state)
        else:
            X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size = 0.2, shuffle = False)

        # Scale df
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled= scaler.transform(X_test)

        # optimized model
        mod = model
        # fit model
        mod.fit(X_train_scaled, y_train)
        # predict_probability
        proba = mod.predict_proba(X_test_scaled)

        df_prob = pd.DataFrame()
        df_prob[['Date']] = df.loc[y_test.index, ['date']]
        df_prob[['HomeTeam','AwayTeam']] = df.loc[y_test.index, ['home','away']]
        df_prob['outcome'] = y_test
        df_prob['home_win'] = proba[:,0]
        df_prob['draw'] = proba[:,1]
        df_prob['away_win'] = proba[:,2]

    else:
        #Create X and y
        X = df.drop(columns=['home','away','date','outcome'],axis=1)
        y = df['outcome']

        # Scale df
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # optimized model
        mod = model
        # fit model
        mod.fit(X_scaled, y)
        # predict_probability
        proba = mod.predict_proba(X_scaled)

        df_prob = pd.DataFrame()
        df_prob[['Date']] = df.loc[:, ['date']]
        df_prob[['HomeTeam','AwayTeam']] = df.loc[:, ['home','away']]
        df_prob['outcome'] = y
        df_prob['home_win'] = proba[:,0]
        df_prob['draw'] = proba[:,1]
        df_prob['away_win'] = proba[:,2]

    return df_prob
