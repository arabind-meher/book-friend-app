from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.get("/")
def home():
    # Minimal: render home page. You can fetch backend welcome if you like.
    return render_template("home.html", title="Home")
