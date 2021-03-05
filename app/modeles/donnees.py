"""
Instanciation du modèle de base de données
"""

from app import db

articleHasPersonne = db.Table('articleHasPersonne',
                           db.Column('artid', db.Integer, db.ForeignKey('article.article_id')),
                           db.Column('persid', db.Integer, db.ForeignKey('personne.personne_id')),
                           db.UniqueConstraint('artid', 'persid')
                            )
articleHasLieu = db.Table('articleHasLieu',
                          db.Column('artid', db.Integer, db.ForeignKey('article.article_id')),
                          db.Column('lid', db.Integer, db.ForeignKey('lieu.lieu_id')),
                          db.UniqueConstraint('artid', 'lid')
                          )


class Article(db.Model):
    __tablename__ = "article"
    __table_args__ = {'extend_existing': True}
    #instanciation du modèle, définition de la classe
    article_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    article_titre = db.Column(db.String(45), nullable=False)
    article_date = db.Column(db.String(45), nullable=False)
    article_numJournal = db.Column(db.Integer, nullable=False)
    personnes = db.relationship("Personne", secondary=articleHasPersonne)
    lieux = db.relationship("Lieu", secondary=articleHasLieu)

class Personne(db.Model):
    __tablename__="personne"
    __table_args__ = {'extend_existing': True}
    personne_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    personne_nom = db.Column(db.String(45), nullable=False)
    personne_prenom = db.Column(db.String(45), nullable=False)
    personne_date_naissance = db.Column(db.String(45))
    personne_date_mort = db.Column(db.String(45))
    personne_role_dreyf = db.Column(db.String(45))
    personne_notes = db.Column(db.Text)


class Lieu(db.Model):
    __tablename__ = "lieu"
    __table_args__ = {'extend_existing': True}
    lieu_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    lieu_nom = db.Column(db.String(45), nullable=False)
    lieu_emplacement = db.Column(db.String(63))
    lieu_notes = db.Column(db.Text)



