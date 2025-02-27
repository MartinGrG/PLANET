import pandas as pd

# Charger le fichier CSV
def calculate_flight_duration(file_path):
    df = pd.read_csv(file_path)
    
    # Convertir les colonnes de date en format datetime
    df['firstseen'] = pd.to_datetime(df['firstseen'], errors='coerce')
    df['lastseen'] = pd.to_datetime(df['lastseen'], errors='coerce')
    
    # Calculer la durée du vol
    df['flightDuration'] = (df['lastseen'] - df['firstseen']).dt.total_seconds() / 60  # en minutes
    
    # Écraser le fichier original avec la nouvelle colonne
    df.to_csv(file_path, index=False)
    print(f"Fichier mis à jour sauvegardé sous : {file_path}")
    
    return df

# Exemple d'utilisation
file_path = 'A/4d215f.csv'  # Remplace par le nom de ton fichier
calculate_flight_duration(file_path)