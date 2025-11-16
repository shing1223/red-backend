from fastapi import APIRouter
from clients.meilisearch_client import get_meili_index

router = APIRouter()

@router.get("/search")
def search(q: str = ""):
    index = get_meili_index()
    results = index.search(q, {
        "limit": 10,
        "attributesToRetrieve": ["id", "title", "url", "host", "snippet", "tags", "language"]
    })
    return results