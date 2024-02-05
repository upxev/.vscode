import os
import json
import numpy as np

# Pfade zu den Ordnern
folders = [
    r'C:\Users\kimsp\.vscode\.vscode\Studienaufbereitung\Reifegrad_Studie_RLS\Auswertung_1',
    r'C:\Users\kimsp\.vscode\.vscode\Studienaufbereitung\Reifegrad_Studie_RLS\Auswertung_2',
    r'C:\Users\kimsp\.vscode\.vscode\Studienaufbereitung\Reifegrad_Studie_RLS\Auswertung_3'
]

# Funktion zum Einlesen der JSON-Dateien und Berechnung des Mittelwerts
import numpy as np

def calculate_average(files):
    # Initialisierung einer leeren Liste für jede Schlüsselkategorie
    num_stations_data = {k: [] for k in ["MS", "MLS", "RLS", "AS"]}
    utilization_stations_data = {k: [] for k in ["MS", "MLS", "RLS", "AS", "all_stations"]}
    
    # Durchlaufen der Dateien und Sammeln der Daten
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            for key in num_stations_data:
                num_stations_data[key].append(data["num_stations"][key])
            for key in utilization_stations_data:
                clean_data = []
                for item in data["utilization_stations"][key]:
                    if isinstance(item, list):  # Wenn das Element eine Liste ist
                        clean_sublist = [float(x) if x != "-" else np.nan for x in item]
                        clean_data.append(clean_sublist)
                    else:  # Wenn das Element ein float oder "-" ist
                        clean_data.append(float(item) if item != "-" else np.nan)
                utilization_stations_data[key].append(clean_data)
                
    # Berechnung des Mittelwerts, ignoriert np.nan Werte
    average_data = {
        "num_stations": {k: np.nanmean(np.array(v), axis=0).tolist() for k, v in num_stations_data.items()},
        "utilization_stations": {}
    }
    
    for k, v in utilization_stations_data.items():
        try:
            # Berechnung des Mittelwerts für jede Kategorie, wobei np.nan Werte ignoriert werden
            clean_array = np.array(v, dtype=object)
            # Prüfung, ob nach der Umwandlung in ein NumPy-Array die Operation durchführbar ist
            if clean_array.size == 0 or np.all(np.isnan(clean_array)):
                average = np.nan
            else:
                average = np.nanmean(clean_array.astype(float), axis=0)
            average_data["utilization_stations"][k] = average.tolist()
        except ZeroDivisionError:
            # Fallback für den Fall, dass eine Division durch Null versucht wird
            average_data["utilization_stations"][k] = np.nan
    
    return average_data



# Hauptfunktion
def main():
    # Annahme: Jeder Ordner enthält Dateien mit identischen Namen
    file_names = os.listdir(folders[0])
    for file_name in file_names:
        if file_name.endswith('.json'):
            files = [os.path.join(folder, file_name) for folder in folders]
            average_data = calculate_average(files)
            
            # Speichern der durchschnittlichen Daten in einer neuen Datei
            new_file_path = os.path.join(folders[0], 'average_' + file_name)  # Beispiel für Speicherort
            with open(new_file_path, 'w') as new_file:
                json.dump(average_data, new_file, indent=4)

if __name__ == '__main__':
    main()
