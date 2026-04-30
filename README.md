# Book Friend

A Flask web application for browsing, searching, and discovering book recommendations. It acts as a frontend layer over a backend REST API, providing a clean dark-mode UI for exploring a book library.

## Features

- Browse and search a book library by title or author
- Filter books by minimum rating
- View detailed book information (description, genres, ratings, cover art)
- Get similar book recommendations on each book detail page

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Flask 3.1+ |
| Language | Python 3.12+ |
| Templating | Jinja2 |
| Styling | Tailwind CSS 3.4 (CDN) |
| HTTP Client | requests |
| Config | python-dotenv |
| Package Manager | [uv](https://github.com/astral-sh/uv) |

## Prerequisites

- Python 3.12+
- `uv` package manager (`pip install uv`)
- A running backend API server (see [Backend API](#backend-api))

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd book-friend-app

# Install dependencies
uv sync

# Copy and configure environment variables
cp .env.example .env   # or create .env manually
```

Create a `.env` file in the project root:

```env
API_BASE_URL=http://127.0.0.1:8000
FLASK_DEBUG=1
```

## Running the App

```bash
uv run python app.py
```

The app starts on [http://127.0.0.1:5000](http://127.0.0.1:5000) by default.

## Backend API

This app is a frontend-only layer — all book data comes from an external API. The backend must be running and accessible at `API_BASE_URL` before starting this app.

Expected endpoints:

| Method | Path | Description |
|---|---|---|
| `GET` | `/library/books/` | List books. Supports `q`, `min_rating`, `sort`, `limit`, `offset` query params |
| `GET` | `/library/books/{id}` | Get a single book by ID |
| `GET` | `/library/recommendation/{id}` | Get recommendations for a book |

## Project Structure

```
book-friend-app/
├── app.py                  # Flask app and route definitions
├── core/
│   └── config.py           # Settings loaded from environment
├── services/
│   ├── api_client.py       # HTTP calls to the backend API
│   └── books_adapter.py    # Normalizes varied API response formats
├── templates/
│   ├── base.html           # Base layout (dark-mode Tailwind)
│   ├── home.html           # Landing page
│   ├── books.html          # Book listing with search/filter
│   └── book_detail.html    # Book detail + recommendations sidebar
└── static/
    └── js/
        └── app.js          # Form submission handler
```

## Routes

| Path | Description |
|---|---|
| `/` | Home / landing page |
| `/books/` | Book listing; supports `?q=`, `?min_rating=`, `?sort=` |
| `/books/<book_id>` | Book detail page with recommendations |
