import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, classification_report
from sklearn.preprocessing import StandardScaler


def make_predict_df(df, model):

    #Create X and y
    X = df.drop(columns=['home','away','date','outcome'],axis=1)
    y = df['outcome']
    # Split df into train, test set
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.2, random_state = 42)

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
    df_prob[['home','away']] = df.loc[y_test.index, ['home','away']]
    df_prob['outcome'] = y_test
    df_prob['home_win'] = proba[:,0]
    df_prob['draw'] = proba[:,1]
    df_prob['away_win'] = proba[:,2]

    return df_prob
