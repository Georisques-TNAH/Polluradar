import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_wtf.csrf import CSRFProtect

app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='statics')

app.config.from_object(Config)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


csrf = CSRFProtect(app)

# Création de l'objet SQLAlchemy
db = SQLAlchemy(app)

from .routes import generales, erreur, insertion, suppression
