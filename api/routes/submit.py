from fastapi import APIRouter, HTTPException
from api.models.site import WebsiteSubmit, WebsiteResult
from scrapers.metadata_scraper import fetch_site_metadata
from clients.supabase_client import supabase_insert
from clients.meilisearch_client import get_meili_index, get_meili_client
from urllib.parse import urlparse

site_router = APIRouter()   # <-- 避免 router 名稱衝突

@site_router.post("/submit-site", response_model=WebsiteResult)
def submit_site(site: WebsiteSubmit):

    parsed = urlparse(str(site.url))
    host = parsed.netloc or None

    metadata = fetch_site_metadata(str(site.url))

    data = {
        "url": str(site.url),
        "host": host,
        "title": site.title or metadata.get("title"),
        "description": site.description or metadata.get("description"),
        "language": site.language,
        "region": site.region,
        "category": site.category,
        "tags": site.tags or [],
        "favicon": metadata.get("favicon"),
        "og_image": metadata.get("og_image"),
    }

    try:
        row = supabase_insert("websites", data)[0]
    except Exception as e:
        print("SUPABASE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Supabase insert failed")

    website_id = row["id"]

    doc = {**row, "id": website_id}

    try:
        index = get_meili_index()
        client = get_meili_client()
        task = index.add_documents([doc])
        client.wait_for_task(task["taskUid"])
    except Exception as e:
        print("MEILI ERROR:", e)

    return WebsiteResult(**doc, score=1.0)