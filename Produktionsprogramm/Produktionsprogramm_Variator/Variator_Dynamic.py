import json
import plotly.graph_objects as go

import math

def distribute_quality_dynamic(json_dateipfad, base_ratio=0.5, amplitude=0.25, frequency=1):
    """
    Verteilt die Gesamtproduktion jedes Motors pro Periode auf die
    Qualitätsklassen mit einer entgegengesetzt sinusförmigen Schwankung,
    wobei berücksichtigt wird, dass nicht jeder Motor in jeder Periode produziert wird.
    
    :param production_plan: Produktionsprogramm als Dictionary
    :param base_ratio: Basisanteil der sehr guten Qualität ohne Schwankung
    :param amplitude: Amplitude der Schwankung um den Basisanteil
    :param frequency: Frequenz der Schwankungen pro tatsächlich produzierter Periode für jeden Motor
    :return: Neuer Produktionsplan mit verteilter Qualität
    """
    with open(json_dateipfad, 'r') as json_datei:
            production_plan = json.load(json_datei)
    
    motor_period_count = {}  # Zählt, wie viele Perioden seit der letzten Produktion für jeden Motor vergangen sind

    for period, details in production_plan.items():
        if "ID" in details:
            for motor, production in details.items():
                if motor in ["ID", "duration"]:
                    continue
                
                # Initialisiere den Zähler für den Motor, wenn noch nicht geschehen
                if motor not in motor_period_count:
                    motor_period_count[motor] = 0
                
                total_production = sum(production.values())
                if total_production > 0:
                    # Berechne quality_ratio für diesen Motor basierend auf einer Sinusfunktion
                    phase = (2 * math.pi * frequency * motor_period_count[motor]) / len(production_plan)
                    quality_ratio = base_ratio + amplitude * math.sin(phase)
                    
                    production['c0p0s0m0'] = round(total_production * quality_ratio)
                    production['c1p1s0m0'] = total_production - production['c0p0s0m0']
                    
                    # Setze alle anderen Qualitätsklassen auf 0
                    for key in production:
                        if key not in ['c0p0s0m0', 'c1p1s0m0']:
                            production[key] = 0
                    
                    # Zähle die Perioden für diesen Motor
                    motor_period_count[motor] += 1
                else:
                    # Wenn ein Motor in einer Periode nicht produziert wird, überspringe diese Periode
                    continue
                    
    return production_plan


# Anpassbare Parameter
base_ratio = 0.5  # Basisanteil der sehr guten Qualität
amplitude = 0.25  # Amplitude der Schwankung
frequency = 5   # Frequenz der Schwankungen pro tatsächlich produzierter Periode für jeden Motor --> hier schwankt x mal über 64/ 48 Perioden
json_dateipfad = r"C:\Users\kimsp\.vscode\.vscode\Produktionsprogramm\Produktionsprogramm_Variator\Input\weekly_allQK_gleichmäßig_ein_Jahr.json"
# Verteile die Qualität basierend auf einer entgegengesetzt sinusförmigen Schwankung
new_production_plan = distribute_quality_dynamic(json_dateipfad, base_ratio, amplitude, frequency)

with open(r"C:\Users\kimsp\.vscode\.vscode\Produktionsprogramm\Produktionsprogramm_Variator\Output\output_Produktionsprogramm_ein_Jahr_dynamic", 'w') as json_datei:
        json.dump(new_production_plan, json_datei, indent=2)  



def plot_quality_distribution_relative_all(production_plan, file_name):
    """
    Erstellt ein Plotly-Diagramm, das den relativen Anteil der Qualitätsklassen pro Motortyp
    über die verschiedenen Perioden visualisiert.
    
    :param production_plan: Produktionsprogramm nach Verteilung der Qualität
    """
    # Erstelle Datenstrukturen für die Plots
    data = {}
    for period, details in production_plan.items():
        period_id = details['ID'] if 'ID' in details else period
        for motor, production in details.items():
            if motor in ["ID", "duration"]:
                continue
            if motor not in data:
                data[motor] = {'periods': [], 'high_quality_ratio': [], 'low_quality_ratio': []}
            
            total_production = sum(production.values())
            if total_production > 0:
                high_quality_ratio = (production.get('c0p0s0m0', 0) / total_production) * 100
                low_quality_ratio = (production.get('c1p1s0m0', 0) / total_production) * 100
            else:
                high_quality_ratio = 0
                low_quality_ratio = 0
            
            data[motor]['periods'].append(period_id)
            data[motor]['high_quality_ratio'].append(high_quality_ratio)
            data[motor]['low_quality_ratio'].append(low_quality_ratio)
    
    # Erstelle Plots für jeden Motortyp
    fig = go.Figure()
    
    for motor, values in data.items():
        fig.add_trace(go.Scatter(x=values['periods'], y=values['high_quality_ratio'],
                                 mode='lines+markers', name=f'{motor} High Quality %'))
        fig.add_trace(go.Scatter(x=values['periods'], y=values['low_quality_ratio'],
                                 mode='lines+markers', name=f'{motor} Low Quality %'))
    
    # Update Plot Layout
    fig.update_layout(title='Relativer Anteil der Qualitätsklassen pro Motortyp über die Zeit',
                      xaxis_title='Periode',
                      yaxis_title='Anteil (%)',
                      legend_title='Legende',
                      yaxis=dict(tickformat=".2f"))

    fig.write_html(file_name)
    fig.show()
   
   
plot_quality_distribution_relative_all(new_production_plan, "quality-distribution-all.html")

import plotly.graph_objects as go

def plot_quality_distribution_relative_motors(production_plan, file_name):
    data = {}
    motor_types = set()  # Ein Set, um alle Motortypen zu speichern
    for period, details in production_plan.items():
        period_id = details['ID'] if 'ID' in details else period
        for motor, production in details.items():
            if motor in ["ID", "duration"]:
                continue
            motor_types.add(motor)  # Füge Motortyp zum Set hinzu
            if motor not in data:
                data[motor] = {'periods': [], 'high_quality_ratio': [], 'low_quality_ratio': []}
            
            total_production = sum(production.values())
            high_quality_ratio = (production.get('c0p0s0m0', 0) / total_production) * 100 if total_production > 0 else 0
            low_quality_ratio = (production.get('c1p1s0m0', 0) / total_production) * 100 if total_production > 0 else 0
            
            data[motor]['periods'].append(period_id)
            data[motor]['high_quality_ratio'].append(high_quality_ratio)
            data[motor]['low_quality_ratio'].append(low_quality_ratio)
    
    fig = go.Figure()
    trace_visibility = {motor: [False] * 2 * len(motor_types) for motor in motor_types}  # Initialisiere alle Spuren als unsichtbar
    
    for i, motor in enumerate(motor_types):
        values = data[motor]
        # High Quality Trace
        fig.add_trace(go.Scatter(x=values['periods'], y=values['high_quality_ratio'],
                                 mode='lines+markers', name=f'{motor} High Quality %', visible=False))
        # Low Quality Trace
        fig.add_trace(go.Scatter(x=values['periods'], y=values['low_quality_ratio'],
                                 mode='lines+markers', name=f'{motor} Low Quality %', visible=False))
        trace_visibility[motor][i*2] = True  # Setze nur die aktuellen Spuren auf sichtbar
        trace_visibility[motor][i*2 + 1] = True

    # Erstelle Dropdown-Buttons für jeden Motortyp
    buttons = [dict(label=motor,
                    method="update",
                    args=[{"visible": visible},
                          {"title": f"Qualitätsverteilung: {motor}"}])
               for motor, visible in trace_visibility.items()]
    
    # Füge einen Button hinzu, um alle Daten anzuzeigen
    buttons.append(dict(label="Alle Motortypen",
                        method="update",
                        args=[{"visible": [True] * 2 * len(motor_types)},  # Alle Spuren sichtbar
                              {"title": "Qualitätsverteilung: Alle Motortypen"}]))

    # Dropdown-Menü hinzufügen
    fig.update_layout(
        updatemenus=[dict(buttons=buttons,
                          direction="down",
                          pad={"r": 10, "t": 10},
                          showactive=True,
                          x=0.1,
                          xanchor="left",
                          y=1.15,
                          yanchor="top")],
        title='Qualitätsverteilung: Alle Motortypen',
        xaxis_title='Periode',
        yaxis_title='Anteil (%)',
        legend_title='Legende',
        yaxis=dict(tickformat=".2f"))

    fig.write_html(file_name)
    fig.show()

# Beispielaufruf der Funktion
plot_quality_distribution_relative_motors(new_production_plan, "quality_distribution_motortypes_motors.html")


