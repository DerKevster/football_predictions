from python_files.ml_logic.feature_dataframe import make_dataframe_row as md
from python_files.feature_engineering.merge_dataframes import make_merged_df
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, train_test_split

from sklearn.pipeline import make_pipeline
from sklearn.pipeline import make_union
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler

#create dataframe, X and y

df = make_merged_df()
data = md('Bayern Munich', 'Ein Frankfurt', 34, df)

X = data.drop(columns=['home','away','matchday','win_home','draw','win_away'],axis=1)
y = data[['win_home', 'draw', 'win_away']]

# Preprocessor
num_transformer = make_pipeline(StandardScaler())

preproc = make_column_transformer(
    (num_transformer),
    remainder='passthrough'
    )

#XGBclassifier pipeline
xgb_cla = XGBClassifier(max_depth=10, n_estimators=100, learning_rate=0.1, objective='multi:softmax', num_class=3, random_state=42)
xgb_cla.fit(X, y)
y_pred = xgb_cla.predict(X_val)

pipe_xgb = make_pipeline(preproc, xgb_cla)
cv_results = cross_val_score(pipe_xgb, X, y, cv=5, scoring='accuracy').mean()

# RandomizedSearchCV parameters
params = [
        {'learning_rate': [0.0001, 0.001, 0.01, 0.1, 0.2, 0.3]},
        {'n_estimators': [int(x) for x in np.linspace(start=100, stop=500, num=9)]},
    ]

rgs = RandomizedSearchCV(estimator=xgb_cla, param_distributions=params, n_iter=10, cv=5, random_state=42, n_jobs=-1,
                            scoring='accuracy', return_train_score=True)

rgs.fit()
