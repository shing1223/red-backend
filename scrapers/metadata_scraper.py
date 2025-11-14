import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_site_metadata(url: str):
    try:
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (compatible; MetadataBot/1.0)"}
        )

        soup = BeautifulSoup(r.text, "lxml")

        # title
        title = soup.title.string.strip() if soup.title else None

        # meta description
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else None

        # og:image
        og_tag = soup.find("meta", property="og:image")
        og_image = og_tag["content"] if og_tag and og_tag.get("content") else None
        if og_image:
            og_image = urljoin(url, og_image)

        # favicon — handle multiple rel types
        favicon = None
        favicon_candidates = [
            {"rel": "icon"},
            {"rel": "shortcut icon"},
            {"rel": "apple-touch-icon"},
        ]

        for attrs in favicon_candidates:
            icon_tag = soup.find("link", rel=attrs["rel"])
            if icon_tag and icon_tag.get("href"):
                favicon = icon_tag["href"]
                break

        # fallback: search any <link rel contains icon>
        if not favicon:
            for tag in soup.find_all("link"):
                rel = tag.get("rel")
                if rel and any("icon" in r for r in rel):
                    if tag.get("href"):
                        favicon = tag["href"]
                        break

        if favicon:
            favicon = urljoin(url, favicon)

        return {
            "title": title,
            "description": description,
            "og_image": og_image,
            "favicon": favicon,
        }

    except Exception:
        return {}