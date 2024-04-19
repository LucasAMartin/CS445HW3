import pandas as pd
import numpy as np

# Load the data, assuming the first row is header and the first column is index
df = pd.read_csv('taxData2021.txt', sep='\t', index_col=0)

# Replace 'X' with NaN
df.replace('X', np.nan, inplace=True)

# Convert the DataFrame to float
df = df.astype(float)

# Calculate the mean of each row excluding the first two columns
row_mean = df.iloc[:, 2:].mean(axis=1)

# Replace NaN values with the row mean if no zero in the row, else replace with 0
for i in df.index:
    if 0 in df.loc[i].values:
        df.loc[i] = df.loc[i].fillna(0)
    else:
        df.loc[i] = df.loc[i].fillna(row_mean[i])

# Save the cleaned data
df.to_csv('cleaned_data.csv')