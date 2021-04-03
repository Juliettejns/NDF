# Notes d'une frondeuse de Séverine
Notes d'une frondeuse est une application Flask présentant des textes écrits par la journaliste Séverine et publiés dans le journal féministe "La Fronde". Cette application est développée par Juliette Janes dans le cadre des enseignements de Master 2 Technologies numériques appliquées à l'Histoire de l'École nationale des Chartes (XML-TEI, XSLT, HTML, CSS, Python, SQL).

## Fonctionnalités
  - Une édition numérique d'un échantillon d'articles choisis, publiés entre 1897 et 1899 par Caroline Rémy dite Séverine dans La Fronde sous le nom "Notes d'une frondeuse". Les notes sont exploitées sous la forme d'un encodage XML-TEI, disponible dans le dépôt. Son guide d'encodage est également accessible dans le fichier ODD.
  - Des index de lieux et personnes, présentant pour chaque lieu ou personne, les articles où il en est fait mention, ainsi qu'un lien permettant d'accéder directement à la page de l'article.
  - Une recherche plein texte permettant de récupérer tout les articles où un mot clef choisi par l'utilisateur est présent.

## Installation
  - Installer python3
  - Cloner le dépôt sur sa machine: ```git clone https://github.com/Juliettejns/NDF.git``` et rentrer dans le dossier créé
  - Créer l'environnement: ```virtualenv -p python3 env```
  - Lancer l'environnement: ```source env/bin/activate```
  - Installer les librairies nécessaires: ```pip install -r requirements.txt```

## Lancement
  - Lancer l'environnement: ```source env/bin/activate```
  - Lancer les tests: ```python -m unittest discover test```
  - Lancer l'application: ```python3 run.py```
  - Aller sur ```http://127.0.0.1:5000/``` dans le navigateur
  - Arrêter l'application: ```CRTL + C```
  - Arrêter l'environnement: ```source env/bin/deactivate```
