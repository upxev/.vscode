import json
import plotly.graph_objects as go

json_dateipfad = r'C:\Users\Wiwi\.vscode\Produktionsprogramm_Visualisator\weekly_QK1_perfekter_Zustand.json'

with open(json_dateipfad, 'r') as datei:
    daten = json.load(datei)

# Dictionary für JSON
produktionsdaten = {}

for periode, periode_daten in daten.items():
    produktionsdaten[periode] = {
        "ID": periode_daten["ID"],
        "duration": periode_daten["duration"],
        "motoren": {}
    }
    for motor, motor_daten in periode_daten.items():
        if motor not in ["ID", "duration"]:  # ID und duration ausschließen
            produktionsdaten[periode]["motoren"][motor] = {}
            for qualitaetsklasse, menge in motor_daten.items():
                produktionsdaten[periode]["motoren"][motor][qualitaetsklasse] = menge

#print(json.dumps(produktionsdaten, indent=4))
#Plot für Produktionsmenge pro Motortyp
fig = go.Figure()

for periode, periode_daten in produktionsdaten.items():
    periode_id = periode_daten["ID"]  # Die ID der Periode, z.B. "2021-W39"
    for motor, motor_daten in periode_daten["motoren"].items():
        # Extrahiere die Produktionsmengen für jede Qualitätsklasse des Motors
        mengen = [menge for qualitaetsklasse, menge in motor_daten.items() if qualitaetsklasse.startswith('c0p0s0')]
        
        # Überprüfe, ob der Motor bereits einen Trace hat; wenn nicht, füge einen neuen hinzu
        if not any(trace.name == motor for trace in fig.data):
            fig.add_trace(go.Bar(name=motor, x=[periode_id], y=[sum(mengen)]))
        else:
            # Finde den bestehenden Trace und füge die neue Menge hinzu
            for trace in fig.data:
                if trace.name == motor:
                    trace.x = trace.x + (periode_id,)
                    trace.y = trace.y + (sum(mengen),)

# Layout
fig.update_layout(
    title='Produktionsprogramm',
    xaxis_title='Periode',
    yaxis_title='Produktionsmenge',
    barmode='group'
)
fig.show()
fig.write_html('C:/Users/Wiwi/.vscode/Produktionsprogramm_Visualisator/Produktionsprogramm_weeekly_by_motortype.html')



# Plot für Gesamtproduktionsmenge pro Periode
gesamt_fig = go.Figure()

periode_ids = []
gesamtproduktionsmengen = []

# Durchlaufe alle Perioden und summiere die Produktionsmengen aller Motoren
for periode, periode_daten in produktionsdaten.items():
    periode_id = periode_daten["ID"]
    gesamtmenge_pro_periode = 0

    for motor, motor_daten in periode_daten["motoren"].items():
        # Summiere die Mengen für alle Qualitätsklassen des Motors
        gesamtmenge_pro_periode += sum(motor_daten.values())

    # Füge die gesammelten Daten den Listen hinzu
    periode_ids.append(periode_id)
    gesamtproduktionsmengen.append(gesamtmenge_pro_periode)

# Füge die gesammelten Daten als Trace zum Diagramm hinzu
gesamt_fig.add_trace(go.Bar(x=periode_ids, y=gesamtproduktionsmengen))


gesamt_fig.update_layout(
    title='Gesamtproduktionsmenge pro Periode',
    xaxis_title='Periode',
    yaxis_title='Gesamtproduktionsmenge',
    barmode='group'
)


gesamt_fig.show()
gesamt_fig.write_html('C:/Users/Wiwi/.vscode/Produktionsprogramm_Visualisator/Produktionsprogramm_weeekly_total.html')
