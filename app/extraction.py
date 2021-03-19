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
    # définition du namespaces tei
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # extraction et insertion des éléments concernant la table Article

    # récupération de listes contenant les titres, date et numéro de parution pour chaque Article grâce à la méthode
    # xpath
    element_titre = document.xpath("//tei:titlePart[@type='sub']/text()", namespaces=namespaces)
    element_date = document.xpath("//tei:docDate/tei:date/text()", namespaces=namespaces)
    element_numeroJournal = document.xpath("//tei:text/@xml:id", namespaces=namespaces)
    n = 0
    for element in document.xpath("//tei:group/tei:text", namespaces=namespaces):
        # pour chaque article, répètition des actions suivantes:
        n += 1
        # récupération d'une chaîne de caractères contenant le texte de l'article
        element_texte = " ".join(
            document.xpath("//tei:text[@n=" + str(n) + "]//tei:div/descendant-or-self::*/text()",
                               namespaces=namespaces))
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
    # récupération sous forme de liste des éléments nom et prenom pour chaque personne présente dans le listPerson
    element_nom_personne = document.xpath("//tei:persName/tei:surname/text()", namespaces=namespaces)
    element_prenom = document.xpath("//tei:persName/tei:forename/text()", namespaces=namespaces)
    #initialisation de l'élement concernant le role dans l'affaire dreyfus sous la forme d'une liste vide
    element_dreyf = []
    n = 0
    for element in document.xpath("//tei:listPerson/tei:person", namespaces=namespaces):
        # pour chaque person dans le listPerson, répétition des actions suivantes:
        n += 1
        # extraction de l'élément dreyf sous la forme de conditions (certains personnes n'ayant pas d'attribut role)
        if document.xpath("//tei:person[@n=" + str(n) + "and @role='dreyf']", namespaces=namespaces):
            element_dreyf.append('dreyfusard')
        elif document.xpath("//tei:person[@n=" + str(n) + "and @role='antidreyf']", namespaces=namespaces):
            element_dreyf.append('antidreyfusard')
        else:
            element_dreyf.append('')
        # récupération d'une chaîne de caractères contenant les notes bibliographiques d'un personnage précis
        element_notes_personne = " ".join(
            document.xpath("//tei:person[@n=" + str(n) + "]/tei:note/descendant-or-self::*/text()",
                               namespaces=namespaces))
        # insertion dans Personne de tout les éléments correspondants à une personne précise n
        personne = Personne(personne_nom=element_nom_personne[int(n) - 1],
                            personne_prenom=element_prenom[int(n) - 1],
                            personne_role_dreyf=element_dreyf[int(n) - 1],
                            personne_notes=element_notes_personne
                            )
        # ajout de Personne dans la base de données
        db.session.add(personne)
        # commit pour enregistrement de la modification
        db.session.commit()
        # possibilité de récupérer les dates de naissance et de mort d'une personne (élément à supprimer de la base)
        '''try:
            personne_bdate = document.xpath("//tei:person[@n=" + str(n) + "]/tei:birth/@when",
                                                namespaces=namespaces)
            personne_ddate = document.xpath("//tei:person[@n=" + str(n) + "]/tei:death/@when",
                                                namespaces=namespaces)
            dates = Personne(personne_date_naissance= personne_bdate,
                             personne_date_mort= personne_ddate)
            db.session.add(dates)
            db.session.commit()
        except Exception:
            db.session.add(personne)
            db.session.commit()'''

    # extraction et insertion des éléments concernant la table Lieu
    # récupération des éléments nom et descriptions sous la forme de listes pour tout les lieux
    element_nom_lieu = document.xpath("//tei:place/tei:placeName/text()", namespaces=namespaces)
    element_desc_lieu = document.xpath("//tei:place/tei:desc/text()", namespaces=namespaces)
    n = 0
    for element in document.xpath("//tei:listPlace/tei:place", namespaces=namespaces):
        #pour chaque lieu contenu dans le listPlace, réitération de ces actions:
        n += 1
       # récupération d'une chaîne de caractères contenant l'adresse du lieu n
        element_localisation = " ".join(
            document.xpath("//tei:place[@n=" + str(n) + "]//tei:address/descendant-or-self::*/text()",
                               namespaces=namespaces))
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
    idPerson = document.xpath("//tei:person/@xml:id", namespaces=namespaces)
    nPerson = document.xpath("//tei:person/@n", namespaces=namespaces)
    # réalisation d'un dictionnaire où chaque clé est l'identifiant d'une personne ayant pour valeur son numéro
    dictionnaire_nid_personne = dict(zip(idPerson, nPerson))

    # récupération de l'identifiant et du numéro sous forme de listes pour tous les lieux
    idPlace = document.xpath("//tei:place/@xml:id", namespaces=namespaces)
    nPlace = document.xpath("//tei:place/@n", namespaces=namespaces)
    # réalisation d'un dictionnaire où chaque clé est l'identifiant d'un lieu ayant pour valeur son numéro
    dictionnaire_nid_place = dict(zip(idPlace, nPlace))

    n = 0
    for element in document.xpath("//tei:div", namespaces=namespaces):
        # pour chaque article, reproduction des actions suivantes afin de remplir la table articleHasPersonne:
        n += 1
        # récupération de tout les pointeurs présent dans les balises persNames du texte (sous la forme d'une liste)
        refPersName = document.xpath("//tei:text[@n=" + str(n) + "]//tei:persName/@ref", namespaces=namespaces)
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
        refPlaceName = document.xpath("//tei:text[@n=" + str(n) + "]//tei:placeName/@ref", namespaces=namespaces)
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
