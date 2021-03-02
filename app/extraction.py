"""
extraction des données présentes dans le fichier xml
association de ces données à la bd
"""

from app import db
from constantes import document_xml
from donnees import Article

#Réinitalisation de la base à chaque lancement
db.drop_all()
db.create_all()

liste_titre=[]
liste_date=[]
liste_texte=[]

namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

for element in document_xml.xpath("//tei:group/tei:text", namespaces=namespaces):
    numero = element.attrib['n']
    element_titre = document_xml.xpath("//tei:docTitle/tei:titlePart[@type='sub']/text()", namespaces=namespaces)
    liste_titre.append(element_titre)
    element_date = document_xml.xpath("//tei:docDate/tei:date/text()", namespaces=namespaces)
    liste_date.append(element_date)
    element_texte = document_xml.xpath("//tei:body/tei:div/tei:p/text()", namespaces=namespaces)
    liste_texte.append(element_texte)
    db.session.add(Article(numero,
                           liste_titre[int(numero)-1],
                           liste_date[int(numero)-1],
                           liste_texte[int(numero)-1]))
    db.session.commit()

