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

    def __init__(self, titre, date, texte):
        #instanciation des attributs de la classe Article
        self.titre = titre
        self.date = date
        self.texte = texte

    @staticmethod
    def db_init():
        liste_id = []
        liste_titre = []
        liste_date = []
        liste_texte = []

        namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
        db.drop_all()
        db.create_all()
        for element in document_xml.xpath("//tei:group/tei:text/", namespaces=namespaces):
            numero = element.attrib['n']
            element_titre = document_xml.xpath("//tei:docTitle/tei:titlePart[@type='sub']/text()", namespaces=namespaces)
            liste_titre.append(element_titre)
            element_date = document_xml.xpath("//tei:docDate/tei:date/text()", namespaces=namespaces)
            liste_date.append(element_date)
            element_texte = document_xml.xpath("//tei:body/tei:div/tei:p/text()", namespaces=namespaces)
            liste_texte.append(element_texte)
            db.session.add(Article(numero,
                                   liste_titre[numero-1],
                                   liste_date[numero-1],
                                   liste_texte[numero-1]))
            db.session.commit()
