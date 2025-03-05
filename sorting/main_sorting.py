from delete_not_relevant_data import delete_not_relevant_csv
from sort_by_date import sort_date
from flightduration import calculate_flight_duration
from fillingGaps import (fill_missing_arrivals, fill_missing_departure, fill_round_trip
                        ,count_na_airports, delete_too_much_blanks, fill_with_unknown,
                        delete_if_unknown)
import pandas as pd
import os

root_folder = "Folder to sort"

for folder in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, folder)  # Ajout du chemin complet
    
    if not os.path.isdir(folder_path):  # Vérifie que c'est bien un dossier
        continue

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        # Supprime les fichiers .DS_Store directement
        if file.lower() == ".ds_store":
            os.remove(file_path)
            continue  # Passe au fichier suivant
        
    #Delete files that contain not enough or too many lines 
    min_lines = 48  
    for file in os.listdir(folder_path):  # Utilisation de folder_path
        path = os.path.join(folder_path, file)
        if delete_not_relevant_csv(path, min_lines):
            os.remove(path)

    #Sort all flights by date and add flight duration column
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        sort_date(path)
        calculate_flight_duration(path)

    # Fills the missing airports 
    acceptable_range_round_trip = 0.1  
    acceptable_range_missing = 0.1  
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        df = pd.read_csv(path)
        blanks = 10000
        while (blanks - count_na_airports(df, ["departure", "arrival"])[0]) != 0:
            blanks = count_na_airports(df, ["departure", "arrival"])[0]
            df = fill_round_trip(df, acceptable_range_round_trip)
            df = fill_missing_arrivals(df, acceptable_range_missing)
            df = fill_missing_departure(df, acceptable_range_missing)
        df.to_csv(path, index=False)

    # Delete files if the ratio blank lines/total lines is over 'acceptable_range_blank_lines'
    acceptable_range_blank_lines = 4
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        df = pd.read_csv(path)
        result, output, percentage1, percentage2 = delete_too_much_blanks(df, acceptable_range_blank_lines)
        if result:
            os.remove(path)
        else:
            output.to_csv(path, index=False)

    acceptable_range_blank_airport = 15
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        df = pd.read_csv(path)
        total_na, _, _ = count_na_airports(df)
        percentage = round(total_na / len(df) * 100, 1)
        if percentage > acceptable_range_blank_airport:
            os.remove(path)
        #print(f"{file}: {percentage}%")

    # Filling remaining blanks with 'unknown departure' and 'unknown arrival'
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        df = pd.read_csv(path)
        df = fill_with_unknown(df)
        df = delete_if_unknown(df)
        df.to_csv(path, index=False)

# Fusionner tous les fichiers CSV restants en un seul
merged_df = pd.DataFrame()  # Crée un DataFrame vide pour la fusion

for folder in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, folder)
    if not os.path.isdir(folder_path):
        continue

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        if file.endswith(".csv"):  # Vérifie que c'est bien un fichier CSV
            df = pd.read_csv(path)
            merged_df = pd.concat([merged_df, df], ignore_index=True)  # Concatène les fichiers

# Sauvegarde dans un fichier unique
merged_df.to_csv("sorted_DB.csv", index=False)
print("Fusion terminée : sorted_DB.csv créé.")




