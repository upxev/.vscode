import json

# Schritt 1: JSON-Datei einlesen
def lade_produktionsprogramm(dateiname):
    with open(dateiname, 'r') as datei:
        return json.load(datei)

# Schritt 2: Produktionsprogramm umbenennen
def umbenennen_produktionsprogramm(produktionsprogramm):
    sortierte_schlussel = sorted(produktionsprogramm.keys(), key=lambda x: int(x.split("_")[1]))
    neues_programm = {}
    for neue_periodennummer, alter_schlussel in enumerate(sortierte_schlussel, start=1):
        neuer_schlussel = f"period_{neue_periodennummer}"
        neues_programm[neuer_schlussel] = produktionsprogramm[alter_schlussel]
    return neues_programm

# Schritt 3: Das aktualisierte Produktionsprogramm in einer neuen JSON-Datei speichern
def speichern_neues_produktionsprogramm(neues_programm, dateiname):
    with open(dateiname, 'w') as datei:
        json.dump(neues_programm, datei, indent=4)

# Die Funktionen ausführen
dateiname_einlesen =  r'C:\Users\kimsp\.vscode\.vscode\Produktionsprogramm\Produktionsprogramm_Verkürzer\output_Produktionsprogramm_zufällig' # Name der ursprünglichen Datei
dateiname_speichern = 'produktionsprogramm_verkürzt_zufällig.json' # Name der neuen Datei

# Lese das ursprüngliche Produktionsprogramm ein
produktionsprogramm = lade_produktionsprogramm(dateiname_einlesen)

# Benenne das Produktionsprogramm um
umbenanntes_programm = umbenennen_produktionsprogramm(produktionsprogramm)

# Speichere das umbenannte Produktionsprogramm
speichern_neues_produktionsprogramm(umbenanntes_programm, dateiname_speichern)
