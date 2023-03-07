import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, cross_val_score


xgb = XGBClassifier(max_depth=10, n_estimators=100, learning_rate=0.1)
xgb.fit()

scores = cross_val_score(xgb, X, y, cv=5, scoring='roc_auc')

params = {
    'learning_rate': [0.0001, 0.001, 0.01, 0.1, 0.2, 0.3],
    'n_estimators': [int(x) for x in np.linspace(start=100, stop=500, num=9)],
}

rgs = RandomizedSearchCV(estimator=xgb, param_distributions=params, n_iter=20, cv=5, random_state=42, n_jobs=-1,
                         scoring='roc_auc', return_train_score=True)

rgs.fit()
print(rgs.results(gs=rgs, print_all=False))
