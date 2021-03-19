from flask import render_template, request
from app import app,db
from modeles.donnees import *
from constantes import document_xml, xslt_transformation
from itertools import groupby



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
    affichage_texte = xslt_transformation(document_xml, num=str(article_id))
    return render_template("pages/note.html", note=unique_note, texte=str(affichage_texte))


@app.route("/lieux")
def lieux():
    association_Article_Lieu = db.session.query(articleHasLieu, Article, Lieu).join(Article).join(Lieu).all()
    index_lieu_article = {key: [v[2] for v in val] for key, val in
             groupby(sorted(association_Article_Lieu, key=lambda ele: ele[1]), key=lambda ele: ele[3])}
    return render_template("pages/index_lieu.html", index=index_lieu_article)


@app.route("/personnes")
def personnes():
    association_Article_Personne = db.session.query(articleHasPersonne, Article, Personne).join(Article).join(
        Personne).all()
    index_personne_article = {key: [v[2] for v in val] for key, val in
                              groupby(sorted(association_Article_Personne, key=lambda ele: ele[1]),
                                      key=lambda ele: ele[3])}
    return render_template("pages/index_pers.html", index=index_personne_article)

@app.route("/recherche")
def recherche():
    motclef = request.args.get("keyword", None)
    resultats=[]
    if motclef:
        resultats= Article.query.filter(Article.article_texte.like("%{}%".format(motclef))).all()
    return render_template("pages/recherche.html", resultats=resultats)
