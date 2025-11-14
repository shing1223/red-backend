from core.config import get_settings
from meilisearch import Client

settings = get_settings()

meili_client = Client(
    settings.MEILISEARCH_URL,
    settings.MEILISEARCH_MASTER_KEY,
)

index_name = "websites"

# Create index if it does not exist
try:
    meili_client.get_index(index_name)
except Exception:
    meili_client.create_index(index_name, {"primaryKey": "id"})

meili_index = meili_client.index(index_name)