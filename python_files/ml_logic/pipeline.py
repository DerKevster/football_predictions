import pandas as pd
from feature_analysis import get_correlation()

# Create TEST DATAFRAME

columns = pd.read_csv("~/code/DerKevster/football_predictions/Columns.csv", delimiter=';').iloc[:,:2]
data = pd.DataFrame(columns=columns['Key'])
for i in list(columns['Key']):
    data[i] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

get_correlation(data)
