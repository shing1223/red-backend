from fastapi import APIRouter, Query
from clients.meilisearch_client import get_meili_index

router = APIRouter()

@router.get("/search")
def search_websites(q: str = Query(..., min_length=1)):
    index = get_meili_index()

    result = index.search(q, {
        "limit": 10,
        "attributesToCrop": ["description"],
        "attributesToHighlight": ["title", "description"],
    })

    return {
        "hits": result["hits"],
        "total": result["estimatedTotalHits"],
    }