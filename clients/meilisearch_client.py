from functools import lru_cache
from core.config import get_settings
from meilisearch import Client

@lru_cache()
def get_meili_client():
    settings = get_settings()
    return Client(settings.MEILISEARCH_URL, settings.MEILISEARCH_MASTER_KEY)

@lru_cache()
def get_meili_index():
    client = get_meili_client()
    index_name = "websites"
    try:
        client.get_index(index_name)
    except Exception:
        client.create_index(index_name, {"primaryKey": "id"})
    return client.index(index_name)