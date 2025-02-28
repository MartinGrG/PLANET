import pandas as pd

def fill_missing_arrivals(df, acceptable_range):
    for index, row in df.iterrows():
        if pd.isna(row['arrival']):  # If 'arrival' is missing
            if pd.isna(row['departure']):
                continue  # Skip if 'departure' is also missing
            
            departure_airport = row['departure']
            flight_duration = row['flightDuration']
            
            # Filter flights with the same departure or arrival airport, excluding the current row
            similar_flights = df[
                ((df['departure'] == departure_airport) | (df['arrival'] == departure_airport)) &
                df['departure'].notna() & df['arrival'].notna()
            ]
            similar_flights = similar_flights[similar_flights.index != index]
            
            # Filter flights with a similar flight duration (±acceptable_range)
            similar_flights = similar_flights[
                similar_flights['flightDuration'].between(
                    flight_duration * (1 - acceptable_range), 
                    flight_duration * (1 + acceptable_range), 
                    inclusive='both'
                )
            ]
            
            # Skip if no similar flights are found
            if len(similar_flights) < 1:
                continue
            
            if len(similar_flights) == 1:  # If only one match is found
                if similar_flights.iloc[0]['departure'] != row['departure']:
                    df.at[index, 'arrival'] = similar_flights.iloc[0]['departure'] 
                else:
                    df.at[index, 'arrival'] = similar_flights.iloc[0]['arrival']  
                print(f"{index + 2}: {df.at[index, 'arrival']} from {similar_flights.index[0] + 2}")
            elif len(similar_flights) > 1:
                # Ensure similar_flights is not empty before accessing idxmin()
                if not similar_flights.empty:
                    closest_idx = (similar_flights['flightDuration'] - flight_duration).abs().idxmin()
                    if closest_idx in similar_flights.index:  # Ensure index exists
                        closest_match = similar_flights.loc[closest_idx]
                        if closest_match['departure'] != row['departure']:
                            df.at[index, 'arrival'] = closest_match['departure']
                        else:
                            df.at[index, 'arrival'] = closest_match['arrival']
                        print(f"{index + 2}: {df.at[index, 'arrival']} from {closest_idx + 2}")
    return df

def fill_missing_departure(df, acceptable_range):
    for index, row in df.iterrows():
        if pd.isna(row['departure']):  # If 'departure' is missing
            if pd.isna(row['arrival']):
                continue  # Skip if 'arrival' is also missing
            
            arrival_airport = row['arrival']
            flight_duration = row['flightDuration']
            
            # Filter flights with the same departure or arrival airport, excluding the current row
            similar_flights = df[
                ((df['departure'] == arrival_airport) | (df['arrival'] == arrival_airport)) &
                df['departure'].notna() & df['arrival'].notna()
            ]
            similar_flights = similar_flights[similar_flights.index != index]
            
            # Filter flights with a similar flight duration (±acceptable_range)
            similar_flights = similar_flights[
                similar_flights['flightDuration'].between(
                    flight_duration * (1 - acceptable_range), 
                    flight_duration * (1 + acceptable_range), 
                    inclusive='both'
                )
            ]
            
            # Skip if no similar flights are found
            if len(similar_flights) < 1:
                continue
            
            if len(similar_flights) == 1:  # If only one match is found
                if similar_flights.iloc[0]['arrival'] != row['arrival']:
                    df.at[index, 'departure'] = similar_flights.iloc[0]['arrival'] 
                else:
                    df.at[index, 'departure'] = similar_flights.iloc[0]['departure']  
                print(f"{index + 2}: {df.at[index, 'arrival']} from {similar_flights.index[0] + 2}")
            elif len(similar_flights) > 1:
                # Ensure similar_flights is not empty before accessing idxmin()
                if not similar_flights.empty:
                    closest_idx = (similar_flights['flightDuration'] - flight_duration).abs().idxmin()
                    if closest_idx in similar_flights.index:  # Ensure index exists
                        closest_match = similar_flights.loc[closest_idx]
                        if closest_match['arrival'] != row['arrival']:
                            df.at[index, 'departure'] = closest_match['arrival']
                        else:
                            df.at[index, 'departure'] = closest_match['departure']
                        print(f"{index + 2}: {df.at[index, 'arrival']} from {closest_idx + 2}")
    return df

def fill_round_trip(df, acceptable_range):
    # Detects round trips and fills missing values
    for index, row in df.iterrows():
        if pd.isna(row['departure']) and pd.isna(row['arrival']):  
            continue
        
        if pd.isna(row['departure']):  # 'arrival' filled - 'departure' missing 
            if index > 0 and row['arrival'] == df.at[index-1, 'departure']:
                if row['flightDuration'] * (1 - acceptable_range) < df.at[index-1, 'flightDuration'] < row['flightDuration'] * (1 + acceptable_range):
                    df.at[index, 'departure'] = df.at[index-1, 'arrival']
                    print(f"Round trip departure -1: {index+2}")
            if index < df.shape[0] - 1 and row['arrival'] == df.at[index+1, 'departure']:
                if row['flightDuration'] * (1 - acceptable_range) < df.at[index+1, 'flightDuration'] < row['flightDuration'] * (1 + acceptable_range):
                    df.at[index, 'departure'] = df.at[index+1, 'arrival']
                    print(f"Round trip departure +1: {index+2}")

        if pd.isna(row['arrival']):  # 'arrival' missing - 'departure' filled
            if index > 0 and row['departure'] == df.at[index-1, 'arrival']:
                if row['flightDuration'] * (1 - acceptable_range) < df.at[index-1, 'flightDuration'] < row['flightDuration'] * (1 + acceptable_range):
                    df.at[index, 'arrival'] = df.at[index-1, 'departure']
                    print(f"Round trip arrival -1: {index+2}")
            if index < df.shape[0] - 1 and row['departure'] == df.at[index+1, 'arrival']:
                if row['flightDuration'] * (1 - acceptable_range) < df.at[index+1, 'flightDuration'] < row['flightDuration'] * (1 + acceptable_range):
                    df.at[index, 'arrival'] = df.at[index+1, 'departure']
                    print(f"Round trip arrival +1: {index+2}")
    return df

def count_na(df, columns):
    na_counts = df[columns].isna().sum()  # Count NaN values in specified columns
    total_na = na_counts.sum()
    
    for col, count in na_counts.items():
        print(f" - {col}: {count}")
    
    print(f"\nTotal {total_na}")


