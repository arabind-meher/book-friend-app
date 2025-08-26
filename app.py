from flask import Flask, render_template, request, redirect, url_for, abort
from services import list_books, get_book, get_recommendations

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("home.html")


@app.get("/books/")
def books():
    q = request.args.get("q", "").strip() or None
    min_rating = request.args.get("min_rating")
    try:
        min_rating_val = float(min_rating) if min_rating not in (None, "",) else None
    except ValueError:
        min_rating_val = None

    items = list_books(q=q, limit=50, offset=0, min_rating=min_rating_val, sort="title")
    return render_template("books.html", books=items, q=q or "", min_rating=min_rating or "")


@app.get("/books/<book_id>")
def book_detail(book_id: str):
    try:
        book = get_book(book_id)
    except Exception:
        abort(404)
    try:
        recs = get_recommendations(book_id)
    except Exception:
        recs = []
    return render_template("book_detail.html", book=book, recs=recs)


if __name__ == "__main__":
    app.run(debug=True)
