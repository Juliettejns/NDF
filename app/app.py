"""
Initialisation de l'application
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

#définition des chemins
courant = os.path.join(os.path.abspath(__file__))
templates = os.path.join(courant, "templates")

#création de l'application Flask
app = Flask("Application", template_folder=templates)

#configuration de la base de donnée
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite'
#désactivation de l'enregistrement des modifications de la bdd entre chaque lancement de l'application
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inititiation de la bdd à l'application Flask
db=SQLAlchemy(app)

#association des routes à l'application
from routes import *

#démarrage de l'application (avec un paramètre debug permettant de se mettre en mode développement)
if __name__ == "__main__":
    app.run(debug=True)
