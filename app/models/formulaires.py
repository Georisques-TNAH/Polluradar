from flask_wtf import FlaskForm
from wtforms import StringField, SelectField

class Recherche(FlaskForm):
    nom_commune = StringField("nom_commune", validators=[]) 
    code_postal = SelectField('code_postal', choices=[])
