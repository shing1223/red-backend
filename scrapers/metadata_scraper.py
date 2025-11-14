import requests
from bs4 import BeautifulSoup

def fetch_site_metadata(url: str):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        title = soup.title.string if soup.title else None
        description = soup.find("meta", attrs={"name": "description"})
        description = description.get("content") if description else None

        og_image = soup.find("meta", property="og:image")
        og_image = og_image.get("content") if og_image else None

        favicon = soup.find("link", rel="icon")
        favicon = favicon.get("href") if favicon else None

        return {
            "title": title,
            "description": description,
            "og_image": og_image,
            "favicon": favicon
        }
    except Exception:
        return {}