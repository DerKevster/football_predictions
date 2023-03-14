import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
import python_files.ml_logic.feature_dataframe as fd
from python_files.feature_engineering.merge_dataframes import make_merged_df
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


def make_basemodel(data, matrix=False):
    #create Dataframe
    #df = make_merged_df()
    #data = fd.make_feature_df(df,5)

    # Calculate correlation matrix
    if matrix==True:
        corr_matrix = data.corr()

        # Plot correlation matrix as a clustermap
        sns.clustermap(corr_matrix, annot=True, cmap='coolwarm', figsize=(20, 20))
        plt.title("Feature Correlation Clustermap")
        plt.show()

    #Create X and y
    X = data.drop(columns=['home','away','date','outcome'],axis=1)
    y = data['outcome']

    # Split data into train, test set
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.2, random_state = 42)

    # Scale data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled= scaler.transform(X_test)

    # optimized model
    xgb = XGBClassifier(objective='multi:softmax', num_class=3,learning_rate=0.01, colsample_bytree=0.8, max_depth=3, n_estimators=50, subsample=0.8)
    # fit model
    xgb.fit(X_train_scaled, y_train)
    # make predictions
    pred = xgb.predict(X_test_scaled)

    # evaluate predictions
    accuracy = accuracy_score(pred, y_test)
    f1 = f1_score(pred, y_test, average="weighted")

    y_true = y_test
    y_pred = pred
    target_names = ['home', 'draw', 'away']
    report = classification_report(y_true, y_pred, target_names=target_names)
    print(f'Classification Report:\n\n{report}')

    return accuracy
