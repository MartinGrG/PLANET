import os
import pandas as pd



def sort_date(folder_path):
    # Parcourir tous les fichiers dans le dossier
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            
            # Charger le fichier CSV
            df = pd.read_csv(file_path)

            # Convertir les colonnes de dates en format datetime
            df['firstseen'] = pd.to_datetime(df['firstseen'])

            # Trier les données par la colonne 'firstseen'
            df_sorted = df.sort_values(by='firstseen')

            # Sauvegarder le fichier trié en écrasant l'ancien fichier
            df_sorted.to_csv(file_path, index=False)

            print(f"Le fichier '{filename}' a été trié et a remplacé l'ancien fichier.")

