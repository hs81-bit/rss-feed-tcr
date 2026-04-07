import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# -----------------------------
# Einstellungen
# -----------------------------
output_dir = "out"  # relativer Pfad, Ordner im Repo
os.makedirs(output_dir, exist_ok=True)
output_file = Path(output_dir) / "archiv.json"

# URL für die AIDA Presse-News (kann angepasst werden)
url = "https://www.aida.de/content/aida-component-library/requests/pressnewssearch.json/content/aida/deutschland/de/unternehmen/presse/archiv"

# -----------------------------
# Playwright starten und Seite abrufen
# -----------------------------
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # headless für GitHub Actions
    page = browser.new_page()
    # Header setzen, bevor du die Seite aufrufst
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "de-DE,de;q=0.9",
        # Falls nötig weitere Header, z. B. Cookies
    })
    try:
        print(f"Starte Zugriff auf: {url}")
        page.goto(url, timeout=60000)  # Timeout auf 60s
        page.wait_for_load_state("networkidle")
        
        # Content als JSON parsen
        content = page.content()
        
        # Wenn die Seite JSON liefert, versuche direkt zu laden
        try:
            # Manche Seiten liefern JSON direkt im Body
            data = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: JSON aus <pre> oder <script> extrahieren
            # Hier ein einfaches Beispiel, falls die Seite HTML liefert
            print("Fehler beim JSON parsen, speichere Roh-HTML")
            data = {"html_content": content}
        
        # Datei speichern
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Daten gespeichert in {output_file}")
    
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    finally:
        browser.close()
