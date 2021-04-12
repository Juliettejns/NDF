"""
Instanciation du modèle de base de données
Author:Juliette Janes
Date: 03/03/2021
"""
# import de la classe db issue du module app situé dans le dossier parent
from .. app import db

# création de la table d'association articleHasPersonne qui lie article et personne
articleHasPersonne = db.Table('articleHasPersonne',
                              # création des colonnes artid et persid, chacune étant une clé étrangère
                           db.Column('artid', db.Integer, db.ForeignKey('article.article_id')),
                           db.Column('persid', db.Integer, db.ForeignKey('personne.personne_id')),
                              # chaque paire artid-persid doit être unique
                           db.UniqueConstraint('artid', 'persid')
                            )

# création de la table d'association articleHasLieu qui lie article et lieu de la même façon que articleHasPersonne
articleHasLieu = db.Table('articleHasLieu',
                          db.Column('artid', db.Integer, db.ForeignKey('article.article_id')),
                          db.Column('lid', db.Integer, db.ForeignKey('lieu.lieu_id')),
                          db.UniqueConstraint('artid', 'lid')
                          )


# définition de la classe Article
class Article(db.Model):
    # description des métadonnées de la classe, nom et arguments
    __tablename__ = "article"
    # création des différents attributs de la classe (id, titre, date, numJournal et texte)
    article_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    article_titre = db.Column(db.String(45), nullable=False)
    article_date = db.Column(db.String(45), nullable=False)
    article_numJournal = db.Column(db.String(45), nullable=False)
    article_texte = db.Column(db.Text, nullable=False)


    # initialisation des constructeurs de classe
    def __init__(self, article_id, article_titre, article_date, article_numJournal, article_texte):
        self.article_id = article_id
        self.article_titre = article_titre
        self.article_date = article_date
        self.article_numJournal = article_numJournal
        self.article_texte = article_texte


# définition de la class Personne sur le même modèle que pour Article
class Personne(db.Model):
    __tablename__="personne"
    # création des différents attributs de la table: id, nom, prénom, date de naissance et mort, role et notes
    personne_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    personne_nom = db.Column(db.String(45), nullable=False)
    personne_prenom = db.Column(db.String(45), nullable=False)
    personne_dreyf = db.Column(db.String(45))
    personne_role = db.Column(db.String(45))
    personne_notes = db.Column(db.Text)
    personne_pointeur=db.Column(db.String(45))

    #initialisation des constructeurs de classe
    def __init__(self, personne_id, personne_nom, personne_prenom, personne_dreyf, personne_role, personne_notes, personne_pointeur):
        self.personne_id = personne_id
        self.personne_nom = personne_nom
        self.personne_prenom = personne_prenom
        self.personne_dreyf = personne_dreyf
        self.personne_role = personne_role
        self.personne_notes = personne_notes
        self.personne_pointeur=personne_pointeur


# définition de la classe Lieu sur le même modèle que les classes précédentes
class Lieu(db.Model):
    __tablename__ = "lieu"
    # création des attributs de la table Lieu: id, nom, emplacement et notes
    lieu_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    lieu_nom = db.Column(db.String(45), nullable=False)
    lieu_emplacement = db.Column(db.String(63))
    lieu_notes = db.Column(db.Text)
    lieu_pointeur = db.Column(db.String(45))

    #initialisation des constructeurs de classe
    def __init__(self, lieu_id, lieu_nom, lieu_emplacement, lieu_notes, lieu_pointeur):
        self.lieu_id = lieu_id
        self.lieu_nom = lieu_nom
        self.lieu_emplacement = lieu_emplacement
        self.lieu_notes = lieu_notes
        self.lieu_pointeur = lieu_pointeur

from ..extraction import extraction_donnees
from ..constantes import document_xml
# Après avoir instancié la base, on la remplie:
# suppression des données existantes dans la base au chargement de l'application
db.drop_all()
# création des tables
db.create_all()
# appel de la fonction extraction_donnees avec pour entrée le fichier tei NDF, permettant ainsi de extraire chaque don-
# # née directement du document tei et de l'insérer dans la base de données
extraction_donnees(document_xml)
