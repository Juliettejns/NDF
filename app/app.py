"""
Initialisation de l'application
Author: Juliette Janes
Date: 03/03/2021
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# définition des chemins
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")
# création de l'application Flask
app = Flask("Application",
            template_folder=templates,
            static_folder=statics
            )

# configuration de la base de donnée
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite'
# désactivation de l'enregistrement des modifications de la bdd entre chaque lancement de l'application
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inititiation de la bdd à l'application Flask
db=SQLAlchemy(app)

# association des routes à l'application
from .routes import *

