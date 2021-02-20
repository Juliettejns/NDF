"""
Initialisation de la base de données
Extraction de données du fichier xml en vue de leur intégration dans la base
"""

from app import db
from constantes import document_xml

class Article(db.Model):
    #instanciation du modèle, définition de la classe
    article_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    article_titre = db.Column(db.String(45))
    article_date = db.Column(db.Date)
    article_texte = db.Column(db.Text)

    def __init__(self, id, titre, date, texte):
        #instanciation des attributs de la classe Article
        self.id = id
        self.titre = titre
        self.date = date
        self.texte = texte

db.create_all()

