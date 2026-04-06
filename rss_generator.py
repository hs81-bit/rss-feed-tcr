import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

JSON_URL = "https://www.meinschiff.com/presse/archiv/archiv.json"
BASE_URL = "https://www.meinschiff.com"

response = requests.get(JSON_URL, headers={"User-Agent": "Mozilla/5.0"})
response.raise_for_status()

data = response.json()

entries = data["content"]["slots"]["content"][1]["properties"]["entries"]

fg = FeedGenerator()
fg.title("Mein Schiff Pressemitteilungen")
fg.link(href=BASE_URL + "/presse/archiv")
fg.description("Automatischer RSS Feed für Mein Schiff Pressemitteilungen")

for item in entries[:30]:
    fe = fg.add_entry()

    clean_text = BeautifulSoup(
        item["description"],
        "html.parser"
    ).get_text(" ", strip=True)

    title = clean_text[:120]
    link = BASE_URL + item["link"]["href"]

    fe.title(title)
    fe.link(href=link)
    fe.description(clean_text)
    fe.guid(link)

fg.rss_file("docs/rss.xml")
print("RSS erfolgreich erstellt")
