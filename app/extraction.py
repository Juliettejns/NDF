"""
extraction des données présentes dans le fichier xml
association de ces données à la bd
"""

from app import db
from constantes import document_xml
from modeles.donnees import *
db.drop_all()
db.create_all()

namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

n=0
element_titre = document_xml.xpath("//tei:titlePart[@type='sub']/text()", namespaces=namespaces)
element_date = document_xml.xpath("//tei:docDate/tei:date/@when-iso", namespaces=namespaces)
element_numeroJournal = document_xml.xpath("//tei:text/@n", namespaces=namespaces)
for element in document_xml.xpath("//tei:group/tei:text", namespaces=namespaces):
    n+=1
    note=Article(article_titre=element_titre[int(n)-1],
                 article_date=element_date[int(n)-1],
                 article_numJournal=element_numeroJournal[int(n)-1]
                 )
    db.session.add(note)
    db.session.commit()

element_nom = document_xml.xpath("//tei:persName/tei:surname/text()", namespaces=namespaces)
element_prenom = document_xml.xpath("//tei:persName/tei:forename/text()", namespaces=namespaces)
element_note = document_xml.xpath("//tei:person/tei:note/text()", namespaces=namespaces)
n=0
for element in document_xml.xpath("//tei:listPerson/tei:person", namespaces=namespaces):
    n+=1
    personne = Personne(personne_nom = element_nom[int(n)-1],
                        personne_prenom = element_prenom[int(n)-1],
                        personne_notes = element_prenom[int(n)-1])
    db.session.add(personne)
    db.session.commit()
