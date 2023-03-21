from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier

def make_xgb():
    xgb = XGBClassifier(objective='multi:softproba', num_class=3,learning_rate=0.01, colsample_bytree=0.8, max_depth=3, n_estimators=50, subsample=0.8)
    return xgb

def make_random_forest():
    random_forest = RandomForestClassifier()
    return random_forest

def make_svc():
    svc = SVC(kernel='rbf', probability=True)
    return svc

def adaboost_svc():
    svc = SVC(kernel='rbf', probability=True)
    adb_svc = AdaBoostClassifier(svc)
    return adb_svc
