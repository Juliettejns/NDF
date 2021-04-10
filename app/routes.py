"""
Définition des routes URL de l'application NDF
Author:Juliette Janes
Date: 03/03/2021

dans l'ordre:
/
/corpus
/corpus/<int:article_id>
/corpus/<int:article_id>/<pointeur>
/lieux
/personnes
/recherche
/about
/contexte
"""

# import des classes render_templates, request et groupby depuis les modules flask et itertools
from flask import render_template, request
from itertools import groupby
from flask_paginate import Pagination, get_page_parameter, get_page_args
from lxml import etree

# import des classes app et db depuis le module app
from .app import app,db
# import de toutes les classes du module donnees situé dans le dossier modeles
from .modeles.donnees import *
# import des classes document_xml et xslt_transformation depuis le module constantes
from .constantes import document_xml, xslt_transformation


def get_index(index, offset=0, per_page=10):
    """
    Fonction, qui prennant en entrée une liste, un décalage (offset) et un nombre d'items à garder, permet de récupérer
    un morceau de cette liste.
    :param index: liste d'éléments
    :type index: list
    :param offset: entier signalant la page sur laquelle se trouve l'utilisateur (décalage)
    :type offset: int
    :param per_page: entier signalant le nombre d'items devant se trouvant sur la page
    :return: partie de la liste de per_page items et commençant à l'item offset*per_page
    :rtype: list
    """
    return index[offset: offset + per_page]


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
    # création de la pagination
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    # récupération de la portion de la liste concernant la page à afficher
    pagination_notes = get_index(notes, offset=offset, per_page=per_page)
    # définition de la pagination
    pagination = Pagination(page=page, per_page=per_page, total=len(notes))
    return render_template("pages/corpus.html", notes=notes, page=page, per_page=per_page, pagination=pagination)


@app.route("/corpus/<article_id>/<pointeur>")
@app.route("/corpus/<int:article_id>")
def note(article_id, pointeur=''):
    """
    Route permettant l'affichage d'un article demandé.
    :param article_id: identifiant unique représentant un article en particulier
    :type article_id: int
    :param pointeur: chaine de caractères représentant un personnage ou lieu précis
    :type pointeur: str
    :return: template note.html
    :rtype: template
    """
    # récupération de l'article ayant pour identifiant l'entier article_id
    unique_note=Article.query.get(article_id)
    # application de la feuille de transformation xslt_transformation au document xml uniquement pour l'article choisi
    if pointeur =='':
        affichage_texte = xslt_transformation(document_xml, num=str(article_id))
    else:
        affichage_texte = xslt_transformation(document_xml, num=etree.XSLT.strparam(article_id),
                                              pointeur=etree.XSLT.strparam(pointeur))
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
    # transformation du dictionnaire en liste de dictionnaire
    index_lieu_article = [{k: v} for (k, v) in index_lieu_article.items()]
    # création de la pagination
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    # récupération de la portion de la liste concernant la page à afficher
    pagination_index = get_index(index_lieu_article, offset=offset, per_page=per_page)
    # définition de la pagination
    pagination = Pagination(page=page, per_page=per_page, total=len(index_lieu_article))
    return render_template("pages/index_lieu.html", list=index_lieu_article, page=page, per_page=per_page,
                           pagination=pagination)


@app.route("/personnes", methods=['POST', 'GET'])
def personnes():
    """
    Route permettant l'affichage d'un index de personnes présentant toutes les personnes mentionnées, leurs occurences
    et un lien vers chacun de ces articles.
    :return: template index_personne.html
    :rtype: template
    """
    # récupération de la table d'association articleHasPersonne:
    # Dans un premier temps, on essaie de récupérer rôle social et rôle dreyfus, les éléments qui permettent de filtrer
    # les personnes.
    role_social = request.args.get('role_social')
    role_dreyfus = request.args.get('role_dreyfus')
    if role_dreyfus and role_social:
        # si l'utilisateur a demandé de filtrer les deux termes, on réalise une query dans la base de données qui filtre
        # tout les roles dreyfus et role social correspondants
        association_Article_Personne = db.session.query(
            articleHasPersonne, Article, Personne).join(Article).join(Personne).filter_by(
            personne_dreyf=role_dreyfus, personne_role=role_social).all()
        # sinon, on fait cela soit pour role_social soit pour role_dreyfus
    elif role_dreyfus:
        association_Article_Personne = db.session.query(
            articleHasPersonne, Article, Personne).join(Article).join(Personne).filter_by(
            personne_dreyf=role_dreyfus).all()
    elif role_social:
        association_Article_Personne = db.session.query(
            articleHasPersonne, Article, Personne).join(Article).join(Personne).filter_by(
            personne_role=role_social).all()
    else:
        # si role_dreyfus et role_social sont tout les deux vides, alors on récupère toutes les personnes de la base
        association_Article_Personne = db.session.query(articleHasPersonne, Article, Personne).join(Article).join(
            Personne).all()

    # comme pour la fonction lieux, on obtient une liste de tuple que l'on restructure sous la forme d'une liste ayant
    # pour clé une personne et pour valeurs les articles correspondants
    index_personne_article ={key: [v[2] for v in val] for key, val in
                              groupby(sorted(association_Article_Personne, key=lambda ele: ele[1]),
         key=lambda ele: ele[3])}
    # transformation du dictionnaire obtenu en liste de petits dictionnaires pour pouvoir le découper (assez long et
    # lourd, à corriger)
    index_personne_article = [{k: v} for (k, v) in index_personne_article.items()]
    # création de la pagination
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    # récupération de la portion de la liste concernant la page à afficher
    pagination_index= get_index(index_personne_article, offset=offset, per_page=per_page)
    # définition de la pagination
    pagination = Pagination(page=page, per_page=per_page, total=len(index_personne_article),
                            css_framework='bootstrap4')

    # on récupère toutes les valeurs pouvant être prises par role_social et role_dreyfus afin de les afficher
    # dans deux listes déroulantes dans le but de permettre à l'utilisateur de filtrer les personnes.
    role_liste= ['']
    for role in db.session.query(Personne.personne_role).distinct():
        role_liste.append(role.personne_role)
    role_dreyf_liste = ['']
    for dreyf in db.session.query(Personne.personne_dreyf).distinct():
        role_dreyf_liste.append(dreyf.personne_dreyf)

    return render_template("pages/index_pers.html", list=pagination_index, page=page, per_page=per_page,
                           pagination=pagination, roles=role_liste, role_dreyf=role_dreyf_liste,
                           role_social=role_social, role_dreyfus=role_dreyfus)


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

    #création de la pagination
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination_resultats = get_index(resultats, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=len(resultats))
    return render_template("pages/recherche.html", resultats=pagination_resultats, page=page, per_page=per_page,
                           pagination=pagination)

# routes pour les pages annexes décrivant le projet
@app.route("/about")
def about():
    return render_template("pages/a_propos.html")


@app.route("/contexte")
def contexte():
    return render_template("pages/contexte.html")

# routes pour les pages d'erreurs
# errorhandler permet de retourner une page erreur lorsque le code de la réponse http renvoyé est 404 ou 500.

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/error404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/error500.html"), 500
