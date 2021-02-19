"""
Initialisation de la base de données
"""

from app import db

class Article(db.Model):
    #instanciation du modèle
    article_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    article_titre = db.Column(db.String(45))
    article_date = db.Column(db.Date)
    article_texte = db.Colum(db.Text)

def __init__(self, id, titre, date, texte):
    #instanciation des attributs de la classe Article
    self.id = id
    self.titre = titre
    self.date = date
    self.texte = texte
