import requests
import json
import re
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

URL = "https://www.meinschiff.com/presse/archiv"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html = response.text

# JSON Block per Regex extrahieren
match = re.search(r'(\{"version".*?\})\s*</script>', html, re.DOTALL)

if not match:
    raise Exception("JSON Block nicht gefunden")

json_text = match.group(1)
data = json.loads(json_text)

entries = data["content"]["slots"]["content"][1]["properties"]["entries"]

fg = FeedGenerator()
fg.title("Mein Schiff Pressemitteilungen")
fg.link(href=URL)
fg.description("Automatischer RSS Feed")

for item in entries[:30]:
    fe = fg.add_entry()

    clean_text = BeautifulSoup(
        item["description"],
        "html.parser"
    ).get_text(" ", strip=True)

    title = clean_text[:120]
    link = "https://www.meinschiff.com" + item["link"]["href"]

    fe.title(title)
    fe.link(href=link)
    fe.description(clean_text)
    fe.guid(link)

fg.rss_file("docs/rss.xml")
print("RSS erfolgreich erstellt")
