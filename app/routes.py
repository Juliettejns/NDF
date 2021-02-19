from flask import render_template
from app import app
from constantes import titres


@app.route("/")
def accueil():
    return render_template("pages/accueil.html")


@app.route("/corpus")
def corpus():
    return render_template("pages/corpus.html", titres=titres)


@app.route("/note")
def note():
    return render_template("note.html")
