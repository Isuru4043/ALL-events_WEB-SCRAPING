from undetected_playwright import stealth_sync
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=True if you don't want a window
    context = browser.new_context()

    # --- your actual cookies ---
    cookies = [
        {
            "name": "cf_clearance",
            "value": "PRIhB8tzIlnE_5I9JkokvBkoqoUjrX47OI.3_U2Z_AM-1761030152-1.2.1.1-r8bQk3gn2MWqd7xKqBCDshdp5rH5UGaNfJTgkwji9afuFOljZ5S8P549kLZFyoz4iq5G.11dj3uAujNVv4PT_ZB4K.gDgIHt27eUydC0tvu9i0YQq_2Yb2EIU4ewOeswd2sBTj5Ad_l1Go5oeOq6V0bHRiwSNApnBdEnO4e5tp9hxy1jNsiOl4H25BV9W3Udj0ynMVy4A83NfMJTYZEDC0ZjNgLsItTYW3WXSPxezAE",
            "domain": ".allevents.in",
            "path": "/"
        },
        {
            "name": "_ga",
            "value": "GA1.1.1174964861.1760945302",
            "domain": ".allevents.in",
            "path": "/"
        }
    ]
    context.add_cookies(cookies)

    page = context.new_page()
    stealth_sync(page)
    print("Navigating to page...")
    page.goto("https://allevents.in/new-york", wait_until="networkidle", timeout=60000)

    html = page.content()
    browser.close()

# --- parsing part ---
soup = BeautifulSoup(html, "html.parser")

events = []
for tag in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(tag.string)
        if isinstance(data, list):
            for e in data:
                if e.get("@type") == "Event":
                    events.append(e)
        elif data.get("@type") == "Event":
            events.append(data)
    except Exception:
        continue

for e in events:
    print({
        "title": e.get("name"),
        "start_date": e.get("startDate"),
        "venue": e.get("location", {}).get("name"),
        "url": e.get("url"),
    })
