import os
import json

# Pfad zum Ordner, der die JSON-Dateien enthält
folder_path = r'C:\Users\kimsp\.vscode\.vscode\Studienaufbereitung\Reifegrad_Studie_RLS\Auswertung_2'

# Liste aller JSON-Dateien im angegebenen Ordner
file_names = [f for f in os.listdir(folder_path) if f.endswith('.json')]

# Funktion zum Hinzufügen eines neuen Schlüssels basierend auf dem Dateinamen
def add_key_to_json(file_path, key_name):
    with open(file_path, 'r') as file:
        data = json.load(file)
        # Hinzufügen des neuen Schlüssels
        base_name = os.path.basename(file_path)  # Z.B. "processed_stats_Eff0.3_Rob0.5.json"
        specific_name = base_name.replace('processed_stats_', '').rsplit('.', 1)[0]  # Entfernt "processed_stats_" und ".json"
        data[key_name] = specific_name
    return data

# Durchgehen aller Dateien und Anwenden der Funktion
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    modified_data = add_key_to_json(file_path, 'file_name')
    # Optional: Speichern der modifizierten Daten in einer neuen Datei
    new_file_path = os.path.join(folder_path, 'modified_' + file_name)
    with open(new_file_path, 'w') as new_file:
        json.dump(modified_data, new_file, indent=4)


