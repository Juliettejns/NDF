from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask('Application')

current = os.path.dirname(os.path.relpath(__file__))
templates = os.path.join(current, "templates")
print(templates)
db_path = os.path.join(current, "db.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)


from routes import *

if __name__ == '__main__':
    app.run()
