from typing import Any, Dict, List, Optional
import requests
from urllib.parse import urlencode
from core import settings

BASE = settings.API_BASE_URL.rstrip("/")


def list_books(q: Optional[str] = None, limit: int = 50, offset: int = 0,
               min_rating: Optional[float] = None, sort: str = "title") -> List[Dict[str, Any]]:
    """
    Calls: GET /library/books/?q=&limit=&offset=&min_rating=&sort=
    Returns a list of book dicts. Keeps it simple: no pagination UI here.
    """
    params = {"limit": limit, "offset": offset, "sort": sort}
    if q: params["q"] = q
    if min_rating is not None: params["min_rating"] = min_rating

    url = f"{BASE}/library/books/"
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    # Handle either a pure list or an object with "items" key
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "items" in data:
        return data["items"]
    return data  # best effort


def get_book(book_id: str) -> Dict[str, Any]:
    """GET /library/books/{book_id}"""
    url = f"{BASE}/library/books/{book_id}"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json()


def get_recommendations(book_id: str) -> List[Dict[str, Any]]:
    """GET /library/recommendation/{book_id} -> list of rec_book dicts"""
    url = f"{BASE}/library/recommendation/{book_id}"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    raw = resp.json()
    items = raw if isinstance(raw, list) else raw.get("items", [])

    # Flatten: pull rec_book up and keep rank/score/reason
    flattened = []
    for x in items:
        rb = (x or {}).get("rec_book") or {}
        if isinstance(rb, dict):
            rb = {
                **rb,
                "rank": x.get("rank"),
                "score": x.get("score"),
                "reason": x.get("reason"),
                "base_book_id": x.get("base_book_id"),
            }
            flattened.append(rb)
    return flattened
