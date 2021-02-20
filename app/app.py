from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("Application")
courant = os.path.join(os.path.abspath(__file__))
templates = os.path.join(courant, "templates")
#configuration de la base de donnée
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inititiation d'extension
db=SQLAlchemy(app)
from routes import *
if __name__ == "__main__":
    app.run(debug=True)