from fastapi import APIRouter, HTTPException
from api.models.site import WebsiteSubmit, WebsiteResult
from scrapers.metadata_scraper import fetch_site_metadata
from clients.supabase_client import supabase
from clients.meilisearch_client import meili_index, meili_client

router = APIRouter()

@router.post("/submit-site", response_model=WebsiteResult)
def submit_site(site: WebsiteSubmit):

    metadata = fetch_site_metadata(str(site.url))

    data = {
        "url": str(site.url),
        "title": site.title or metadata.get("title"),
        "description": site.description or metadata.get("description"),
        "language": site.language,
        "region": site.region,
        "category": site.category,
        "tags": site.tags or [],  # 🔥 NULL → []
        "favicon": metadata.get("favicon"),
        "og_image": metadata.get("og_image"),
    }

    # Insert Supabase
    try:
        res = supabase.table("websites").insert(data).execute()
    except Exception as e:
        print("SUPABASE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Supabase insert failed")

    row = res.data[0]
    website_id = row["id"]

    # Index to Meilisearch
    doc = {**row, "id": website_id}
    try:
        task = meili_index.add_documents([doc])
        meili_client.wait_for_task(task["taskUid"])
    except Exception:
        pass

    return WebsiteResult(**doc, score=1.0)