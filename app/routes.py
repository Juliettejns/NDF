"""
Définition des routes URL de l'application NDF
Author:Juliette Janes
Date: 03/03/2021

dans l'ordre:
/
/corpus
/corpus/<int:article_id>
/lieux
/personnes
/recherche
"""

# import des classes render_templates, request et groupby depuis les modules flask et itertools
from flask import render_template, request
from itertools import groupby

# import des classes app et db depuis le module app
from .app import app,db
# import de toutes les classes du module donnees situé dans le dossier modeles
from .modeles.donnees import *
# import des classes document_xml et xslt_transformation depuis le module constantes
from .constantes import document_xml, xslt_transformation


@app.route("/")
def accueil():
    """
    Route permettant l'affichage de la page d'accueil de l'application NDF.
    :return: template accueil.html
    :rtype: template
    """
    return render_template("pages/accueil.html")


@app.route("/corpus")
def corpus():
    """
    Route permettant l'affichage de tous les articles disponibles et encodés.
    :return: template corpus.html
    :rtype: template
    """
    # récupération de tout les éléments de la table article triés chronologiquement par leur numéro de parution
    notes = Article.query.order_by(Article.article_numJournal.asc()).all()
    return render_template("pages/corpus.html", notes=notes)


@app.route("/corpus/<int:article_id>")
def note(article_id):
    """
    Route permettant l'affichage d'un article demandé.
    :param article_id: identifiant unique représentant un article en particulier
    :type article_id: int
    :return: template note.html
    :rtype: template
    """
    # récupération de l'article ayant pour identifiant l'entier article_id
    unique_note=Article.query.get(article_id)
    # application de la feuille de transformation xslt_transformation au document xml uniquement pour l'article choisi
    affichage_texte = xslt_transformation(document_xml, num=str(article_id))
    return render_template("pages/note.html", note=unique_note, texte=str(affichage_texte))


@app.route("/lieux")
def lieux():
    """
    Route permettant l'affichage d'un index de lieux présentant tous les lieux mentionnés,, leurs occurences et un lien
    vers chacun de ces articles.
    :return: template index_lieu.html
    :rtype: template
    """
    # récupération de la table d'association articleHasLieu ainsi que les articles et lieux qui lui sont associé
    association_Article_Lieu = db.session.query(articleHasLieu, Article, Lieu).join(Article).join(Lieu).all()
    # on obtient une liste de tuple que l'on va restructurer pour former un dictionnaire ayant pour clé un lieu et
    # pour valeurs tous les articles correspondants
    index_lieu_article = {key: [v[2] for v in val] for key, val in
             groupby(sorted(association_Article_Lieu, key=lambda ele: ele[1]), key=lambda ele: ele[3])}
    return render_template("pages/index_lieu.html", index=index_lieu_article)


@app.route("/personnes")
def personnes():
    """
    Route permettant l'affichage d'un index de personnes présentant toutes les personnes mentionnées, leurs occurences
    et un lien vers chacun de ces articles.
    :return: template index_personne.html
    :rtype: template
    """
    # récupération de la table d'association articleHasPersonne ainsi que les articles et personnes qui lui sont associé
    association_Article_Personne = db.session.query(articleHasPersonne, Article, Personne).join(Article).join(
        Personne).all()
    # comme pour la fonction lieux, on obtient une liste de tuple que l'on restructure sous la forme d'une liste ayant
    # pour clé une personne et pour valeurs les articles correspondants
    index_personne_article = {key: [v[2] for v in val] for key, val in
                              groupby(sorted(association_Article_Personne, key=lambda ele: ele[1]),
                                      key=lambda ele: ele[3])}
    return render_template("pages/index_pers.html", index=index_personne_article)


@app.route("/recherche")
def recherche():
    """
    Route permettant d'afficher les articles correspondants au mot rentré par l'utilisateur
    :return: template recherche.html
    :rtype: template
    """
    # récupération du mot clef rentré par l'utilisateur avec la méthode get afin d'éviter un if trop long
    motclef = request.args.get("keyword", None)
    # initialisation du resultat en une liste vide (afin d'avoir une liste vide comme résultat par défaut)
    resultats= []
    # vérification de l'existence d'un mot clef
    if motclef:
        # récupération sous la forme d'une liste de tout les articles pour lesquels le mot clef est contenu dans
        # l'attribut texte, trié par date de parution
        resultats= Article.query.filter(Article.article_texte.like("%{}%".format(motclef))).order_by(
            Article.article_numJournal.asc()).all()
    return render_template("pages/recherche.html", resultats=resultats)
