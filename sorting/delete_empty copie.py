import os
import csv

def delete_empt(dossier,deleted_file):
    deleted_icao24 = []  # Liste pour stocker les numéros ICAO24
    for fichier in os.listdir(dossier):
        if fichier.endswith("_vide.csv"):
            # Extraire le numéro ICAO24 du nom du fichier
            icao24 = fichier.split('_')[0]
            # Ajouter l'ICAO24 à la liste
            deleted_icao24.append(icao24)
            
            # Supprimer le fichier
            chemin_fichier = os.path.join(dossier, fichier)
            os.remove(chemin_fichier)
            print(f"Supprimé : {chemin_fichier}")
    
    # Enregistrer les numéros ICAO24 dans le fichier CSV
    if deleted_icao24:
        with open(deleted_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["icao24"])  # En-tête
            for icao24 in deleted_icao24:
                writer.writerow([icao24])

