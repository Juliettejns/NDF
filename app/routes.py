from flask import render_template
from app import app
from donnees import Article


@app.route("/")
def accueil():
    return render_template("pages/accueil.html")


@app.route("/corpus")
def corpus():
    notes = Article.query.all()
    return render_template("pages/corpus.html", notes=notes)


@app.route("/note")
def note():
    return render_template("pages/note.html")
