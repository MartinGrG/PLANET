import os
import csv

# Specify the folder path
def delete_small_csv(folder, minimum, output_file):
    # Ouvrir le fichier de sortie en mode ajout
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Vérifier si le fichier est vide et ajouter l'en-tête si nécessaire
        file.seek(0, os.SEEK_END)  # Aller à la fin du fichier
        if file.tell() == 0:  # Si le fichier est vide, ajouter l'en-tête
            writer.writerow(["icao24"])

        # Parcourir les fichiers du dossier
        for fichier in os.listdir(folder):
            if fichier.endswith(".csv"):
                file_path = os.path.join(folder, fichier)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Vérifier si le fichier a moins de lignes que le minimum
                    if len(lines) < minimum:
                        # Extraire le numéro ICAO24 du nom du fichier
                        icao24 = fichier.split('.')[0]
                        # Ajouter l'ICAO24 dans le fichier CSV
                        writer.writerow([icao24])
                        
                        # Supprimer le fichier
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")

