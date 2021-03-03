from flask import render_template
from app import app
from modeles.donnees import Article


@app.route("/")
def accueil():
    return render_template("pages/accueil.html")


@app.route("/corpus")
def corpus():
    notes = Article.query.all()
    return render_template("pages/corpus.html", notes=notes)


@app.route("/note/<int:article_id>")
def note(article_id):
    unique_note=Article.query.get(article_id)
    return render_template("pages/note.html", note=unique_note)
