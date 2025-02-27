import pytest
from sqlalchemy import func, not_, select

import pandas as pd
from pyopensky.trino import Trino
import os
import time  

# Création de l'instance Trino
trino = Trino()

def fetch_trino(icao):
    # Création du dossier s'il n'existe pas
    output_dir = "jets_flightlist/651-700"
    os.makedirs(output_dir, exist_ok=True)
    
    # Récupération des vols
    df = trino.flightlist("2018-01-01", "2024-12-31", icao24=icao)

    if df is None or df.empty:
        # Si la DataFrame est vide ou None, enregistrer un fichier vide
        output_file = os.path.join(output_dir, f"{icao}_vide.csv")
        df_empty = pd.DataFrame()  # Créer une DataFrame vide
        df_empty.to_csv(output_file, index=False)
        print(f"Aucun vol trouvé pour ICAO {icao}, fichier {icao}_vide.csv sauvegardé.")
        
        # Ajouter l'ICAO à la liste des ICAO sans vol
        save_missing_icao(icao)
        
        return None  # Retourne None pour indiquer qu'il n'y a pas de données
    else:
        # Si la DataFrame contient des données
        df = df.drop("day", axis=1)
        output_file = os.path.join(output_dir, f"{icao}.csv")
        df.to_csv(output_file, index=False)
        print(f"Les données de vol pour ICAO {icao} ont été récupérées et sauvegardées.")
        return True  # Retourne True pour indiquer que les données ont été sauvegardées
    

def save_missing_icao(icao):
    missing_file = "icaos_sans_vol.csv"
    
    # Vérifier si le fichier existe déjà
    if os.path.exists(missing_file):
        # Si le fichier existe, on l'ouvre pour ajouter l'ICAO
        df_missing = pd.read_csv(missing_file, dtype=str)
        # Utiliser pd.concat() pour ajouter l'ICAO
        df_new = pd.DataFrame({"icao24": [icao]})
        df_missing = pd.concat([df_missing, df_new], ignore_index=True)
    else:
        # Si le fichier n'existe pas, on le crée avec l'ICAO
        df_missing = pd.DataFrame({"icao24": [icao]})
    
    # Sauvegarder le fichier mis à jour
    df_missing.to_csv(missing_file, index=False)
    print(f"ICAO {icao} ajouté à {missing_file}")

def data_icao(debut, stop):
    # Lire le fichier CSV
    df = pd.read_csv("icao_jets.csv", dtype=str)
    
    # Récupérer les ICAO entre les indices debut et stop (inclus)
    icaos = df["icao24"].iloc[debut-1:stop].tolist()
    i = debut 
    # Appeler la fonction fetch_trino pour chaque ICAO
    for icao in icaos:
        print(f"{i}/{stop}")
        success = fetch_trino(icao)
        if success is None:
            print(f"ICAO {icao} a été traité mais aucun vol n'a été trouvé.")
        
        # Ajouter un délai de sécurité de 2 secondes avant de relancer la fonction
        time.sleep(2)

        i = i + 1 
        
# Exemple d'utilisation
data_icao(701, 750)
