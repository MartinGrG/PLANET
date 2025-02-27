from delete_empty import delete_empt
from delete_not_enought_data import delete_small_csv
from sort_by_date import sort_date
dossier = "A"
dossier_stockage_supprimees = "deleted_jets_1-50.csv"
##Supprime tous les fichier ayant "_vide".
#delete_empt(dossier,dossier_stockage_supprimees)

##Supprime les fichiers avec moins de 48 lignes (correspond à moins de 1 vol par mois)
#delete_small_csv(dossier,48,dossier_stockage_supprimees)

##Tri les vols par ordre chronologique
sort_date(dossier)
