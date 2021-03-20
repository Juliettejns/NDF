"""
extraction des données présentes dans le fichier xml
association de ces données à la bd
"""

from constantes import document_xml
from app import db
from modeles.donnees import *
from sqlalchemy.exc import IntegrityError


def extraction_donnees(document):
    """
    Fonction permettant, pour un fichier tei, d'extraire les différentes informations contenues et de les insérer dans
    la base de données db.
    :param document: fichier tei parsé par etree
    :type document: lxml.etree._ElementTree
    :return: base de données db.sqlite remplie
    :rtype: database
    """


    # extraction et insertion des éléments concernant la table Article
    # récupération de listes contenant les titres, date et numéro de parution pour chaque Article grâce à la méthode
    # xpath
    element_titre = document.xpath("//titlePart[@type='sub']/text()")
    element_date = document.xpath("//docDate/date/text()")
    element_numeroJournal = document.xpath("//text/@xml:id")
    n = 0
    for element in document.xpath("//group/text"):
        # pour chaque article, répètition des actions suivantes:
        n += 1
        # récupération d'une chaîne de caractères contenant le texte de l'article
        element_texte = " ".join(
            document.xpath("//text[@n=" + str(n) + "]//div/descendant-or-self::*/text()"))
        # insertion de chaque élément correspondant à l'article précis dans la table Article
        note = Article(article_titre=element_titre[int(n) - 1],
                       article_date=element_date[int(n) - 1],
                       article_numJournal=element_numeroJournal[int(n) - 1],
                       article_texte=element_texte
                       )
        # ajout de l'élément dans la base de données
        db.session.add(note)
        # commit de la modification
        db.session.commit()

    # extraction et insertion des éléments concernants la table personne
    # récupération sous forme de liste des éléments nom, prenom et role pour chaque personne présente dans le listPerson
    element_nom_personne = document.xpath("//persName/surname/text()")
    element_prenom = document.xpath("//persName/forename/text()")
    element_role = document.xpath("//person/@role")
    n = 0
    for element in document.xpath("//particDesc//person"):
        # pour chaque person dans le listPerson, répétition des actions suivantes:
        n += 1
        # récupération d'une chaîne de caractères contenant les notes bibliographiques d'un personnage précis
        element_notes_personne = " ".join(
            document.xpath("//person[@n=" + str(n) + "]/note/descendant-or-self::*/text()"))
        # insertion dans Personne de tout les éléments correspondants à une personne précise n
        personne = Personne(personne_nom=element_nom_personne[int(n) - 1],
                            personne_prenom=element_prenom[int(n) - 1],
                            personne_role=element_role[int(n)-1],
                            personne_notes=element_notes_personne
                            )
        # ajout de Personne dans la base de données
        db.session.add(personne)
        # commit pour enregistrement de la modification
        db.session.commit()
    # extraction et insertion des éléments concernant la table Lieu
    # récupération des éléments nom et descriptions sous la forme de listes pour tout les lieux
    element_nom_lieu = document.xpath("//place/placeName/text()")
    element_desc_lieu = document.xpath("//place/desc/text()")
    n = 0
    for element in document.xpath("//listPlace/place"):
        #pour chaque lieu contenu dans le listPlace, réitération de ces actions:
        n += 1
       # récupération d'une chaîne de caractères contenant l'adresse du lieu n
        element_localisation = " ".join(
            document.xpath("//place[@n=" + str(n) + "]//address/descendant-or-self::*/text()"))
        # création de l'objet lieu un nouveau Lieu ayant pour attributs les éléments suivants
        lieu = Lieu(lieu_nom=element_nom_lieu[int(n) - 1],
                    lieu_notes=element_desc_lieu[int(n) - 1],
                    lieu_emplacement=element_localisation
                    )
        # ajout de l'objet lieu dans la base de données
        db.session.add(lieu)
        # commit pour enregistrement de la modification
        db.session.commit()

    # extraction des éléments des tables d'association articleHasPersonne et articleHasLieu
    # récupération de l'identifiant et du numéro sous forme de listes pour toutes les personnes
    idPerson = document.xpath("//person/@xml:id")
    nPerson = document.xpath("//person/@n")
    # réalisation d'un dictionnaire où chaque clé est l'identifiant d'une personne ayant pour valeur son numéro
    dictionnaire_nid_personne = dict(zip(idPerson, nPerson))

    # récupération de l'identifiant et du numéro sous forme de listes pour tous les lieux
    idPlace = document.xpath("//place/@xml:id")
    nPlace = document.xpath("//place/@n")
    # réalisation d'un dictionnaire où chaque clé est l'identifiant d'un lieu ayant pour valeur son numéro
    dictionnaire_nid_place = dict(zip(idPlace, nPlace))

    n = 0
    for element in document.xpath("//div"):
        # pour chaque article, reproduction des actions suivantes afin de remplir la table articleHasPersonne:
        n += 1
        # récupération de tout les pointeurs présent dans les balises persNames du texte (sous la forme d'une liste)
        refPersName = document.xpath("//text[@n=" + str(n) + "]//persName/@ref")
        # suppression pour chaque élément de la liste du # du pointeur pour obtenir uniquement l'identifiant
        refPersName = [e.replace('#', '') for e in refPersName]
        for pointeur in refPersName:
            if pointeur in idPerson:
                # comparaison de chaque occurence persName dans le texte avec chaque pointeur dans la liste des
                # pointeurs provenant du listPerson
                try:
                    # récupération de la valeur numérique correspondant au pointeur alphabétique dans le dictionnaire
                    pointeur_numerique = dictionnaire_nid_personne[pointeur]
                    # insertion des éléments correspondant dans la table et enregistrement dans la base
                    relation_articlePersonne = articleHasPersonne.insert().values(artid=n,
                                                                                  persid=pointeur_numerique)
                    db.session.execute(relation_articlePersonne)
                    db.session.commit()
                except IntegrityError:
                    # chaque paire artid-persid devant être unique, obtention d'erreur lorsque l'on veut ajouter une
                    # paire déjà existante à la base. L'association try-except permet de passer les erreurs
                    pass

        # pour chaque article, reproduction des actions suivantes pour insertion des éléments de la table articleHasLieu
        # récupération de tout les pointeurs présent dans les balises placeName du texte (sous la forme d'une liste)
        refPlaceName = document.xpath("//text[@n=" + str(n) + "]//placeName/@ref")
        # suppression pour chaque élément de la liste du # du pointeur pour obtenir uniquement l'identifiant
        refPlaceName = [e.replace('#', '') for e in refPlaceName]
        for pointeur in refPlaceName:
            if pointeur in idPlace:
                # comparaison de chaque occurence d'un placeName dans le texte, avec chaque pointeur dans la liste
                # des pointeurs provenant du listPlace
                try:
                    # récupération de la valeur numérique correspondant au pointeur alphabétique dans le dictionnaire
                    pointeur_numerique = dictionnaire_nid_place[pointeur]
                    # insertion des éléments correspondant dans la table et enregistrement dans la base
                    relation_articlePlace = articleHasLieu.insert().values(artid=n,
                                                                           lid=pointeur_numerique)
                    db.session.execute(relation_articlePlace)
                    db.session.commit()
                except IntegrityError:
                    pass


# suppression des données existantes dans la base au chargement de l'application
db.drop_all()
# création des tables
db.create_all()
# appel de la fonction extraction_donnees avec pour entrée le fichier tei NDF
extraction_donnees(document_xml)
