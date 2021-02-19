from flask import Flask, render_template, url_for
from app import app


@app.route("/")
def accueil():
    return render_template("accueil.html")


@app.route("/corpus")
def corpus():
    return render_template("corpus.html")


@app.route("/note")
def note():
    return render_template("note.html")
