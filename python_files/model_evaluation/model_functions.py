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

    X_test = pd.DataFrame(X_df.iloc[p + n, :]).T
    y_test = y_df.iloc[p + n]
    return X_train, X_test, y_train, y_test


# Function to split the data in chronological order (i.e take n previous games and predict the following one, then iterate through data in steps of p)
def make_preds_with_split(feature_df, model, n=15, p_increment=1):
    p = 0
    pred_list = []
    scaler = StandardScaler()

    while p <= len(feature_df)-(n+1):
      #Create X and y
      merge_info_df = feature_df[['home','away','date','outcome']].iloc[n:, :]
      X_df = feature_df.drop(columns=['home','away','date','outcome'],axis=1)
      y_df = feature_df['outcome']

      X_train, X_test, y_train, y_test = make_X_y_split(X_df, y_df, p, n)
      X_train = scaler.fit_transform(X_train)
      X_test = scaler.transform(X_test)
      model = model.fit(X_train, y_train)
      res_preds = list(model.predict_proba(X_test)[0])
      preds_dict = {key: value for key, value in zip(y_train.value_counts().index, res_preds)}
      if len(y_train.value_counts()) == 2:
          preds_dict[list({0, 1, 2} - set(y_train.value_counts().index))[0]] = 0

      pred_list.append(preds_dict)
      p += p_increment
    return pred_list, merge_info_df


def make_predict_df(pred_list, merge_info_df):
    df_prob = merge_info_df
    df_prob['home_win'] = [pred[0] for pred in pred_list]
    df_prob['draw']     = [pred[1] for pred in pred_list]
    df_prob['away_win'] = [pred[2] for pred in pred_list]

    return df_prob



if __name__ == '__main__':
    from python_files.ml_logic.feature_dataframe import make_feature_df
    from sklearn.svm import SVC
    feature_df = make_feature_df('BL','18-19', 5)
    svc = SVC(kernel= 'rbf', probability=True)
    pred_list, merge_info_df = make_preds_with_split(feature_df, svc)

    result1 = make_predict_df(pred_list, merge_info_df)
    print(result1)
