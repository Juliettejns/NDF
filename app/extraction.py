"""
extraction des données présentes dans le fichier xml
association de ces données à la bd
"""

from app import db
from constantes import document_xml
from modeles.donnees import *
from sqlalchemy.exc import IntegrityError
db.drop_all()
db.create_all()

namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

n=0

#extraction des éléments articles
element_titre = document_xml.xpath("//tei:titlePart[@type='sub']/text()", namespaces=namespaces)
element_date = document_xml.xpath("//tei:docDate/tei:date/@when-iso", namespaces=namespaces)
element_numeroJournal = document_xml.xpath("//tei:text/@xml:id", namespaces=namespaces)
for element in document_xml.xpath("//tei:group/tei:text", namespaces=namespaces):
    n+=1
    note=Article(article_titre=element_titre[int(n)-1],
                 article_date=element_date[int(n)-1],
                 article_numJournal=element_numeroJournal[int(n)-1]
                 )
    db.session.add(note)
    db.session.commit()

#extraction des éléments personne
element_nom_personne = document_xml.xpath("//tei:persName/tei:surname/text()", namespaces=namespaces)
element_prenom = document_xml.xpath("//tei:persName/tei:forename/text()", namespaces=namespaces)
element_dreyf=[]
n=0
for element in document_xml.xpath("//tei:listPerson/tei:person", namespaces=namespaces):
    n+=1
    if document_xml.xpath("//tei:person[@n=" + str(n) + "and @role='dreyf']", namespaces=namespaces):
        element_dreyf.append('True')
    elif document_xml.xpath("//tei:person[@n=" + str(n) + "and @role='antidreyf']", namespaces=namespaces):
        element_dreyf.append('False')
    else:
         element_dreyf.append('')
    element_notes_personne = " ".join(document_xml.xpath("//tei:person[@n=" + str(n) + "]/tei:note/descendant-or-self::*/text()", namespaces=namespaces))
    personne = Personne(personne_nom = element_nom_personne[int(n)-1],
                        personne_prenom = element_prenom[int(n)-1],
                        personne_role_dreyf = element_dreyf[int(n)-1],
                        personne_notes = element_notes_personne
                        )
    db.session.add(personne)
    db.session.commit()
    '''try:
        personne_bdate = document_xml.xpath("//tei:person[@n=" + str(n) + "]/tei:birth/@when",
                                            namespaces=namespaces)
        personne_ddate = document_xml.xpath("//tei:person[@n=" + str(n) + "]/tei:death/@when",
                                            namespaces=namespaces)
        dates = Personne(personne_date_naissance= personne_bdate,
                         personne_date_mort= personne_ddate)
        db.session.add(dates)
        db.session.commit()
    except Exception:
        db.session.add(personne)
        db.session.commit()'''

#extraction des éléments lieux
element_nom_lieu = document_xml.xpath("//tei:place/tei:placeName/text()", namespaces=namespaces)
element_desc_lieu = document_xml.xpath("//tei:place/tei:desc/text()", namespaces=namespaces)
n=0
for element in document_xml.xpath("//tei:listPlace/tei:place", namespaces= namespaces):
    n+=1
    element_localisation = " ".join(document_xml.xpath("//tei:place[@n=" + str(n) + "]//tei:address/descendant-or-self::*/text()", namespaces=namespaces))
    lieu = Lieu(lieu_nom = element_nom_lieu[int(n)-1],
                lieu_notes = element_desc_lieu[int(n)-1],
                lieu_emplacement = element_localisation
                )
    db.session.add(lieu)
    db.session.commit()

#extraction des éléments de la table d'association articleHasPersonne
idPerson=document_xml.xpath("//tei:person/@xml:id", namespaces=namespaces)
nPerson= document_xml.xpath("//tei:person/@n", namespaces=namespaces)
dictionnaire_nid_personne =dict(zip(idPerson,nPerson))

idPlace=document_xml.xpath("//tei:place/@xml:id", namespaces=namespaces)
nPlace= document_xml.xpath("//tei:place/@n", namespaces=namespaces)
dictionnaire_nid_place =dict(zip(idPlace,nPlace))

n=0
for element in document_xml.xpath("//tei:div", namespaces=namespaces):
    n+=1
    refPersName = document_xml.xpath("//tei:text[@n="+str(n)+"]//tei:persName/@ref", namespaces=namespaces)
    refPersName = [e.replace('#', '') for e in refPersName]
    for pointeur in refPersName:
        if pointeur in idPerson:
            try:
                pointeur_numerique = dictionnaire_nid_personne[pointeur]
                relation_articlePersonne=articleHasPersonne.insert().values(artid=n,
                                                        persid=pointeur_numerique)
                db.session.execute(relation_articlePersonne)
                db.session.commit()
            except IntegrityError:
                pass
    refPlaceName = document_xml.xpath("//tei:text[@n=" + str(n) + "]//tei:placeName/@ref", namespaces=namespaces)
    refPlaceName = [e.replace('#', '') for e in refPlaceName]
    for pointeur in refPlaceName:
        if pointeur in idPlace:
            pointeur_numerique = dictionnaire_nid_place[pointeur]
            try:
                relation_articlePlace=articleHasLieu.insert().values(artid=n,
                                                        lid=pointeur_numerique)
                db.session.execute(relation_articlePlace)
                db.session.commit()
            except IntegrityError:
                pass