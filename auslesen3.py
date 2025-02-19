import toml
import csv
import os

# Aktuelles Verzeichnis (Ordner mit den TOML-Dateien)
script_dir = os.path.dirname(os.path.abspath(__file__))
toml_folder = r"Filepath hier einfuegen"  # Dateipfad
csv_file_path = os.path.join(script_dir, "Regeln.csv")  # Pfad für die CSV-Datei


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

    for threat in threats:
        for technique in threat.get("technique", []):  # Falls keine Techniken existieren, bleibt die Liste leer
            technique_name = technique.get("name", "")

            # Falls Subtechniken existieren, iterieren, sonst leeren Eintrag setzen
            subtechniques = technique.get("subtechnique", [])
            if subtechniques:
                for subtechnique in subtechniques:
                    entries.append([toml_file, rule_name, technique_name, subtechnique.get("name", "")])
            else:
                entries.append([toml_file, rule_name, technique_name, ""])

# In CSV-Datei speichern
with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Rule Name", "Technique Name", "Subtechnique Name"])  # Header
    writer.writerows(entries)

print(f"CSV-Datei wurde gespeichert: {csv_file_path}")

