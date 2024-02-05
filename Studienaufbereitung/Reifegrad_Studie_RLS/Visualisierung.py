import os
import json
import plotly.graph_objects as go

# Pfad zum Ordner, der die JSON-Dateien enthält
folder_path = r'C:\Users\kimsp\.vscode\.vscode\Studienaufbereitung\Reifegrad_Studie_RLS\Auswertung_1\Auswertung1_aufbereitet'
file_names = [f for f in os.listdir(folder_path) if f.endswith('.json')]

# Initialisierung der Plotly Figur
fig = go.Figure()

# Durchgehen aller Dateien und Extrahieren der Daten
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
        # Spezifischen Namen für die Legende extrahieren
        specific_name = file_name.replace('modified_processed_stats_', '').rsplit('.', 1)[0]
        # Daten für RLS Stationen extrahieren
        rls_stations = data['num_stations']['RLS']
        # Daten zu Plotly Figur hinzufügen
        fig.add_trace(go.Scatter(x=list(range(1, len(rls_stations) + 1)), y=rls_stations, mode='lines', name= specific_name))

# Aktualisierung des Layouts der Figur
fig.update_layout(title='Anzahl der RLS Stationen über die Perioden', xaxis_title='Perioden', yaxis_title='Anzahl verwendeter RLS Stationen', legend_title='Datei')

# Initialisierung der Plotly Figur
fig2 = go.Figure()

# Durchgehen aller Dateien und Extrahieren der Daten
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
        # Spezifischen Namen für die Legende extrahieren
        specific_name = file_name.replace('modified_processed_stats_', '').rsplit('.', 1)[0]
        # Daten für RLS Stationen extrahieren
        rls_stations = data['utilization_stations']['RLS']
        # Daten zu Plotly Figur hinzufügen
        fig2.add_trace(go.Scatter(x=list(range(1, len(rls_stations) + 1)), y=rls_stations, mode='lines', name= specific_name))

# Aktualisierung des Layouts der Figur
fig2.update_layout(title='Aulastung RLS Stationen über die Perioden', xaxis_title='Perioden', yaxis_title='Auslastung RLS Stationen', legend_title='Datei')


# Diagramm anzeigen
html_file_path_1 = os.path.join(folder_path, 'RLS_Stationen_Auswertung.html')
fig.write_html(html_file_path_1)
html_file_path_2 = os.path.join(folder_path, 'RLS_Auslastung_Auswertung.html')
fig.write_html(html_file_path_2)
fig.show()
fig2.show()
