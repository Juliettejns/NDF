"""
extraction des données présentes dans le fichier xml
association de ces données à la bd
"""

from app import db
from constantes import document_xml
from modeles.donnees import Article
db.drop_all()
db.create_all()

namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
for numero in document_xml.xpath("//tei:group/tei:text/@n", namespaces=namespaces):
    element_titre = document_xml.xpath("//tei:titlePart[@type='sub']/text()", namespaces=namespaces)
    element_date = document_xml.xpath("//tei:docDate/tei:date/text()", namespaces=namespaces)
    element_texte = document_xml.xpath("//tei:body/tei:div/tei:p/text()", namespaces=namespaces)
    note=Article(article_titre=element_titre[int(numero)-1], article_date=element_date[int(numero)-1], article_texte=element_texte[int(numero)-1])
    db.session.add(note)
    db.session.commit()

article=Article.query.all()
print(Article.query.filter_by(article_titre="Heures d'angoisse").first())
