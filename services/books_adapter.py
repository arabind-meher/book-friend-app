from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse
from core import settings


def _first(*vals):
    for v in vals:
        if v is not None and v != "":
            return v
    return None


def _ensure_list(v: Union[str, List[str], None]) -> List[str]:
    if not v:
        return []
    if isinstance(v, list):
        return [str(x) for x in v if x not in (None, "")]
    return [str(v)]


def _ensure_absolute_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    if url.startswith("http://") or url.startswith("https://"):
        return url
    # Build origin from API_BASE
    base = config.API_BASE
    p = urlparse(base)
    origin = f"{p.scheme}://{p.netloc}"
    if url.startswith("/"):
        return origin + url
    return urljoin(origin + "/", url)


class BookAdapter:
    """Adapter to normalize raw book/recommendation data into a consistent format."""

    @staticmethod
    def normalize_book(raw: Dict[str, Any]) -> Dict[str, Any]:
        if not raw or not isinstance(raw, dict):
            return {
                "id": None,
                "title": "Untitled",
                "author": "Unknown",
                "year": None,
                "genres": [],
                "media_type": None,
                "description": None,
                "cover_url": None,
                "average_rating": None,
                "ratings_count": None,
            }

        # ---------- Author(s) ----------
        authors = _first(raw.get("author"), raw.get("authors"), raw.get("creator"))
        if isinstance(authors, list):
            author_str = ", ".join([str(a) for a in authors if a])
        else:
            author_str = str(authors) if authors else "Unknown"

        # ---------- Year ----------
        year = _first(raw.get("year"), raw.get("published_year"), raw.get("publication_year"))
        if not year:
            date_str = _first(
                raw.get("publishedDate"),
                raw.get("release_date"),
                raw.get("date"),
                raw.get("start_date"),
            )
            if isinstance(date_str, str) and len(date_str) >= 4:
                try:
                    year = int(date_str[:4])
                except Exception:
                    year = None

        # ---------- Image / Cover ----------
        image_links = raw.get("imageLinks") or {}
        cover_url = _first(
            raw.get("cover_url"),
            raw.get("image_url"),
            raw.get("cover_image"),
            raw.get("image"),
            raw.get("cover"),
            raw.get("thumbnail"),
            raw.get("poster"),
            raw.get("poster_url"),
            image_links.get("thumbnail"),
            image_links.get("smallThumbnail"),
        )
        cover_url = _ensure_absolute_url(cover_url)

        # ---------- Genres / Tags ----------
        genres = _first(raw.get("genres"), raw.get("tags"), raw.get("categories"))
        genres_list = _ensure_list(genres)

        # ---------- Media type ----------
        media_type = _first(
            raw.get("media_type"),
            raw.get("media"),
            raw.get("format"),
            raw.get("type"),
        )
        media_type = str(media_type).lower() if media_type else None

        # ---------- Ratings (if available) ----------
        avg_rating = _first(
            raw.get("average_rating"),
            raw.get("avg_rating"),
            raw.get("rating"),
        )
        try:
            average_rating = float(avg_rating) if avg_rating is not None else None
        except Exception:
            average_rating = None

        ratings_count = _first(
            raw.get("ratings_count"),
            raw.get("num_ratings"),
            raw.get("ratings"),
            raw.get("members"),
        )
        try:
            ratings_count = int(ratings_count) if ratings_count is not None else None
        except Exception:
            ratings_count = None

        # ---------- ID ----------
        book_id = _first(
            raw.get("id"),
            raw.get("_id"),
            raw.get("isbn"),
            raw.get("slug"),
            str(raw.get("title")) if raw.get("title") else None,
        )

        return {
            "id": book_id,
            "title": _first(raw.get("title"), raw.get("name"), "Untitled"),
            "author": author_str,
            "year": year,
            "genres": genres_list,
            "media_type": media_type,
            "description": _first(raw.get("description"), raw.get("summary")),
            "cover_url": cover_url,
            "average_rating": average_rating,
            "ratings_count": ratings_count,
        }

    @classmethod
    def normalize_books(cls, raw_list: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        if not raw_list:
            return []
        return [cls.normalize_book(item) for item in raw_list if item]


# App-wide singleton
book_adapter = BookAdapter()
