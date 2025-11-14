import httpx
from core.config import get_settings

settings = get_settings()

def supabase_insert(table: str, data: dict):
    url = f"{settings.SUPABASE_URL}/rest/v1/{table}"

    headers = {
        "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    r = httpx.post(url, headers=headers, json=data, timeout=10)
    r.raise_for_status()
    return r.json()