import pandas as pd

# Input- und Output-Dateien, hardcoded
input_file = 'Protokollierungsprofil_Linux_WIP(1).xlsx'
output_file = 'audit_rules_output_clean_fixed.txt'

# Excel-Datei laden
df = pd.read_excel(input_file)

written_rules = set() # ein python set erlaubt keine duplikate
output_lines = []

for index, row in df.iterrows():
    use_case = str(row.get('Use Case/Technique 1', '')).strip()
    audit_rules = str(row.get('Audit Rule', '')).strip()

    if pd.isna(audit_rules) or audit_rules == '' or audit_rules.lower() == 'nan':
        continue

    output_lines.append(f"# {use_case}")
#mehrzeilen regeln aufbrechen
    for rule_line in audit_rules.splitlines():
        rule_line = rule_line.strip()
        if rule_line == '':
            continue

        # Entferne auditctl oder sudo auditctl, falls da noch anderer text kommt bitte neue elif einfügen
        if rule_line.startswith('sudo auditctl'):
            rule_line = rule_line.replace('sudo auditctl', '', 1).strip()
        elif rule_line.startswith('auditctl'):
            rule_line = rule_line.replace('auditctl', '', 1).strip()

        if rule_line.startswith('#'):
            output_lines.append(rule_line)  # Kommentar direkt übernehmen
        else:
            if rule_line not in written_rules:
                output_lines.append(rule_line)
                written_rules.add(rule_line)

# Ausgabe in Datei schreiben
with open(output_file, 'w', encoding='utf-8') as f_out:
    for line in output_lines:
        f_out.write(f"{line}\n")

print(f"Fertig! Ausgabe gespeichert in: {output_file}")
