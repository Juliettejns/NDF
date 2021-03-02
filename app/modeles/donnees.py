"""
Instanciation du modèle de base de données
"""

from app import db

class Article(db.Model):
    __tablename__ = "article"
    __table_args__ = {'extend_existing': True}
    #instanciation du modèle, définition de la classe
    article_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    article_titre = db.Column(db.String(45))
    article_date = db.Column(db.String(45))
    article_texte = db.Column(db.Text)
