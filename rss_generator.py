import requests
import json
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

URL = "https://www.meinschiff.com/presse/archiv"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
html = response.text

start = html.find('{"version"')
end = html.rfind("</script>")

json_text = html[start:end]
data = json.loads(json_text)

entries = data["content"]["slots"]["content"][1]["properties"]["entries"]

fg = FeedGenerator()
fg.title("Mein Schiff Pressemitteilungen")
fg.link(href=URL)
fg.description("Automatischer RSS Feed für Pressemitteilungen")

for item in entries[:30]:
    fe = fg.add_entry()

    clean_text = BeautifulSoup(
        item["description"],
        "html.parser"
    ).get_text()

    title = clean_text[:120]
    link = "https://www.meinschiff.com" + item["link"]["href"]

    fe.title(title)
    fe.link(href=link)
    fe.description(clean_text)
    fe.guid(link)

fg.rss_file("docs/rss.xml")
print("rss.xml erstellt")
