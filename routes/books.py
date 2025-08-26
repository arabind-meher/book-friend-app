from flask import Blueprint, render_template, abort
from services import api_client, book_adapter

books_bp = Blueprint("books", __name__)


@books_bp.get("/")
def list_books():
    raw = api_client.get_books() or {}
    books = []

    if isinstance(raw, dict):
        items = raw.get("items") or raw.get("books") or raw.get("data") or raw.get("results") or raw.get("list")
        if isinstance(items, list):
            books = book_adapter.normalize_books(items)
    elif isinstance(raw, list):
        books = book_adapter.normalize_books(raw)

    return render_template("books.html", title="Books", books=books or [])


@books_bp.get("/<book_id>/")
def book_detail(book_id: str):
    raw = api_client.get_book(book_id)
    if not raw:
        abort(404)
    book = book_adapter.normalize_book(raw)

    # Optional: pull recommendations; ignore failures
    rec_raw = api_client.get_recommendations(book_id) or {}
    rec_items = None
    if isinstance(rec_raw, dict):
        rec_items = rec_raw.get("items") or rec_raw.get("recommendations") or rec_raw.get("results")
    elif isinstance(rec_raw, list):
        rec_items = rec_raw

    recommendations = book_adapter.normalize_books(rec_items) if rec_items else []
    return render_template("book_detail.html", title=book.get("title") or "Book", book=book,
                           recommendations=recommendations)
