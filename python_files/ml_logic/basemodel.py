import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, train_test_split
from sklearn.metrics import accuracy_score

def get_validation(data):
    data = data.drop(columns=['home', 'away', 'date'])

    X = data.drop(columns=['win_home', 'draw', 'win_away'])
    y = data[['win_home', 'draw', 'win_away']]

    xgb = XGBClassifier(max_depth=10, n_estimators=100, learning_rate=0.1)
    xgb.fit(X, y)

    scores = cross_val_score(xgb, X, y, cv=5, scoring='accuracy')

    params = {
        'learning_rate': [0.0001, 0.001, 0.01, 0.1, 0.2, 0.3],
        'n_estimators': [int(x) for x in np.linspace(start=100, stop=500, num=9)],
    }

    rgs = RandomizedSearchCV(estimator=xgb, param_distributions=params, n_iter=20, cv=5, random_state=42, n_jobs=-1,
                            scoring='accuracy', return_train_score=True)

    rgs.fit()
    return print(f'The mean accuracy score is {scores.mean()}') and print(f'the best parameters are {rgs.results(gs=rgs, print_all=False)}')
