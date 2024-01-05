import json
from datetime import datetime
import sys

def updateLog(errors_list):
    errors_list = list(errors_list)
    # Créer un dictionnaire avec la date et l'heure actuelles
    log_entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "logs": errors_list}

    # Charger les données existantes du fichier logs.json
    try:
        with open("caches/logs.json", "r") as file:
            logs_data = json.load(file)
    except:
        logs_data = []

    # Ajouter l'entrée de log aux données existantes
    logs_data.append(log_entry)

    # Réécrire le fichier logs.json avec les nouvelles données en ajoutant une ligne vide entre chaque élément
    with open("caches/logs.json", "w") as file:
        json.dump(logs_data, file, indent=4, separators=(", ", ": "))

def handle_crash():
    print("fermeture du logiciel")
    # Récupérer la raison du crash à partir de sys.exc_info() puis l'enregistre dans les logs
    exception_type, exception_value, exception_traceback = sys.exc_info()
    reason = repr(exception_value)
    if reason != None : 
        updateLog([reason])
    



updateLog(["Starting Security Scan"])


