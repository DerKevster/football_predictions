import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns

def get_correlation(data):
    # Apply Standard Scaler

    data = data.drop(columns=['home', 'away', 'date'])

    scaler = StandardScaler()

    scaled_df = scaler.fit_transform(data)
    scaled_df = pd.DataFrame(scaled_df, columns=data.columns)

    # Showing the Correlation Matrix

    correlation_matrix = data.corr()
    column_names = correlation_matrix.columns
    print(sns.heatmap(correlation_matrix, xticklabels=column_names, yticklabels=column_names,cmap= "bwr"))
