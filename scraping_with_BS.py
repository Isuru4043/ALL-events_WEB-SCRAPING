import requests
from bs4 import BeautifulSoup
import json

url = "https://allevents.in/new-york"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print(response.text[:1000])

soup = BeautifulSoup(response.text, "html.parser")

events = []

# find all JSON-LD scripts
for tag in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(tag.string)
        if isinstance(data, list):  # multiple events
            for e in data:
                if e.get("@type") == "Event":
                    events.append(e)
        elif data.get("@type") == "Event":
            events.append(data)
    except Exception:
        continue

# print or store event details
for e in events:
    print({
        "title": e.get("name"),
        "start_date": e.get("startDate"),
        "venue": e.get("location", {}).get("name"),
        "address": e.get("location", {}).get("address", {}).get("streetAddress"),
        "url": e.get("url"),
    })
