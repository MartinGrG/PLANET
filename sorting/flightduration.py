import pandas as pd

# Load the CSV file
def calculate_flight_duration(file_path):
    df = pd.read_csv(file_path, encoding="utf-8")

    
    # Convert the date columns to datetime format
    df['firstseen'] = pd.to_datetime(df['firstseen'], errors='coerce')
    df['lastseen'] = pd.to_datetime(df['lastseen'], errors='coerce')
    
    # Calculate the flight duration
    df['flightDuration'] = (df['lastseen'] - df['firstseen']).dt.total_seconds() / 60  # in minutes
    
    # Overwrite the original file with the new column
    df.to_csv(file_path, index=False)
    #print(f"Updated file saved as: {file_path}")
    
    return df
