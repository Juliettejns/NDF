"""
Instanciation du modèle de base de données
Author:Juliette Janes
Date: 03/03/2021
"""
# import de la classe db issue du module app situé dans le dossier parent
from app import db

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
    # extend_existing permet d'empêcher d'avoir une erreur lors de la modification de la classe
    __table_args__ = {'extend_existing': True}
    # création des différents attributs de la classe (id, titre, date, numJournal et texte)
    article_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    article_titre = db.Column(db.String(45), nullable=False)
    article_date = db.Column(db.String(45), nullable=False)
    article_numJournal = db.Column(db.Integer, nullable=False)
    article_texte = db.Column(db.Text, nullable=False)
    # jointures avec les tables de relation
    personnes = db.relationship("Personne", secondary=articleHasPersonne)
    lieux = db.relationship("Lieu", secondary=articleHasLieu)


# définition de la class Personne sur le même modèle que pour Article
class Personne(db.Model):
    __tablename__="personne"
    __table_args__ = {'extend_existing': True}
    # création des différents attributs de la table: id, nom, prénom, date de naissance et mort, role et notes
    personne_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    personne_nom = db.Column(db.String(45), nullable=False)
    personne_prenom = db.Column(db.String(45), nullable=False)
    personne_date_naissance = db.Column(db.String(45))
    personne_date_mort = db.Column(db.String(45))
    personne_role_dreyf = db.Column(db.String(45))
    personne_notes = db.Column(db.Text)


# définition de la classe Lieu sur le même modèle que les classes précédentes
class Lieu(db.Model):
    __tablename__ = "lieu"
    __table_args__ = {'extend_existing': True}
    # création des attributs de la table Lieu: id, nom, emplacement et notes
    lieu_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    lieu_nom = db.Column(db.String(45), nullable=False)
    lieu_emplacement = db.Column(db.String(63))
    lieu_notes = db.Column(db.Text)

