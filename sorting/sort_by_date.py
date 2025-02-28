import os
import pandas as pd


def sort_date(file):
    # Iterate through all files in the folder
    if file.endswith('.csv'):        
        # Load the CSV file
        df = pd.read_csv(file)

        # Convert the date columns to datetime format
        df['firstseen'] = pd.to_datetime(df['firstseen'])

        # Sort the data by the 'firstseen' column
        df_sorted = df.sort_values(by='firstseen')

        # Save the sorted file, overwriting the old file
        df_sorted.to_csv(file, index=False)

        print(f"The file '{file}' has been sorted and replaced the old file.")
