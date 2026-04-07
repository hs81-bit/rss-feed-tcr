import os
import requests
import json

# Zielordner
output_dir = "/config/playwright_env/AIDA/out"
output_file = os.path.join(output_dir, "archiv.json")

# AIDA Presse-Archiv JSON Endpoint
url = (
    "https://aida.de/content/aida-component-library/requests/"
    "pressnewssearch.json/content/aida/deutschland/de/"
    "unternehmen/presse/archiv/_jcr_content/root/container/"
    "container/pressarchivesearchba?size=15&p=1"
)

# Verzeichnis sicherstellen
os.makedirs(output_dir, exist_ok=True)
print(f"✅ Verzeichnis existiert: {os.path.abspath(output_dir)}")

# Minimal notwendige Header
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://aida.de/unternehmen/presse/archiv?p=1",
}

# Request senden
response = requests.get(url, headers=headers, timeout=30)
print(f"✅ HTTP-Status: {response.status_code}")

# JSON prüfen
try:
    data = response.json()
    print("✅ JSON erfolgreich geparst")
except Exception as e:
    print("❌ JSON konnte nicht geparst werden:", e)
    print("Antwortanfang:")
    print(response.text[:1000])
    exit(1)

# Datei speichern
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Datei gespeichert unter: {os.path.abspath(output_file)}")
