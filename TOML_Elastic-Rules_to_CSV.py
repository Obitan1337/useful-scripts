import toml
import csv
import os

# ✅ Ausgabeformat: True = Spaltenbasiert, False = Zeilenbasiert
columns = True  # Setze auf True für spaltenbasiertes Format

# ✅ Steuerung, ob Subtechniques ausgegeben werden
include_subtechniques = True  # Setze auf False, um nur Techniques auszugeben

# Aktuelles Verzeichnis (Ordner mit den TOML-Dateien)
script_dir = os.path.dirname(os.path.abspath(__file__))
toml_folder = r"PFAD Change dis"  # Dateipfad
csv_file_path = os.path.join(script_dir, "outputsub.csv")  # Pfad für die CSV-Datei

# Alle .toml-Dateien im Ordner suchen
toml_files = [f for f in os.listdir(toml_folder) if f.endswith(".toml")]

# Extrahierte Daten speichern
entries = []

for toml_file in toml_files:
    toml_file_path = os.path.join(toml_folder, toml_file)

    try:
        # TOML-Datei einlesen
        with open(toml_file_path, "r", encoding="utf-8") as file:
            data = toml.load(file)
    except toml.TomlDecodeError as e:
        print(f"Fehler in Datei '{toml_file}': {e}")
        continue  # Fehlerhafte Datei überspringen

    # Hauptregelname aus [rule]
    rule_name = data.get("rule", {}).get("name", "")

    # Alle [[rule.threat]]-Einträge
    threats = data.get("rule", {}).get("threat", [])

    if not columns:
        # Zeilenbasiertes Format
        for threat in threats:
            for technique in threat.get("technique", []):
                technique_name = technique.get("name", "")
                subtechniques = technique.get("subtechnique", [])
                if include_subtechniques and subtechniques:
                    for subtechnique in subtechniques:
                        entries.append([toml_file, rule_name, technique_name, subtechnique.get("name", "")])
                else:
                    entries.append([toml_file, rule_name, technique_name, ""])
    else:
        # Spaltenbasiertes Format mit sortierter Struktur
        entry = [toml_file, rule_name]
        techniques_data = []

        for threat in threats:
            for technique in threat.get("technique", []):
                technique_name = technique.get("name", "")
                subtechniques = technique.get("subtechnique", [])

                # Füge Technique und zugehörige Subtechniques hinzu
                subtechnique_names = [sub.get("name", "") for sub in subtechniques] if include_subtechniques else []
                techniques_data.append((technique_name, subtechnique_names))

        # Eintrag nach gewünschter Sortierung (Technique 1, Subtechnique 1.1-1.n, Technique 2, ...)
        for technique_name, subtechnique_list in techniques_data:
            entry.append(technique_name)  # Technik hinzufügen
            if include_subtechniques:
                for subtechnique_name in subtechnique_list:
                    entry.append(subtechnique_name)

        entries.append(entry)

# In CSV-Datei speichern
with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    # Header je nach Format
    if not columns:
        writer.writerow(["Filename", "Rule Name", "Technique Name", "Subtechnique Name"])
    else:
        # Dynamische Header für spaltenbasiertes Format
        max_techniques = max((len(entry) - 2) for entry in entries)  # Maximal gefundene Techniken & Subtechniques
        headers = ["Filename", "Rule Name"]
        i = 1
        while len(headers) - 2 < max_techniques:
            headers.append(f"Technique {i}")
            if include_subtechniques:
                # Dynamisch Subtechniques für jede Technik
                subtech_count = max(len(entry) - 2 - (i * (1 + i - 1)) for entry in entries)  # Schätzung der Subtechs
                for j in range(1, subtech_count + 1):
                    headers.append(f"Subtechnique {i}.{j}")
            i += 1
        writer.writerow(headers)

    # Schreibe alle Daten
    writer.writerows(entries)

print(f"CSV-Datei wurde gespeichert: {csv_file_path}")
