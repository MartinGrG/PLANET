import pandas as pd

def fill_missing_arrivals(df,acceptable_range):
    for index, row in df.iterrows():
        if pd.isna(row['arrival']):  # Si arrival est vide
            if pd.isna(row['departure']):
                continue  # Laisser vide si departure aussi est vide
            
            departure_airport = row['departure']
            flight_duration = row['flightDuration']
            
            # Filtrer les vols ayant le même aéroport de départ ou d'arrivée, exclure la ligne courante
            similar_flights = df[
            ((df['departure'] == departure_airport) | (df['arrival'] == departure_airport)) &
            df['departure'].notna() & df['arrival'].notna()]
            similar_flights = similar_flights[similar_flights.index != index]
            
            # Filtrer les vols avec un temps de vol similaire (+-10%)
            similar_flights = similar_flights[
                similar_flights['flightDuration'].between(flight_duration * (1-acceptable_range), flight_duration * (1+acceptable_range), inclusive='both')
            ]
            
            # Si aucun vol similaire n'est trouvé, continuer
            if len(similar_flights) < 1:
                continue
            
            if len(similar_flights) == 1: # s'il n'y a qu'une seule correspondance 
                if similar_flights.iloc[0]['departure'] != row['departure']:
                    df.at[index, 'arrival'] = similar_flights.iloc[0]['departure'] 
                else : 
                    df.at[index, 'arrival'] = similar_flights.iloc[0]['arrival']  
                print(f"{index + 2}: {df.at[index, 'arrival']} from {similar_flights.index[0] + 2}")
            elif len(similar_flights) > 1:
                # Vérifier que similar_flights n'est pas vide avant d'accéder à idxmin()
                if not similar_flights.empty:
                    closest_idx = (similar_flights['flightDuration'] - flight_duration).abs().idxmin()
                    if closest_idx in similar_flights.index:  # Vérifier que l'index existe
                        closest_match = similar_flights.loc[closest_idx]
                        if closest_match['departure'] != row['departure']:
                            df.at[index, 'arrival'] = closest_match['departure']
                        else: 
                            df.at[index, 'arrival'] = closest_match['arrival']
                        print(f"{index + 2}: {df.at[index, 'arrival']} from {closest_idx + 2}")
    
    return df

def fill_missing_departure(df,acceptable_range):
    for index, row in df.iterrows():
        if pd.isna(row['departure']):  # Si arrival est vide
            if pd.isna(row['arrival']):
                continue  # Laisser vide si departure aussi est vide
            
            arrival_airport = row['arrival']
            flight_duration = row['flightDuration']
            
            # Filtrer les vols ayant le même aéroport de départ ou d'arrivée, exclure la ligne courante
            similar_flights = df[
            ((df['departure'] == arrival_airport) | (df['arrival'] == arrival_airport)) &
            df['departure'].notna() & df['arrival'].notna()]
            similar_flights = similar_flights[similar_flights.index != index]
            
            # Filtrer les vols avec un temps de vol similaire (+-10%)
            similar_flights = similar_flights[
                similar_flights['flightDuration'].between(flight_duration * (1-acceptable_range), flight_duration * (1+acceptable_range), inclusive='both')
            ]
            
            # Si aucun vol similaire n'est trouvé, continuer
            if len(similar_flights) < 1:
                continue
            
            if len(similar_flights) == 1: # s'il n'y a qu'une seule correspondance 
                if similar_flights.iloc[0]['arrival'] != row['arrival']:
                    df.at[index, 'departure'] = similar_flights.iloc[0]['arrival'] 
                else : 
                    df.at[index, 'departure'] = similar_flights.iloc[0]['departure']  
                print(f"{index + 2}: {df.at[index, 'arrival']} from {similar_flights.index[0] + 2}")
            elif len(similar_flights) > 1:
                # Vérifier que similar_flights n'est pas vide avant d'accéder à idxmin()
                if not similar_flights.empty:
                    closest_idx = (similar_flights['flightDuration'] - flight_duration).abs().idxmin()
                    if closest_idx in similar_flights.index:  # Vérifier que l'index existe
                        closest_match = similar_flights.loc[closest_idx]
                        if closest_match['arrival'] != row['arrival']:
                            df.at[index, 'departure'] = closest_match['arrival']
                        else: 
                            df.at[index, 'departure'] = closest_match['departure']
                        print(f"{index + 2}: {df.at[index, 'arrival']} from {closest_idx + 2}")
    
    return df

def fill_round_trip(df,acceptable_range):
    #Detects round trips and fill the blanks 
    for index, row in df.iterrows():
        #If departure is empty
        if pd.isna(row['departure']) and pd.isna(row['arrival']):  
            continue
        
        if pd.isna(row['departure']): #arrival remplie - departure vide 
            if index > 0:
                if row['arrival'] == df.at[index-1,'departure']:
                    borneInf = row['flightDuration'] * (1-acceptable_range)
                    borneSupp = row['flightDuration'] * (1+acceptable_range)
                    if borneInf < df.at[index-1,'flightDuration'] < borneSupp: #+- 10%
                        df.at[index,'departure'] = df.at[index-1,'arrival']
                        print(f"Round trip departure -1: {index+2}")
            if index < df.shape[0] - 1:
                if row['arrival'] == df.at[index+1,'departure']:
                    borneInf = row['flightDuration'] * (1-acceptable_range)
                    borneSupp = row['flightDuration'] * (1+acceptable_range)
                    if borneInf < df.at[index+1,'flightDuration'] < borneSupp: #+- 10%
                        df.at[index,'departure'] = df.at[index+1,'arrival']
                        print(f"Round trip departure +1: {index+2}")

        if pd.isna(row['arrival']): #arrival vide - departure remplie
            if index > 0: 
                if row['departure'] == df.at[index-1,'arrival']:
                    borneInf = row['flightDuration'] * (1-acceptable_range)
                    borneSupp = row['flightDuration'] * (1+acceptable_range)
                    if borneInf < df.at[index-1,'flightDuration'] < borneSupp: #+- 10%
                        df.at[index,'arrival'] = df.at[index-1,'departure']
                        print(f"Round trip arrival -1: {index+2}")
            if index < df.shape[0] - 1:
                if row['departure'] == df.at[index+1,'arrival']:
                    borneInf = row['flightDuration'] * (1-acceptable_range)
                    borneSupp = row['flightDuration'] * (1+acceptable_range)
                    if borneInf < df.at[index+1,'flightDuration'] < borneSupp: #+- 10%
                        df.at[index,'arrival'] = df.at[index+1,'departure']
                        print(f"Round trip arrival + 1: {index+2}")
    return df

def count_na(df, columns):

    na_counts = df[columns].isna().sum()  # Count NaN in columns
    total_na = na_counts.sum()  

    for col, count in na_counts.items():
        print(f" - {col}: {count}")
    
    print(f"\nTotal {total_na}")







