import pandas as pd
from python_files.ml_logic.feature_analysis import get_correlation
from python_files.ml_logic.basemodel import get_validation

# Create TEST DATAFRAME

columns = pd.read_csv("~/code/DerKevster/football_predictions/Columns.csv", delimiter=';').iloc[:,:2]
data = pd.DataFrame(columns=columns['Key'])
for i in list(columns['Key']):
    data[i] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print(get_correlation(data))

print(get_validation(data))
