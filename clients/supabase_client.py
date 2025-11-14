import httpx
from core.config import get_settings

settings = get_settings()

def supabase_insert(table: str, data: dict):
    url = f"{settings.SUPABASE_URL}/rest/v1/{table}"

    key = settings.SUPABASE_SERVICE_ROLE_KEY

    headers = {
        "apikey": key,
        "ApiKey": key,          # 👈 新 gateway 在某些 region 必要
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    r = httpx.post(url, headers=headers, json=data, timeout=10)
    r.raise_for_status()
    return r.json()