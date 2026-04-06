#!/usr/bin/env python3
# rss_generator.py
# Erstellt einen RSS-Feed aus dem TUI Cruises Presse-Archiv

import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime

# --- Konfiguration ---
JSON_URL = "https://www.meinschiff.com/presse/archiv.json"
RSS_FILE = "rss.xml"
RSS_TITLE = "TUI Cruises Pressemitteilungen"
RSS_LINK = "https://www.meinschiff.com/presse/archiv"
RSS_DESC = "Aktuelle Pressemitteilungen von TUI Cruises"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# --- JSON abrufen ---
response = requests.get(JSON_URL, headers=headers)
if not response.headers.get("Content-Type", "").startswith("application/json"):
    print("Keine JSON-Antwort erhalten, überprüfe die URL oder Header!")
    print(response.text[:500])
    exit(1)

data = response.json()

# --- RSS-Feed erstellen ---
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = RSS_TITLE
ET.SubElement(channel, "link").text = RSS_LINK
ET.SubElement(channel, "description").text = RSS_DESC
ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

# --- Pressemitteilungen aus JSON auslesen ---
entries = data.get("content", {}).get("slots", {}).get("content", [])
for item in entries:
    if item.get("element") != "tui-presslist":
        continue
    for entry in item.get("properties", {}).get("entries", []):
        title = entry.get("filter", {}).get("search", "") or entry.get("properties", {}).get("headline", {}).get("text", "Pressemitteilung")
        link = entry.get("url") or RSS_LINK
        desc = entry.get("description", "Keine Beschreibung verfügbar.")
        pub_date = entry.get("filter", {}).get("year", [str(datetime.utcnow().year)])[0] + "-01-01"

        rss_item = ET.SubElement(channel, "item")
        ET.SubElement(rss_item, "title").text = title
        ET.SubElement(rss_item, "link").text = link
        ET.SubElement(rss_item, "description").text = desc
        ET.SubElement(rss_item, "pubDate").text = datetime.strptime(pub_date, "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S GMT")

# --- RSS-Datei speichern ---
tree = ET.ElementTree(rss)
tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)
print(f"RSS-Feed erfolgreich erstellt: {RSS_FILE}")
